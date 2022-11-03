from main import *
import tkinter as tk
from loguru import logger
from datetime import date

current_date = date.today()
logger.add(f"{current_date}-TESPY.Interface.log", format="{time} | {level} | {message}")

window = tk.Tk()
title = tk.Label(text="TES")
title.grid(row=0, columnspan=3, pady=2)

driver = None

def initialize():
    global driver
    driver = initialize_driver()


init_button = tk.Button(text="Initialize browser", command=initialize)
init_button.grid(row=1, column=0, pady=2)


def login_init():
    global driver
    login(driver)
    logger.debug('Logged into Tesseract')


login_button = tk.Button(text="Login", command=login_init)
login_button.grid(row=1, column=1, pady=2)

employee_label = tk.Label(text="Employee Number")
employee_label.grid(row=2, column=0, pady=2)
employee_entry = tk.Entry()
employee_entry.grid(row=2, column=1, pady=2)
employee_save = tk.IntVar()
employee_save_query = tk.Checkbutton(text="save?", variable=employee_save)
employee_save_query.grid(row=2, column=2, pady=2)
time_taken_label = tk.Label(text="Time Taken")
time_taken_label.grid(row=3, column=0, pady=2)
time_taken_entry = tk.Entry()
time_taken_entry.grid(row=3, column=1, pady=2)
time_taken_save = tk.IntVar()
time_taken_save_query = tk.Checkbutton(text="save?", variable=time_taken_save)
time_taken_save_query.grid(row=3, column=2, pady=2)

job_number_label = tk.Label(text="Job Number")
job_number_label.grid(row=4, column=0, pady=2)
job_number_entry = tk.Entry()
job_number_entry.grid(row=4, column=1, pady=2)
job_number_save = tk.IntVar()
job_number_save_query = tk.Checkbutton(text="save?", variable=job_number_save)

next_area_label = tk.Label(text="Next Aera")
next_area_label.grid(row=5, column=0, pady=2)
next_area_entry = tk.Entry()
next_area_entry.grid(row=5, column=1, pady=2)
next_area_save = tk.IntVar()
next_area_save_query = tk.Checkbutton(text="save?", variable=next_area_save)
next_area_save_query.grid(row=5, column=2, pady=2)

custom_fault_code_label = tk.Label(text="Fault Code")
custom_fault_code_label.grid(row=6, column=0, pady=2)
custom_fault_code_entry = tk.Entry()
custom_fault_code_entry.grid(row=6, column=1, pady=2)
custom_fault_code_save = tk.IntVar()
custom_fault_code_query = tk.Checkbutton(text="save?", variable=custom_fault_code_save)
custom_fault_code_query.grid(row=6, column=2, rowspan=2, pady=2)


def disable_fault_code_cdm():
    if is_cust_damage_var.get():
        custom_fault_code_entry.delete(0, tk.END)
        custom_fault_code_entry.insert(0, "CDM")
        custom_fault_code_entry.config(state="disabled")
    else:
        custom_fault_code_entry.config(state="normal")


is_cust_damage_var = tk.IntVar()
is_cust_damage_checkbox = tk.Checkbutton(
    text="Customer Damage?", variable=is_cust_damage_var, command=disable_fault_code_cdm
)
is_cust_damage_checkbox.grid(row=7, column=1, pady=2)

custom_repair_code_label = tk.Label(text="Repair Code")
custom_repair_code_label.grid(row=8, column=0, pady=2)
custom_repair_code_entry = tk.Entry()
custom_repair_code_entry.grid(row=8, column=1, pady=2)
custom_repair_code_save = tk.IntVar()
custom_repair_code_query = tk.Checkbutton(
    text="save?", variable=custom_repair_code_save
)
custom_repair_code_query.grid(row=8, column=2, rowspan=2, pady=2)


def disable_repair_code_nff():
    if is_nff_var.get():
        custom_repair_code_entry.delete(0, tk.END)
        custom_repair_code_entry.insert(0, "8")
        custom_repair_code_entry.config(state="disabled")
    else:
        custom_repair_code_entry.config(state="normal")


is_nff_var = tk.IntVar()
is_nff_checkbox = tk.Checkbutton(
    text="NFF?", variable=is_nff_var, command=disable_repair_code_nff
)
is_nff_checkbox.grid(row=9, column=0, pady=2)


