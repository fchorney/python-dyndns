#!/usr/bin/env python

from Output import exit, message, info, debug

class Config:
    def __init__(self):
        self.api_key = ''
        self.ip = ''
        self.records = {}

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        string = "Configuration:\nAPI Key: %s\nCached IP: %s\nRecords:\n"
        string = string % (self.api_key, self.ip)
        for key in self.records.keys():
            host = key
            value = self.records[host]
            string += "%s: %s\n" % (host, value)
        return string


def parse_config(filepath, verbosity=0):
    """ Parse Configuration File """
    import ConfigParser
    v = verbosity

    # Assume filepath is good, since it is already checked
    info(v, 'Importing Configuration File: %s' % filepath)
    config = ConfigParser.SafeConfigParser(allow_no_value=True)
    try:
        config.readfp(open(filepath, 'r'))
    except Exception, e:
        exit(1, "Error reading config file (%s): %s" % (filepath, e))

    # Error Check
    if not config.has_section('authentication'):
        exit(1, "Malformed Config File. Missing 'authentication' section")
    if not config.has_option('authentication', 'api_key'):
        exit(1, "Malformed Config File. Missing 'api_key' option")

    # Create a dictionary of config values
    config_dict = {}
    for section in config.sections():
        config_dict[section] = {}
        for name, value in config.items(section):
            config_dict[section][name] = value
            debug(v, "Section: %s\nName: %s\nValue: %s" % (section, name,
                value))

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
    from re import match as re_match
    if not re_match('[0-9a-fA-F]{40}', config_obj.api_key):
        exit(1, 'Malformed API Key. Must be 40 hex character SHA1 Hash')

    info(v, 'Successfully Imported Configuration File: %s' % filepath)
    return config_obj
