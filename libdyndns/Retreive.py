#!/usr/bin/env python

from Output import info, debug, error

def get_current_ip(verbosity=0):
    v = verbosity
    url = "http://checkip.dyndns.org"
    info(v, "Retreiving current external ip from %s" % url)

    # Open URL
    try:
        from urllib2 import urlopen
        html_result = urlopen(url)
    except Exception, e:
        error("Url(%s) - %s" % (url, e))
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


def get_records(api_key, verbosity=0):
    v = verbosity
    url = "https://freedns.afraid.org/api/?action=getdyndns&sha=%s&style=xml"
    url = url % api_key
    info(v, "Retreiving records from %s" % url)

    # Open URL
    try:
        from urllib2 import urlopen
        html_result = urlopen(url)
    except Exception, e:
        error("url(%s) - %s" % (url, e))
        return None

    # Read result
    raw_xml = html_result.read().strip()
    debug(v, "Full XML Result: %s" % raw_xml)

    # Check for authentication error
    if raw_xml == 'ERROR: Could not authenticate.':
        error("Could Not Authenticate")
        return None

    # Parse XML
    import xml.etree.cElementTree as et
    try:
        xml = et.fromstring(raw_xml)
    except Exception, e:
        error("XML Parsing Error - %s\nRaw XML: %s" % (e, raw_xml))
        return None

    # Parse xml object into array of dicts
    all_items = xml.findall('item')
    records = [{y.tag: y.text for y in x} for x in all_items]

    debug(v, "Retreived Records: %s" % records)

    # Return records if they exist, else return none
    return records if records != [] else None
