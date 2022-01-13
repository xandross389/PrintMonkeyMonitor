from datetime import datetime
from dataclasses import dataclass


@dataclass
class Printer:
    name: str
    ip: str
    desc: str
    computer_name: str
    computer_ip: str
    comment: str
    flags: str


@dataclass
class Job:
    job_id: int
    printer_name: str
    printer_ip: str
    machine_name: str
    machine_ip: str
    username: str
    document: str
    data_type: str
    pstatus: str
    status: str
    priority: int
    position: int
    total_pages: int
    pages_printed: int
    submit_time: datetime
