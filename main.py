from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
import pickle
import toml
import requests
import json

# Read the config file
config = toml.load("./config.toml")

# Place constant variables directly below
WEBDRIVER_PATH = config["File_Path"]["web_driver"]
SUBDOMAIN = config["Tesseract"]["instance"]
USERNAME = config["Tesseract"]["username"]
PASSWORD = config["Tesseract"]["password"]


def get_cookies(driver):
    cookies = {}
    selenium_cookies = driver.get_cookies()
    for cookie in selenium_cookies:
        cookies[cookie["name"]] = cookie["value"]
    return cookies


def login(driver=None):
    driver.get(
        f"https://{SUBDOMAIN}.asolvi.io/ServiceCentre/SC_Login/aspx/Login_Launch.aspx"
    )
    driver.find_element(By.ID, "btnsubmit").click()
    if "tesseractidp.eu.auth0.com" in driver.current_url:
        wait = WebDriverWait(driver, 15, poll_frequency=0.5)
        email_input = wait.until(EC.element_to_be_clickable((By.NAME, "email")))
        email_input.send_keys(USERNAME)
        password_input = wait.until(EC.element_to_be_clickable((By.NAME, "password")))
        password_input.send_keys(PASSWORD)
        submit_button = wait.until(EC.element_to_be_clickable((By.NAME, "submit")))
        submit_button.click()
        wait.until(EC.element_to_be_clickable((By.ID, "scmaster_sidebar")))
    if (
        f"https://{SUBDOMAIN}.asolvi.io/ServiceCentre/SC_MyHome/aspx/myhome.aspx"
        in driver.current_url
    ):
        return True
    else:
        raise Exception(f"Failed to find home: {driver.current_url}")


def OpenExistingCall(driver=None, call_num=None, ro=None):
    if ro:
        url = f"https://{SUBDOMAIN}.asolvi.io/ServiceCentre/SC_RepairJob/aspx/repairjob_query.aspx"

        resp = requests.post(
            url,
            data={
                "ajax-source-id": "scmaster_cplMainContent_grdPowerQuery_ctlPowerQueryGrid",
                #"ajax-data-instance-id": "f37fa3af-93aa-43a0-9f2c-e87f2976fe5e",
                "ajax-method": "PowerQueryGrid.RequestData",
                "ajax-data-config": json.dumps(
                    {
                        "listconfigh_id": 109,
                        "listconfigh_functions_num": 7080,
                        "listconfigh_pass_group": "",
                        "listconfigh_pass_user": "kieranw",
                        "listconfigh_default": False,
                        "listconfigh_name": "RO2Call",
                        "listconfigh_object_source": "RepairJob",
                        "listconfigh_last_update": "2022-10-22T20:45:26",
                        "columns": [
                            {
                                "listconfigl_id": 1094,
                                "listconfigl_listconfigh_id": 109,
                                "listconfigl_column_name": "Call_Num",
                                "listconfigl_data_type": "System.Int32",
                                "listconfigl_header_text": "Job",
                                "listconfigl_rank": 1,
                                "listconfigl_data_format": "",
                                "listconfigl_column_width": 50,
                                "listconfigl_alignment": 0,
                                "listconfigl_sort_order": 2,
                                "listconfigl_filter_expr": 3,
                                "listconfigl_filter_value1": "",
                                "listconfigl_filter_value2": "",
                                "listconfigl_last_update": "2022-10-22T20:44:53",
                                "filterapplies": False,
                            },
                            {
                                "listconfigl_id": 1095,
                                "listconfigl_listconfigh_id": 109,
                                "listconfigl_column_name": "Job_Ref6",
                                "listconfigl_data_type": "System.String",
                                "listconfigl_header_text": "RO Number",
                                "listconfigl_rank": 2,
                                "listconfigl_data_format": "",
                                "listconfigl_column_width": 100,
                                "listconfigl_alignment": 0,
                                "listconfigl_sort_order": 0,
                                "listconfigl_filter_expr": 9,
                                "listconfigl_filter_value1": ro,
                                "listconfigl_filter_value2": "",
                                "listconfigl_last_update": "2022-10-22T20:44:53",
                                "filterapplies": False,
                            },
                        ],
                        "issystemconfig": False,
                    }
                ),
                "ajax-data-pagenumber": 1,
                "ajax-data-pagesize": 100,
                "ajax-data-format": 0,
                "ajax-initial-load": False,
                "ajax-custom-query-filter": "Call_StatusWORK",
                "ajax-custom-exclude-criteria": None,
                "__AntiXsrfToken": None,
            },
            cookies=get_cookies(driver),
        )
        call_num = resp.json()["results"][0]["call_num"]
    driver.get(
        f"https://{SUBDOMAIN}.asolvi.io/ServiceCentre/SC_RepairJob/aspx/repairjob_modify.aspx?CALL_NUM={call_num}"
    )


if __name__ == "__main__":
    # Start the browser
    service = Service(WEBDRIVER_PATH)
    driver = webdriver.Edge(service=service)
    driver.get(
        f"https://{SUBDOMAIN}.asolvi.io/ServiceCentre/SC_Login/aspx/Login_Launch.aspx"
    )
    login(driver)
    OpenExistingCall(driver, ro="4802993696")
    #driver.quit()
