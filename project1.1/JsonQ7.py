import pandas as pd

racer = pd.read_csv("data/racer.csv")
data=pd.read_csv('output', sep="\t", names=['Article', 'Pageviews'])

result = racer.merge(data, on='Article')

print(",".join(result.columns.values.tolist()))
for index, row in result.iterrows():
    print("{state},{article},{seats},{pgview}".format(state='"' + row["State/District"] + '"' if "," in row["State/District"] else row["State/District"],
                                                          article='"' + row["Article"] + '"' if "," in row["Article"] else row["Article"],
                                                          seats=row["Seats"],
                                                          pgview=row["Pageviews"]))

