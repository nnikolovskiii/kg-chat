from SPARQLWrapper import SPARQLWrapper, JSON

# Set up SPARQL endpoint and query
sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
query = """
SELECT ?predicate1 ?neighbor1 ?neighbor1Label ?predicate2 ?neighbor2 ?neighbor2Label
WHERE {
  wd:Q937 ?predicate1 ?neighbor1 .
  ?neighbor1 ?predicate2 ?neighbor2 .
  FILTER(?predicate1 != rdfs:label && ?predicate2 != rdfs:label) # Exclude rdfs:label
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
LIMIT 20

"""
sparql.setQuery(query)
sparql.setReturnFormat(JSON)

results = sparql.query().convert()

for result in results["results"]["bindings"]:
    if "predicate" not in result or "neighborLabel" not in result:
        print("Incomplete result:", result)
    else:
        predicate = result["predicate"]["value"]
        neighbor = result["neighborLabel"]["value"]
        print(f"Predicate: {predicate}, Neighbor: {neighbor}")