def disable_repair_code_warranty():
    if warranty_return_var.get():
        custom_repair_code_entry.delete(0, tk.END)
        custom_repair_code_entry.insert(0, "1")
        custom_repair_code_entry.config(state="disabled")
    else:
        custom_repair_code_entry.config(state="normal")


warranty_return_var = tk.IntVar()
warranty_return_checkbox = tk.Checkbutton(
    text="warranty return?",
    variable=warranty_return_var,
    command=disable_repair_code_warranty,
)
warranty_return_checkbox.grid(row=9, column=1, pady=2)

solution_label = tk.Label(text="Solution")
solution_label.grid(row=10, column=0, pady=2)
solution_text = tk.Text(height=3, width=30)
solution_text.grid(row=10, column=1, pady=2)
solution_save = tk.IntVar()
solution_query = tk.Checkbutton(text="save?", variable=solution_save)
solution_query.grid(row=10, column=2, pady=2)

is_repaired_checkbox_var = tk.IntVar()
is_repaired_checkbox = tk.Checkbutton(
    text="Item Repaired?", variable=is_repaired_checkbox_var
)
is_repaired_checkbox.grid(row=11, column=0, columnspan=3, pady=2)


def submit():
    global driver
    employee = employee_entry.get()
    time_taken = int(time_taken_entry.get())
    job_number = job_number_entry.get()
    next_area = next_area_entry.get()
    fault_code = custom_fault_code_entry.get()
    customer_damage = is_cust_damage_var.get() == 1
    repair_code = custom_repair_code_entry.get()
    nff = is_nff_var.get() == 1
    warranty_return = warranty_return_var.get() == 1
    solution = solution_text.get("1.0", tk.END)
    item_repaired = is_repaired_checkbox_var.get() == 1
    logger.info(f'Employee: {employee}, Time Taken: {time_taken}, Job Number: {job_number}, '
                f'Next Area: {next_area}, Fault Code:{fault_code}, Customer Damage?: {customer_damage}, '
                f'Repair Code: {repair_code}, NFF?: {nff}, Warranty Return: {warranty_return}, '
                f'Solution: {solution}, Item Repaired?: {item_repaired}')
    if len(job_number) > 6:
        logger.debug('Sending job number through conversion service report method')
        AddServiceReport(
            driver,
            employee=employee,
            time_taken=time_taken,
            solution=solution,
            next_area=next_area,
            is_repaired=item_repaired,
            is_cust_damage=customer_damage,
            is_nff=nff,
            had_parts=False,
            custom_fault_code=fault_code,
            custom_repair_code=repair_code,
            warranty_return=warranty_return,
            ro=job_number,
        )
        if item_repaired:
            print_window(driver, ro=job_number)
    else:
        logger.debug('Sending job number to Service Report')
        AddServiceReport(
            driver,
            employee=employee,
            time_taken=time_taken,
            solution=solution,
            next_area=next_area,
            is_repaired=item_repaired,
            is_cust_damage=customer_damage,
            is_nff=nff,
            had_parts=False,
            custom_fault_code=fault_code,
            custom_repair_code=repair_code,
            warranty_return=warranty_return,
            call_num=job_number,
        )
        if item_repaired:
            print_window(driver, call_num=job_number)

    if not employee_save.get():
        employee_entry.delete(0, tk.END)
    if not time_taken_save.get():
        time_taken_entry.delete(0, tk.END)
    if not solution_save.get():
        solution_text.delete("1.0", tk.END)
    if not next_area_save.get():
        next_area_entry.delete(0, tk.END)
    is_repaired_checkbox_var.set(0)
    if not custom_fault_code_save.get():
        custom_fault_code_entry.delete(0, tk.END)
        is_cust_damage_var.set(0)
    if not custom_repair_code_save.get():
        custom_repair_code_entry.delete(0, tk.END)
        warranty_return_var.set(0)
        is_nff_var.set(0)
    job_number_entry.delete(0, tk.END)

    pass


submit_button = tk.Button(text="Submit", command=submit)
submit_button.grid(row=12, column=0, columnspan=3, pady=2)

# had_parts = False,

author = tk.Label(text="by Kieran Wynne")
author.grid(row=13, column=0, columnspan=3, pady=2)
window.mainloop()
