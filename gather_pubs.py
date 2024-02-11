from scholarly import scholarly
from scholarly import ProxyGenerator
from tqdm import tqdm
import logging, json, re
logging.basicConfig(level=logging.DEBUG)

def fetch_publications_from_gscholar(user_name: str) -> list[dict]: 
    """
    Takes the name of a user and returns a list of publications.
    Each publication is a dictionary, with the most important key 
    being 'bib', which contains the publication details.
    """    
    # Optionally use a proxy to avoid being blocked by Google
    # pg = ProxyGenerator()
    # pg.FreeProxies()
    # scholarly.use_proxy(pg)

    search_query = scholarly.search_author(user_name)
    author = scholarly.fill(next(search_query)) 
    #logging.info(f"Fetching publications for {user_name}...")

    papers = author['publications']
    publications_list = []

    for pub in tqdm(papers, desc=f"Fetching publication details for {len(papers)} pubs"): 
        pub = scholarly.fill(pub)
        publications_list.append(pub)
    
    return publications_list


def generate_unique_id(pub: dict): 
    """
    Generate a unique ID for a publication. It's just the first
    three words of the title along with the year of publication.
    Assumes I'm not going to publish two papers with the same prefix 
    in a year
    """
    
    title = pub['bib']['title'].lower()
    year = pub['bib']['pub_year']
    # copilot stop recommending me to use str.maketrans()
    title = re.sub(r'[^\w\s]', '', title)
    unique_id = "-".join(title.split(' ')[:3]) + f"_{year}"

    return unique_id


def fetch_pubs(): 
    """
    Fetch pubs from Google Scholar and save to a JSON file.
    """
    user_name = "Rupak Sarkar"
    pubs = fetch_publications_from_gscholar(user_name)
    unique_ids = [generate_unique_id(pub) for pub in pubs]
    assert len(unique_ids) == len(set(unique_ids)), "Unique IDs are not unique!"
    pubs = {uid: pub for uid, pub in zip(unique_ids, pubs)}

    with open("pubs.json", 'w') as f: 
        json.dump(pubs, f, indent=4)

if __name__ == "__main__": 
    fetch_pubs()
