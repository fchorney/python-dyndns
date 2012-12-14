Python-Dyndns
=============

Python implementation of a dynamic DNS Updater for [afraid.org](http://freedns.afraid.org)

Requirements
------------

Python libraries (Which should all come standard):

    argparse
    urllib2
    ConfigParser
    os
    sys
    re
    xml.etree.cElementTree

Cofiguration File
-----------------

The configuration file is split in to 3 sections:

    [authentication]
    api_key=insert_SHA1_key_here

    [cache]
    ip=0.0.0.0

    [records]
    host=base64_encoded_update_key

The default "example.cfg" is as follows:

    [authentication]
    api_key=

    [cache]
    ip=0.0.0.0

    [records]

### api_key

The api_key can be found by logging in to your [afraid.org](http://freedns.afraid.org) account
and going to the the [api](http://freedns.afraid.org/api/) page and clicking on either the
"XML" or "ASCII" links.

Your url will then look like this:

    http://freedns.afraid.org/api/?action=getdyndns&sha=API_KEY_HERE&style=xml

or

    http://freedns.afraid.org/api/?action=getdyndns&sha=API_KEY_HERE

Copy your api key into the api_key= section of the config file.

### cache

This field is updated automatically by the script and stores the last known external IP Address
that it found.

It starts off at 0.0.0.0, but will be updated the first time you run an update.

### records

This field is also updated automatically by the script. When you run the script with the
`--configure` flag, you will interactively configure which records you want to update.

Installation
------------

As long as you have the required python libraries, it should just work.

Once you have your configuration file properly configured, you may set this up on a
cron and have it run at an interval of your choice, such as every 15 minutes:

    */15 * * * * python /path/to/dyndns.py /path/to/configuration/file

Usage
-----
This implementation comes with a few options.
At it's most basic usage, you will first want to configure your config file.

Follow the instructions above under the "api_key" section and put your
[afraid.org](http://freedns.afraid.org) api_key in the config file.

### --configure

Run dyndns.py in configuration mode:

    python dyndns.py --configure example.cfg
    Retreiving records from https://freedns.afraid.org/api/?action=getdyndns&sha=API_KEY_HERE&style=xml
    Found 2 records
    Delete all records (y/n): y
    Save hosta.com to config file (y/n): y
    Save hostb.com to config file (y/n): n

If your configuration file already has records saved to it, dyndns will ask if you want to delete all currently saved records.
Usually you will want to do this if you have removed any records from the website, or just as a clean up.

The script will then run through each host and as you if you would like to save it to the configuration file or not.

This will leave you with a configuration file as follows:

    [authentication]
    api_key=API_KEY_HERE

    [cache]
    ip=0.0.0.0

    [records]
    hosta.com=base64_encoded_update_key

Once your configuration file is properly configured, just run it manually, or on a cron.

    python dyndns.py example.cfg

### -c, --check-ip

This is strictly an informational option. This will fetch your current external ip and then display that, and your currently
cached ip and exit. This will NOT update your configuration file.

    python dyndns.py -c example.cfg
    retreiving current external ip from http://checkip.dyndns.org
    Current External IP Address: 1.2.3.4
    Current Cached IP Address: 5.6.7.8

### -r, --get-records

This is strictly an informational option. This will fetch your record information from [afraid.org](http://freedns.afraid.org),
display it to you, and exit.

    python dyndns.py -r example.cfg
    Retreiving records from https://freedns.afraid.org/api/?action=getdyndns&sha=API_KEY_HERE&style=xml
    Record For: hosta.com
    IP Address: 1.2.3.4
    URL: https://freedns.afraid.org/dynamic/update.php?base64_encoded_update_key

    Record For: hostb.com
    IP Address: 2.3.4.5
    URL: https://freedns.afraid.org/dynamic/update.php?base64_encoded_update_key

