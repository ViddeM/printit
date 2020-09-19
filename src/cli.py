#!/usr/bin/env python3
from typing import List

import click

from src.PrinterOptions import get_options
from src.configuration import ALLOWED_PAGE_SPLITS, ALLOWED_PAGE_SPLITS_STR
from src.get_printer_list import get_printer_list
from src.print_via_ssh import print_via_ssh
from src.printer import Printer


def validate_page_split(ctx, param, page_split):
    if page_split not in ALLOWED_PAGE_SPLITS:
        raise click.BadParameter("page_split must be one of the following: {0}".format(ALLOWED_PAGE_SPLITS_STR))

    return page_split


@click.command()
@click.option("-p", "--printer", help="The printer to print to")
@click.option("-n", "--pages", type=int, default=1, help="Number of pages to print")
@click.option("-g", "--gray-scale", is_flag=True, default=False, help="Print in grayscale")
@click.option("-t", "--two-sided", is_flag=True, default=False, help="Print on both sides")
@click.option("-w", "--wrap-short", is_flag=True, default=False, help="Wrap on the short-edge instead of long-edge (requires -t to work)")
@click.option("-r", "--page-range", nargs=2, type=(int, int), default=(-1, -1), help="Which pages to print (example '--page-range=3-7')")
@click.option("-s", "--page-split", type=int, callback=validate_page_split, default=1, help="How many pages that should fit on each paper, must be one of the following {0}".format(ALLOWED_PAGE_SPLITS_STR))
@click.option("-l", "--landscape", is_flag=True, default=False, help="Print in landscape")
@click.argument("filename", type=click.Path(exists=True))
def print_file_to_printer(filename, printer, pages, gray_scale, two_sided, wrap_short, page_range, page_split, landscape):
    """A simple program that prints the given file on the given chalmers printer"""
    printers = get_printer_list()
    if len(printers) == 0:
        click.echo("Unable to retrieve any printers")
        return

    if printer is None:
        # Display list of printers.
        printer = select_printer(printers)

    username = click.prompt("Enter your chalmers cid", type=str)
    password = click.prompt("Enter your chalmers password", type=str, hide_input=True)

    options_res = get_options(pages, gray_scale, two_sided, wrap_short, page_range[0], page_range[1], page_split, landscape)
    if options_res.is_error:
        click.echo(options_res.message)
        exit(0)

    if printer_exists(printer, printers):
        print_res = print_via_ssh(filename, printer, username, password, options_res.data)
        if print_res.is_error:
            click.echo("Failed to print: \n{0}".format(print_res.message))
        else:
            click.echo("Print successful!")
    else:
        click.echo("Invalid printer {0}".format(printer))


def select_printer(printers: List[Printer]) -> str:
    # convert the list of printers to a dictionary of int -> Printer
    printer_dict = dict()
    longest_name = 0
    longest_number = len(str(len(printers)))
    for i in range(len(printers) - 1, -1, -1):
        printer = printers[i]
        printer_dict[i] = printer
        printer_length = len(printer.printer)
        if printer_length > longest_name:
            longest_name = printer_length

    for index in printer_dict:
        printer = printer_dict[index]
        printer_text = "({0})".format(index).rjust(longest_number + 2)
        printer_text += " {0} ".format(printer.printer).ljust(longest_name + 2)
        printer_text += " |- {0}".format(printer.location)

        click.echo(printer_text)

    click.echo("===========================")

    while True:
        printer_num = click.prompt("Select printer", type=int)

        if printer_num not in printer_dict:
            click.echo("Number must be one of the above")
        else:
            return printer_dict[printer_num].printer


def printer_exists(printer, printers: List[Printer]) -> bool:
    for pr in printers:
        if pr.printer == printer:
            return True
    return False
