from SPARQLWrapper import SPARQLWrapper, JSON
import urllib.parse


def get_wikidata_url(wikidata_label: str)->str:
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

    encoded_label = urllib.parse.quote(wikidata_label)

    query = f"""
    SELECT ?sitelink WHERE {{
      VALUES ?item {{ wd:{encoded_label} }}
      ?sitelink schema:about ?item ;
                schema:isPartOf <https://en.wikipedia.org/>.
    }}
    """

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    try:
        results = sparql.query().convert()
        for result in results["results"]["bindings"]:
            wikipedia_url = result["sitelink"]["value"]
            if wikipedia_url is not None:
                return wikipedia_url
    except Exception as e:
        print(f"An error occurred: {e}")

# get_wikidata_url("Q937")

