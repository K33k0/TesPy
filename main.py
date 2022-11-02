#! python
import time

from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
import toml
import requests
import json
from datetime import datetime, timedelta

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
        call_num = getCallNumFromRO(driver, ro)
    driver.get(
        f"https://{SUBDOMAIN}.asolvi.io/ServiceCentre/SC_RepairJob/aspx/repairjob_modify.aspx?CALL_NUM={call_num}"
    )

def UpdateCall(driver=None, problem=None, engineer=None, rma=None, prob_code=None,
               awaiting_part=None, ship_site=None, is_repaired=None, next_area=None):
    wait = WebDriverWait(driver, 15, poll_frequency=0.5)

    wait.until(EC.element_to_be_clickable((By.ID, 'scmaster_cplMainContent_ruDateTime_header'))).click()
    wait.until(EC.element_to_be_clickable((By.ID, 'scmaster_cplMainContent_ruRefDetails_header'))).click()
    wait.until(EC.element_to_be_clickable((By.ID, 'scmaster_cplMainContent_ruShippingDetails_header'))).click()

    ship_status_selector = 'scmaster_cplMainContent_txtJobShipDate1'
    job_shipped = wait.until(EC.element_to_be_clickable((By.ID, ship_status_selector))).text



    if problem:
        # Text area id
        elem_selector = 'scmaster_cplMainContent_txtCallProblem'
        elem = wait.until(EC.element_to_be_clickable((By.ID, elem_selector)))
        elem.send_keys(f' ## {problem} ##')

    if engineer:
        # input id
        elem_selector = 'scmaster_cplMainContent_cboCallEmployNum'
        elem = wait.until(EC.element_to_be_clickable((By.ID, elem_selector)))
        current_employee = elem.text
        elem.clear()
        elem.send_keys(engineer)
        
    if rma:
        # input id
        elem_selector = 'scmaster_cplMainContent_txtJobApproveRef'
        elem = wait.until(EC.element_to_be_clickable((By.ID, elem_selector)))
        current_rma = elem.text
        elem.clear()
        elem.send_keys(rma)

    if prob_code:
        # input id
        elem_selector = 'scmaster_cplMainContent_cboCallProbCode'
        elem = wait.until(EC.element_to_be_clickable((By.ID, elem_selector)))
        current_prob_code = elem.text   
        elem.clear()
        elem.send_keys(prob_code)

    if awaiting_part:
        # input id
        elem_selector = 'scmaster_cplMainContent_txtCallRef'
        elem = wait.until(EC.element_to_be_clickable((By.ID, elem_selector)))
        current_awaiting_part = elem.text     
        elem.clear()
        elem.send_keys(awaiting_part)
        
    if ship_site and not job_shipped == "":
        # input id
        elem_selector = 'scmaster_cplMainContent_cboShipSiteNum'
        elem = wait.until(EC.element_to_be_clickable((By.ID, elem_selector)))
        current_ship_site = elem.text 
        elem.clear()
        elem.send_keys(awaiting_part)

        pass
    # if not blank true (if blank repaired)
    repair_status = wait.until(EC.element_to_be_clickable((By.ID, 'scmaster_cplMainContent_txtCompDate' ))).text
    current_ro = wait.until(EC.element_to_be_clickable((By.ID, 'scmaster_cplMainContent_txtJobRef6'))).text
    current_rico = wait.until(EC.element_to_be_clickable((By.ID, 'scmaster_cplMainContent_txtJobRef4'))).text

    submit_btn = wait.until(EC.element_to_be_clickable((By.ID, "scmaster_btnSubmit")))
    submit_btn.click()

    ## Next area
    next_area_input = wait.until(EC.element_to_be_clickable((By.ID, "scmaster_cplMainContent_cboCallUpdAreaCode")))
    if next_area:
        next_area_input.clear()
        next_area_input.send_keys(next_area)

    if is_repaired and not repair_status == "":
        item_repaired_box = wait.until(
            EC.element_to_be_clickable(
                (By.ID, "scmaster_cplMainContent_chkItemRepaired")
            )
        )
        item_repaired_box.click()

    submit_btn = wait.until(EC.element_to_be_clickable((By.ID, "scmaster_btnSubmit")))
    submit_btn.click()

    alert = WebDriverWait(driver, 15).until(EC.alert_is_present())
    if alert.text == 'Repair Job record was successfully updated':
        alert.accept()
    else:
        raise Exception("Something went wrong with the update")

