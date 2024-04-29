import os
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
import time
# Danh sách các file Python bạn muốn chạy
python_files = ["clear_data.py"]
def click_safe(driver, xpath):
    try:
        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        element.click()
    except (StaleElementReferenceException, TimeoutException) as e:
        print(f"Error clicking element with xpath {xpath}: {e}")
        print("Retrying...")
        click_safe(driver, xpath)
    except Exception as e:
        print(f"Error clicking element with xpath {xpath}: {e}")

# Thư mục tải về
download_dir = '\\root\\tool_crawl_sapo\\data'

# Khởi tạo Chrome WebDriver
chrome_options = webdriver.ChromeOptions()
prefs = {'download.default_directory': download_dir}
chrome_options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(options=chrome_options)
print("Initializing Chrome WebDriver with specified options.")
# Chờ cho tải về hoàn tất
def wait_for_download(dir_path):
    while not any(filename.endswith('.xlsx') for filename in os.listdir(dir_path)):
        time.sleep(1)

print("Opening Sapo login page.")
wait = WebDriverWait(driver, 10)
driver.get("https://accounts.sapo.vn/login")
wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="username"]'))).send_keys('0764402536')
wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="password"]'))).send_keys('tamtrinh123@')
login_button = driver.find_element(By.XPATH, "//button[@type='submit' and text()='Đăng nhập']")
login_button.click()
wait.until(EC.url_contains("https://accounts.sapo.vn/sso/access-to-store"))

print("Navigating to the orders page.")
driver.get("https://tamtrinhshop.mysapogo.com/admin/orders")
time.sleep(3)

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
    time.sleep(3)  # Đợi 3 giây giữa các lần click

print("Selecting the 'HẰNG' checkbox.")
try:
    wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[7]/div/div/div[1]/div[2]/input'))).send_keys('HẰNG')
    time.sleep(2)
    element = wait.until(EC.visibility_of_element_located((By.XPATH, "//p[contains(text(),'Chọn tất cả')]")))
    parent_element = element.find_element(By.XPATH, "..")
    parent_element.click()
except TimeoutException:
    print("Timeout occurred while waiting for element")

print("Clicking the completion button.")
xpath_button = '/html/body/div[7]/div/button'
click_safe(driver, xpath_button)

print("Attempting to download the Excel file.")
try:
    element = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[2]/div/div[3]/div[1]/div[1]/table/tbody/tr[1]/td[7]/a')))
    element.click()
    wait_for_download(download_dir)  # Chờ tải về hoàn tất
    print("Downloaded Excel file successfully!")
    for file in python_files:
        subprocess.run(["python", file])
except TimeoutException:
    print("Timeout occurred while waiting for dowload")
