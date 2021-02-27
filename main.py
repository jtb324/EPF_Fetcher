import sys
import os
import getpass
from datetime import datetime

# importing for the modules directory
import modules


def welcome_message():
    print("-" * 60)
    print(
        "'Insert Program name': A simple cli to get the ClinVar assession id from rsids"
    )
    print(f"run started at: {datetime.now().strftime('%b %d, %Y - %H:%M:%S')}")
    print(f"Current User: {getpass.getuser()}")

    print("-" * 60)


def parser(arguments: list) -> str:
    """function to parse arguments that the user has passed
    Parameters:
    ___________
    arguments: list
        list of the command line arguments that the user passed

    Returns:
    ________
    str
        string containing the rsid
    """

    if len(arguments) < 4:
        print("The program was expecting at least two arguments")
        print("Expecting arguments in the format: main.py 'RSID' -o 'output_path'")
        sys.exit(1)
    else:
        rsid: str = arguments[1]
        output_path: str = arguments[3]
        print(f"rsid: {rsid}")
        print(f"outputing files to: {output_path}\n")

    return rsid


def main():
    """"""
    welcome_message()
    rsid: str = parser(sys.argv)
    accession_id: str = modules.make_request(rsid)
    print(accession_id)


if __name__ == "__main__":
    main()
