#!/usr/bin/python3

from sys import exit as sexit
from sys import stderr as sstderr
from re import search as rsearch
from re import compile as rcompile
from json import dumps
from subprocess import run as srun
from subprocess import PIPE as stdPIPE
from os import geteuid

import argparse

RKHUNTER_PATH = '/usr/bin/rkhunter'
RKHUNTER_LOG = '/var/log/rkhunter.log'
WORKING_VERSION = '1.4.6'
WARNING_CHECK_LST = ['Checking for hidden files and directories', 'Checking for prerequisites', 'Checking if SSH root access is allowed']

# TODO:
# - add hostname and ip addresses for identification
# - test output to elasticsearch

def check_rkhunter_log(checkname):
    sr1 = rcompile('\[.*?\][\s\t]+(.*)')
    #sr2 = rcompile('\[.*?\] Warning:(.*)')
    with open(RKHUNTER_LOG) as fp:
        lines = fp.readlines()
    result = []
    inline = False
    stop = False
    for index in range(0, len(lines)):
        if stop:
            break
        line = lines[index].strip()
        if line.count(checkname)>0 and line.count('Warning')>0 and not inline:
            inline = True
            continue
        if inline:
            if line.count('Checking')>0 or line.count('[ OK ]')>0 or line.count('[ Warning ]')>0:
                inline = False
                stop = True
                continue
            match = sr1.search(line.strip())
            if match:
                result.append(match.groups()[0])
    return result


def rkhunter_version_check():
    cp = srun([RKHUNTER_PATH, '--version'], stdout=stdPIPE)
    output_lst = cp.stdout.decode('utf-8').split('\n')
    for index in range(0, len(output_lst)):
        line = output_lst[index].strip()
        if line == '':
            continue
        #vmatch = rsearch('^\[ Rootkit Hunter version (.*?) \]$', line)
        vmatch = rsearch('^Rootkit Hunter ([0-9\.]+?)$', line)
        if vmatch:
            rkhunter_version = vmatch.groups()[0]
            if rkhunter_version != WORKING_VERSION:
                print('Incompatible version found! Aborting.')
                sexit(255)
            return rkhunter_version
    print('Unable to identify RKHunter Version! Aborting.')
    sexit(255)
    return False

if __name__ == '__main__':
    # check arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", help="increase output verbosity", action="store_true")
    args = parser.parse_args()
    # root required for rkhunter
    if geteuid() != 0:
        if args.verbose:
            print('> You must be the root user to run this program.')
        else:
            print('root permissions required!', file=sstderr)
        sexit(0)
    if args.verbose:
        print('> Running RKHunter ...')
    # check version
    if args.verbose:
        print('> Version check: ', end='')
    rkhunter_version = rkhunter_version_check()
    if not rkhunter_version:
        if args.verbose:
            print('not supported!')
        else:
            print('unsupported version!', file=sstderr)
        sexit(255)
    if args.verbose:
        print(rkhunter_version)
    # run rkhunter as subprocess
    cp = srun([RKHUNTER_PATH, '-c', '--sk', '--nocolors', '--noappend-log'], stdout=stdPIPE)
    output_lst = cp.stdout.decode('utf-8').split('\n')
    # run report parser on output
    hunter_report = {'information': {}, 'summary': {}}
    section = None
    for index in range(0, len(output_lst)):
        line = output_lst[index].strip()
        if line == '':
            continue
        # search for rkhunter version
        if 'information' in hunter_report.keys() and 'version' not in hunter_report['information'].keys():
            if rkhunter_version:
                hunter_report['information']['version'] = rkhunter_version
        # generic parser
        if line.startswith('Performing '):
            perf, rest = line.split(' ', 1)
            section = rest.replace("'", "")
            hunter_report[section] = {}
            continue
        generic_match = rsearch('^(?P<checkname>.+?)\s+?\[ (?P<checkresult>.*?) \]$', line)
        if generic_match and section:
            if generic_match.group('checkname').count("'") > 1:
                checkname = generic_match.group('checkname').replace("'", "")
            else:
                checkname = generic_match.group('checkname')
            if generic_match.group('checkresult').count("'") > 1:
                checkresult = generic_match.group('checkresult').replace("'", "")
            else:
                checkresult = generic_match.group('checkresult')
            if checkname in WARNING_CHECK_LST and checkresult == 'Warning':
                #print('>> checking warning value of: %s' % checkname)
                warning_mess = check_rkhunter_log(checkname)
            elif section == 'file properties checks' and checkresult == 'Warning':
                warning_mess = check_rkhunter_log(checkname)
            else:
                warning_mess = []
            if len(warning_mess)<=0:
                hunter_report[section][checkname] = checkresult
            else:
                hunter_report[section][checkname] = (checkresult, warning_mess)
            continue
        # summary information
        match_files_check = rsearch('^Files checked: (.*?)$', line)
        if match_files_check:
            hunter_report['summary']['files checked'] = int(match_files_check.groups()[0])
            continue
        match_suspect_files = rsearch('^Suspect files: (.*?)$', line)
        if match_suspect_files:
            hunter_report['summary']['suspect files'] = int(match_suspect_files.groups()[0])
            continue
        match_rootkits_check = rsearch('^Rootkits checked : (.*?)$', line)
        if match_rootkits_check:
            hunter_report['summary']['rootkits checked'] = int(match_rootkits_check.groups()[0])
            continue
        match_rootkits_found = rsearch('^Possible rootkits: (.*?)$', line)
        if match_rootkits_found:
            hunter_report['summary']['possible rootkits'] = int(match_rootkits_found.groups()[0])
            continue
        # missed something?
        if 'missing' in hunter_report:
            hunter_report['missing'].append(line)
        else:
            hunter_report['missing'] = [line]
    if args.verbose:
        print(dumps(hunter_report, indent=4, sort_keys=True))
    else:
        print(dumps(hunter_report, sort_keys=True))
