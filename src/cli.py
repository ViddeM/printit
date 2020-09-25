#!/usr/bin/env python3
from typing import List, Dict

import click

from PrinterOptions import get_options
from ResultWithData import ResultWithData, get_result_with_error, get_result_with_data
from configuration import ALLOWED_PAGE_SPLITS, ALLOWED_PAGE_SPLITS_STR
from get_printer_list import get_printer_list
from print_via_ssh import print_via_ssh
from printer import Printer


def validate_page_split(ctx, param, page_split):
    if page_split not in ALLOWED_PAGE_SPLITS:
        raise click.BadParameter("page_split must be one of the following: {0}".format(ALLOWED_PAGE_SPLITS_STR))

    return page_split


@click.group()
def cli():
    pass


@cli.command("list")
def list_printers():
    printers = get_printer_list()
    res = print_printers(get_printers_dict(printers, ""))
    if res.is_error:
        click.echo(res.message)
        exit(-1)


@cli.command("print")
@click.option("-p", "--printer", help="The printer to print to")
@click.option("-n", "--pages", type=int, default=1, help="Number of pages to print")
@click.option("-s", "--search", type=str, default="", help="Search for printer")
@click.option("-g", "--gray-scale", is_flag=True, default=False, help="Print in grayscale")
@click.option("-t", "--two-sided", is_flag=True, default=False, help="Print on both sides")
@click.option("-w", "--wrap-short", is_flag=True, default=False,
              help="Wrap on the short-edge instead of long-edge (requires -t to work)")
@click.option("-r", "--page-range", nargs=2, type=(int, int), default=(-1, -1),
              help="Which pages to print (example '--page-range=3-7')")
@click.option("-u", "--page-split", type=int, callback=validate_page_split, default=1,
              help="How many pages that should fit on each paper, must be one of the following {0}".format(
                  ALLOWED_PAGE_SPLITS_STR))
@click.option("-h", "--horizontal", is_flag=True, default=False, help="Print the page horizontally (landscape)")
@click.argument("filename", type=click.Path(exists=True))
def print_file(filename, printer, pages, search, gray_scale, two_sided, wrap_short, page_range, page_split,
               horizontal):
    """A simple program that prints the given file on the given chalmers printer"""
    printers = get_printer_list()
    if len(printers) == 0:
        click.echo("Unable to retrieve any printers")
        return

    if printer is None:
        # Display list of printers.
        printer_res = select_printer(printers, search)
        if printer_res.is_error:
            click.echo(printer_res.message)
            exit(-1)

    username = click.prompt("Enter your chalmers cid", type=str)
    password = click.prompt("Enter your chalmers password", type=str, hide_input=True)

    options_res = get_options(pages, gray_scale, two_sided, wrap_short, page_range[0], page_range[1], page_split,
                              horizontal)
    if options_res.is_error:
        click.echo(options_res.message)
        exit(-1)

    if printer_exists(printer, printers):
        print_res = print_via_ssh(filename, printer, username, password, options_res.data)
        if print_res.is_error:
            click.echo("Failed to print: \n{0}".format(print_res.message))
        else:
            click.echo("Print successful!")
    else:
        click.echo("Invalid printer {0}".format(printer))


def get_printers_dict(printers: List[Printer], search: str) -> Dict[int, Printer]:
    search = search.lower()
    filtered_printers = []
    # filter the list on the search term
    if search != "":
        for printer in printers:
            to_search = "{0}{1}".format(printer.printer.lower(), printer.location.lower())
            if search in to_search:
                filtered_printers.append(printer)

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


def select_printer(printers: List[Printer], search: str) -> ResultWithData[str]:
    # convert the list of printers to a dictionary of int -> Printer
    printer_dict = get_printers_dict(printers, search)
    res = print_printers(printer_dict)
    if res.is_error:
        return get_result_with_error(res.message)

    click.echo("===========================")

    while True:
        printer_num = click.prompt("Select printer", type=int)

        if printer_num not in printer_dict:
            click.echo("Number must be one of the above")
        else:
            return get_result_with_data(printer_dict[printer_num].printer)


def printer_exists(printer, printers: List[Printer]) -> bool:
    for pr in printers:
        if pr.printer == printer:
            return True
    return False
