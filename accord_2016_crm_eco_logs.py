#!/usr/bin/python

# Python 3 script that reads crm.db "eco_logs" table and outputs details to TSV file
# Author: A. Leong (based on data shared by M. Fuentes)
# Tested on Win10x64 running Python 3.9
# crm.db can be found at: \data\com.honda.telematics.core\databases\crm.db

import argparse
import datetime
import sqlite3
from os import path

version_string = "accord_2016_crm_eco_logs.py v2021-03-22"

def main():
    usagetxt = " %(prog)s [-d inputfile -o outputfile]"
    parser = argparse.ArgumentParser(description='Reads Honda Accord (2016) crm.db history "eco_logs" table and outputs details to TSV', usage=usagetxt)
    parser.add_argument("-d", dest="database", action="store", required=True, help='SQLite DB filename i.e. crm.db')
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

    query = "SELECT _id, trip_date, trip_id, mileage, start_pos_time, start_pos_odo, finish_pos_time, finish_pos_odo, fuel_used, driving_range FROM eco_logs ORDER BY _id ASC;"
    cursor = dbcon.cursor()
    cursor.execute(query)
    row = cursor.fetchone()

    entries = []

    while row:
        id = row[0]
        trip_date = row[1]
        trip_id = row[2]
        mileage = row[3]
        start_pos_time = row[4]
        start_pos_odo = row[5]
        finish_pos_time = row[6]
        finish_pos_odo = row[7]
        fuel_used = row[8]
        driving_range = row[9]
        
        trip_date_ts = datetime.datetime.utcfromtimestamp(trip_date/1000) # Ass-ume UTC millisecs since 1JAN1970
        trip_date_timestr = trip_date_ts.isoformat()
        
        start_pos_ts = datetime.datetime.utcfromtimestamp(start_pos_time/1000) # Ass-ume UTC millisecs since 1JAN1970
        start_pos_timestr = start_pos_ts.isoformat()

        fin_pos_ts = datetime.datetime.utcfromtimestamp(finish_pos_time/1000) # Ass-ume UTC millisecs since 1JAN1970
        fin_pos_timestr = fin_pos_ts.isoformat()
        
        # store each row returned    
        entries.append((id, trip_date_timestr, trip_id, mileage, start_pos_timestr, start_pos_odo, fin_pos_timestr, finish_pos_odo, fuel_used, driving_range))
        
        row = cursor.fetchone()

    cursor.close()
    dbcon.close()

    # Write TSV report
    with open(args.output, "w") as outputTSV:
        outputTSV.write("_id\ttrip_date\ttrip_id\tmileage\tstart_pos_time\tstart_pos_odo\tfinish_pos_time\tfinish_pos_odo\tfuel_used\tdriving_range\n")
        
        for entry in entries:
            id = str(entry[0])
            trip_date = entry[1]
            trip_id = str(entry[2])
            mileage = str(entry[3])
            start_pos_time = entry[4]
            start_pos_odo = str(entry[5])
            finish_pos_time = entry[6]
            finish_pos_odo = str(entry[7])
            fuel_used = str(entry[8])
            driving_range = str(entry[9])
            
            outputTSV.write(id+"\t"+trip_date+"\t"+trip_id+"\t"+mileage+"\t"+start_pos_time+"\t"+start_pos_odo+"\t"+finish_pos_time+"\t"+finish_pos_odo+"\t"+fuel_used+"\t"+driving_range+"\n")

    print("Processed/Wrote " + str(len(entries)) + " entries to: " + args.output + "\n")
    print("Exiting ...\n")

if __name__ == "__main__":
    main()

    
    
