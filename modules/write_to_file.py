import os
import os.path
import sys


def write_to_file(return_val_dict: dict, output_str: str, rsid: str,
                  chr_num: str):
    """function to write the information about the variant to file



    """

    accession_id: str = return_val_dict["accession_id"]
    clinical_significance: str = return_val_dict["clinical_significance"]
    gnomad_exome_freq: str = str(return_val_dict["gnomad_exome_freq"])

    with open(output_str, "a+") as output_file:

        # if the file is empty then add a header line
        if os.path.getsize(output_str) == 0:
            output_file.write(
                "rsid\tClinVar Accession ID\tchr\tGnomAD exome frequency\tclinical_significance\n"
            )

        output_file.write(
            f"{rsid}\t{accession_id}\t{chr_num}\t{gnomad_exome_freq}\t{clinical_significance}\n"
        )
