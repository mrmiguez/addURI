#!/usr/bin/env python3

import sys
import requests
from lxml import etree
from bs4 import BeautifulSoup

def tgm_simple(subject_LOC_reply): 
    subject_html = subject_LOC_reply
    subject_heading = ''
    subject_uri = "http://id.loc.gov/vocabulary/graphicMaterials/tgm002909"
    subject_soup = BeautifulSoup(subject_html, 'lxml')
    for authority_div in subject_soup.find_all('div', about=subject_uri):
        if authority_div.find('span', property="madsrdf:authoritativeLabel skos:prefLabel") is not None:
            subject_heading = authority_div.find('span', property="madsrdf:authoritativeLabel skos:prefLabel").text
        elif authority_div.find('a', property="madsrdf:authoritativeLabel skos:prefLabel") is not None:
            subject_heading = authority_div.find('span', property="madsrdf:authoritativeLabel skos:prefLabel").text
        elif authority_div.find('span', property="madsrdf:variantLabel skosxl:literalForm"):
#            print(authority_div)
            use_instead = authority_div.find('h3', text="Use Instead")
#            print(use_instead)
            print(use_instead.find_next('a').text)
    return subject_uri, subject_heading
            

with open(sys.argv[1]) as in_file:        
    print(tgm_simple(in_file))
