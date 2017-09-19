# import re
#
# print(re.findall(r"[\w]+", "_cloud_asdas"))

# count = 0
# with open("output") as ifile:
#     for line in ifile:
#         line = line.lower()
#         if line.startswith("cloud") or line.endswith("cloud"):
#             count += 1

# print(count)


cur = []
all = []
diff = []

with open("data/Q8Cur") as lines:
    for line in lines:
        cur.append(line.replace("\n", "").split("\t")[0])


with open("data/Q8All") as lines:
    for line in lines:
        all.append(line.replace("\n", "").split("\t")[0])
        if line.replace("\n", "").split("\t")[0] not in cur:
            diff.append(line.replace("\n", "").split("\t")[0])

print(diff)
