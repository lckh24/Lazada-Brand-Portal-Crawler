🛒 Lazada Brand Portal Crawling – Automated Sales Data Retrieval  

📌 Overview  

This script automates the extraction of daily sales reports from Lazada's Brand Portal for multiple sellers across different countries. It efficiently processes and renames downloaded files using a predefined mapping while optimizing performance with multi-threading. Additionally, the script retrieves revenue details via external APIs to enhance data accuracy.  

🛠️ Key Features  

✅ Automated Data Crawling – Fetches sales data for multiple sellers across different regions.  
✅ Multi-threading for Speed – Uses concurrent execution to improve performance.  
✅ API-Integrated Revenue Retrieval – Fetches revenue details dynamically from external APIs.  
✅ File Processing & Renaming – Reads, processes, and renames files based on a structured mapping.  

🔧 Dependencies  

datetime – Manages date calculations for data retrieval.  
concurrent.futures – Implements multi-threading for faster execution.  
pandas – Handles data manipulation, CSV/Excel processing, and mapping.  
requests – Sends API requests to fetch sales data.  
os – Manages file operations (reading, writing, renaming).  
sys – Handles command-line arguments.  

🚀 How to Use  

1️⃣ Login to the Lazada Brand Portal and access seller data.  
2️⃣ Extract Cookies from your browser's Developer Tools (DevTools).  
3️⃣ Prepare a Mapping File (mapping.csv) with the following columns:   
| Store Name | Country | Seller ID (formatted as Country.SellerID) |
|------------|---------|---------------------------------|
| Example Store | VN | VN.123456 |

4️⃣ Run the Script in the terminal:  
```bash
python script.py "<COOKIES_STRING>" YYYY/MM/DD YYYY/MM/DD
```
 * <COOKIES_STRING>: Your extracted cookies from DevTools.
 * YYYY/MM/DD YYYY/MM/DD: Start and end dates for data retrieval.
This setup ensures a fast, efficient, and structured approach to collecting sales data from Lazada’s Brand Portal. ✅
