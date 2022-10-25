from main import *

EMPLOYEE = '406'

driver = initialize_driver()
login(driver)


all_jobs = [
    {
        'employee': EMPLOYEE, 'time_taken': 30, 'solution': 'Tesseract Test', 'next_area': 'WREP',
        'is_repaired': False, 'is_cust_damage': False, 'is_nff': False, 'had_parts': False, 'custom_fault_code': None,
        'custom_repair_code': None, 'warranty_return': False, 'job_num': '4802993696'
    },
    {
        'employee': EMPLOYEE, 'time_taken': 30, 'solution': 'Tesseract Test', 'next_area': 'WREP',
        'is_repaired': False, 'is_cust_damage': False, 'is_nff': True, 'had_parts': False, 'custom_fault_code': None,
        'custom_repair_code': None, 'warranty_return': False, 'job_num': '721644'
    }
]
for job in all_jobs:


    if len(job['job_num']) > 6:
        print("Running with ro")
        AddServiceReport(
            driver = driver,
            ro= job['job_num'],
            employee = job['employee'],
            time_taken = job['time_taken'],
            solution = job['solution'],
            next_area = job['next_area'],
            is_repaired = job['is_repaired'],
            is_cust_damage = job['is_cust_damage'],
            is_nff = job['is_nff'],
            had_parts = job['had_parts'],
            custom_fault_code = job['custom_fault_code'],
            custom_repair_code = job['custom_repair_code'],
            warranty_return = job['warranty_return']
        )
        print_window(driver, ro=job['job_num'])
    else:
        AddServiceReport(
            driver = driver,
            call_num= job['job_num'],
            employee = job['employee'],
            time_taken = job['time_taken'],
            solution = job['solution'],
            next_area = job['next_area'],
            is_repaired = job['is_repaired'],
            is_cust_damage = job['is_cust_damage'],
            is_nff = job['is_nff'],
            had_parts = job['had_parts'],
            custom_fault_code = job['custom_fault_code'],
            custom_repair_code = job['custom_repair_code'],
            warranty_return = job['warranty_return']
        )
        print_window(driver, call_num=job['job_num'])

