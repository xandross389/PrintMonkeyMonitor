from ast import Try
from cmath import nan
from datetime import datetime
from json import dumps
import json
import time
import logging
from traceback import print_tb
from urllib import response
from win32 import win32print
from classes import Job, Printer
import requests

logging.basicConfig(filename="printmonkeymonitor.log", level=logging.INFO)


API_ROOT_PATH = "/api/v1"
BACKEND_SERVER = "http://127.0.0.1:3000"

notified_jobs = []
registered_printers = []


def log_printer_job(printer, printer_job):
    """
    printer: Tuple -> (8388608, 'Send To OneNote 2016,Send to Microsoft OneNote 16 Driver,', 'Send To OneNote 2016', '')
    printer_job: Dict -> {'JobId': 9, 'pPrinterName': 'NPI602C37 (HP LaserJet 400 M401n)',
                        'pMachineName': '\\\\PC12ads40', 'pUserName': 'uasername', 'pDocument': 'new 4',
                        'pDatatype': 'RAW', 'pStatus': None, 'Status': 12288, 'Priority': 1, 'Position': 1,
                        'TotalPages': 1, 'PagesPrinted': 1, 'Submitted': pywintypes.datetime(2021, 12, 27, 16, 46, 17, 74000,
                        tzinfo=TimeZoneInfo('GMT Standard Time', True))}
    """

    flags, desc, name, comment = printer

    logging.info(f"New printer job for printer {name}: {printer_job}")
    notified_jobs.append(printer_job)
    logging.info(
        f"JobId {printer_job['JobId']} printer details: name: {name}, desc: {desc}, comment: {comment}"
    )


def is_registered_printer(printer):
    flags, desc, name, comment = printer
    for reg_printer in registered_printers:
        reg_flags, reg_desc, reg_name, reg_comment = reg_printer
        if name == reg_name and desc == reg_desc:
            return True
    return False


def is_notified_job(printer_job):
    for job in notified_jobs:
        if int(job["JobId"]) == int(printer_job["JobId"]):
            return True
    return False


def print_job_checker():

    for printer in win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL, None, 1):
        flags, desc, name, comment = printer

        if not is_registered_printer(printer):
            print("New registered printer found. Lets submit")
            registered_printers.append(printer)
            printer_obj = Printer(name=name, desc=desc, comment=comment, flags=flags)
            submit_printer(printer_obj)
        else:
            print("Already registered printer")

        # logging.info(f"Printer object example: {printer}")

        try:
            phandle = win32print.OpenPrinter(name)
            print_jobs = win32print.EnumJobs(phandle, 0, -1, 1)

            if print_jobs:
                for print_job in print_jobs:
                    print(
                        f"Current jobs: {len(print_jobs)} - notified jobs {len(notified_jobs)}"
                    )

                    if len(notified_jobs) == 0 or not is_notified_job(print_job):
                        log_printer_job(printer, print_job)

        except:
            logging.error(
                f"Error triying to obtain handler and printer jobs. Printer name: {name}"
            )
        finally:
            win32print.ClosePrinter(phandle)


def submit_printers_list(printers_lst: list()):
    endpoint_url = f"{BACKEND_SERVER}{API_ROOT_PATH}/printers"

    # TODO: Check if some printer in the list aleready submitted to the server

    try:
        response = requests.post(
            url=endpoint_url,
            json={"printers": [printer.as_json() for printer in printers_lst]},
        )

        if response.status_code == 201:
            print(f"Printers list submited")
            return True
        else:
            print(f"Printer not created - STATUS {response.status_code}")
            return False
    except Exception as ex:
        print(f"Error submiting printers list ({ex})")
        return False


def submit_printer(printer: Printer):
    endpoint_url = f"{BACKEND_SERVER}{API_ROOT_PATH}/printer"

    # TODO: Check if printer aleready submited to the server

    try:
        response = requests.post(url=endpoint_url, json=printer.as_json())

        if response.status_code == 201:
            print(f"Printer submited")
            return True
        else:
            print(f"Printer not created - STATUS {response.status_code}")
            return False
    except Exception as ex:
        print(f"Error submiting printer ({ex})")
        return False


def submit_jobs_list(jobs_lst: list()):
    endpoint_url = f"{BACKEND_SERVER}{API_ROOT_PATH}/jobs"

    try:
        response = requests.post(
            url=endpoint_url,
            json={"jobs": [job.as_json() for job in jobs_lst]},
        )

        if response.status_code == 201:
            # print(f"Jobs list submited")
            return True
        else:
            print(f"Jobs list not created - STATUS {response.status_code}")
            return False
    except Exception as ex:
        print(f"Error submiting jobs list ({ex})")
        return False


def submit_job(job: Job):
    endpoint_url = f"{BACKEND_SERVER}{API_ROOT_PATH}/job"

    try:
        response = requests.post(url=endpoint_url, json=job.as_json())

        if response.status_code == 201:
            print(f"Job submited")
            return True
        else:
            print(f"Job not created - STATUS {response.status_code}")
            return False
    except Exception as ex:
        print(f"Error submiting job ({ex})")
        return False


if __name__ == "__main__":
    # print("Monitoring print jobs!")
    # print(datetime.now())
    # job = Job(
    #     1,
    #     "Job",
    #     1,
    #     1,
    #     1,
    #     1,
    #     datetime.now(),
    # )
    # print(job.submit_time)
    # submit_job(job)

    # jobs_list = []

    # for i in range(2):
    #     job = Job(i, f"Printer job {i}", 1, 1, 1, 1, datetime.now())
    #     jobs_list.append(job)

    # submit_jobs_list(jobs_list)
    ###########
    # printers_list = []

    # for i in range(2):
    #     printer = Printer(f"PDF Virtual Printer N{i}")
    #     printers_list.append(printer)

    # submit_printers_list(printers_list)

    print("Monitoring print jobs!")
    while True:
        print_job_checker()
        time.sleep(1)
