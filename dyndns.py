#!/usr/bin/python

import re

from sys import exit, stderr, stdout
from urllib2 import urlopen
import xml.etree.cElementTree as et


def get_current_ip(args, config):
    path = 'http://checkip.dyndns.org'
    print >> stdout, "Retreiving current external ip from %s" % path

    result = urlopen(path)
    line = result.read()

    ip = None
    if line is not None:
        # Grab IP from result
        ip = re.sub('^.*Current IP Address: ([0-9.]*).*$', r'\1', line)

    return ip.strip()

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

def update_records(args, config):
    path = 'https://freedns.afraid.org/dynamic/update.php?%s&address=%s'
    cached_ip = config['cache']['ip']

    if 'records' in config.keys():
        ip = get_current_ip(args, config)
        if ip is not None and ip != cached_ip:
            print >> stdout, "Saving New External IP: %s" % ip
            config['cache']['ip'] = ip

        for record in config['records']:
            value = config['records'][record]
            url = path % (value, ip)
            print >> stdout, "Attempting to update %s: %s" % (record, url)

            result = urlopen(url)
            line = result.read().strip()
            if "Error" in line:
                print >> stderr, line
            else:
                print >> stdout, line

def main():
    args = parse_args()
    config = parse_config(args.config_file)

    if args.current_ip:
        ip = get_current_ip(args, config)

        # Print Result
        if ip is None:
            print >> stderr, "Error Retreiving IP Address"
        else:
            print >> stdout, "Current External IP Address: %s" % ip
            print >> stdout, "Current Cached IP Address: %s" % config['cache']['ip']

    if args.get_records:
        records = get_records(args, config)
        for item in records:
            print >> stdout, "Record For: %s\nIP Address: %s\nURL: %s\n" % (item['host'],
                     item['address'], item['url'])

    if not args.current_ip and not args.get_records:
        update_records(args, config)

    write_config_file(args, config)
    exit(0)


def write_config_file(args, config):
    path = args.config_file
    with open(path, 'w') as f:
        for section in sorted(config.keys()):
            f.write("[%s]\n" % section)
            for name in config[section].keys():
                value = config[section][name]
                f.write("%s=%s\n" % (name, value))
            f.write("\n")


def parse_config(filepath):
    import ConfigParser
    # Assume filepath is good, since it is already checked
    config = ConfigParser.SafeConfigParser(allow_no_value=True)
    try:
        config.readfp(open(filepath, 'r'))
    except Exception, e:
        print >> syderr, "Error reading config file (%s): %s" % (filepath, e)
        exit(1)

    # Error Check
    if not config.has_section('authentication'):
        print >> stderr, "Malformed Config File. Missing 'authentication' section"
        exit(1)
    if not config.has_option('authentication', 'api_key'):
        print >> stderr, "Malformed Config File. Missing 'api_key' option'"
        exit(1)

    config_dict = {}
    for section in config.sections():
        config_dict[section] = {}
        for name, value in config.items(section):
            config_dict[section][name] = value

    # Make sure api key is correct
    if not re.match('[0-9a-fA-F]{40}', config_dict['authentication']['api_key']):
        print >> stderr, "Malformed API Key. Must be 40 hex character SHA1 Hash"
        exit(1)


    # Add any default options
    if not config.has_section('cache'):
        config_dict['cache'] = {}

    if not config.has_option('cache', 'ip'):
        config_dict['cache']['ip'] = '0.0.0.0'

    if not config.has_section('records'):
        config_dict['records'] = {}

    return config_dict


def parse_args():
    import argparse
    parser = argparse.ArgumentParser(description="afraid.org Dynamic DNS",
             formatter_class=argparse.ArgumentDefaultsHelpFormatter);

    parser.add_argument('config_file', type=str,
                        help='Update record(s) using configuration file')
    parser.add_argument('--configure', action='store_true',
                        help='Interactively configure your dyndns config file')

    # Check and Exit Arguments
    check_and_exit_group = parser.add_argument_group('Check and Exit')
    check_and_exit = check_and_exit_group.add_mutually_exclusive_group()
    check_and_exit.add_argument('-c', '--current-ip', action='store_true',
                        help='Check current IP and exit')
    check_and_exit.add_argument('-r', '--get-records', action='store_true',
                        help='Return all records and exit')
    args = parser.parse_args()

    # Error check aruments
    import os
    path = args.config_file
    if not os.path.exists(path) or not os.path.isfile(path):
        print >> stderr, "%s does not exit" % path
        exit(1)

    return args


if __name__ == "__main__":
    main()
