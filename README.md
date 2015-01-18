# KStracker
Kickstarter tracker
This is an amended version of a KS tracker that I wrote back in October 2014
http://raspi.tv/2014/programming-a-kickstarter-tracker-in-python-part-2

It's been updated because some of the 'on-page' stuff it scrapes data from has changed on KickStarter.

I also added a new feature to include an accurate £/hr raised track.

It's a fun project. A lot more could be done...

*Logging of stats
*Graphing
*Tweets
*Push notifications

It will probably break again at some point if KS change their on-page information, but that's OK. 
We'll fix it again

ks3.py is a basic kickstarter tracker that shows a display on the terminal window

ks4.py added capability to log data in a text file, which takes its name from the first word of the unique part of the KS URL.

Data is stored...
target, percent, amount_raised, campaign_duration, time_left,time_left_unit, backers, amount_per_hour, hours_into_campaign

32768.0,114.03,37366.0,30.0,28,days,442,1134.59,32.934

The idea here is to allow more detailed analysis of the progress of a KS campaign. Sites like Kicktraq don't give much granularity, just daily data. As a person who has run KS campaigns "I want MORE data."

Still hoping to add graphing etc at some point.
