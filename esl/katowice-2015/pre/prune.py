import sys, os, getopt
import csv
from dateutil.parser import parse
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import operator

#PRUNE_IDS = [2, 3, 5, 6]
PRUNE_IDS = [2, 4, 5, 7, 8, 10]

def get_streams(path):
    streams = []
    with open(path, 'r') as f:
        reader = csv.reader(f)
        reader.next()
        sid = None
        partials = []

        for row in reader:
            rid = int(row[0])
            rstreamer = row[1]
            rcount = int(row[2])
            rtime = parse(row[3])

            if sid != rid:
                if partials:
                    streams.append(partials)
                sid = rid
                partials = []

            partials.append({
                'id': rid,
                'streamer': rstreamer,
                'count': rcount,
                'timestamp': rtime
            })
        if partials:
            streams.append(partials)
    return streams

def write(streams, streamer):
    with open(streamer + '-pruned.csv', 'w') as f:
        f.write('id,streamer,count,timestamp\n')
        sid = 1
        for stream in streams:
            for partial in stream:
                f.write( '%d,%s,%d,%s\n' % (sid, streamer, partial['count'], partial['timestamp'].strftime('%Y-%m-%dT%H:%M:%S')) )
            sid += 1 

if __name__ == "__main__":
    streamer = sys.argv[1]
    csvfile = streamer + ".csv"
    streams = get_streams(csvfile)
    pruned = [partial for partial in streams if not partial[0]['id'] in PRUNE_IDS]
    write(pruned, streamer)
