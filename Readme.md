# Amazon Product Scraping Automation (Selenium + Python)

## Project Overview

This project automates scraping of Amazon products using Python and Selenium.  
It searches for a product, scrapes all products from Page 1 and Page 2, visits their detail pages, and collects information like:

- Product Name  
- Price  
- Rating  
- Number of Reviews  
- Product URL  

It also generates full-page screenshots, Excel files, and HTML reports.

---

## Features

- Opens Amazon homepage and takes a full-page screenshot
- Searches for a product keyword
- Scrapes all products from Page 1 and Page 2
- Navigates automatically through pagination
- Visits each product’s detail page
- Extracts product information: Name, Price, Rating, Reviews, URL
- Takes full-page screenshots of:
  - Search result pages
  - Product detail pages
- Generates:
  - Excel file (`output/amazon_products.xlsx`)
  - HTML report with screenshots (`reports/amazon_report.html`)
- Handles layout changes gracefully

---

## Tech Stack

- Python 3  
- Selenium WebDriver  
- Google Chrome  
- WebDriver Manager  
- Pandas for data handling  
- Chrome DevTools Protocol for full-page screenshots

---

## Project Structure

amazon-automation/
│
├── screenshots/
│ ├── amazon_home_full.png
│ ├── search_page_1_full.png
│ ├── search_page_2_full.png
│ ├── product_1.png
│ └── ...
│
├── output/
│ └── amazon_products.xlsx
│
├── reports/
│ └── amazon_report.html
│
├── test_amazon.py
└── README.md


## Installation & Setup

### 1. Clone the repository

git clone https://github.com/your-username/amazon-automation.git
cd amazon-automation
2. Create a virtual environment (recommended)


python -m venv venv
venv\Scripts\activate
3. Install dependencies

pip install selenium webdriver-manager pandas

How to Run the Script
python test_amazon.py
Output Details
Screenshots
Amazon homepage (full page)

Search results Page 1 & 2 (full page)

Individual product detail pages

Excel File
Location: output/amazon_products.xlsx

Contains all scraped product details

HTML Report
Location: reports/amazon_report.html

Includes product details, clickable URLs, and screenshots

Important Notes
Amazon layout may change frequently

Prices & ratings may vary per product

Some products may show N/A if data is not available

Script exits safely if automation is blocked






Author
Nayab Fatima
Software Engineering | Automation & Web Development
Email: nayab.fatima.mithani@gmail.com




