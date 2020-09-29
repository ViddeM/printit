import requests
from lxml import html
from requests.auth import HTTPBasicAuth

from src.ResultWithData import get_result_with_error, get_result_with_data

from src.ResultWithData import ResultWithData
from src.configuration import PQ_URL

xpath = 'string(//tr[contains(.,"Student Quota")][1])'


def get_pq(username: str, password: str) -> ResultWithData[str]:
    response = requests.get(PQ_URL, auth=HTTPBasicAuth(username=username, password=password))
    if response.status_code != 200:
        if response.status_code == 401:
            return get_result_with_error("Invalid cid or password")
        return get_result_with_error("Unable to retrieve PQ data, status code {0}".format(response.status_code))

    tree = html.fromstring(response.content)
    row_text = tree.xpath(xpath)

    pos = -1
    for i, c in enumerate(row_text):
        if c.isdigit():
            prev = i - 1
            if row_text[prev] == "-":
                pos = prev
            else:
                pos = i
            break

    if pos < 0:
        return get_result_with_error("Invalid PQ response from server, the API may have been updated, contact the "
                                     "maintainer of this package.")
    # Validate that it is a number
    number = row_text[i:].strip()
    return get_result_with_data(number)

