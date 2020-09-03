import mimetypes
from pprint import pprint

import requests
from requests.auth import HTTPBasicAuth

from auth import username, password
from get_printer_list import get_printer_list

print_url = "https://print.chalmers.se/auth/uploadme.cgi"


print_url = "http://127.0.0.1:5000"

# pprint(get_printer_list())

def print_file(filepath, printername) -> str:
    with open(filepath, "rb") as file:
        headers = {
            "Host": "print.chalmers.se",
            "Origin": "https://print.chalmers.se",
            "Referer": "https://print.chalmers.se/auth/uploadme.cgi"
        }

        file_dict = {
            "printers": printername,
            "inputfile": file,
            "report": "Print"
        }

        try:
            r = requests.post(print_url, files=file_dict, auth=HTTPBasicAuth(username=username, password=password),
                              headers=headers)
            if r.status_code != 200:
                return "Failed to print, error code: {0}, see response.html for errors".format(r.status_code)

            with open("response.html", "w") as write_file:
                write_file.write(r.content.decode("UTF-8"))
            return "Print successful!"
        except requests.RequestException:
            return "Unable to connect to chalmers printers server"
