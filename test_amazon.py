from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import os
import time
import base64


def full_page_screenshot(driver, filename):
    metrics = driver.execute_cdp_cmd("Page.getLayoutMetrics", {})
    width = metrics["contentSize"]["width"]
    height = metrics["contentSize"]["height"]

    driver.execute_cdp_cmd("Emulation.setDeviceMetricsOverride", {
        "mobile": False,
        "width": width,
        "height": height,
        "deviceScaleFactor": 1
    })

    screenshot = driver.execute_cdp_cmd("Page.captureScreenshot", {
        "format": "png",
        "captureBeyondViewport": True
    })

    with open(filename, "wb") as f:
        f.write(base64.b64decode(screenshot["data"]))


def test_amazon_product_scraping():

    for folder in ["screenshots", "reports", "output"]:
        os.makedirs(folder, exist_ok=True)

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    wait = WebDriverWait(driver, 20)

    # -------------------------
    # Amazon Home (FULL PAGE SS)
    # -------------------------
    driver.get("https://www.amazon.com")
    time.sleep(5)

    try:
        driver.find_element(By.ID, "sp-cc-accept").click()
        time.sleep(2)
    except:
        pass

    full_page_screenshot(driver, "screenshots/amazon_home_full.png")

    # -------------------------
    # Search
    # -------------------------
    search_box = wait.until(
        EC.presence_of_element_located((By.ID, "twotabsearchtextbox"))
    )
    search_box.send_keys("Wireless Headphones")
    search_box.submit()
    time.sleep(5)

    product_links = set()

    # -------------------------
    # PAGE 1 + PAGE 2 (FULL PAGE SS)
    # -------------------------
    for page in range(1, 3):
        time.sleep(4)

        full_page_screenshot(
            driver,
            f"screenshots/search_page_{page}_full.png"
        )

        products = driver.find_elements(
            By.XPATH,
            "//div[@data-component-type='s-search-result' and @data-asin!='']"
        )

        for p in products:
            try:
                link = p.find_element(
                    By.XPATH, ".//a[@class='a-link-normal s-no-outline']"
                ).get_attribute("href")
                if link:
                    product_links.add(link)
            except:
                pass

        if page < 2:
            try:
                next_btn = wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//a[contains(@class,'s-pagination-next')]")
                    )
                )
                driver.execute_script("arguments[0].click();", next_btn)
                time.sleep(5)
            except:
                break

    # -------------------------
    # Visit Product Pages (FULL PAGE SS)
    # -------------------------
    data = []

    for i, link in enumerate(product_links, start=1):
        driver.get(link)
        time.sleep(5)

        # ✅ FULL PAGE product screenshot
        full_page_screenshot(
            driver,
            f"screenshots/product_{i}_full.png"
        )

        try:
            name = wait.until(
                EC.presence_of_element_located((By.ID, "productTitle"))
            ).text.strip()
        except:
            name = "N/A"

        price = "N/A"
        for xp in [
            "//span[@class='a-price']//span[@class='a-offscreen']",
            "//span[@class='a-price-whole']"
        ]:
            try:
                price = driver.find_element(By.XPATH, xp).text
                if price:
                    break
            except:
                pass

        rating = "N/A"
        for xp in [
            "//a[@class='a-popover-trigger a-declarative mvt-cm-cr-review-stars-mini-popover']",
            "//i[contains(@class,'a-size-small a-color-base')]/span"
        ]:
            try:
                rating = driver.find_element(By.XPATH, xp).text
                if rating:
                    break
            except:
                pass

        try:
            reviews = driver.find_element(By.ID, "acrCustomerReviewText").text
        except:
            reviews = "N/A"

        data.append({
            "Product Name": name,
            "Price": price,
            "Rating": rating,
            "Reviews": reviews,
            "Product URL": driver.current_url
        })

        print(f"✔ Scraped {i}: {name}")

    # -------------------------
    # Save Excel
    # -------------------------
    pd.DataFrame(data).to_excel("output/amazon_products.xlsx", index=False)

    # -------------------------
    # HTML Report
    # -------------------------
    html = "<html><body><h2>Amazon Product Report</h2><table border='1'>"
    html += "<tr><th>Name</th><th>Price</th><th>Rating</th><th>Reviews</th><th>URL</th></tr>"

    for i, d in enumerate(data, start=1):
        html += f"""
        <tr>
        <td>{d['Product Name']}</td>
        <td>{d['Price']}</td>
        <td>{d['Rating']}</td>
        <td>{d['Reviews']}</td>
        <td><a href="{d['Product URL']}">Link</a></td>
        </tr>
        """

    html += "</table></body></html>"

    with open("reports/amazon_report.html", "w", encoding="utf-8") as f:
        f.write(html)

    print("✅ Done: All FULL-PAGE screenshots captured")


if __name__ == "__main__":
    test_amazon_product_scraping()
