#!/usr/bin/python

# Python 3 script that reads phonedb.db "callhistory", "contact", "contactnumber" tables and outputs details to TSV file
# Author: A. Leong (based on data shared by M. Fuentes)
# Tested on Win10x64 running Python 3.9
# phonedb.db can be found at: \data\com.clarion.bluetooth\databases\phonedb.db

import argparse
import datetime
import sqlite3
from os import path

version_string = "accord_2016_phonedb.py v2021-03-22"

def main():
    usagetxt = " %(prog)s [-d inputfile -o outputfile]"
    parser = argparse.ArgumentParser(description='Reads Honda Accord (2016) phonedb.db "callhistory", "contact", "contactnumber" tables and outputs details to TSV', usage=usagetxt)
    parser.add_argument("-d", dest="database", action="store", required=True, help='SQLite DB filename i.e. phonedb.db')
    parser.add_argument("-o", dest="output", action="store", required=True, help='Output file basename for Tab-Separated-Value report')

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
    
    #Callhistory query
    query1 = "SELECT _id, address, phonenum, calldate, calltype FROM call_history ORDER BY calldate ASC;" 
    cursor = dbcon.cursor()
    cursor.execute(query1)
    row = cursor.fetchone()
    callentries = []
    while row:
        id = row[0]
        address = row[1] # ass-ume these fields are never null
        phonenum = row[2]
        calldate = row[3]
        calltype = row[4]
        
        timestamp = datetime.datetime.utcfromtimestamp(calldate/1000) # Ass-ume UTC millisecs since 1JAN1970
        timestr = timestamp.isoformat()
               
        # store each row returned    
        callentries.append((id, address, phonenum, timestr, calltype))
        
        row = cursor.fetchone()

    #Contacts query - note: Join on contact_id to be confirmed/validated
    query2 = """SELECT contact._id, contact.address, contact.firstName, contact.lastName, contact.phonename, contactnumber.number, contactnumber.numbertype 
    FROM contact JOIN contactnumber ON contactnumber.contact_id = contact._id ORDER BY contact._id ASC;""" 
    cursor.execute(query2)
    row = cursor.fetchone()  
    contactentries = []
    while row:
        id = row[0]
        address = row[1] # ass-ume MAC address is never null
        firstname = "NULL"
        if row[2] is not None:
            firstname = row[2] # firstname could be null
        lastname = "NULL"
        if row[3] is not None:
            lastname = row[3]  # lastname could be null
        phonename = row[4] # ass-ume phonename cannot be null (user needs to be able to select)
        contactnum = row[5] # ass-ume number cannot be null
        contacttype = row[6]
        
        # store each row returned    
        contactentries.append((id, address, firstname, lastname, phonename, contactnum, contacttype))
        
        row = cursor.fetchone()
    
    # end of queries
    cursor.close()
    dbcon.close()

    # Write TSV report for call history
    with open(args.output+"_CALLS.txt", "w") as outputcallsTSV:
        outputcallsTSV.write("_id\taddress\tphonenum\tcalldate\tcalltype\n")
        
        for entry in callentries:
            id = str(entry[0])
            address = entry[1]
            phonenum = entry[2]
            calldate = entry[3]
            calltype = str(entry[4])
           
            outputcallsTSV.write(id + "\t" + address + "\t" + phonenum + "\t" + calldate + "\t" + calltype + "\n")

    print("Processed/Wrote " + str(len(callentries)) + " CALL entries to: " + args.output+"_CALLS.txt" + "\n")
    
    # Write TSV report for contacts
    with open(args.output+"_CONTACTS.txt", "w") as outputcontaxTSV:
        outputcontaxTSV.write("_id\taddress\tfirstname\tlastname\tphonename\tcontactnum\tcontacttype\n")
        
        for entry in contactentries:
            id = str(entry[0])
            address = entry[1]
            firstname = entry[2]
            lastname = entry[3]
            phonename = entry[4]
            contactnum = entry[5]
            contacttype = str(entry[6])
            
            outputcontaxTSV.write(id + "\t" + address + "\t" + firstname + "\t" + lastname + "\t" + phonename + "\t" + contactnum + "\t" + contacttype + "\n")

    print("Processed/Wrote " + str(len(contactentries)) + " CONTACT entries to: " + args.output+"_CONTACTS.txt" + "\n")
    print("Exiting ...\n")

if __name__ == "__main__":
    main()

    
    
