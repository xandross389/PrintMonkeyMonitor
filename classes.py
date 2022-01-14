from datetime import datetime
from dataclasses import dataclass
import json


@dataclass
class Printer:
    name: str
    ip: str = ""
    desc: str = ""
    computer_name: str = ""
    computer_ip: str = ""
    comment: str = ""
    flags: str = ""

    def as_json(self):
        return {
            "name": self.name,
            "ip": self.ip,
            "desc": self.desc,
            "computer_name": self.computer_name,
            "computer_ip": self.computer_ip,
            "comment": self.comment,
            "flags": self.flags,
        }


@dataclass
class Job:
    """
    submit_time: Format "%Y-%m-%d %H:%M:%S" | example datetime.now() -> 2022-01-13 23:24:11.408399

    """

    job_id: int
    printer_name: str
    priority: int
    position: int
    total_pages: int
    pages_printed: int
    submit_time: datetime
    printer_ip: str = ""
    machine_name: str = ""
    machine_ip: str = ""
    username: str = ""
    document: str = ""
    data_type: str = ""
    pstatus: str = ""
    status: str = ""

    def as_json(self):
        return {
            "job_id": self.job_id,
            "printer_name": self.printer_name,
            "priority": self.priority,
            "position": self.position,
            "total_pages": self.total_pages,
            "pages_printed": self.pages_printed,
            "submit_time": self.submit_time.strftime("%Y-%m-%d %H:%M:%S"),
            "printer_ip": self.printer_ip,
            "machine_name": self.machine_name,
            "machine_ip": self.machine_ip,
            "user_name": self.username,
            "document": self.document,
            "data_type": self.data_type,
            "pstatus": self.pstatus,
            "status": self.status,
        }
