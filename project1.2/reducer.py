#!/usr/bin/env python3

'''
Output format:
    0, For every article that has over 100,000 page-views (100,000 excluded), print the following line as output
    1, [total month views]\t[article name]\t[page views for date1]\t[page views for date2]...\t[page views for date30]
    2, Merge your results into one output file.
        Sort the output in descending numerical order of the number of monthly accesses
        Break ties by ascending lexicographical order (based on the Unicode value of each character in the strings) of page titles.
'''

import sys

total_count = 0
date_count = 0
currentWord = None
word = None
page_view = []
date = 20161101
for line in sys.stdin:
    segment = line.replace("\n", "").split("\t")
    word = segment[0]

    try:
        count = int(segment[2])
    except ValueError:
        pass

    try:
        currentDate = int(segment[1])
    except ValueError:
        pass

    if (currentWord == word or not currentWord) and currentDate == date:
        date_count += count

    if currentWord == word:
        if currentDate != date:
            page_view.append(date_count)
            total_count += date_count
            date_count = count

            for i in range(date + 1, currentDate):
                page_view.append(0)

            date = currentDate
    else:
        page_view.append(date_count)
        total_count += date_count

        for i in range(date + 1, 20161131):
            page_view.append(0)

        if currentWord and total_count > 100000:
            print("%s\t%s\t%s" % (total_count, currentWord, "\t".join([str(view) for view in page_view])))

        currentWord = word
        total_count = 0
        date_count = count
        date = 20161101
        page_view = []


if currentWord == word and total_count > 100000:
    page_view.append(date_count)
    total_count += date_count
    for i in range(date + 1, 20161131):
        page_view.append(0)
    print("%s\t%s\t%s" % (total_count, currentWord, "\t".join([str(view) for view in page_view])))





