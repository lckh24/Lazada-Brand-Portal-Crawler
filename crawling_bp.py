from datetime import datetime, timedelta, date
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd
import requests
import os
import time
import shutil
import io
import sys

from dotenv import load_dotenv
load_dotenv()

API1 = os.getenv("HIDDEN_API")
API2 = os.getenv("HIDDEN_API2")


def get_clean_cookies(cookies_list):
    result_list = []
    for cookies in cookies_list:
        result_dict = {}
        cookies_df = pd.read_csv(io.StringIO(cookies),sep=";")
        cookies_list = cookies_df.columns.tolist()
        clean_list = [cookie.strip() for cookie in cookies_list]
        for node in clean_list:
            key = node.split("=")[0]
            value = node.split("=")[1]
            result_dict[key] = value
        result_list.append(result_dict)
        
    return result_list

def get_files_by_keyword(extension: str):
    files = [file for file in os.listdir() if file.endswith(extension)]
    print(f"Found {len(files)} file(s) with extension '{extension}'.")
    return files

def get_seller_id_list(mapping_file: str = 'mapping.csv'):
    try:
        df = pd.read_csv(mapping_file, usecols=['seller_used_id'])
        return df['seller_used_id'].tolist()
    except FileNotFoundError:
        print(f"Error: {mapping_file} not found!")
        return []

def get_revenue(daterange, seller_id, country):
    url = API1
    params = {
    "dateType": "day",
    "dateRange": f"{daterange}|{daterange}",
    "venture": f"{country}",
    "storeId": f"{seller_id}",
    "pageSize": 5,
    "page": 1,
    "orderBy": "gmv",
    "order": "desc"
    }

    print(f"Requesting: API1")
    response = requests.get(url, cookies=cookies[0], params=params)
    
    try:
        revenue = response.json().get('data', {}).get('data', [{}])[0].get('gmvLocal', {}).get('value', 0)
        return round(revenue, 0)
    except Exception as e:
        print(f"Error parsing revenue data: {e}")
        return 0

def filename_generator(seller_id: str, execution_date: str, revenue) -> str:
    current_date = time.strftime('%Y-%m-%d')
    return f"{seller_id}_{execution_date}_brand-portal-report_daily_level_revenue-{revenue}-0"

def fetch_data(seller_id, start_date):
    try:
        id = seller_id.split('.')[1]
        country = seller_id.split('.')[0]
        print(f"Retrieve data for {country}_{id}")
        url = API2
        print(f"Requesting: API2")
        params = {
            "ventures": f"{country}",
            "sellerIds": f"{id}",
            "dateType": "day",
            "dateRange": f"{start_date}|{start_date}"
        }
        response = requests.get(url, cookies=cookies[0], params=params)
        revenue = get_revenue(start_date, id, country)
        file_name = f"{start_date}_{revenue}.xls"
        
        with open(file_name, "wb") as file:
            file.write(response.content)
        
        print(f"Saved: {file_name}")
    except Exception as e:
        print(f"Error fetching data for {seller_id}: {e}")

def get_data_brand_portal(start_date, end_date, list_seller_id):
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        while start_date <= end_date:
            for seller_id in list_seller_id:
                futures.append(executor.submit(fetch_data, seller_id, start_date))
            start_date += timedelta(days=1)
        
        for future in as_completed(futures):
            future.result()  

def rename_files(file_list, mapping_file: str = 'mapping.csv'):
    print('Starting file renaming process...')
    try:
        df = pd.read_csv(mapping_file)
        df.set_index(['Venture', 'Store name'], inplace=True)
        seller_mapping = df.groupby(level=0).apply(lambda x: x.droplevel(0).to_dict()['seller_used_id']).to_dict()
    except Exception as e:
        print(f"Error reading mapping file: {e}")
        return
    
    for file in file_list:
        try:
            df = pd.read_excel(file, sheet_name='Product', skiprows=5, usecols=['Venture', 'Store Name'])
            country, store = df.iloc[0]['Venture'], df.iloc[0]['Store Name']
            seller_id = seller_mapping.get(country, {}).get(store, 'Not Found')
            
            if seller_id == 'Not Found':
                print(f"Seller ID not found for {country}, {store}")
                continue

            data_date = pd.read_excel(file, header=None).iloc[0, 0]
            execution_date = data_date.split(':')[-1].split('_')[0].strip()
            revenue = file.split('_')[-1].split('.')[0]
            new_file_name = filename_generator(seller_id, execution_date, revenue) + ".xls"
            
            os.rename(file, new_file_name)
            print(f"Renamed: {file} -> {new_file_name}")
        
        except Exception as e:
            print(f"Error processing file {file}: {e}")
            
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Error: Invalid number of arguments!")
    
    else:
        args = sys.argv[1:]
        cookie = args[0]
        start_date = args[1].split('/')
        start_date = date(int(start_date[0]), int(start_date[1]), int(start_date[2]))
        end_date = args[2].split('/')
        end_date = date(int(end_date[0]), int(end_date[1]), int(end_date[2]))

        cookies = get_clean_cookies([cookie])
        seller_list = get_seller_id_list()

        get_data_brand_portal(start_date, end_date, seller_list)
        files = get_files_by_keyword('.xls')

        rename_files(files)
        print("All tasks completed!")






