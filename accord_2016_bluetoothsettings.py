#!/usr/bin/python

# Python 3 script that reads bluetoothsettings.db "bluetooth_device" table and outputs details to TSV file
# Author: A. Leong (based on data shared by M. Fuentes)
# Tested on Win10x64 running Python 3.9
# bluetoothsettings.db can be found at: \data\com.clarion.bluetooth\databases\bluetoothsettings.db

import argparse
import datetime
import sqlite3
from os import path

version_string = "accord_2016_bluetoothsettings.py v2021-03-23"

def main():
    usagetxt = " %(prog)s [-d inputfile -o outputfile]"
    parser = argparse.ArgumentParser(description='Reads Honda Accord (2016) bluetoothsettings.db "bluetooth_device" table and outputs details to TSV', usage=usagetxt)
    parser.add_argument("-d", dest="database", action="store", required=True, help='SQLite DB filename i.e. bluetoothsettings.db')
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

    query = "SELECT device_bank, device_addr, device_name FROM bluetooth_device ORDER BY device_bank ASC;"
    cursor = dbcon.cursor()
    cursor.execute(query)
    row = cursor.fetchone()

    entries = []

    while row:
        device_bank = str(row[0])
        device_addr = row[1]
        device_name = row[2]

        # store each row returned    
        entries.append((device_bank, device_addr, device_name))
        
        row = cursor.fetchone()

    cursor.close()
    dbcon.close()

    # Write TSV report
    with open(args.output, "w") as outputTSV:
        outputTSV.write("device_bank\tdevice_addr\tdevice_name\n")
        
        for entry in entries:
            device_bank = entry[0]
            device_addr = entry[1]
            device_name = entry[2]
           
            outputTSV.write(device_bank + "\t" + device_addr + "\t" + device_name + "\n")

    print("Processed/Wrote " + str(len(entries)) + " entries to: " + args.output + "\n")
    print("Exiting ...\n")

if __name__ == "__main__":
    main()

    
    
