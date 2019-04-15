#!/usr/bin/env python
# extract cross sections from Pythia8 log file: HBP
# updated: 15-Apr-2019 HBP - make compatible with Python 3
import os, sys
argv = sys.argv[1:]
if len(argv) < 1:
    sys.exit("./getxsection.py log-file")

records = open(argv[0]).readlines()
ii = -1
while ii < len(records)-1:
    ii += 1
    record = str.strip(records[ii])
    if record == '': continue
    t = str.split(record)
    if len(t) < 7: continue
    if t[4] != 'Cross': continue
    if t[5] != 'Section': continue
    if t[6] != 'Statistics': continue
    break

ii += 1
process = ''
xsec = ""
exsec = ""
while ii < len(records)-1:
    ii += 1
    record = str.strip(records[ii])
    if record == '': continue
    if record[:3] != '|--':continue
    break

ii += 1
while ii < len(records)-1:
    ii += 1
    record = str.replace(records[ii], '|', '')
    record = str.strip(record)
    if record == '': continue
    t = str.split(record)

    xsec, exsec = t[-2:]
    xsec = float(xsec)*1.e12 # change to fb
    xsec = "%10.2e" % xsec
    exsec= float(exsec)*1.e12
    exsec= "%10.2e" % exsec

    if t[0] == 'sum':
        break
    else:
        process = ' '.join(t[:-6])
        print(" %-42s\t%s\t+/- %-s" % (process, xsec, exsec))

print("\t\t\t\t\t\t  ----------------------------")
print(" %-42s\t%s\t+/- %-s" % ('total cross-section (fb)',
                                  xsec, exsec))


