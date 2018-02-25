import csv
import sys
import re


# match_transaction = re.compile("(?P<date>[0-9][0-9]/[0-9][0-9]/[0-9][0-9]) +(?P<vendor>(([A-Za-z0-9#,*]+[ ])+))")
match_transaction = re.compile(r"(?P<date>[0-9][0-9]/[0-9][0-9]/[0-9][0-9]) +(?P<vendor>([^ ]+[ ])+) +(?P<amount>-?[\d,.]+)")
# match_transaction = re.compile(r"(?P<date>[0-9][0-9]/[0-9][0-9]/[0-9][0-9]) +(?P<vendor>[^,]+, [A-Z][A-Z]) +(?P<amount>[\d,.]+)")

writer = csv.writer(sys.stdout)

for line in open(sys.argv[1]):
    # fix vendors with many spaces before a store number
    line = re.sub(r" +(?P<id>[\d]+,[^\d])", r" \g<id>", line)

    # fix vendors with many spaces before odd characters
    line = re.sub(r" +(?P<thing>[*]+)", r" \g<thing>", line)

    # fix VONS
    line = re.sub(r"VONS +Store", r"VONS Store", line)

    for m in match_transaction.finditer(line):
        # print "%s, %s, %s" % (m.group("date"), m.group("vendor")[:-1], m.group("amount").replace(",", ""))
        row = (m.group("date"), m.group("vendor")[:-1], m.group("amount").replace(",", ""))
        writer.writerow(row)
