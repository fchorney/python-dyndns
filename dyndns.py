#!/usr/bin/env python

from libdyndns.Output import error, exit, message, extra, debug, info
from libdyndns.Config import Config
from libdyndns.Retreive import Record, get_records, update_record
from libdyndns.Retreive import get_external_ip
from libdyndns.Utils import get_yes_no


def get_and_print_ip(cached_ip, v):
    external_ip = get_external_ip(v)
    message("Cached IP: %s" % cached_ip)
    if external_ip is None:
        error("Could not retreive external IP")
        return
    message("External IP: %s" % external_ip)


def get_and_print_records(api_key, v):
    records = get_records(api_key, v)
    if records is None:
        error("Could not retreive records")
        return
    for record in records:
        message(record)


def configure_config_file(config, v):
    # First gather records from the web
    external_records = get_records(config.api_key, v)
    message("Found %s Records" % len(external_records))

    # Prompt to delete current records
    has_records = len(config.records.keys()) > 0
    if has_records and get_yes_no("Delete all records (y/n): "):
        debug(v, "Deleting all records")
        for key in config.records.keys():
            extra(v, "Deleting Record: %s" % config.records[key])
            del(config.records[key])

    # Go through each record and prompt the user to save it
    for new_record in external_records:
        if get_yes_no("Save %s to config file (y/n): " % new_record.host):
            config.records[new_record.host] = new_record.updateKey()
            extra(v, "Saving New Record: %s" % config.records[new_record.host])

    config.save()


def update_records(config, v):
    # First gather records and current IP from the web
    external_records = get_records(config.api_key, v)
    external_ip = get_external_ip(v)

    # Check if current external ip differs from cached ip
    if external_ip != config.ip:
        message("External IP Changed. Saving %s to config" % external_ip)
        config.ip = external_ip
        config.save()

    # If records have been saved in the config
    has_records = len(config.records.keys()) > 0
    if not has_records:
        # User has no records stored in the config, return
        error("No records saved in config. Try using the --configure flag")
        return

    # Cycle through returned external records.
    # Filter so we only have records we are interested in updating
    stored_hosts = config.records.keys()
    for e_record in [x for x in external_records if x.host in stored_hosts]:
        if e_record.address == config.ip:
            info(v, "%s does not need to be updated" % e_record.host)
            continue
        # External record has different ip then our currently cached ip
        # Update the record
        update_record(e_record, config.ip, v)

def main():
    args = parse_args()
    config = Config(args.config_file, args.v)
    update = True

    if args.external_ip:
        get_and_print_ip(config.ip, args.v)
        update = False
    if args.get_records:
        get_and_print_records(config.api_key, args.v)
        update = False
    if args.configure:
        configure_config_file(config, args.v)
        update = False

    if update:
        update_records(config, args.v)

    exit(0)


def parse_args():
    import argparse
    parser = argparse.ArgumentParser(description="afraid.org Dynamic DNS",
             formatter_class=argparse.ArgumentDefaultsHelpFormatter);

    parser.add_argument('config_file', type=str,
                        help='Path to configuration file')
    parser.add_argument('-v', action='count', default=0,
                        help='Set level of verbosity')
    parser.add_argument('--configure', action='store_true',
                        help='Interactively configure your dyndns config file')

    # Check and Exit Arguments
    check_and_exit = parser.add_argument_group('Check and Exit')
    check_and_exit.add_argument('-e', '--external-ip', action='store_true',
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
