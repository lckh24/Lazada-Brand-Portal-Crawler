Brand Portal Crawling on Lazada
📌 Overview
This script automates data crawling from the Lazada Brand Portal, retrieving daily sales reports for multiple sellers across different countries. It processes downloaded files and renames them based on a predefined mapping. To enhance performance, it leverages multi-threading and fetches revenue details via external APIs.

🛠️ Core Dependencies
datetime – Manages date calculations for the data crawling period.
concurrent.futures – Uses ThreadPoolExecutor for multi-threading to speed up crawling.
pandas – Handles reading/writing CSV and Excel files, processes seller data, and renames files.
requests – Sends HTTP requests to APIs to fetch sales data.
os – Manages file operations (reading, writing, renaming).
sys – Handles command-line arguments for script execution.
🚀 How to Use
1️⃣ Log in to the Lazada Brand Portal.
2️⃣ Save cookies from the browser's Developer Tools (DevTools).
3️⃣ Create a mapping file containing:

Store Name
Country (e.g., VN, TH, PH, etc.)
Seller ID (formatted as Country.SellerID, e.g., VN.123456)
4️⃣ Run the script in the terminal:
bash
python script.py "<COOKIES_STRING>" YYYY/MM/DD YYYY/MM/DD
<COOKIES_STRING>: Your saved cookies from DevTools.
YYYY/MM/DD YYYY/MM/DD: Start and end dates for data crawling.
This setup ensures efficient and structured data retrieval from Lazada's Brand Portal ✅
