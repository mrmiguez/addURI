#!/usr/bin/env python3

from lxml import etree
from bs4 import BeautifulSoup

LCSH_complex_type_page = etree.parse(web_page_data, etree.HTMLParser)
LCSH_complex_type_html = etree.tostring(LCSH_complex_type_page.getroot())
LCSH_complex_type_soup = BeautifulSoup(LCSH_complex_type_html, 'lxml')
LCSH_complex_type_components = LCSH_complex_type_soup.find_all("ul", rel="madsrdf:componentList")
for heading in LCSH_complex_type_components[0].find_all('div'):
    if 'madsrdf:Authority' in heading.get('typeof'):
        print(heading.text)
