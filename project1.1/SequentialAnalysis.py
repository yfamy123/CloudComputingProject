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

import re
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


def dataProcess(inputFile, outputFile):
    result_dict = {}
    total_count = 0
    valid_count = 0
    try:
        with open(inputFile, encoding="utf-8") as log_data:
            for line in log_data:
                total_count += 1
                decode_line = decode(line)

                segment = decode_line.split()
                if len(segment) != 4:
                    continue

                if segment[0] not in domain_whitelist:
                    continue

                # if segment[1][0].islower() or\
                if re.match("^[a-z]", segment[1]) or\
                        segment[1].lower().split(":")[0] in prefix_blacklist or \
                        segment[1].lower().endswith(tuple(file_blacklist)) or \
                        segment[1].lower().endswith(tuple(suffix_blacklist)) or \
                        segment[1] in title_blacklist:
                    continue

                valid_count += 1
                result_dict[segment[1]] = result_dict.get(segment[1], 0) + int(segment[2])

        # Order the dictionary based on value then by key
        result_dict = sorted(result_dict.items(), key=lambda x: (-x[1], x[0]))

        with open(outputFile, 'w', encoding='utf-8') as result:
            for (key, value) in result_dict:
                result.write("%s\t%d\n" % (key, value))

        print("Total number of lines is %d" % total_count)
        print("Total number of valid line is %d" % valid_count)

    except IOError as e:
        print("I/O error(%s): %s" % (e.errno, e.strerror))


'''
Main function of Sequential Analysis. 
'''

if __name__ == "__main__":
    # dataProcess("data/test", "output")
    dataProcess("data/pageviews-20161109-000000", "output")