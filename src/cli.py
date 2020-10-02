#!/usr/bin/env python3

import click

from src.PrinterOptions import get_options
from src.config_handler import set_config
from src.configuration import ALLOWED_PAGE_SPLITS, ALLOWED_PAGE_SPLITS_STR
from src.credentials import get_account_details
from src.get_pq import get_pq
from src.print_via_ssh import print_via_ssh
from src.printers_utils import get_printer_list, print_printers, get_printers_dict, select_printer, printer_exists


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

        printer = printer_res.data

    username, password = get_account_details()

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


@cli.command("pq")
def print_pq():
    username, password = get_account_details()
    pq_res = get_pq(username, password)
    if pq_res.is_error:
        click.echo(pq_res.message)
        exit(-1)
    click.echo("Your PQ is {0}".format(pq_res.data))


# @cli.group("config")
# def config():
#     pass
#
#
# @config.command("set")
# @click.option("-c", "--cid", type=str, default="", help="The chalmers cid to set for (will prompt if not passed)")
# @click.argument("config", type=str)
# def config_set(cid: str, config: str):
#     result = set_config(config, cid)
#     if result.is_error:
#         click.echo("Error {0}".format(result.message))
#         exit(-1)
#
#     click.echo(result.data)
#
#
# @config.command("get")
# def config_get():
#     click.echo("Not implemented yet :(")
#     pass
#
#
# @config.command("clear")
# def config_clear():
#     click.echo("Not implemented yet :(")
#     pass


