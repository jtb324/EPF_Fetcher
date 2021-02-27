import requests


def make_request(variant_name: str) -> str:
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

    for element in json_subset:
        # print(type(element))
        clinVar_list: list = [
            inner_dict
            for inner_dict in element["component_ids"]
            if inner_dict["type"] == "clinvar"
        ]
        if len(clinVar_list) != 0:
            break

    # Getting a list of the clinVar Accession numbers
    accession_id: str = clinVar_list[0]["value"]

    return accession_id
