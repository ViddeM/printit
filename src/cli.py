#!/usr/bin/env python3
from time import sleep
from typing import List

import click

from src.get_printer_list import get_printer_list
from src.print_file import print_file
from src.printer import Printer

sleep_time = 0.3


@click.command()
@click.option("-p", "--printer")
@click.option("-n", "--pages", type=int, default=1)
@click.argument("filename", type=click.Path(exists=True))
def print_file_to_printer(filename, printer, pages):
    """"A simple program that prints the given file on the given chalmers printer"""
    printers = get_printer_list()
    if len(printers) == 0:
        click.echo("Unable to retrieve any printers")
        return

    if printer is None:
        # Display list of printers.
        printer = select_printer(printers)

    username = click.prompt("Enter your chalmers cid", type=str)
    password = click.prompt("Enter your chalmers password", type=str, hide_input=True)

    if printer_exists(printer, printers):
        for i in range(0, pages):
            click.echo("Printing page {0}/{1}\r".format(i + 1, pages), nl=i == pages - 1)
            msg, error = print_file(filename, printer, username, password)
            if error:
                click.echo(msg)
                exit(-1)
            sleep(sleep_time)
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
