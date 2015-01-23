#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# cli arguments: nolog nodis noloop
from urllib2 import Request, urlopen, URLError
from time import sleep          # we need sleep for a delay between readings
import sys                      # we use sys for command line arguments
                                # insert the path to your log file 
file_path = ''                  # without it's name e.g. /home/pi/
                                # not really needed unless running from cron

# Here we list the urls of the KS campaigns we want to track
urls =['https://www.kickstarter.com/projects/pimoroni/flotilla-for-raspberry-pi-making-for-everyone',
       'https://www.kickstarter.com/projects/ryanteckltd/raspberry-pi-debug-clip',
       'https://www.kickstarter.com/projects/955730101/protocam-raspberry-pi-a-b-camera-module-add-on-boa']

if 'nolog' in sys.argv:
    logging_enabled = 0 
else:
    logging_enabled = 1         # change to 0 to switch off logging
if 'nodis' in sys.argv:
    display_enabled = 0
else:
    display_enabled = 1         # change to 0 to switch off screen output
if 'noloop' in sys.argv:
    loop_forever = 0            
else:
    loop_forever = 1            # change to 0 to just scan once and not loop

pc='%'                          # defining % as a variable avoids confusion

def log(project_name, target, percent, amount_raised, campaign_duration, 
        time_left, time_left_unit, backers, amount_per_hour, hours_into_campaign):
    # convert non-string variables to strings for writing to file
    percent = "%.2f" % percent
    hours_into_campaign = "%.3f" % hours_into_campaign
    if len(str(campaign_duration)) > 4:                   # restrict length stored
        campaign_duration = "{:.4f}".format(campaign_duration)
    else:
        campaign_duration = str(campaign_duration)
    backers = str(backers)
    amount_per_hour = "%.2f" % amount_per_hour
    logfile = file_path + project_name + ".txt"

    write_list = [target, percent, amount_raised, campaign_duration, time_left, 
                  time_left_unit, backers, amount_per_hour, hours_into_campaign]
    write_string = ','.join(write_list) + '\n'
    log_data = open(logfile, 'a') # open file for appending
    log_data.write(write_string)
    log_data.close()     

def scan(someurl):                # page scanning function
    global logging_enabled
    req = Request(someurl)
    try:
        response = urlopen(req)
    except URLError as e:
        if hasattr(e, 'reason'):
            print 'We failed to reach a server.'
            print 'Reason: ', e.reason
        elif hasattr(e, 'code'):
            print 'The server couldn\'t fulfill the request.'
            print 'Error code: ', e.code
    else:
        the_page = response.readlines()
        project_name = someurl.split('/')[5].split('-')[0] # take project name from URL
        for line in the_page:
            if 'data-duration' in line:  # line 457
                time_left = float(line.split('"')[5])
                campaign_duration = float(line.split('"')[1])
                hours_into_campaign = (24 * campaign_duration) - time_left
                if time_left >= 72:
                    time_left_unit = "days"
                    time_left = str(int(time_left / 24))
                elif time_left >= 1:
                    time_left_unit = "hours"
                    time_left = str(int(time_left))
                elif 0 < time_left < 1:
                    time_left_unit = "minutes"
                    time_left = str(int(time_left * 60))
                else:
                    time_left_unit = ""
                    logging_enabled = 0          # stop logging if campaign finished
            if 'data-backers-count' in line:
                backers = int(line.split('"')[3])      
            if 'data-goal' in line:       # line 449
                words = line.split(" ")
                for word in words:
                    if 'data-goal' in word:
                        target = word.split('"')
                            # bold and yellow for labels, bold and white for figures
                    if 'data-percent-raised' in word:
                        percent = word.split('"')
                    if 'data-pledged' in word:
                        amount_raised = word.split('"')
            if 'project_currency_code' in line: 
                project_currency = line.split('"')[1]
                project_currency = project_currency.split(' ')[1]
                if project_currency == 'usd':
                    project_currency = '$'
                elif project_currency == 'gbp':
                    project_currency = '£'
                else:
                    project_currency = '£' # we can add more currencies as needed

        amount_per_hour = float(amount_raised[1]) / hours_into_campaign

        if display_enabled:
            print '\033[34m\033[1m' + project_name + '\033[0m' # bold and blue title
            print '\033[33m\033[1mtarget:\033[0m \033[1m\033[37m%s%.2f\033[0m' % (project_currency,float(target[1]))        
            print '\033[33m\033[1mpercentage raised:\033[0m \033[1m\033[37m%.2f%s\033[0m' % ((float(percent[1]) * 100) , pc)
            print '\033[33m\033[1mTotal so far:\033[0m \033[1m\033[37m%s%.2f\033[0m' % (project_currency, float(amount_raised[1]))   
            print '\033[33m\033[1mTime left:\033[0m \033[1m\033[37m%s %s\033[0m' % (time_left, time_left_unit)
            print '\033[33m\033[1mBackers:\033[0m \033[1m\033[37m%d \033[0m' % backers
            print '\033[33m\033[1m%s/hr:\033[0m \033[1m\033[37m%s%.2f \033[0m \n' % (project_currency, project_currency, amount_per_hour)

        if (logging_enabled and counter % log_interval == 0):
            log(project_name, target[1], (float(percent[1]) * 100), amount_raised[1], 
                campaign_duration, time_left, time_left_unit, backers, amount_per_hour,
                hours_into_campaign)
counter = 0
log_interval = 10
while True:          # continuous loop scans each URL we define
    for url in urls:
        scan(url)
        sleep(15)
    counter += 1     # to be able to limit logging frequency
    if not loop_forever:
        break

# Instructions for ks4.py
# To use this script, edit lines 12-13 to include the KS URLs you want to track,
# save, then type...
# python ks4.py 

# By default, it will display on-screen output, loop continuously until you
# CTRL+C out of it (or it errors out), and log every tenth cycle to a file

# python ks4.py [nolog | nodis | noloop]
# You can add nolog and/or nodis and/or noloop to the command 
# 
# These will disable logging | display | looping respectively
# You can use any, all or none of the above, but if you use...
# nolog nodis noloop, the program won't do anything with the KS page it scans.

# If you want to run it from cron, you'll need to add the file_path (line 8)
# e.g. /home/pi (but not the filename itself, just the path)
