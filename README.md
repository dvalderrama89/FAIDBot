FAIDBot
=======

Reddot bot that monitors /r/Random_Acts_Of_Amazon for new [Intro] submissions and flash contests.
When an [Intro] is found, a comment welcome message is posted to the submission.
When a flash contest is found, a message with the details of the submission is posted
to the console.

Getting Started
----------------

Replace the fields in r.login() on line 53 in raoa_monitor.py with the login credentials of the Reddit account you wish to use as a commenter on any [Intro] submissions posted. Then run the bot with:

        $ python raoa_monitor.py 
        
Requires PRAW (Python Reddit API Wrapper) installation to work correctly.
