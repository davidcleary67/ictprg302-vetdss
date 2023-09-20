#!/usr/bin/python3

jobs = {"job1" : "/home/ec2-user/environment/ictprg302-vetdss/test/file1",
        "job2" : "/home/ec2-user/environment/ictprg302-vetdss/test/dir1",
        "job3" : "/home/ec2-user/environment/ictprg302-vetdss/test/dir2"}

        
backupDir = "/home/ec2-user/environment/ictprg302-vetdss/backups"

backupLog = "/home/ec2-user/environment/ictprg302-vetdss/backup.log"

smtp = {"sender": "dcleary@sunitafe.edu.au",
        "recipient": "davidcgcleary@gmail.com",
        "server": "smtp.gmail.com",
        "port": 587,
        "user": "davidcgcleary@gmail.com", # need to specify a gmail email address with an app password setup
        "password": "lemkllikuhmpdoog"}   # need a gmail app password     