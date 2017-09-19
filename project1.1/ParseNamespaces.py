import json

prefix_blacklist = []

with open("./data/namespaces.json", encoding="utf-8") as json_data:
    query = json.load(json_data)
    namespaces = query["query"]['namespaces']
    for item in namespaces:
        prefix = namespaces[item]['*']

        if not prefix:
            continue

        prefix = prefix.replace(" ", "_").lower()
        prefix_blacklist.append(prefix)


    print(prefix_blacklist)
