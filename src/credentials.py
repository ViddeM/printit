from typing import Tuple

import click
# import keyring

from src.ResultWithData import ResultWithData


def get_account_details() -> Tuple[str, str]:
    username = prompt_cid()
    password = prompt_password()
    return username, password


def prompt_cid() -> str:
    return click.prompt("Enter your chalmers cid", type=str)


def prompt_password() -> str:
    return click.prompt("Enter your chalmers password", type=str, hide_input=True)


def set_password(cid: str) -> ResultWithData[str]:
    password = prompt_password()
    if cid == "":
        cid = prompt_cid()
    # keyring.set_password("printit-git", cid, password)
    return ""


def set_cid():
    pass
