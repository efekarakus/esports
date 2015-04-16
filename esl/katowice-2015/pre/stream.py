import sys, csv, os
from dateutil.parser import parse
from datetime import datetime, timedelta

def usage():
    print "python stream.py <data>.csv <streamer>"

def get_partials(path, streamer):
    partials = []
    with open(path, 'r') as f:
        reader = csv.reader(f)
        reader.next()
        for row in reader:
            s = row[0]
            if s == streamer:
                partials.append({
                    'count': int(row[1]),
                    'timestamp': parse(row[2])
                })
    return partials

def is_new_stream(partials, index, delta):
    if index == 0:
        return True
    current = partials[index]
    previous = partials[index - 1]

    gap = current['timestamp'] - delta

    if previous['timestamp'] < gap: #previous timestamp too long ago
        return True
    return False

def split(partials):
    delta = timedelta(minutes=30)
    streams = []
    stream = []
    for index in range(len(partials)):
        partial = partials[index]
        if is_new_stream(partials, index, delta):
            if stream: # to handle first case
                streams.append(stream)
            stream = []
        stream.append(partial)
    if stream:
        streams.append(stream)
    return streams
   
def write(streams, streamer):
    with open(streamer + '.csv', 'w') as f:
        f.write('id,streamer,count,timestamp\n')
        sid = 1
        for stream in streams:
            for partial in stream:
                f.write( '%d,%s,%d,%s\n' % (sid, streamer, partial['count'], partial['timestamp'].strftime('%Y-%m-%dT%H:%M:%S')) )
            sid += 1 

def find_streams(path, streamer):
    partials = get_partials(path, streamer)
    streams = split(partials)
    write(streams, streamer)

if __name__=='__main__':
    if len(sys.argv) != 3:
        usage()
        sys.exit(-1)

    path = sys.argv[1]
    streamer = sys.argv[2]

    find_streams(path, streamer)
