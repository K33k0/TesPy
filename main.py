from selenium import webdriver
from selenium.webdriver.edge.service import Service
import toml

# Read the config file
config = toml.load('./config.toml')

# Place constant variables directly below
WEBDRIVER_PATH = config['File_Path']['web_driver']
SUBDOMAIN = config['Tesseract']['instance']

if __name__ == '__main__':
    # Start the browser
    service = Service(WEBDRIVER_PATH)
    driver = webdriver.Edge(service=service)
    driver.get(f'https://{SUBDOMAIN}.asolvi.io/ServiceCentre/SC_Login/aspx/Login_Launch.aspx')

