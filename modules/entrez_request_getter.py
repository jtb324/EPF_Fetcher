import requests
import json
import os


def get_accession_id(json_object: dict) -> str:

    for element in json_object:
        # print(type(element))
        clinVar_list: list = [
            inner_dict for inner_dict in element["component_ids"]
            if inner_dict["type"] == "clinvar"
        ]
        if len(clinVar_list) != 0:
            break

    # Getting a list of the clinVar Accession numbers
    return clinVar_list[0]["value"]


def get_significance(request_object) -> str:
    # Subsetting the initial dictionary
    json_subset = request_object["primary_snapshot_data"]
    significance_list_total: list = []

    # for loop iterating through each clinical significance entry to get them all
    for i in range(0, len(json_subset["allele_annotations"][1]["clinical"])):

        significance_list: list = json_subset["allele_annotations"][1][
            "clinical"][i]["clinical_significances"]

        for element in significance_list:
            significance_list_total.append(element)

    # getting rid of similar elements
    significance_list_total = set(significance_list_total)

    return ", ".join(significance_list_total)


# TODO: Create a function to get the allele frequencies and then write that to a file
def get_frequencies(request_object) -> str:

    json_subset = request_object["primary_snapshot_data"]
    # This is how you get frequencies
    for i in range(0, len(json_subset["allele_annotations"][1]["frequency"])):

        frequency_dict: dict = json_subset["allele_annotations"][1][
            "frequency"][i]
        if frequency_dict["study_name"] == "GnomAD_exomes":

            affected_alleles: int = int(frequency_dict["allele_count"])
            total_alleles: int = int(frequency_dict["total_count"])

            allele_freq: int = affected_alleles / total_alleles

            return allele_freq

    return "N/A"


def log_to_file(variant_name: str, output_path: str):
    output_dir: str = output_path.rfind("/")

    if output_dir == -1:
        output_dir = output_path.rfind("\\")

    output_dir_str: str = output_path[:output_dir + 1]
    log_output_path: str = os.path.join(output_dir_str,
                                        "frequencies_not_found.txt")

    with open(log_output_path, "a+") as err_file:
        err_file.write(f"no variant found for the variant, {variant_name}\n")


def make_request(variant_name: str, output: str) -> dict:
    """make request to the entrez website to get the cliVar accession id
    Parameters:
    ___________
    variant_name: str
        string containing the rsid for the variant of interest

    Returns:
        string contain the ClinVar accession id for the corresponding rsid

    """

    req = requests.get(
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=snp&id="
        + variant_name[2:] + "&rettype=json&retmode=text")

    if req.status_code != 200:
        print("failed to connect")
    else:

        json_response: dict = req.json()
        json_subset: dict = json_response["present_obs_movements"]

        accession_id: str = get_accession_id(json_subset)

        signficance_str: str = get_significance(json_response)

        allele_freq: int = get_frequencies(json_response)

        if allele_freq == "N/A":
            log_to_file(variant_name, output)

        return_dict: dict = {
            "accession_id": accession_id,
            "clinical_significance": signficance_str,
            "gnomad_exome_freq": allele_freq
        }
    return return_dict
