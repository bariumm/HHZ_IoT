#!/usr/bin/python
# -*- coding: utf-8 -*-

# Import required modules
import sys
import os
import datetime
import sqlite3
import dropbox

# Definition of functions for uploading the database backup to Dropbox
class TransferData:
    def __init__(self, access_token):
        self.access_token = access_token

    def upload_file(self, file_from, file_to):
        """upload a single file <150MB to Dropbox using API v2"""
        dbx = dropbox.Dropbox(self.access_token)
        with open(file_from, 'rb') as f:
            print(dbx.files_upload(f.read(), file_to))

    def upload_large_file(self, file_from, file_to, file_size, chunk_size):
        """upload a file >150MB to Dropbox using API v2"""
        dbx = dropbox.Dropbox(self.access_token)
        with open(file_from, 'rb') as f:
            upload_session_start_result = dbx.files_upload_session_start(f.read(chunk_size))
            cursor = dropbox.files.UploadSessionCursor(session_id=upload_session_start_result.session_id,
                                               offset=f.tell())
            commit = dropbox.files.CommitInfo(path=file_to, mute=False)
            while f.tell() < file_size:
                if ((file_size - f.tell()) <= chunk_size):
                    print(dbx.files_upload_session_finish(f.read(chunk_size), cursor, commit))
                else:
                    dbx.files_upload_session_append(f.read(chunk_size), cursor.session_id, cursor.offset)
                    cursor.offset = f.tell()

print "START: Regular backup, upload and cleaning of the Home Assistant DB"

# Stop the Home Assistant service
print "1. Stopping the Home Assistant service"
#cmdStopHA = "sudo systemctl stop home-assistant@homeassistant.service"
#os.system(cmdStopHA)
print "Successfully stopped the Home Assistant service"

# Create a timestamp and include it into the backup's name
now = datetime.datetime.now()
timestamp = now.strftime("%d%m%Y-%H%M%S")
backupName = timestamp + "_" + "HA_DB_BACKUP.tar.gz"

# Create a Home Assistant database backup (.tar.gz)
print "2. Creating the Home Assistant DB backup"
cmdBackup = "tar -zcvf " + backupName + " home-assistant_v2.db"
os.system(cmdBackup)
print("Successfully created the Home Assistant DB backup")

# Upload the Home Assistant database backup to Dropbox
print "3. Uploading the Home Assistant DB backup to Dropbox"

access_token = 'WuaHcCL6RXMAAAAAAAAAbvBKI2e5scMa8Mp0V0npoBItoU8bUsdXBaDTY5uYfi-u'
transferData = TransferData(access_token)

file_from = backupName
file_to = '/Test/' + backupName  # The full path to upload the file to, including the file name

file_size = os.path.getsize(file_from)
chunk_size = 134217728
    
if file_size <= chunk_size:
    transferData.upload_file(file_from, file_to)
else:
    transferData.upload_large_file(file_from, file_to, file_size, chunk_size)

print "Successfully uploaded the Home Assistant DB backup to Dropbox"

# Delete all (!) records from the original Home Assistant database and optimize its space consumption
print "4. Deleting all records from the original Home Assistant DB and optimizing its space consumption"
connection = sqlite3.connect("home-assistant_v2.db")
cursor = connection.cursor()
cursor.execute("""DELETE FROM states;""")
connection.commit()
print "Successfully deleted all records from the Home Assistant DB"
cursor.execute("""VACUUM;""")
connection.commit()
print "Successfully optimized the space consumption of the Home Assistant DB"
connection.close()
print "Successfully finished all database operations"

# Start the Home Assistant service
print "5. Starting the Home Assistant service"
#cmdStartHA = "sudo systemctl start home-assistant@homeassistant.service"
#os.system(cmdStartHA)
print "Successfully started the Home Assistant service"

print "END: Successfully finished the regular backup, upload and cleaning of the Home Assistant DB"
