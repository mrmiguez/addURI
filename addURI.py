#!/usr/bin/env python3

import requests
import sys
from lxml import etree

def get_keyword_list(record):
    keywords = []
    for note in mods.note(record):
        if 'Keywords' in note.keys():
            for keyword in note['Keywords'].split(','):
                keywords.append(keyword.strip())
    return keywords

class mods:

    nameSpace_default = {'oai_dc': 'http://www.openarchives.org/OAI/2.0/oai_dc/', 
                     'dc': 'http://purl.org/dc/elements/1.1/', 
                     'mods': 'http://www.loc.gov/mods/v3', 
                     'dcterms': 'http://purl.org/dc/terms'}


    def load(input_file, nameSpace_dict=nameSpace_default):
        record_list = []
        tree = etree.parse(input_file)
        root = tree.getroot()
        for record in root.iterfind('.//{%s}mods' % nameSpace_dict['mods']):
            record_list.append(record)
        return record_list
        
    
    def note(record, nameSpace_dict=nameSpace_default):
        allNotes = []
        for note in record.iterfind('./{%s}note' % nameSpace_dict['mods']):
            if len(note.attrib) >= 1:
                if 'type' in note.attrib.keys():
                    typed_note = {note.attrib['type'] : note.text}
                    allNotes.append(typed_note)
                elif 'displayLabel' in note.attrib.keys():
                    labeled_note = {note.attrib['displayLabel'] : note.text}
                    allNotes.append(labeled_note)
                else:
                    allNotes.append(note.text)
            else:
                allANotes.append(note.text)
        return allNotes    
        


class uri_lookup:

    #TGM
    def tgm(keyword):   
        keyword = keyword.replace(' ','%20')
        try:
            tgm_lookup = requests.get('http://id.loc.gov/vocabulary/graphicMaterials/label/{0}'.format(keyword),
                                        timeout=5)
            if tgm_lookup.status_code == 200:
                print(tgm_lookup.url[0:-5])
            elif tgm_lookup.status_code == 404:
                print('404: resource not found')
            elif tgm_lookup.status_code == 503:
                print(tgm_lookup.headers)
            else:
                print(tgm_lookup.status_code)
        except requests.exceptions.Timeout:
            print('The request timed out after five seconds.')

   #LCSH
    def lcsh(keyword):
        keyword = keyword.replace(' ','%20')
        try: 
            lcsh_lookup = requests.get('http://id.loc.gov/authorities/subjects/label/{0}'.format(keyword),
                                    timeout=5)
            if lcsh_lookup.status_code == 200:
                print(lcsh_lookup.url[0:-5])
            elif lcsh_lookup.status_code == 404:
                print('404: resource not found')
            elif lcsh_lookup.status_code == 503:
                print(lcsh_lookup.headers)
            else:
                print(lcsh_lookup.status_code) 
        except requests.exceptions.Timeout:
            print('The request timed out after five seconds.')
          
modsXML = etree.parse(sys.argv[1])
modsRecord = modsXML.getroot()
for keyword in get_keyword_list(modsRecord):
    uri_lookup.lcsh(keyword)
