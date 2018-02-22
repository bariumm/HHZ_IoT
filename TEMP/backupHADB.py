#!/usr/bin/python

# Import required modules
import sys
import os
import datetime
import sqlite3


print "Monthly backup, upload and cleaning of the Home Assistant database started"


# Stop the Home Assistant service
print "1. Stopping the Home Assistant service"
cmdStopHA = "sudo systemctl stop apache2"
os.system(cmdStopHA)
print "Successfully stopped the Home Assistant service"


# Create a timestamp and include it into the backup's name
now = datetime.datetime.now()
timestamp = now.strftime("%d%m%Y")
backupName = timestamp + "_" + "HA_DB_BACKUP.tar.gz"


# Create a Home Assistant database backup (.tar.gz)
print "2. Creating the Home Assistant database backup"
cmdBackup = "tar -zcvf " + backupName + " home-assistant_v2.db"
os.system(cmdBackup)
print("Successfully created the Home Assistant database backup")

################# JULIA ##############

print "3. Uploading the Home Assistant database backup to Dropbox"

print "Successfully uploaded the Home Assistant database backup to Dropbox"


# Delete all (!) records from the original Home Assistant database
#print "4. Deleting all current records from the original Home Assistant database"
#connection = sqlite3.connect("home-assistant_v2.db")
#cursor = connection.cursor()
#cursor.execute("""DELETE FROM states;""")
#connection.commit()
#connection.close()
#print "Successfully deleted all records from the Home Assistant database"


# Start the Home Assistant service
print "5. Starting the Home Assistant service"
cmdStartHA = "sudo systemctl start apache2"
os.system(cmdStartHA)
print "Successfully started the Home Assistant service"