def getCallNumFromRO(driver, ro):
    url = f"https://{SUBDOMAIN}.asolvi.io/ServiceCentre/SC_RepairJob/aspx/repairjob_query.aspx"

    resp = requests.post(
        url,
        data={
            "ajax-source-id": "scmaster_cplMainContent_grdPowerQuery_ctlPowerQueryGrid",
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
    return call_num


def AddServiceReport(
    driver,
    employee,
    time_taken,
    solution,
    next_area,
    is_repaired,
    is_cust_damage=False,
    is_nff=False,
    had_parts=False,
    custom_fault_code=None,
    custom_repair_code=None,
    warranty_return=False,
    call_num=None,
    ro=None,
):
    if ro:
        call_num = getCallNumFromRO(driver, ro)
    driver.get(
        f"https://{SUBDOMAIN}.asolvi.io/ServiceCentre/SC_RepairJobFSR/aspx/RepairJobFSR_Add.aspx?CALL_NUM={call_num}&Action="
    )

    wait = WebDriverWait(driver, 15, poll_frequency=0.5)

    # Set Employee number
    employ_num_input = wait.until(
        EC.element_to_be_clickable((By.NAME, "scmaster$cplMainContent$cboFSREmployNum"))
    )
    employ_num_input.clear()
    employ_num_input.send_keys(employee)

    # Read current time
    now = datetime.now()
    start_time = now - timedelta(minutes=time_taken)
    ## Set start time
    start_time_input = wait.until(
        EC.element_to_be_clickable((By.NAME, "scmaster$cplMainContent$txtFSRStartTime"))
    )
    start_time_input.clear()
    start_time_input.send_keys(start_time.strftime("%H:%M"))
    ## Set end time
    end_time_input = wait.until(
        EC.element_to_be_clickable(
            (By.NAME, "scmaster$cplMainContent$txtFSRCompleteTime")
        )
    )
    end_time_input.clear()
    end_time_input.send_keys(now.strftime("%H:%M"))

    ## Fault code
    if custom_fault_code:
        fault_code = custom_fault_code
    elif is_cust_damage:
        fault_code = "CDM"
    else:
        fault_code = "HEP"

    fault_code_input = wait.until(
        EC.element_to_be_clickable((By.NAME, "scmaster$cplMainContent$cboFSRFaultCode"))
    )
    fault_code_input.clear()
    fault_code_input.send_keys(fault_code)

    ## Repair code
    if custom_repair_code:
        repair_code = custom_repair_code
    elif had_parts:
        repair_code = "17"
    elif is_nff:
        repair_code = "8"
    elif warranty_return:
        repair_code = "1"
    else:
        repair_code = "3"

    repair_code_input = wait.until(
        EC.element_to_be_clickable((By.NAME, "scmaster$cplMainContent$cboFSRRepCode"))
    )
    repair_code_input.clear()
    repair_code_input.send_keys(repair_code)

    ## Solution

    solution_text_area = wait.until(
        EC.element_to_be_clickable((By.NAME, "scmaster$cplMainContent$txtFSRSolution"))
    )
    solution_text_area.clear()
    solution_text_area.send_keys(solution)

    ## Submit form 1
    submit_btn = wait.until(EC.element_to_be_clickable((By.ID, "scmaster_btnSubmit")))
    submit_btn.click()

    ## Next area
    next_area_input = wait.until(
        EC.element_to_be_clickable(
            (By.NAME, "scmaster$cplMainContent$cboCallUpdAreaCode")
        )
    )
    next_area_input.clear()
    next_area_input.send_keys(next_area)

    ## Item Repaired
    if is_repaired:
        try:
            wait = WebDriverWait(driver, 1, poll_frequency=0.5)
            item_repaired_box = wait.until(
                EC.element_to_be_clickable(
                    (By.NAME, "scmaster$cplMainContent$chkItemRepaired")
                )
            )
            item_repaired_box.click()
        except:
            pass  # item already repaired
    wait = WebDriverWait(driver, 15, poll_frequency=0.5)

    ## Submit form 2
    submit_btn = wait.until(EC.element_to_be_clickable((By.ID, "scmaster_btnSubmit")))
    submit_btn.click()

    alert = WebDriverWait(driver, 15).until(EC.alert_is_present())
    if alert.text == 'This record was successfully added.':
        alert.accept()
    else:
        raise Exception("Something went wrong with your service report")
def print_window(driver, call_num=None, ro=None):
    if ro:
        call_num = getCallNumFromRO(driver, ro)
    url = f"https://{SUBDOMAIN}.asolvi.io/ServiceCentre/SC_Reporting/aspx/report_ssrs_selections.aspx?Report_Id=386&FromName=call&FromURL=SC_RepairJob%2faspx%2fRepairJob_query.aspx&StdInput=KeyValue%3d{call_num}&EmbedReport=Y&KEY_VALUE=SCCall%1eCall_Num%1f{call_num}%1flong&ORIGIN=PRINT&FROM=call"
    data = {
        "txtXLControlId": None,
        "txtCustomMandatoryFields": None,
        "txtCustomMandatoryMsgs": None,
        "txtCustomMaskFields": None,
        "txtCustomMaskMsgs": None,
        "txtCustomMaskRegex": None,
        "__EVENTTARGET": None,
        "__EVENTARGUMENT": None,
        "scmaster_cplMainContent_rolParameters_state": 0,
        "__VIEWSTATE": None,
        "__VIEWSTATEGENERATOR": "09BFEFC8",
        "__VIEWSTATEENCRYPTED": None,
        "scmaster%24cplMainContent%24txtReport_Title": "Workshop+Shipping+-+DYMO",
        "scmaster%24cplMainContent%24txtQueryH_ID": None,
        "scmaster%24cplMainContent%24txtQueryH_Desc": None,
        "scmaster%24cplMainContent%24cboQueryHGroupCode": None,
        "scmaster%24cplMainContent%24grdResults%24ctl02%24txtParamValueSelect": f"{call_num}",
        "scmaster%24cplMainContent%24grdResults%24ctl02%24lstParamMultiValueListField": None,
        "scmaster%24cplMainContent%24txtFormEvent": "onSubmit",
        "scmaster%24cplMainContent%24txtReturnMsg": None,
        "scmaster%24cplMainContent%24txtFunctionsDesc": "reports+selection",
        "scmaster%24cplMainContent%24txtSubmitEnabled": "Y",
        "scmaster%24cplMainContent%24txtPrintEnabled": "N",
        "scmaster%24cplMainContent%24txtHelpEnabled": "Y",
        "scmaster%24cplMainContent%24txtDeleteEnabled": "N",
        "scmaster%24cplMainContent%24txtRunReportFlag": None,
        "scmaster%24cplMainContent%24txtAltReportID": 0,
        "scmaster%24cplMainContent%24txtDropdownStandardWidth": "600px",
        "scmaster%24cplMainContent%24txtDropdownWideWidth": "950px",
        "scmaster%24cplMainContent%24txtReport_ID": 386,
        "scmaster%24cplMainContent%24txtReport_File_Name": "WorkshopShippingLabel-DYMO",
        "scmaster%24cplMainContent%24txtReport_Table_Name": "SCCALL",
        "scmaster%24cplMainContent%24txtCompanyName": None,
        "scmaster%24cplMainContent%24txtReportURL": None,
        "scmaster%24cplMainContent%24txtDirectFromInvoicing": None,
        "scmaster%24cplMainContent%24txtFromName": "call",
        "scmaster%24cplMainContent%24txtFromURL": "SC_RepairJob%2Faspx%2FRepairJob_query.aspx",
        "scmaster%24cplMainContent%24txtStdInput": f"KeyValue%3D{call_num}",
        "scmaster%24cplMainContent%24txtOrigin": "PRINT",
        "scmaster%24cplMainContent%24txtEmbedReport": False,
        "scmaster%24cplMainContent%24txtLoad_QueryH_ID": None,
        "scmaster%24cplMainContent%24txtAdvSelRowCount": 1,
        "scmaster%24cplMainContent%24txtPass_Group": "ADMIN",
        "scmaster%24cplMainContent%24txtAllowInvoicePrintedUpdate": None,
        "scmaster%24cplMainContent%24txtAllowPReqPrintedUpdate": None,
        "scmaster%24cplMainContent%24txtUpdateMsg1": "Do+you+wish+to+update+these+Invoices+as+having+been+Printed%3F",
        "scmaster%24cplMainContent%24txtUpdateMsg2": "Do+you+wish+to+update+these+Parts+Requests+as+having+been+Printed%3F",
        "scmaster%24cplMainContent%24txtInvType": None,
        "scmaster%24cplMainContent%24txtCreditPrinted": None,
        "scmaster%24cplMainContent%24txtAllowCreditPrintedUpdate": None,
        "scmaster%24cplMainContent%24txtUpdateMsg3": "This+Credit+Note+has+already+been+updated+as+Printed.",
        "scmaster%24cplMainContent%24txtUpdateMsg4": "Do+you+wish+to+update+this+Credit+Note+as+having+been+Printed%3F",
        "scmaster%24txtMenuBtnClickBgColor": None,
        "scmaster%24txtLayoutStyle": None,
        "scmaster%24txtShowPageListMenuAsDropdown": None,
        "scmaster%24txtClientDateFormat": "dd%2FMM%2Fyyyy",
        "scmaster%24txtClientTimeFormat": "HH%3Amm",
        "scmaster%24txtClientLongDateFormat": "dd+MMMM+yyyy",
        "scmaster%24txtClientLongTimeFormat": "HH%3Amm%3Ass",
        "scmaster%24txtClientDateSeparator": "%2F",
        "scmaster%24txtClientTimeSeparator": "%3A",
        "scmaster%24txtClientTimeAMDesignator": "AM",
        "scmaster%24txtClientTimePMDesignator": "PM",
        "scmaster%24txtClientDecimalSeparator": ".",
        "scmaster%24txtSiteRoot": "%2FServiceCentre%2F",
        "scmaster%24txtPageFunctionsNum": 1640,
        "scmaster%24txtInitialFocusControlId": None,
        "scmaster%24txtInitialScrollPosControlId": None,
    }
    response = requests.post(
        url,
        data=data,
        headers={
            "referer": f"https://{SUBDOMAIN}.asolvi.io/ServiceCentre/SC_Reporting/aspx/report_ssrs_selections.aspx?Report_Id=386&FromName=call&FromURL=SC_RepairJob%2faspx%2fRepairJob_query.aspx&StdInput=KeyValue%3d{SUBDOMAIN}&EmbedReport=N&KEY_VALUE=SCCall%1eCall_Num%1f{SUBDOMAIN}%1flong&ORIGIN=PRINT&FROM=call"
        },
        cookies=get_cookies(driver),
    )
    driver.get(response.url)

    wait = WebDriverWait(driver, 15, poll_frequency=0.5)
    print_button_1 = wait.until(
        EC.element_to_be_clickable(
            (By.ID, "SSRSReportViewer_ctl09_ctl06_ctl00_ctl00_ctl00")
        )
    )
    print_button_1.click()

    print_button_2 = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                '//*[@id="SSRSReportViewer_fixedTable"]/tbody/tr[4]/td/div[2]/div[1]/div[2]/div[1]/p',
            )
        )
    )
    print_button_2.click()

    driver.execute_script(
    "download_link = document.querySelector('#SSRSReportViewer_fixedTable > tbody > tr:nth-child(4) > td > div.msrs-printdialog-main > div.msrs-printdialog-printing > div.msrs-printdialog-divbuttonscontainer > div > p')\n"
    "download_link.textContent = 'Job Done'\n"
    "download_link.addEventListener('click', function(){\n"
    f"    window.location.href = 'https://{SUBDOMAIN}.asolvi.io/ServiceCentre/SC_MyHome/aspx/myhome.aspx'\n"
    "})"
    )
    time.sleep(3)

    wait = WebDriverWait(driver, 300, poll_frequency=0.5)
    wait.until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="scmaster_sidebarToggle"]/div'))
    )


def initialize_driver():
    service = Service(WEBDRIVER_PATH)
    driver = webdriver.Edge(service=service)
    driver.get(
        f"https://{SUBDOMAIN}.asolvi.io/ServiceCentre/SC_Login/aspx/Login_Launch.aspx"
    )
    return driver


if __name__ == "__main__":
    # Start the browser
    driver = initialize_driver()
    login(driver)
    OpenExistingCall(driver, ro="4802993696")
    # 4802993696 is 414 call
    UpdateCall(driver,"Tesseract test", '406', 'rma', 'TS1', 'awaiting part', 'zulu',True, '3rdp')
