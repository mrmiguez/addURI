#!/usr/bin/env python3
import sys

def clean(in_file):
    with open(in_file + 'out', 'w') as out_file:
        for line in open(in_file, 'r'):
            if 'mods:mods' in line:
                out_file.write(line)
            else:
                out_file.write(line.replace('mods:',''))

clean(sys.argv[1])                
