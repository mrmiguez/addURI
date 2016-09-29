#!/usr/bin/env python3

import requests
import sys
from lxml import etree

class uri_lookup:

    #TGM
    def tgm(keyword):   
        keyword = keyword.replace(' ','%20')
        tgm_lookup = requests.get('http://id.loc.gov/vocabulay/graphicMaterials/label/{0}'.format(keyword),
                                    timeout=5)
        if tgm_lookup.status_code == 200:
            print(tgm_lookup.url[0:-5])
        elif tgm_lookup.status_code == 404:
            print('404: resource not found')
        elif tgm_lookup.status_code == 503:
            print(tgm_lookup.headers)
        else:
            print(tgm_lookup.status_code)
   

   #LCSH
    def lcsh(keyword):
        keyword = keyword.replace(' ','%20')
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
  
uri_lookup.tgm(sys.argv[1])