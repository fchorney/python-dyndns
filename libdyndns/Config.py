#!/usr/bin/env python

from Output import exit, message, info, debug

class Config:
    def __init__(self):
        self.api_key = ''
        self.ip = ''
        self.records = {}

def parse_config(args, filepath):
    """ Parse Configuration File """
    import ConfigParser

    # Assume filepath is good, since it is already checked
    info(args['v'], 'Importing Configuration File: %s' % filepath)
    config = ConfigParser.SafeConfigParser(allow_no_value=True)
    try:
        config.readfp(open(filepath, 'r'))
    except Exception, e:
        exit(1, "Error reading config file (%s): %s" % (filepath, e))

    # Error Check
    if not config.has_section('authentication'):
        err = "Malformed Config File. Missing 'authentication' section"
        exit(1, err)
    if not config.has_option('authentication', 'api_key'):
        err = "Malformed Config File. Missing 'api_key' option"
        exit(1, err)

    # Create a dictionary of config values
    config_dict = {}
    for section in config.sections():
        config_dict[section] = {}
        for name, value in config.items(section):
            config_dict[section][name] = value

    # Transform dict into Config Object
    config_obj = Config()
    config_obj.api_key = config_dict['authentication']['api_key']
    if config.has_option('cache', 'ip'):
        config_obj.ip = config_dict['cache']['ip']
    if config.has_section('records'):
        for key in config_dict['records'].keys():
            host = key
            value = config_dict['records'][host]
            config_obj.records[host] = value

    # Make sure api key is correct
    from re import match
    api_key_re = '[0-9a-fA-F]{40}'
    api_key = config_obj.api_key
    match = match(api_key_re, api_key)
    if not match:
        exit(1, 'Malformed API Key. Must be 40 hex character SHA1 Hash')

    info(args['v'], 'Successfully Imported Configuration File: %s' % filepath)
    return config_obj
