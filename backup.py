#!/usr/bin/python3

import sys 
import os
import pathlib
import shutil
import smtplib
from backupcfg import jobs, backupDir, backupLog, smtp
from datetime import datetime

def writeLogMessage(logMessage, dateTimeStamp, isSuccess):
    try:
        file = open(backupLog, "a")
        
        if isSuccess:
            file.write(f"SUCCESS {dateTimeStamp} {logMessage}\n")
        else:
            file.write(f"FAILURE {dateTimeStamp} {logMessage}\n")
            
        file.close()
        
    except FileNotFoundError:
        print("ERROR: File does not exist.")
    except IOError:
        print("ERROR: File is not accessible.")
    
def errorHandler(errorMessage, dateTimeStamp):
    print(errorMessage)
    writeLogMessage(errorMessage, dateTimeStamp, False)
    sendEmail(errorMessage)

# append all error messages to email and send
def sendEmail(message):

    email = 'To: ' + smtp["recipient"] + '\n' + 'From: ' + smtp["sender"] + '\n' + 'Subject: Backup Error\n\n' + message + '\n'

    # connect to email server and send email
    try:
        smtp_server = smtplib.SMTP(smtp["server"], smtp["port"])
        smtp_server.ehlo()
        smtp_server.starttls()
        smtp_server.ehlo()
        smtp_server.login(smtp["user"], smtp["password"])
        smtp_server.sendmail(smtp["sender"], smtp["recipient"], email)
        smtp_server.close()
    except Exception as e:
        print("ERROR: An error occurred.")    

def main():
    dateTimeStamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    argCount = len(sys.argv)
    if argCount < 2:
        errorHandler("ERROR: job not specified", dateTimeStamp)
    else:
        for job in sys.argv[1:]:
            if not job in jobs:
                errorHandler(f"ERROR: job {job} does not exist", dateTimeStamp)
            else:
                source = jobs[job]
                if not os.path.exists(source):
                    errorHandler(f"ERROR: source {source} does not exist", dateTimeStamp)
                else:
                    destination = backupDir
                    if not os.path.exists(destination):
                        errorHandler(f"ERROR: destination {destination} does not exist", dateTimeStamp)
                    else:
                        srcPath = pathlib.PurePath(source)
                        dstLoc = destination + "/" + srcPath.name + "-" + dateTimeStamp
                        if pathlib.Path(source).is_dir():
                            shutil.copytree(source, dstLoc)
                        else:
                            shutil.copy2(source, dstLoc)
                            
                        writeLogMessage(f"Backed up {source} to {dstLoc}", dateTimeStamp, True)
                        

if __name__ == "__main__":
    main()
