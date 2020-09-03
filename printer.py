from dataclasses import dataclass


@dataclass
class Printer:
    support: str
    color_mode: str
    cost: str
    description: str
    location: str
    printer: str
    printer_link: str
    size: str

