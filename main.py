import time
import logging
from win32 import win32print

logging.basicConfig(filename="printmonkeymonitor.log", level=logging.INFO)

notified_jobs = []


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


def is_notified_job(printer_job):
    for job in notified_jobs:
        if int(job["JobId"]) == int(printer_job["JobId"]):
            return True
    return False


def print_job_checker():

    for printer in win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL, None, 1):
        flags, desc, name, comment = printer

        logging.info(f"Printer object example: {printer}")

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


if __name__ == "__main__":
    print("Monitoring print jobs!")
    while True:
        print_job_checker()
        time.sleep(1)
