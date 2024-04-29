import os
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException

import time

# List of Python files you want to run
python_files = ["clear_data.py"]

def click_safe(driver, xpath, attempts=3):
    try:
        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        element.click()
    except StaleElementReferenceException:
        if attempts > 0:
            print("StaleElementReferenceException caught. Retrying...")
            time.sleep(2)  # Short delay before retrying
            click_safe(driver, xpath, attempts - 1)
        else:
            print("Failed to click on the element after several attempts.")
    except TimeoutException as e:
        print(f"Timeout clicking element with xpath {xpath}: {e}")
    except Exception as e:
        print(f"Error clicking element with xpath {xpath}: {e}")

# Download directory
download_dir = 'C:\\Users\\Administrator\\Desktop\\tool_crawl_sapo\\data'

# Initialize Chrome WebDriver
chrome_options = webdriver.ChromeOptions()
prefs = {'download.default_directory': download_dir}
chrome_options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(options=chrome_options)

# Wait for download completion
def wait_for_download(dir_path):
    while not any(filename.endswith('.xlsx') for filename in os.listdir(dir_path)):
        time.sleep(1)

# Perform login
wait = WebDriverWait(driver, 10)
driver.get("https://accounts.sapo.vn/login")
wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="username"]'))).send_keys('0764402536')
wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="password"]'))).send_keys('tamtrinh123@')
login_button = driver.find_element(By.XPATH, "//button[@type='submit' and text()='Đăng nhập']")
login_button.click()
wait.until(EC.url_contains("https://accounts.sapo.vn/sso/access-to-store"))

# Access the orders page
driver.get("https://tamtrinhshop.mysapogo.com/admin/orders")
time.sleep(3)

# Click elements on the page
xpath_list = [
    # List of xpaths to click
]
for xpath in xpath_list:
    click_safe(driver, xpath)
    time.sleep(3)  # Wait 3 seconds between each click

# Select 'HẰNG' checkbox
try:
    wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[7]/div/div/div[1]/div[2]/input'))).send_keys('HẰNG')
    time.sleep(2)
    element = wait.until(EC.visibility_of_element_located((By.XPATH, "//p[contains(text(),'Select all')]")))
    parent_element = element.find_element(By.XPATH, "..")
    parent_element.click()
except TimeoutException:
    print("Timeout occurred while waiting for element")

# Click the complete button
xpath_button = '/html/body/div[7]/div/button'
click_safe(driver, xpath_button)

# Download the Excel file
try:
    element = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[2]/div/div[3]/div[1]/div[1]/table/tbody/tr[1]/td[7]/a')))
    element.click()
    wait_for_download(download_dir)  # Wait until download is complete
    print("Downloaded Excel file successfully!")
    for file in python_files:
        subprocess.run(["python", file])
except TimeoutException:
    print("Timeout occurred while waiting for download")
