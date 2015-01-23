import json
import sys
from optparse import OptionParser

__author__ = 'Pablo Arce'

parser = OptionParser()
parser.add_option('-f', '--first_file', dest='first_file', type='string', help='First file to compare')
parser.add_option('-s', '--second_file', dest='second_file', type='string', help='Second file to compare')

(options, args) = parser.parse_args()

if options.first_file is None or options.second_file is None:
    parser.print_help()
    sys.exit(1)

first_file = open(options.first_file, 'r')
second_file = open(options.second_file, 'r')

print 'Comparing ' + options.first_file + ' and ' + options.second_file + ' ...'

total_variations = 0
equal_variations = 0


def keys_union(first_dict, second_dict):
    for key in reduce(set.union, map(set, map(dict.keys, [first_dict, second_dict]))):
        yield key


def equal_xrefs(xref_1, xref_2):
    return xref_1 == xref_2


def equal_transcripts(transcript_1, transcript_2):
    return transcript_1 == transcript_2


def equivalent_variations(first_variation, second_variation):
    equivalent = True

    for field in keys_union(first_variation, second_variation):
        if field == 'xrefs':
            equivalent = equal_xrefs(first_variation['xrefs'], second_variation['xrefs'])
        elif field == 'transcriptVariations':
            equivalent = equal_transcripts(first_variation['transcriptVariations'], second_variation['transcriptVariations'])
        elif first_variation[field] != second_variation[field]:
            equivalent = False
        if not equivalent:
            print 'Different variants: ' + first_variation['id']
            break

    return equivalent


for first_file_line, second_file_line in zip(first_file, second_file):
    first_variation = json.loads(first_file_line)
    second_variation = json.loads(second_file_line)
    if equivalent_variations(first_variation, second_variation):
        equal_variations += 1
    total_variations += 1


print str(equal_variations) + ' of ' + str(total_variations) + ' are equals'