from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
import toml

# Read the config file
config = toml.load('./config.toml')

# Place constant variables directly below
WEBDRIVER_PATH = config['File_Path']['web_driver']
SUBDOMAIN = config['Tesseract']['instance']
USERNAME = config['Tesseract']['username']
PASSWORD = config['Tesseract']['password']


def login(web_driver=None):
    web_driver.get(f'https://{SUBDOMAIN}.asolvi.io/ServiceCentre/SC_Login/aspx/Login_Launch.aspx')
    web_driver.find_element(By.ID, "btnsubmit").click()
    if 'tesseractidp.eu.auth0.com' in web_driver.current_url:
        wait = WebDriverWait(web_driver, 15, poll_frequency=0.5)
        email_input = wait.until(EC.element_to_be_clickable((By.NAME, "email")))
        email_input.send_keys(USERNAME)
        password_input = wait.until(EC.element_to_be_clickable((By.NAME, "password")))
        password_input.send_keys(PASSWORD)
        submit_button = wait.until(EC.element_to_be_clickable((By.NAME, "submit")))
        submit_button.click()
        wait.until(EC.element_to_be_clickable((By.ID, "scmaster_sidebar")))
    if f'https://{SUBDOMAIN}.asolvi.io/ServiceCentre/SC_MyHome/aspx/myhome.aspx' in web_driver.current_url:
        return True
    else:
        raise Exception(f'Failed to find home: {web_driver.current_url}')


if __name__ == '__main__':
    # Start the browser
    service = Service(WEBDRIVER_PATH)
    driver = webdriver.Edge(service=service)
    driver.get(f'https://{SUBDOMAIN}.asolvi.io/ServiceCentre/SC_Login/aspx/Login_Launch.aspx')
    login(driver)
