#!/usr/bin/python3

"""Minimal Yara Scanner
    - get rules
    - run scan
    - report findings
"""

from requests import get
from base64 import b64decode
import argparse
import sys
import yara
import os

ow_server = '<OW_IP>'
ow_port = '<OW_PORT>'
my_token = '<OW_TOKEN>'

# DEBUG
ow_server = '127.0.0.1'
ow_port = '8000'
my_token = 'fa6343b3dee5aa4377a1a37ac431b7cfa773540bba979b11e982417adb7334aa'

def get_all_yara_rules():
    """ get all yara rules from API server
    """
    owurl = 'http://'+ow_server+':'+str(ow_port)+'/api/1.0/'+my_token+'/get/yara/rules/all/'
    try:
        resp = get(owurl)
        jrsp = resp.json()
    except Exception as error:
        print('>>> Response Error: %s' % error)
        return None
    if jrsp['cmd'] == 'rules':
        try:
            fp = open('all_rules.yar', 'w')
            fp.write(b64decode(jrsp['data']).decode('utf8'))
            fp.close()
        except Exception as error:
            print('>>> Rule Write Error: %s' % error)
            return None
        print('> Rules downloaded.')
        return 'all_rules.yar'
    print('>>> Server Error: %s' % jrsp['msg'])
    return None

def compile_rules(rules_file):
    """ compile all yara files in given directory
    """
    rules = yara.compile(filepath=rules_file)
    print('> Rules compiled.')
    return rules


def scan(rules, target):
    """ scan target directory with yara
    """
    matches = rules.match(target)
    return matches

if __name__ == '__main__':
    # get all rules
    rule_filename = get_all_yara_rules()
    rules = compile_rules(rule_filename)
    matches = scan(rules, '/')
