#!/usr/bin/env python

from Output import info, debug, error

def get_current_ip(verbosity=0):
    path = "http://checkip.dyndns.org"
    v = verbosity

    info(v, "Retreiving current external ip from %s" % path)

    # Open URL
    try:
        from urllib2 import urlopen
        html_result = urlopen(path)
    except Exception, e:
        error(e)
        return None

    # Read result
    ip_string = html_result.read().strip()
    debug(v, "Full HTML Result: %s" % ip_string)

    # Parse out IP
    ip = None
    if ip_string is not None:
        from re import sub as re_sub
        regex = '^.*Current IP Address: ([0-9.]*).*$'
        ip = re_sub(regex, r'\1', ip_string)
        debug(v, "Retreived IP: %s" % ip)

    return ip



noobs = """
import re

from sys import exit, stderr, stdout
from urllib2 import urlopen
import xml.etree.cElementTree as et

def get_records(args, config):
    path = 'https://freedns.afraid.org/api/?action=getdyndns&sha=%s&style=xml'
    url = path % config['authentication']['api_key']
    print >> stdout, "Retreiving records from %s" % url

    result = urlopen(url)
    raw_xml = result.read()

    tree = et.fromstring(raw_xml)
    items = [{item.tag: item.text for item in ch} for ch in tree.findall('item')]

    records = []
    for item in items:
        records.append(item)

    return records if records != [] else None
"""
