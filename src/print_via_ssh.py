import paramiko
from scp import SCPClient

from src.PrinterOptions import PrinterOptions
from src.keys import username, password

server = "remote11.chalmers.se"
print_filename = "print_this_file"
job_name = "some_booring_school_assignment.ada"


def print_via_ssh(filename: str, printer_name: str, options: PrinterOptions):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print("Connecting to server")
    ssh.connect(server, username=username, password=password)
    scp = SCPClient(ssh.get_transport())

    print("Uploading file to server")
    scp.put(filename, recursive=False, remote_path=print_filename)

    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(
        "/bin/lpr -P '{0}' -J {1} {2} {3}".format(
            printer_name, job_name, options.as_string(), print_filename))

    # If we don't read the stdout / stderr values the print won't work for some reason...
    out = ssh_stdout.readlines()
    err = ssh_stderr.readlines()

    ssh.close()
