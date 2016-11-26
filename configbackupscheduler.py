#!/usr/bin/env python

import sys
import os
import time
import datetime
import smtplib
import string
import re

def main():

    hosts_to_backup = []
    message = ""

    for root, dirs, files in os.walk("/nagios/services/", topdown=False):
        for name in files:
            try:
                if name.split(".")[1] == "cfg":
                    fpath = os.path.join(root, name)
                    #print fpath
                    f = open(fpath)
                    for line in f:
                        if "Configbackup\n" in line:
                        #if re.search(r"\bConfigbackup\n", line): # re um genau nach "Configbackup" zu suchen
                        #if "Configbackup" in line.split(): # split um genau nach "Configbackup" zu suchen
                            hosts_to_backup.append(name.replace(".cfg",""))
                    f.close()
            except:
                pass

    # sort list
    hosts_to_backup = sorted(hosts_to_backup)
    # anzahl der hosts to backup
    hosts_count = len(hosts_to_backup)

    d = datetime.date.today()
    t = datetime.time(23, 00)

    dt = datetime.datetime.combine(d, t)

    s = 0
    for host in hosts_to_backup:
        dt2 = dt + datetime.timedelta(seconds=s)
        s += 5

        unix_time = time.mktime(dt2.timetuple())

        os.system("echo \"['date +%s'] SCHEDULE_SVC_CHECK;" + host + ";Configbackup;" + str(unix_time) + "\" >/omd/sites/nws/tmp/run/nagios.cmd")
        #print "echo \"['date +%s'] SCHEDULE_SVC_CHECK;" + host + ";Configbackup;" + str(unix_time) + "\" >/omd/sites/nws/tmp/run/nagios.cmd"
        #print "echo \"['date +%s'] SCHEDULE_SVC_CHECK;" + host + ";Configbackup;'date -d \"" + str(dt2) + "\" +%s'\" >/omd/sites/nws/tmp/run/nagios.cmd"
        #print "echo \"['date +%s'] SCHEDULE_SVC_CHECK;" + host + ";Configbackup;date -d \"2015-09-25 23:58:00\" +%s\" >/omd/sites/nws/tmp/run/nagios.cmd"

        message += "echo \"['date +%s'] SCHEDULE_SVC_CHECK;" + host + ";Configbackup;'date -d \"" + str(dt2) + "\" +%s'\" >/omd/sites/nws/tmp/run/nagios.cmd\n"

    headline = "Scheduled configbackups: " + str(hosts_count) + "\n\n"

    BODY = string.join((
            "From: nagios@mydomain.com",
            "To: noc@mydomain.com",
            "Subject: Configbackup Scheduler Report" ,
            "",
            headline + message
            ), "\r\n")
    server = smtplib.SMTP("MY-SMTP-SERVER")
    server.sendmail("nagios@mydomain.com", ["noc@mydomain.com"], BODY)
    server.quit()

if __name__ == '__main__':
    main()
