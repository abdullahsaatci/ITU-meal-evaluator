from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import time
from selenium.webdriver.support.ui import Select
from datetime import datetime
import csv
import pywhatkit as kit

### 4 for main meal, 2.75 for second meal, 2.25 for others, 1 for soap
# Specify the phone number (with country code) and the message
phone_number = "+90***"

# Function to search for input data in the CSV file
def search_in_csv(input_data, file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        # Skip the header if present
        header = next(reader, None)
        
        if header:
            food_index = header.index('Food Types')  # Replace 'Food' with the actual header name of food names column
            score_index = header.index('Ratings')  # Replace 'Scores' with the actual header name of scores column
            
            for row in reader:
                if row[food_index] == input_data:
                    return row[score_index]
    
    return None
file_path = 'food_list.csv'
# Get current date and time
current_datetime = datetime.now()

# Extract day, month, and year information
day_number = current_datetime.day  # Day of the month (1 to 31)
month_number = current_datetime.month  # Month (1 to 12)
year_number = current_datetime.year  # Year (e.g., 2023)
year_number %= 100

# Path to your ChromeDriver executable
chrome_driver_path = '/Users/abdullahsaatci/Documents/rarely_used_packages/chromedriver-mac-arm64/chromedriver'

# Set up the Chrome WebDriver
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)

# URL of the page
url = 'https://sks.itu.edu.tr/'
driver.get(url)


wait = WebDriverWait(driver, 10)

lunch_score = 0
dinner_score = 0
date_input = wait.until(EC.presence_of_element_located((By.ID, 'datepicker')))

date_input.clear()

new_date = f'{day_number}-{month_number}-{year_number}'
date_input.send_keys(new_date)
# time.sleep(3)
date_input.send_keys(Keys.RETURN)
for i in range(2):
    if i == 1:
        time.sleep(5)
        select_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'ddlYemekTipi'))
            )
        dropdown = Select(select_element)
        
        # Change the selection to "Akşam Yemeği" (Dinner) by value
        dropdown.select_by_value('itu-aksam-yemegi-genel')
        time.sleep(3)
        button = wait.until(EC.element_to_be_clickable((By.ID, 'btnGoster')))
        button.click()
        time.sleep(10)
    elif i == 0:
        time.sleep(5)
        select_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'ddlYemekTipi'))
            )
        dropdown = Select(select_element)
        
        # Change the selection to "Akşam Yemeği" (Dinner) by value
        dropdown.select_by_value('itu-ogle-yemegi-genel')
        time.sleep(3)
        button = wait.until(EC.element_to_be_clickable((By.ID, 'btnGoster')))
        button.click()
        time.sleep(10)
    try:
        list_first = []
        # Wait for the table to be present
        wait = WebDriverWait(driver, 10)
        table = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'table.table-bordered')))

        if table:
            rows = table.find_elements(By.TAG_NAME, 'tr')
            for row in rows:
                cells = row.find_elements(By.TAG_NAME, 'td')
                for cell in cells:
                    if (cell.text.strip().isupper()):
                        list_first.append(cell.text.strip())
            if len(list_first) > 4 and i == 0:
                print(list_first)
                max = 0
                for j in range(3):
                    if search_in_csv(list_first[j], file_path) != None:
                        lunch_score += float(search_in_csv(list_first[j], file_path))
                for k in range(3, len(list_first)):
                    if search_in_csv(list_first[k], file_path) != None:
                        if float(search_in_csv(list_first[k], file_path)) > max:
                            max = float(search_in_csv(list_first[k], file_path))
                lunch_score += max
            elif len(list_first) <= 4 and i == 0:
                print(list_first)
                for j in range(4):
                    if search_in_csv(list_first[j], file_path) != None:
                        lunch_score += float(search_in_csv(list_first[j], file_path))
            elif len(list_first) > 4 and i == 1:
                print(list_first)
                # print("here")
                max = 0
                for j in range(3):
                    if search_in_csv(list_first[j], file_path) != None:
                        dinner_score += float(search_in_csv(list_first[j], file_path))
                for k in range(3, len(list_first)):
                    # print(list_first[k])
                    if search_in_csv(list_first[k], file_path) != None:
                        if float(search_in_csv(list_first[k], file_path)) > max:
                            max = float(search_in_csv(list_first[k], file_path))
                # print(max)
                dinner_score += max
            elif len(list_first) <= 4 and i == 1:
                print(list_first)
                for j in range(4):
                    if search_in_csv(list_first[j], file_path) != None:
                        dinner_score += float(search_in_csv(list_first[j], file_path))
    except TimeoutException:
        # Handle the case where the table is not found
        # prfloat(f"No table found for date: {new_date}")
        pass
if (lunch_score > 10):
    lunch_score = 10
if (dinner_score > 10):

    dinner_score = 10
lunch_score = round(lunch_score,2)
dinner_score = round(dinner_score,2)
message = f"Lunch score: {lunch_score} and dinner score: {dinner_score}"
print(message)
kit.sendwhatmsg_instantly(phone_number, message)
driver.quit()