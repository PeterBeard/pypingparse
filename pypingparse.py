#!/usr/bin/env python3
"""
pypingparse -- Python script for parsing the output of ping

Copyright Peter Beard, GPLv3 licensed. See LICENSE the complete license.
"""
import argparse
import fileinput
import matplotlib.pyplot as plt

from entry import Entry

def parse_file(fh):
    """
    Parse a file containing the output of ping
    
    Returns a list of Entry objects, one for each line in the input file
    """
    entries = []
    for line in fh:
        e = Entry(line)
        if e.icmp_seq is not None:
            entries.append(e)

    return entries


def get_args():
    """
    Parse command line arguments

    Returns an argparse namespace
    """
    p = argparse.ArgumentParser(description='Parse the output of the ping command',)
    p.add_argument(
        '-t',
        '--histogram-time',
        dest='histogram_time',
        action='store_true',
        help='Plot a histogram of RTTs'
    )
    p.add_argument(
        '-b',
        '--histogram_bins',
        dest='bin_count',
        type=int,
        help='The number of bins to use in the histogram'
    )
    p.add_argument(
        '-x',
        type=str,
        nargs='?',
        choices=['time','icmp_seq'],
        dest='xaxis',
        help='Variable to display on the x-axis (time or icmp_seq)'
    )
    p.add_argument(
        '-y',
        type=str,
        nargs='?',
        choices=['time','icmp_seq'],
        dest='yaxis',
        help='Variable to display on the y-axis (time or icmp_seq)'
    )
    p.add_argument(
        'filename',
        nargs='?',
        default=None,
        help='Logfile location -- will use STDIN if not specified'
    )

    return p.parse_args()


def main():
    """Main function"""
    args = get_args()

    # Parse the log
    if args.filename is None:
        entries = parse_file(fileinput.input('-'))
    else:
        with open(args.filename, 'r') as fh:
            entries = parse_file(fh)

    # Plot
    if args.xaxis == 'icmp_seq' and args.yaxis == 'time':
        line = plt.plot(
            [e.icmp_seq for e in entries],
            [e.time_ms for e in entries]
            )
        plt.title('ICMP RTT to {}'.format(entries[1].ip_from))
        plt.xlabel('icmp_seq')
        plt.ylabel('time (ms)')
    elif args.histogram_time:
        plt.hist([float(e.time_ms) for e in entries], bins=args.bin_count)
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()
