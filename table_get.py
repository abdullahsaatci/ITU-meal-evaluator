from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
import time
import csv

# Path to your ChromeDriver executable
chrome_driver_path = '/Users/abdullahsaatci/........../chromedriver'

# Set up the Chrome WebDriver
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)

# URL of the page
url = 'https://sks.itu.edu.tr/'
driver.get(url)
food_list = []
with open('food_list.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    field = ["Ratings","Food Types"]
    writer.writerow(field)
    for k in range(2):
        if k == 1:
            select_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'ddlYemekTipi'))
            )
            # Use Select class for interacting with <select> elements
            dropdown = Select(select_element)
            # Change the selection to "Akşam Yemeği" (Dinner) by value
            dropdown.select_by_value('itu-aksam-yemegi-genel')
        for j in range(4,12):
            for i in range(2,31): 
                wait = WebDriverWait(driver, 10)
                date_input = wait.until(EC.presence_of_element_located((By.ID, 'datepicker')))

                # Clear the existing date value (if any)
                date_input.clear()

                # Set a new date value (e.g., '12-23-2023')
                if i < 10:
                    new_date = f'0{i}-{j}-23'
                else:
                    new_date = f'{i}-{j}-23'
                date_input.send_keys(new_date)
                # time.sleep(3)
                date_input.send_keys(Keys.RETURN)
                # time.sleep(3)
                button = wait.until(EC.element_to_be_clickable((By.ID, 'btnGoster')))
                # time.sleep(3)
                # Click the button
                button.click()
                time.sleep(8)
                try:
                    # Wait for the table to be present
                    wait = WebDriverWait(driver, 10)
                    table = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'table.table-bordered')))
                    if table:
                        rows = table.find_elements(By.TAG_NAME, 'tr')
                        for row in rows:
                            cells = row.find_elements(By.TAG_NAME, 'td')
                            for cell in cells:
                                list_first = [0]
                                if (cell.text.strip().isupper()):
                                    if cell.text.strip() not in food_list:
                                        food_list.append(cell.text.strip())
                                        list_first.append(cell.text.strip())
                                        writer.writerow(list_first)
                except TimeoutException:
                    # Handle the case where the table is not found
                    print(f"No table found for date: {new_date}")
driver.quit()
