"""
Object representing a single line of ping output

This file is part of pypingparse.
Copyright Peter Beard, GPLv3 licensed. See LICENSE the complete license.
"""
import re

class Entry:
    def __init__(self, string):
        matches = re.match(
                '^.+from ([.0-9]+): icmp_seq=(\d+) ttl=(\d+) time=([.0-9]+) ms\r*\n*$',
                string
        )
        if matches is not None:
            self.ip_from = matches.group(1)
            self.icmp_seq = matches.group(2)
            self.ttl = matches.group(3)
            self.time_ms = matches.group(4)
        else:
            self.ip_from = None
            self.icmp_seq = None
            self.ttl = None
            self.time_ms = None
