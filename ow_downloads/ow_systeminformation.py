#!/usr/bin/python3

import os
import platform

if __name__ == '__main__':
    os_name = os.name
    platform = platform.system()
    release = platform.release()
    # TODO: get IP address, mac address, hostname, iptables rules

