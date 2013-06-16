"""
Flash And Intro Detection Bot(FAIDBot) for /r/Random_Acts_Of_Amazon.
This Reddit bot scrapes the /r/raoa subreddit for new [Intro] posts and flash contests.
When an [Intro] is found, a comment welcome message is posted to the submission.
When a flash contest is found, a message with the details of the submission is posted
to the console.


CHANGELOG:
Version 1.1.2
-Fixed an issue where some title combos made the bot post a comment to the wrong thread
(e.g. [intro][contest] flash would make it skip to the next submission)
-Extended rand from 60 to 90 and added 2 more welcome messages
-Added additional output info to the console on submission detection

Version 1.1.1
-Fixed an issue where the bot crashed due to server lag or thread deletion(48 continuous hours of running
with no problems as of last trial).

Version 1.1.0
-Added detection of flash contests(but still wrongly detects [gifted] flash submissions

Version 1.0.1
-Added multiple welcome messages that are randomly selected
-Added output to the console on submission detection

Version 1.0.0
-Implemented [intro] submission detection

KNOWN ISSUES:
-Bot still wrongly detects a flash submission as a contest when tagged under something else e.g. [Gifted]
-Certain title combos (e.g. [intro][contest] flash) throw the bot off and it believes that the
subsequent submission is actually the flash contest because of the way the IF block logic
is setup.
-Not exactly an issue, but the bot runs continuously and must be manually stopped.
"""

import time
import datetime
import praw
import random


#User_ID
user_agent = ('Flash and Intro Detection Bot(FAIDBot)(v1.1.2) by /u/EpimetheusIncarnate'
              'github.com/ezfuzion/FAIDBot')
r = praw.Reddit(user_agent=user_agent)

#account that the agent logs in with
r.login('your_reddit_username_here', 'your_reddit_password_here')
already_done = []

#consecutive string of characters that the bot looks for
intro_keyword = '[intro]'
flash_keyword = 'flash'
match_found = False
flash_found = False

#Notify the user that the bot is starting
print "RAOA Welcoming Bot started."
while True:
    subreddit = r.get_subreddit('Random_Acts_Of_Amazon')
    

    #Fails if subreddit.get_new() times out. Wait for a bit and try again
    try:
        #Loop through the top 10 posts in 'new'
        for submission in subreddit.get_new(limit=10):
            title = submission.title
            
            #If the submission title is equal to the search criteria then do the following
            #as long as the post hasn't already been catalogued as found.
            #Otherwise match_found remains false
            if title.lower().find(intro_keyword) != -1 and submission.id not in already_done:
                match_found = True
            if title.lower().find(flash_keyword) != -1 and submission.id not in already_done:
                flash_found = True



            #The following if block must come first otherwise the comment has the potential
            #to be posted in the wrong submission(e.g. a post with [intro] flash).
            #If there's a match then comment on the post
            if submission.id not in already_done and match_found:
                #Randomly select from a group of welcome messages
                rand = random.randrange(0, 90)

                #Fails if the comment could not be posted(e.g. the post was deleted)
                try:
                    if rand < 15:
                        submission.add_comment('Hi, welcome to raoa!')
                    elif rand >= 15 and rand < 30:
                        submission.add_comment('Welcome to raoa!')
                    elif rand >= 30 and rand < 45:
                        submission.add_comment('Hey, welcome to raoa!')
                    elif rand >= 45 and rand < 60:
                        submission.add_comment('Welcome! :)')
                    elif rand >= 60 and rand < 75:
                        submission.add_comment('Hi and welcome!')
                    else:
                        submission.add_comment('Hiya! Welcome to raoa!')
                except:
                    ts = time.time()
                    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                    print "ERROR posting comment @ %s" % st
                    print "...continuing."
                    continue

                #Place an alert in the console
                ts = time.time()
                st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                print "[Intro] posted! @ %s" % st
                print "Post title: %s" % submission.title
                #Add the submission to the list
                already_done.append(submission.id)
                match_found = False



            #If there's a flash contest match then alert to the console
            if submission.id not in already_done and flash_found:
                ts = time.time()
                st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                print "***"
                print "FLASH CONTEST FOUND @ %s" % st
                print "Author: %s" % submission.author
                print "Title: %s" % submission.title
                print "Link: %s" % submission.short_link
                print "---------------"
                print "Info: %s" % submission.selftext
                print "***"
                #add the submission to the list
                already_done.append(submission.id)
                flash_found = False

    except:
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        print "NETWORK TIMEOUT @ %s" % st
        continue
        
    #Search the new entries every 31 seconds since the page is
    #cached for 30 seconds there's no need to call a request more often than that
    time.sleep(31)

    #Set timekeeping variables for output to the console
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    
    #Let the user know that the bot is still running
    print "RAOA [Intro] bot is running. (%s)" % st

