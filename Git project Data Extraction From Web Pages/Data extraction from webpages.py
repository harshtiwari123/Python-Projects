from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("headless")
chrome_options.add_argument("--ignore-certificate-errors")

# Initialize the WebDriver
driver = webdriver.Chrome(options=chrome_options)

base_url = "https://culture360.asef.org/resources/organisations-directory/?discipline=design"

# Function to extract additional details from the sidebar
def extract_sidebar_details(driver):
    details = {}
    try:
        website_tag = driver.find_element(By.XPATH, "//p[contains(text(), 'Website')]/following-sibling::ul/li/a")
        details['Website'] = website_tag.get_attribute('href') if website_tag else 'N/A'
    except:
        details['Website'] = 'N/A'

    try:
        country_tag = driver.find_element(By.XPATH, "//p[contains(text(), 'Country')]/following-sibling::ul/li/a")
        details['Country'] = country_tag.text.strip() if country_tag else 'N/A'
    except:
        details['Country'] = 'N/A'

    try:
        disciplines_tag = driver.find_element(By.XPATH, "//p[contains(text(), 'Disciplines')]/following-sibling::ul")
        links = disciplines_tag.find_elements(By.TAG_NAME, 'a')
        details['Disciplines'] = ', '.join([link.text.strip() for link in links])
    except:
        details['Disciplines'] = 'N/A'

    return details

# Start scraping the main page
driver.get(base_url)

# Accept GDPR consent if prompted
try:
    consent_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#dj-gdpr-consent-preferences"))
    )
    consent_button.click()
    time.sleep(2)
except:
    print("Consent button not found or click failed.")

# Determine the total number of pages to scrape
time.sleep(3)
sub_page_elements = driver.find_elements(By.CLASS_NAME, "page-link")
sub_page = [element.get_attribute('href') for element in sub_page_elements if element.get_attribute('href')]
count = int(sub_page[-1].split('=')[-1]) if sub_page else 1

print(f"Total pages to scrape: {count}")

all_data = []

# Loop through pages (up to 9 pages)
for i in range(1, min(count, 9) + 1):
    print(f"Scraping page {i}...")
    driver.get(f"{base_url}&page={i}")
    time.sleep(3)

    elements = driver.find_elements(By.CLASS_NAME, "bg-c360-resources.fw-bold")
    links = [element.get_attribute('href') for element in elements if element.get_attribute('href')]

    for link in links:
        driver.get(link)
        time.sleep(3)

        try:
            org_name_element = driver.find_element(By.CLASS_NAME, 'page-item-title')
            org_name = org_name_element.text.strip() if org_name_element else 'N/A'
        except:
            org_name = 'N/A'

        sidebar_details = extract_sidebar_details(driver)
        all_data.append({
            'Name': org_name,
            'Website': sidebar_details['Website'],
            'Country': sidebar_details['Country'],
            'Disciplines': sidebar_details['Disciplines'],
            'Link': link
        })

        if len(all_data) >= 9:
            break
    if len(all_data) >= 9:
        break

# Save data to an Excel file
pd.DataFrame(all_data).to_excel('C:\\Users\\galav\\OneDrive\\Desktop\\data8_selenium_9_entries.xlsx', index=False)
print(f"Total entries extracted: {len(all_data)}")

# Close the browser
driver.quit()
