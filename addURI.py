#!/usr/bin/env python3

import os
import re
import sys
import logging
import datetime
import requests
from lxml import etree
from bs4 import BeautifulSoup

sys.path.append('./assets')
from pymods import mods

nameSpace_default = {'oai_dc': 'http://www.openarchives.org/OAI/2.0/oai_dc/', 
                     'dc': 'http://purl.org/dc/elements/1.1/', 
                     'mods': 'http://www.loc.gov/mods/v3', 
                     'dcterms': 'http://purl.org/dc/terms'}
LOC_try_index = 0                     
error_log = False

def get_subject_parts(subject_html):
    subject_parts = {}
    
    ''' 
    # LCSH complex
    subject_soup = BeautifulSoup(subject_html.text, 'lxml')
    for componentList in subject_soup.find_all("ul", rel="madsrdf:componentList"):
        for heading in componentList.find_all('div'):
            if 'madsrdf:Authority' in heading.get('typeof'):
                subject_parts['part'] = heading['typeof'].split(' ')[2].split(':')[1]
                subject_parts['heading'] = heading.text.strip()
                subject_parts['URI'] = suject_html.url[0:-5]
    return subject_parts
    '''

def write_record_subjects(record, subjects, PID):
    with open('improvedMODS/' + PID.replace(':','_') + '.xml', 'w') as MODS_out:
        for appending_subject in subjects:
            if 'tgm' in appending_subject.keys():
                subject = etree.Element('{%s}subject' % nameSpace_default['mods'],
                                        authority='tgm', 
                                        authorityURI='http://id.loc.gov/vocabulary/graphicMaterials')
                topic = etree.SubElement(subject, '{%s}topic' % nameSpace_default['mods'])
                topic.text = appending_subject['tgm']['heading']
            elif 'lcsh' in appending_subject.keys():
                subject = etree.Element('{%s}subject' % nameSpace_default['mods'],
                                        authority='lcsh', 
                                        authorityURI='http://id.loc.gov/authorities/subjects')
                subject.text = appending_subject['lcsh']
            record.append(subject)
        MODS_out.write(etree.tostring(record, pretty_print=True, xml_declaration=True, encoding="UTF-8").decode('utf-8'))


def get_keyword_list(record):
    # generate keywords from note@displayLabel="Keywords" element
    keywords = []
    for note in mods.note(record):
        if 'Keywords' in note.keys():
            for keyword in note['Keywords'].split(','):
                keywords.append(keyword.strip())
    return keywords


class uri_lookup:

    #TGM
    def tgm(keyword, record_PID):
#        pass
    
        global LOC_try_index
        global error_log
        tgm_lookup = requests.get('http://id.loc.gov/vocabulary/graphicMaterials/label/{0}'.format(keyword.replace(' ','%20')),
                                   timeout=5)
        # request successful                           
        if tgm_lookup.status_code == 200:
            LOC_try_index = 0
            return get_subject_parts(tgm_lookup)
        # 404    
        elif tgm_lookup.status_code == 404:
            logging.warning('404 - resource not found ; [{0}]--{1}'.format(record_PID, 'tgm:' + keyword))
            error_log = True
            return None
        # 503 (probably wait... but haven't caught one of these yet)    
        elif tgm_lookup.status_code == 503:
            logging.info('503 - {0} ; [{1}]--{2}'.format(tgm_lookup.headers, record_PID, 'tgm:' + keyword))
            error_log = True
            return None
        # anything else
        else:
            logging.warning('Other status code - {0} ; [{1}]--{2}'.format(tgm_lookup.status_code, record_PID, 'tgm:' + keyword))
            error_log = True
            return None
    
   #LCSH
    def lcsh(keyword, record_PID):
        pass
    '''    
        global LOC_try_index
        global error_log
        lcsh_lookup = requests.get('http://id.loc.gov/authorities/subjects/label/{0}'.format(keyword.replace(' ','%20')),
                                    timeout=5)
        # request successful
        if lcsh_lookup.status_code == 200:
            LOC_try_index = 0
            return lcsh_lookup.url[0:-5]
        # 404
        elif lcsh_lookup.status_code == 404:
            logging.warning('404 - resource not found ; [{0}]--{1}'.format(record_PID, 'lcsh:' + keyword))
            error_log = True
            return None
        # 503 (probably wait... but haven't caught one of these yet)
        elif lcsh_lookup.status_code == 503:
            logging.info('503 - {0} ; [{1}]--{2}'.format(tgm_lookup.headers, record_PID, 'lcsh:' + keyword))
            error_log = True
            return None
        # anything else
        else:
            logging.warning('Other status code - {0} ; [{1}]--{2}'.format(tgm_lookup.status_code, record_PID, 'lcsh:' + keyword))
            error_log = True
            return None
    '''

# init error logger
logging.basicConfig(filename='addURI_LOG{0}.txt'.format(datetime.date.today()),
                    level=logging.WARNING,
                    format='%(asctime)s -- %(levelname)s : %(message)s',
                    datefmt='%m/%d/%Y %H:%M:%S %p')

# loop over MODS record list returned by pymods.mods.load                    
for record in mods.load(sys.argv[1]):
    record_write = False
#    record_write = True      # testing value to force record writing
    appending_subjects = []

    # check timeout index
    while LOC_try_index <= 5:
        record_PID = mods.pid_search(record)
        print("Checking:", record_PID)

        # loops over keywords 
        for keyword in get_keyword_list(record): 
            print(keyword)
        '''
            try:
            
                # TGM subject found
                if uri_lookup.tgm(keyword, record_PID) is not None:
                    appending_subjects.append({'tgm': uri_lookup.tgm(keyword, record_PID)}) #need heading & type
                    record_write = True
                    
                # LCSH subject found
                elif uri_lookup.lcsh(keyword, record_PID) is not None:
                    appending_subjects.append({'lcsh': uri_lookup.lcsh(keyword, record_PID)})
                    record_write = True
                
                # no subject found
                else:
                    pass
                    
            # catch timeout exception and increase timeout index        
            except requests.exceptions.Timeout:
                logging.warning("The request timed out after five seconds. {0}-{1}".format(record_PID, keyword))
                LOC_try_index = LOC_try_index + 1
        '''            
        break                
    
    # LOC has timed out
    else:
        print("\nid.loc.gov seems unavailable at this time. Try again later.\n")
        break
        
    # if any records have new subject values, write them    
    if record_write == True:
        if 'improvedMODS' not in os.listdir():
            os.mkdir('improvedMODS')
        print("Writing", record_PID)
        print(appending_subjects)
 #       write_record_subjects(record, appending_subjects, record_PID)

# indicate errors were logged 
if error_log is True:
    print("\nSome keywords not found.\nDetails logged to: addURI_LOG{0}.txt\n".format(datetime.date.today()))

