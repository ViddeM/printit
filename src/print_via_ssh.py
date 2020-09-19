import paramiko
from paramiko import AuthenticationException
from scp import SCPClient

from src.PrinterOptions import PrinterOptions
from src.ResultWithData import ResultWithData, get_result_with_error, get_result_with_data
from src.configuration import SERVER, JOB_NAME, TO_PRINT_FILENAME


def print_via_ssh(filename: str, printer_name: str, username: str, password: str, options: PrinterOptions) -> ResultWithData[bool]:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print("Connecting to server")

    try:
        ssh.connect(SERVER, username=username, password=password)
    except AuthenticationException:
        return get_result_with_error("Invalid username/password")

    scp = SCPClient(ssh.get_transport())

    print("Uploading file to server")
    scp.put(filename, recursive=False, remote_path=TO_PRINT_FILENAME)
    print("Finished uploading file")

    command = "/bin/lpr -P '{0}' -J {1} {2} {3}".format(
            printer_name, JOB_NAME, options.as_string(), TO_PRINT_FILENAME)
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command)

    # If we don't read the stdout / stderr values the print won't work for some reason...
    out = ssh_stdout.readlines()
    err = ssh_stderr.readlines()

    ssh.close()

    if len(err) > 0:
        message = "\n".join([" - {0}".format(a) for a in err])
        return get_result_with_error(message)

    return get_result_with_data(True)
