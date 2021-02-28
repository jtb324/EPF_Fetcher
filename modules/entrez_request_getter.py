import requests
import json
from bs4 import BeautifulSoup


def get_accession_id(json_object: dict) -> str:

    for element in json_object:
        # print(type(element))
        clinVar_list: list = [
            inner_dict
            for inner_dict in element["component_ids"]
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

        significance_list: list = json_subset["allele_annotations"][1]["clinical"][i][
            "clinical_significances"
        ]

        for element in significance_list:
            significance_list_total.append(element)

    # getting rid of similar elements
    significance_list_total = set(significance_list_total)

    return ", ".join(significance_list_total)


# TODO: Create a function to get the allele frequencies and then write that to a file

# This is how you get frequencies
# for i in range(0, 24):
#     print(json_subset["allele_annotations"][1]["frequency"][i])
def make_request(variant_name: str) -> dict:
    """make request to the entrez website to get the cliVar accession id
    Parameters:
    ___________
    variant_name: str
        string containing the rsid for the variant of interest

    Returns:
        string contain the ClinVar accession id for the corresponding rsid

    """

    print("attempting to connect to the entrez site")

    req = requests.get(
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=snp&id="
        + variant_name[2:]
        + "&rettype=json&retmode=text"
    )

    if req.status_code != 200:
        print("failed to connect")
    else:
        print("successfully made the request")

        json_response: dict = req.json()
        json_subset: dict = json_response["present_obs_movements"]

        accession_id: str = get_accession_id(json_subset)

        signficance_str: str = get_significance(json_response)
        print(signficance_str)

        return_dict: dict = {
            "accession_id": accession_id,
            "clinical_significance": signficance_str,
        }
    return return_dict
