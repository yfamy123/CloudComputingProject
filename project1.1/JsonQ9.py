# (5 points) regex capturing groups
  #
  # Question:
  # Rank the years by the sum of pageviews of the films released in each year.
  # Print the result as a JSON object.
  # The keys of the JSON object are the articles.
  # The values are the rankings (not pageviews).
  #
  # Only consider page titles ending with "_(yyyy_film)" when counting pageviews
  # for the year yyyy.
  # Note the underscore in front of the left parenthesis.
  # If a year has no film articles, do not include it in the ranking.
  #
  # Examples of valid cases:
  # Concussion_(2015_film)
  #
  # Examples of invalid cases:
  # Concussion_(film)
  # 2015_film
  #
  # Capturing groups can be used to retrieve the matched unit(s).
  # DO NOT use error-prone approaches such as split, indexOf, etc.
  #
  # Hint:
  # Try to reuse your code in the previous questions so that you can focus on
  # the regex.
  # It will be better practice if you extract the ranking algorithm as a utility
  # which is shared by multiple programs.
  #
  # Standard output format:
  # {"2017":2,"2016":1,"2015":2,...,"1776":251}

import pandas as pd
import json
import re
import collections

result = {}
rank = {}
data = pd.read_csv('output', sep="\t", names=['Article', 'Pageviews'])
match_result = data['Article'].str.contains('\_\(\d{4}_film\)$')
match_result = data[match_result == True]

for index, row in match_result.iterrows():
    year = int(re.findall('\d{4}', row['Article'])[-1])
    if year < 1800 or year > 2020:
        continue
    result[year] = result.get(year, 0) + int(row['Pageviews'])

result = sorted(result.items(), key=lambda x: (-x[1], -x[0]))

rank_num = 0
for i in range(len(result)):
    if i > 0 and result[i][1] == result[i-1][1]:
        rank[result[i][0]] = rank_num
    else:
        rank_num = len(rank) + 1
        rank[result[i][0]] = rank_num

dct = collections.OrderedDict()
for year, rank in sorted(rank.items(), reverse=True):
    dct[year] = rank
print(json.dumps(dct))