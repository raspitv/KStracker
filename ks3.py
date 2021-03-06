#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
from urllib2 import Request, urlopen, URLError
from time import sleep          # we need sleep for a delay between readings
pc='%'                          # I find defining % as a variable avoids confusion

# Here we define the urls of the KS campaigns we want to track as a list
urls =['https://www.kickstarter.com/projects/raspitv/raspio-duino-affordable-arduino-programming-on-ras',
       'https://www.kickstarter.com/projects/pimoroni/flotilla-for-raspberry-pi-making-for-everyone']

def scan(someurl):                     # we've put all the page scanning bits into a function
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
        print '\033[34m\033[1m' + project_name + '\033[0m' # bold and blue title
        for line in the_page:
            if 'data-duration' in line:  # line 457
                time_left = float(line.split('"')[5])
                campaign_duration = float(line.split('"')[1])
                hours_into_campaign = (24 * campaign_duration) - time_left
                if time_left >= 24:
                    time_left_unit = "days"
                    time_left = str(int(time_left / 24))
                else:
                    time_left_unit = "hours"
                    time_left = str(time_left)
            if 'data-backers-count' in line:
                backers = int(line.split('"')[3])      
            if 'data-goal' in line:       # line 449
                words = line.split(" ")
                for word in words:
                    if 'data-goal' in word:
                        target = word.split('"')
                            # bold and yellow for labels, bold and white for figures
                        print '\033[33m\033[1mtarget:\033[0m \033[1m\033[37m£%.2f\033[0m' % float(target[1])
                    if 'data-percent-raised' in word:
                        percent = word.split('"')
                        print '\033[33m\033[1mpercentage raised:\033[0m \033[1m\033[37m%.2f%s\033[0m' % ((float(percent[1]) * 100) , pc)
                    if 'data-pledged' in word:
                        amount_raised = word.split('"')
                        print '\033[33m\033[1mTotal so far:\033[0m \033[1m\033[37m£%.2f\033[0m' % float(amount_raised[1])
        print '\033[33m\033[1mTime left:\033[0m \033[1m\033[37m%s %s\033[0m' % (time_left, time_left_unit)

        amount_per_hour = float(amount_raised[1]) / hours_into_campaign
        print '\033[33m\033[1mBackers:\033[0m \033[1m\033[37m%d \033[0m' % backers
        print '\033[33m\033[1m£/hr:\033[0m \033[1m\033[37m£%.2f \033[0m \n' % amount_per_hour


while True:          # continuous loop which calls our function for each URL we define
    for url in urls:
        scan(url)
        sleep(15)
