import sys, os, getopt
import csv
from dateutil.parser import parse
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import operator

def usage():
    print "python visualize.py --<option> OR python visualize.py <streamer.csv> <subscribers.csv>" 
    print "\tstream=<streamer.csv> e.g. imaqtpie.csv"
    print "\tsub=<subscriber.csv> e.g. tsm_bjergsen-subscribers.csv"
    print "\tmoney=<stats.csv> e.g. data/stats20.csv"
    print "\t for both -- e.g. python visualize data/imaqtpie.csv data/imaqtpie-subscribers.csv"

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

def stream(path):
    streams = get_streams(path)
    for i in range(len(streams)):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        stream = streams[i]

        timestamps = [p['timestamp'] for p in stream]
        counts = [p['count'] for p in stream]
        
        ax.fill_between(timestamps, 0, counts, facecolor='blue', alpha=0.5)
        ax.grid(True)
        ax.set_ylabel('viewers')

        fig.suptitle( '%s for stream %d\n%s' % (stream[0]['streamer'], stream[0]['id'], stream[0]['timestamp'].strftime('%Y-%m-%d')) )
        fig.autofmt_xdate()
    plt.show()

def get_subscribers(path):
    subscribers = {}
    with open(path, 'r') as f:
        reader = csv.reader(f)
        reader.next()

        for row in reader:
            rid = int(row[0])
            rstreamer = row[1]
            rtime = parse(row[2])
            rcount = int(row[3])

            if not rid in subscribers:
                subscribers[rid] = []

            subscribers[rid].append({
                'streamer': rstreamer,
                'timestamp': rtime,
                'count': rcount
            })
    return subscribers


def subscriber(path):
    subscribers = get_subscribers(path)
    for sid in sorted(subscribers.keys()):
        subs = subscribers[sid]

        fig = plt.figure()
        ax = fig.add_subplot(111)

        timestamps = [p['timestamp'] for p in subs]
        counts = [p['count'] for p in subs]
        
        ax.bar(timestamps, counts, width=0.0415, color='r')
        ax.set_ylabel('subscribers')
        ax.xaxis_date()

        fig.suptitle( 'Subscribers for %s over stream %s' % (subs[0]['streamer'], sid) )
        fig.autofmt_xdate()
    plt.show()

def both(viewers_path, sub_path):
    streams = get_streams(viewers_path)
    subscribers = get_subscribers(sub_path)
    for i in range(len(streams)):
        fig = plt.figure()

        # viewers
        ax1 = fig.add_subplot(211)
        stream = streams[i]

        timestamps = [p['timestamp'] for p in stream]
        counts = [p['count'] for p in stream]
        
        ax1.fill_between(timestamps, 0, counts, facecolor='blue', alpha=0.5)
        ax1.grid(True)
        ax1.set_ylabel('viewers')

        # subscribers
        subs = subscribers[ stream[0]['id'] ]
        
        timestamps = [p['timestamp'] for p in subs]
        counts = [p['count'] for p in subs]

        isEmpty = True
        for count in counts:
            if count != 0: isEmpty = False

        if not isEmpty:
            ax2 = fig.add_subplot(212)

            ax2.bar(timestamps, counts, width=0.0415, color='r')
            ax2.set_ylabel('subscribers')
            ax2.fmt_xdata = mdates.DateFormatter("%H:%M:%S")
            ax2.xaxis_date()
           
            ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        else:
            ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))

        fig.suptitle( '%s for stream %d\n%s' % (stream[0]['streamer'], stream[0]['id'], stream[0]['timestamp'].strftime('%Y-%m-%d')) )
        fig.autofmt_xdate()
    plt.show()

def money(path):
    money = {}
    with open(path, 'r') as f:
        reader = csv.reader(f, skipinitialspace=True)
        reader.next()
        for row in reader:
            streamer = row[0]
            earned = float(row[4])

            money[streamer] = earned
    # endwith

    sorted_money = sorted(money.items(), key=operator.itemgetter(1))

    streamers= [pair[0] for pair in sorted_money]
    revenues = [pair[1] for pair in sorted_money]


    plt.title('Money / streamer')
    plt.plot(range(len(streamers)), revenues)
    plt.yticks(np.arange(0, max(revenues) + 100, 1000))
    plt.xticks(range(len(streamers)), streamers)
    locs, labels = plt.xticks()
    plt.setp(labels, rotation=90)
    plt.show()
    

if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hs:m:", ["help", "stream=", "sub=", "money="])
    except getopt.GetoptError as err:
        print str(err)
        usage()
        sys.exit(2)

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-s", "--stream"):
            stream(a)
        elif o in ("-b", "--sub"):
            subscriber(a)
        elif o in ("-m", "--money"):
            money(a)
        else:
            usage()
            sys.exit(3)

    if args:
        both(args[0], args[1])
