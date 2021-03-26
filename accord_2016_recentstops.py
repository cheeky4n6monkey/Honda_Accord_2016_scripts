#!/usr/bin/python

# Python 3 script that reads RecentStops.db "history" table and outputs details to TSV file
# Author: A. Leong (based on data shared by M. Fuentes)
# Tested on Win10x64 running Python 3.9
# RecentStops.db can be found at: \data\com.honda.displayaudio.navi\Garmin\sqlite\RecentStops.db

import argparse
import datetime
import sqlite3
from os import path

version_string = "accord_2016_recentstops.py v2021-03-22"

def main():
    usagetxt = " %(prog)s [-d inputfile -o outputfile]"
    parser = argparse.ArgumentParser(description='Reads Honda Accord (2016) RecentStops.db "history" table and outputs details to TSV', usage=usagetxt)
    parser.add_argument("-d", dest="database", action="store", required=True, help='SQLite DB filename i.e. RecentStops.db')
    parser.add_argument("-o", dest="output", action="store", required=True, help='Output file name for Tab-Separated-Value report')

    args = parser.parse_args()

    print("Running " + version_string + "\n")
    
    if not args.database or not args.output:
        parser.exit("ERROR - Input file or Output file NOT specified")
    
    # Check DB file exists before trying to connect
    if path.isfile(args.database):
        dbcon = sqlite3.connect(args.database)
    else:
        print(args.database + " DB file does not exist!")
        exit(-1)

    query = "SELECT time, lat, lon, name FROM history ORDER BY time ASC;"
    cursor = dbcon.cursor()
    cursor.execute(query)
    row = cursor.fetchone()

    entries = []

    while row:
        timeval = row[0]
        rawlat = row[1]
        rawlon = row[2]
        name = row[3]

        timestamp = datetime.datetime.utcfromtimestamp(timeval + 631065600) # Convert Garmin secs since 31DEC1989 to UTC secs since 1JAN1970
        timestr = timestamp.isoformat()
        
        lat = rawlat * 180 / 2**31 # Garmin lat/lon scaling
        lon = rawlon * 180 / 2**31
        
        # store each row returned    
        entries.append((timestr, lat, lon, name))
        
        row = cursor.fetchone()

    cursor.close()
    dbcon.close()

    # Write TSV report
    with open(args.output, "w") as outputTSV:
        outputTSV.write("time\tlat\tlon\tname\n")
        
        for entry in entries:
            timestamp = entry[0]
            lat = entry[1]
            lon = entry[2]
            name = entry[3]
           
            outputTSV.write(timestamp + "\t" + str(lat) + "\t" + str(lon) + "\t" + name + "\n")

    print("Processed/Wrote " + str(len(entries)) + " entries to: " + args.output + "\n")
    print("Exiting ...\n")

if __name__ == "__main__":
    main()

    
    
