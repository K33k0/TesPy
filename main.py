from selenium import webdriver
import toml

# Read the config file
config = toml.load('./config.toml')

# Place constant variables directly below
WEBDRIVER_PATH = config['File_Path']['web_driver']
SUBDOMAIN = config['Tesseract']['instance']


# Start the browser
driver = webdriver.Edge(WEBDRIVER_PATH)
driver.get(f'https://{SUBDOMAIN}.asolvi.io/ServiceCentre/SC_Login/aspx/Login_Launch.aspx')
