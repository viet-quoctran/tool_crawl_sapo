import os
import subprocess
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

def click_safe(driver, xpath):
    try:
        print("Attempting to click element: ", xpath)
        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        element.click()
    except (StaleElementReferenceException, TimeoutException) as e:
        print(f"Error clicking element with xpath {xpath}: {e}")
        print("Retrying...")
        click_safe(driver, xpath)
    except Exception as e:
        print(f"Error clicking element with xpath {xpath}: {e}")

def wait_for_download(dir_path):
    print("Waiting for the file to download.")
    while not any(filename.endswith('.xlsx') for filename in os.listdir(dir_path)):
        time.sleep(1)

# Setting Chrome options for headless mode
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.binary_location = '/usr/bin/google-chrome
# Set download directory
download_dir = '/root/tool_crawl_sapo/data'
prefs = {'download.default_directory': download_dir}
chrome_options.add_experimental_option('prefs', prefs)

# Setup Chrome WebDriver
print("Initializing Chrome WebDriver with specified options.")
service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Login process
print("Opening Sapo login page.")
driver.get("https://accounts.sapo.vn/login")
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="username"]'))).send_keys('0764402536')
wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="password"]'))).send_keys('tamtrinh123@')
login_button = driver.find_element(By.XPATH, "//button[@type='submit' and text()='Đăng nhập']")
login_button.click()
wait.until(EC.url_contains("https://accounts.sapo.vn/sso/access-to-store"))

# Navigating to orders page
print("Navigating to the orders page.")
driver.get("https://tamtrinhshop.mysapogo.com/admin/orders")
time.sleep(3)

# Interacting with elements on the page
print("Starting to click elements on the page.")
xpath_list = [
    '//*[@id="root"]/div[2]/div[2]/div[2]/div[3]/div[1]/div[2]/div[2]/div',
    '/html/body/div[1]/div[2]/div[2]/div[2]/div[3]/div[1]/div[2]/div[2]/div[2]/div/div/button[2]',
    '/html/body/div[1]/div[2]/div[2]/div[2]/div[3]/div[1]/div[2]/div[2]/div[2]/div/button',
    '/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/div[1]/button[1]/span[1]',
    '/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div[2]/div/div[2]',
    '/html/body/div[1]/div[1]/div[2]/div/div[3]/button[2]',
    '/html/body/div[1]/div[1]/div[2]/div/div[3]/button',
    '/html/body/div[1]/div[2]/div[1]/nav/div[2]/div/nav/a[2]',
    '/html/body/div[1]/div[2]/div[2]/div[2]/div[2]/div[3]/div/div[1]/a',
    '/html/body/div[1]/div[2]/div[2]/div[2]/div/div[1]/div[1]/div/div',
    '/html/body/div[1]/div[2]/div[2]/div[2]/div/div[1]/div[1]/div/div[2]/div/div/button[1]',
    '/html/body/div[1]/div[2]/div[2]/div[2]/div/div[1]/div[1]/div/div[2]/div/button',
    '/html/body/div[1]/div[2]/div[2]/div[2]/div/div[1]/div[1]/div/button[1]'
]
for xpath in xpath_list:
    click_safe(driver, xpath)
    time.sleep(3)

# Selecting specific checkbox
print("Selecting the 'HẰNG' checkbox.")
try:
    wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[7]/div/div/div[1]/div[2]/input'))).send_keys('HẰNG')
    time.sleep(2)
    element = wait.until(EC.visibility_of_element_located((By.XPATH, "//p[contains(text(),'Chọn tất cả')]")))
    parent_element = element.find_element(By.XPATH, "..")
    parent_element.click()
except TimeoutException:
    print("Timeout occurred while waiting for element")

# Completion button click
print("Clicking the completion button.")
xpath_button = '/html/body/div[7]/div/button'
click_safe(driver, xpath_button)

# Attempting to download Excel file
print("Attempting to download the Excel file.")
try:
    element = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[2]/div/div[3]/div[1]/div[1]/table/tbody/tr[1]/td[7]/a')))
    element.click()
    wait_for_download(download_dir)
    print("Downloaded Excel file successfully!")
    for file in python_files:
        subprocess.run(["python", file])
except TimeoutException:
    print("Timeout occurred while waiting for download")

# Closing the driver
driver.quit()
