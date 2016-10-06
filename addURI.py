#!/usr/bin/env python3

import os
import re
import sys
import logging
import datetime
import requests
from lxml import etree


nameSpace_default = {'oai_dc': 'http://www.openarchives.org/OAI/2.0/oai_dc/', 
                     'dc': 'http://purl.org/dc/elements/1.1/', 
                     'mods': 'http://www.loc.gov/mods/v3', 
                     'dcterms': 'http://purl.org/dc/terms'}
LOC_try_index = 0                     
error_log = False

def write_record_subjects(record, subjects, PID):
    with open('improvedMODS/' + PID.replace(':','_') + '.xml', 'w') as MODS_out:
        for appending_subject in subjects:
            if 'tgm' in appending_subject.keys():
                subject = etree.Element('{%s}subject' % nameSpace_default['mods'],
                                        authority='tgm', authorityURI='http://id.loc.gov/vocabulary/graphicMaterials')
                topic = etree.SubElement(subject)
                topic.text = appending_subject['tgm']
            elif 'lcsh' in appending_subject.keys():
                subject = etree.Element('{%s}subject' % nameSpace_default['mods'],
                                        authority='lcsh', authorityURI='http://id.loc.gov/authorities/subjects')
                subject.text = appending_subject['lcsh']
            record.append(subject)
        MODS_out.write(etree.tostring(record, pretty_print=True, xml_declaration=True, encoding="UTF-8").decode('utf-8'))


def get_keyword_list(record):
    keywords = []
    for note in mods.note(record):
        if 'Keywords' in note.keys():
            for keyword in note['Keywords'].split(','):
                keywords.append(keyword.strip())
    return keywords


class oai_dc:

    def pid_search(record, nameSpace_dict=nameSpace_default):
        pid = re.compile('fsu_[0-9]*')
        for identifier in record.iterfind('.//{%s}identifier' % nameSpace_dict['oai_dc']):
            match = pid.search(identifier.text)
            if match:
                return match.group().replace('_',':')
                
    def load(input_file, nameSpace_dict=nameSpace_default):
        record_list = []
        tree = etree.parse(input_file)
        root = tree.getroot()
        for record in root.iterfind('.//{%s}record' % nameSpace_dict['oai_dc']):
            record_list.append(record)
        return record_list                
    
    
class mods:

    def load(input_file, nameSpace_dict=nameSpace_default):
        tree = etree.parse(input_file)
        root = tree.getroot()
        if len(root.findall('.//{%s}mods' % nameSpace_dict['mods'])) > 1:
            record_list = []
            for record in root.iterfind('.//{%s}mods' % nameSpace_dict['mods']):
                record_list.append(record)
            return record_list
        else:
            return root
        
    
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

    def pid_search(mods_record, nameSpace_dict=nameSpace_default):
        pid = re.compile('fsu:[0-9]*')
        for identifier in mods_record.iterfind('.//{%s}identifier' % nameSpace_dict['mods']):
            match = pid.search(identifier.text)
            if match:
                return match.group()
        


class uri_lookup:

    #TGM
    def tgm(keyword, record_PID):
        pass
    '''
        global LOC_try_index
        global error_log
        tgm_lookup = requests.get('http://id.loc.gov/vocabulary/graphicMaterials/label/{0}'.format(keyword.replace(' ','%20')),
                                   timeout=5)
        if tgm_lookup.status_code == 200:
            LOC_try_index = 0
            return tgm_lookup
        elif tgm_lookup.status_code == 404:
            logging.warning('404 - resource not found ; [{0}]--{1}'.format(record_PID, 'tgm:' + keyword))
            error_log = True
            return None
        elif tgm_lookup.status_code == 503:
            logging.info('503 - {0} ; [{1}]--{2}'.format(tgm_lookup.headers, record_PID, 'tgm:' + keyword))
            error_log = True
            return None
        else:
            logging.warning('Other status code - {0} ; [{1}]--{2}'.format(tgm_lookup.status_code, record_PID, 'tgm:' + keyword))
            error_log = True
            return None
    '''
   #LCSH
    def lcsh(keyword, record_PID):
        pass
    '''    
        global LOC_try_index
        global error_log
        lcsh_lookup = requests.get('http://id.loc.gov/authorities/subjects/label/{0}'.format(keyword.replace(' ','%20')),
                                    timeout=5)
        if lcsh_lookup.status_code == 200:
            LOC_try_index = 0
            return lcsh_lookup.url[0:-5]
        elif lcsh_lookup.status_code == 404:
            logging.warning('404 - resource not found ; [{0}]--{1}'.format(record_PID, 'lcsh:' + keyword))
            error_log = True
            return None
        elif lcsh_lookup.status_code == 503:
            logging.info('503 - {0} ; [{1}]--{2}'.format(tgm_lookup.headers, record_PID, 'lcsh:' + keyword))
            error_log = True
            return None
        else:
            logging.warning('Other status code - {0} ; [{1}]--{2}'.format(tgm_lookup.status_code, record_PID, 'lcsh:' + keyword))
            error_log = True
            return None
    '''

logging.basicConfig(filename='addURI_LOG{0}.txt'.format(datetime.date.today()),
                    level=logging.WARNING,
                    format='%(asctime)s -- %(levelname)s : %(message)s',
                    datefmt='%m/%d/%Y %H:%M:%S %p')
for record in mods.load(sys.argv[1]):
    record_write = True
    appending_subjects = [{'tgm':'Frankenstein'},{'lcsh':'His wife'}]
    while LOC_try_index <= 5:
        record_PID = mods.pid_search(record)
        print("Checking:", record_PID)
        for keyword in get_keyword_list(record):
            try:
                if uri_lookup.tgm(keyword, record_PID) is not None:
                    appending_subjects.append({'tgm': uri_lookup.tgm(keyword, record_PID)})
                    record_write = True
                elif uri_lookup.lcsh(keyword, record_PID) is not None:
                    appending_subjects.append({'lcsh': uri_lookup.lcsh(keyword, record_PID)})
                    record_write = True
                else:
                    pass
            except requests.exceptions.Timeout:
                logging.warning("The request timed out after five seconds. {0}-{1}".format(record_PID, keyword))
                LOC_try_index = LOC_try_index + 1
        break                
    else:
        print("\nid.loc.gov seems unavailable at this time. Try again later.\n")
        break
    if record_write == True:
        if 'improvedMODS' not in os.listdir():
            os.mkdir('improvedMODS')
        print("Writing", record_PID)
        write_record_subjects(record, appending_subjects, record_PID)
if error_log is True:
    print("\nSome keywords not found.\nDetails logged to: addURI_LOG{0}.txt\n".format(datetime.date.today()))

