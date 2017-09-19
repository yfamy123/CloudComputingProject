import json
import copy

result = {}
rank_list = []

dct = {}
with open("output", encoding="utf-8") as lines:
    for line in lines:
        line = line.strip().split()
        dct[line[0]] = int(line[1])

rank_list = []
with open("data/voter_minds.txt", encoding="utf-8") as lines:
    for line in lines:
        mind = line.strip()
        rank_list.append([mind, dct.get(mind, 0)])

rank_list.sort(key = lambda x: (-x[1], x[0]))
target = ["Political_positions_of_Hillary_Clinton", "Political_positions_of_Donald_Trump"]
ans = {target[0]: 0, target[1]: 0}

rank = count = 0
for i in range(len(rank_list)):
    count += 1
    if i == 0 or (i > 0 and rank_list[i][1] != rank_list[i - 1][1]):
        rank += 1

    if rank_list[i][0] == target[0]:
        ans[target[0]] = rank
    if rank_list[i][0] == target[1]:
        ans[target[1]] = rank
    rank = count

print(json.dumps(ans))