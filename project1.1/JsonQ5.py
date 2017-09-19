import json

result = []
with open("./output", encoding="utf-8") as lines:
    for i in range(3):
        line = lines.readline()
        result.append(line.split("\t")[0])

result = json.dumps(result)
print(result)