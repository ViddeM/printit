from typing import List

import requests
from lxml import etree

from printer import Printer


def get_printer_list() -> List[Printer]:
    printer_list_url = "https://print.chalmers.se/public/pls.cgi"

    try:
        resp = requests.get(printer_list_url)
    except requests.RequestException:
        return []

    table = etree.HTML(resp.content).find("body/table")
    rows = iter(table)
    headers = [col.text for col in next(rows)]
    headers.insert(1, "printer_link")

    table_dict = []
    for row in rows:
        # values = [col.text for col in row]
        values = []

        for col in row:
            if col.text is not None:
                values.append(col.text.strip())
            else:
                for child in col:
                    if child.tag == "a":
                        values.append(child.text.strip())
                        values.append(child.attrib["href"].strip())

        table_dict.append(dict(zip(headers, values)))

    printers = []
    for printer_data in table_dict:
        printer = Printer(
            support=printer_data["Support"],
            color_mode=printer_data["colormode"],
            cost=printer_data["cost Duplex A4 (PQ)"],
            description=printer_data["description"],
            location=printer_data["location"],
            printer=printer_data["printer"],
            printer_link=printer_data["printer_link"],
            size=printer_data["size"]
        )
        printers.append(printer)

    return printers


