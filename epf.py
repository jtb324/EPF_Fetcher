import sys
import os
import os.path
import getpass
from datetime import datetime

# importing for the modules directory
import modules


def welcome_message():
    print("-" * 65)
    print("'EPF Fetcher': Entrez Pathogenicity and Frequency Fetcher \n\n\
A simple cli to probe the Entrez api for clinical significance information\n")
    print("version: 0.9 alpha\n")

    print(f"run started at: {datetime.now().strftime('%b %d, %Y - %H:%M:%S')}")
    print(f"Current User: {getpass.getuser()}")

    print("-" * 65)


def parser(arguments: list) -> str:
    """function to parse arguments that the user has passed
    Parameters
    __________
    arguments: list
        list of the command line arguments that the user passed

    Returns
    _______
    dict
        dictionary containing the rsid file path string with the key
        'rsid' and the output path file string with the key 'output'
    """

    if len(arguments) < 7:
        print("The program was expecting at least two arguments")
        print(
            "Expecting arguments in the format: main.py -r 'RSID' -o 'output_dir' -f 'file_name'"
        )
        sys.exit(1)
    else:
        rsid_file: str = arguments[2]
        # making sure the rsid_file string is a csv file
        if rsid_file[-4:] != ".csv":
            print("the program expects a csv file as the rsid input file")
            print("program terminating...")
            sys.exit(1)

        output_path: str = arguments[4]
        file_name: str = arguments[6]

        print(f"rsid: {rsid_file}")
        print(
            f"error file written to: {os.path.join(output_path, 'frequencies_not_found.txt')}"
        )
        print(f"outputing files to: {os.path.join(output_path, file_name)}\n")

    # return {"rsid": rsid, "xml_file": xml_file, "output_path": output_path}
    return {
        "rsid": rsid_file,
        "output": os.path.join(output_path, file_name),
        "err_file": os.path.join(output_path, "frequencies_not_found.txt")
    }


def main():
    welcome_message()
    argument_dict: dict = parser(sys.argv)

    # unpacking the values of the dictionary
    rsid_file: str = argument_dict["rsid"]
    output_path: str = argument_dict["output"]
    error_file: str = argument_dict["err_file"]

    # checking to see if the file already exists
    if os.path.isfile(output_path):
        os.remove(output_path)

    # checking to see if the error file already exists and then deleting
    # it if it does
    if os.path.isfile(error_file):
        os.remove(error_file)

    # getting a list of rsids and the corresponding chromosome
    rsid_list: list = modules.get_rsids(rsid_file)

    print("attempting to connect to the entrez site")

    for rsid_tuple in rsid_list:
        # unpacking the tuple
        rsid: str = rsid_tuple[0].strip(" ")

        chr_num: str = str(rsid_tuple[1])

        # getting values like the clinical significance, accession id
        # and the GnomAD exome frequency for the variant
        return_dict: dict = modules.make_request(rsid, output_path)

        modules.write_to_file(return_dict, output_path, rsid, chr_num)

    print("run completed")
    print("successfully terminating the program...")


if __name__ == "__main__":
    main()
