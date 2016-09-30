#!/usr/bin/env python3

import sys
from lxml import etree
from bs4 import BeautifulSoup

LCSH_complex_type_soup = BeautifulSoup(open(sys.argv[1]), 'lxml')
for componentList in LCSH_complex_type_soup.find_all("ul", rel="madsrdf:componentList"):
    for heading in componentList.find_all('div'):
        if 'madsrdf:Authority' in heading.get('typeof'):
            print(heading['typeof'].split(' ')[2], ' : ', heading.text.strip())
