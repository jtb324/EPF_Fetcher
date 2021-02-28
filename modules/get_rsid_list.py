import pandas as pd
import os
import sys


def get_rsids(input_file: str) -> list:
    """function to get a list of rsids and chromosome numbers

    Parameters
    __________
    input_file: str 
        file path to the input file that contains two tabbed spaced columns 
        where the first is titled 'rsid' and the second is 'chr'

    Returns
    _______
    list
        list containing tuples of the rsid and the chromsome number that the 
        variant is on
    """

    column_names: list = ["rsid", "chr"]
    # catching the error if the file does not have the column names
    try:
        rsid_file: pd.DataFrame = pd.read_csv(input_file, usecols=column_names)
    except KeyError:
        print("The expected header was not found within the file")
        print(
            "Please ensure that the file has at least two columns: 'rsid' and 'chr'"
        )
        sys.exit(1)

    rsid_list: list = rsid_file.rsid.values.tolist()
    chr_list: list = rsid_file["chr"].values.tolist()

    total_rsid_list: list = list(zip(rsid_list, chr_list))

    return total_rsid_list
