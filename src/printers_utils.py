from typing import List, Dict

import click
import requests
from lxml import etree

from src.ResultWithData import get_result_with_error, get_result_with_data, ResultWithData
from src.configuration import PRINTER_LIST_URL
from src.printer import Printer


def get_printer_list() -> List[Printer]:
    try:
        resp = requests.get(PRINTER_LIST_URL)
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


def printer_exists(printer, printers: List[Printer]) -> bool:
    for pr in printers:
        if pr.printer == printer:
            return True
    return False


def select_printer(printers: List[Printer], search: str) -> ResultWithData[str]:
    # convert the list of printers to a dictionary of int -> Printer
    printer_dict = get_printers_dict(printers, search)
    res = print_printers(printer_dict)
    if res.is_error:
        return get_result_with_error(res.message)

    click.echo("===========================")

    while True:
        printer_num = click.prompt("Select printer", type=int)
        number = printer_num - 1

        if number not in printer_dict:
            click.echo("Number must be one of the above")
        else:
            return get_result_with_data(printer_dict[number].printer)


def get_printers_dict(printers: List[Printer], search: str) -> Dict[int, Printer]:
    search = search.lower()
    filtered_printers = []
    # filter the list on the search term
    if search != "":
        for printer in printers:
            to_search = "{0}{1}".format(printer.printer.lower(), printer.location.lower())
            if search in to_search:
                filtered_printers.append(printer)
    else:
        filtered_printers = printers

    printer_dict = dict()
    for i in range(len(filtered_printers) - 1, -1, -1):
        printer_dict[i] = filtered_printers[i]

    return printer_dict


def get_longest_name(printer_dict: Dict[int, Printer]) -> int:
    longest_name = 0
    for printer in printer_dict.values():
        printer_length = len(printer.printer)
        if printer_length > longest_name:
            longest_name = printer_length

    return longest_name


def print_printers(printer_dict: Dict[int, Printer]) -> ResultWithData[str]:
    if len(printer_dict) == 0:
        return get_result_with_error("No printers matched the search")

    longest_name = get_longest_name(printer_dict)
    longest_number = len(str(len(printer_dict)))

    for index in printer_dict:
        printer = printer_dict[index]
        printer_text = "({0})".format(index + 1).rjust(longest_number + 2, " ")
        printer_text += " {0} ".format(printer.printer).ljust(longest_name + 2, " ")
        printer_text += " |- {0}".format(printer.location)

        click.echo(printer_text)
    return get_result_with_data("")
