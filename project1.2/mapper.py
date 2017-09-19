#!/usr/bin/env python3

'''
Build a MapReduce job

Data source: 
    s3://cmucc-datasets/wikipediatraf/201611/ for EMR
    
Data clean:
    Same as project 1.1
    
Data file name:
    os.environ["mapreduce_map_input_file"]
    
Target:
    Aggregate the pageviews from hourly views to daily views.
'''

import sys
import re
import os

prefix_blacklist = [u'media', u'special', u'talk', u'user', u'user_talk', u'wikipedia',
                    u'wikipedia_talk', u'file', u'file_talk', u'mediawiki', u'mediawiki_talk',
                    u'template', u'template_talk', u'help', u'help_talk', u'category',
                    u'category_talk', u'portal', u'portal_talk', u'book', u'book_talk',
                    u'draft', u'draft_talk', u'education_program', u'education_program_talk',
                    u'timedtext', u'timedtext_talk', u'module', u'module_talk', u'gadget',
                    u'gadget_talk', u'gadget_definition', u'gadget_definition_talk']


file_blacklist = [u'.png', u'.gif', u'.jpg', u'.jpeg', u'.tiff', u'.tif', u'.xcf', u'.mid', u'.ogg',
                  u'.ogv', u'.svg', u'.djvu', u'.oga', u'.flac', u'.opus', u'.wav', u'.webm', u'.ico', u'.txt']

suffix_blacklist = [u'_(disambiguation)']

title_blacklist = [u'404.php', u'Main_Page', u'-']

domain_whitelist = [u'en', u'en.m']

'''
Decoder for percent encoded strings

In contrast to URLDecoder, this decoder keeps percent signs that are not
followed by hexadecimal digits, and does not convert plus-signs to spaces.
'''


def decode(encoded):
    def getHexValue(b):
        if '0' <= b <= '9':
            return chr(ord(b) - 0x30)
        elif 'A' <= b <= 'F':
            return chr(ord(b) - 0x37)
        elif 'a' <= b <= 'f':
            return chr(ord(b) - 0x57)
        return None

    if encoded is None:
        return None
    encodedChars = encoded
    encodedLength = len(encodedChars)
    decodedChars = ''
    encodedIdx = 0
    while encodedIdx < encodedLength:
        if encodedChars[encodedIdx] == '%' and encodedIdx + 2 < encodedLength and getHexValue(encodedChars[encodedIdx + 1]) and getHexValue(encodedChars[encodedIdx + 2]):
            #  current character is % char
            value1 = getHexValue(encodedChars[encodedIdx + 1])
            value2 = getHexValue(encodedChars[encodedIdx + 2])
            decodedChars += chr((ord(value1) << 4) + ord(value2))
            encodedIdx += 2
        else:
            decodedChars += encodedChars[encodedIdx]
        encodedIdx += 1
    return str(decodedChars)


'''
Data format: 
    domain_code page_title count_views total_response_size

Cleaning rules:
    1. Filter out lines without four columns
    2. Domain_code != 'en' or 'en.m'
    3. Decode percent encoded titles
    4. Not in any of the blacklists (prefix_blacklist and file_blacklist should be case insensitive)
    5. Filter out all page titles that start with lowercase English characters

Output format:
    1. [page_title][TAB][count_views]
    2. Combine desktop and mobile sites into one
    3. Sort the output in descending numerical order of the number of accesses
    4. Break ties by ascending lexicographical order

'''

for line in sys.stdin:
    decode_line = decode(line)

    segment = decode_line.split()
    if len(segment) != 4:
        continue

    if segment[0] not in domain_whitelist:
        continue

    if re.match("^[a-z]", segment[1]) or\
            segment[1].lower().split(":")[0] in prefix_blacklist or \
            segment[1].lower().endswith(tuple(file_blacklist)) or \
            segment[1].lower().endswith(tuple(suffix_blacklist)) or \
            segment[1] in title_blacklist:
        continue

    filename = os.environ["mapreduce_map_input_file"]
    date = filename.split("-")[-2]

    try:
        pageview = int(segment[2])
        print("%s\t%s\t%d" % (segment[1], date, pageview))
    except ValueError:
        pass
