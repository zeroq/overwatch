#!/usr/bin/python3
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

"""Minimal Overwatch agent:
    - deploy on demand via webinterface
    - run with cronjob every 5 minutes
"""

from requests import get, post
from json import dumps
import logging
from sys import exit
from subprocess import Popen, PIPE
from os import remove
from base64 import b64decode

ow_server = '<OW_IP>'
ow_port = '<OW_PORT>'
my_token = '<OW_TOKEN>'

def init_logging():
    """ initialize logging of agent
    """
    logging.basicConfig(filename='ow_agent.log', filemode='w', level=logging.INFO)
    return True


if __name__ == '__main__':
    """ main functionality starts here
    """
    init_logging()
    # construct url to get host profile
    owurl = 'http://'+ow_server+':'+str(ow_port)+'/api/1.0/'+my_token+'/get/profile/'
    logging.debug('connecting to: %s' % owurl)
    try:
        resp = get(owurl)
        logging.debug(dumps(resp.json()))
        jrsp = resp.json()
    except Exception as error:
        logging.error(error)
        exit(255)
    # check returned profiles
    if 'profiles' in jrsp:
        # iterate over each returned profile
        for profilename in jrsp['profiles']:
            logging.debug("found profile: %s" % profilename)
            owurl = 'http://'+ow_server+':'+str(ow_port)+'/api/1.0/'+my_token+'/get/'+profilename+'/'
            logging.debug("downloading profile: %s" % owurl)
            # download profile script
            try:
                resp = get(owurl)
                jrsp = resp.json()
            except Exception as error:
                logging.error(error)
                continue
            # check if it is a command profile
            if 'cmd' in jrsp and 'data' in jrsp:
                if jrsp['cmd'] == 'Dummy':
                    logging.info('running dummy script ...')
                    outs = 'Dummy'
                    errs = ''
                    tid = 0
                elif jrsp['cmd'] == 'run':
                    # execute profile script
                    logging.info('running profile script ...')
                    try:
                        fp = open('%s.py' % profilename, 'w')
                        fp.write(b64decode(jrsp['data']).decode('utf8'))
                        fp.close()
                    except Exception as e:
                        logging.error(e)
                        continue
                    # TODO: get task ID: tid
                    # TODO: get timeout parameter
                    try:
                        proc = Popen(['sudo', 'python3', '%s.py' % profilename], stdin=PIPE, stdout=PIPE, stderr=PIPE)
                    except Exception as e:
                        logging.error(e)
                        continue
                    logging.debug('waiting for output ...')
                    try:
                        outs, errs = proc.communicate(timeout=300) # timeout after x seconds
                        logging.error(errs)
                        logging.debug(outs)
                    except TimeoutExpired:
                        logging.error('profile script timed out: %s' % profilename)
                        proc.kill()
                        outs, errs = proc.communicate()
                        continue
                    logging.debug('execution finished.')
                    # remove script file
                    try:
                        #remove('%s.py' % profilename)
                        pass
                    except Exception as e:
                        logging.error(e)
                        pass
                elif jrsp['cmd'] == 'install':
                    # install provided script (e.g. rkhuner)
                    # TODO: implement this / profile still missing
                    outs = ''
                    errs = 'Command not implemented: %s' % jrsp['cmd']
                    tid = 0
                else:
                    outs = ''
                    errs = 'Unknown cmd: %s' % jrsp['cmd']
                    tid = 0
                logging.debug('submitting results.')
                # submit results back to server
                owurl = 'http://'+ow_server+':'+str(ow_port)+'/api/1.0/'+my_token+'/submit/'+profilename+'/'
                payload = {'profile': profilename, 'data': outs, 'errors': errs}
                try:
                    srsp = post(owurl, data=payload)
                    logging.debug(srsp.content)
                except Exception as e:
                    logging.error(e)
                    logging.error('failed submission of data!')
                    continue
            else:
                logging.error("wrong/broken data received: %s" % jrsp)
                continue
