import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service

def scrape_website(website_url):
    print("Launching Chrome Browser...")

    chrome_driver_path = ""
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)

    try:
        driver.get(website_url)
        print("Page Loaded Successfully!")
        html = driver.page_source
        print("HTML Extracted Successfully!")
        return html
        
    except Exception as e:
        print(f"Error while getting the site content: {e.__str__()}")
    finally:
        driver.quit()