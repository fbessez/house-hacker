# house-hacker

So, before you ask... no, this is not for actual [house hacking](https://www.biggerpockets.com/blog/2013-11-02-hack-housing-get-paid-live-free) but that would be neat. maybe that's my next side project.

This script does a few things:
- Checks Craigslist for Housing that meet the given filters
- For each of those qualifying craigslist posts, send an SMS via Twilio to those interested.
- If you see the same listing twice, don't send the SMS.

Super simple.

## Getting Started

#### Twilio
- Create a free account on [Twilio](https://www.twilio.com/console)
- Create a new project to earn an TWILIO\_SID, TWILIO\_TOKEN and an Active Number
- Save that information in your `config.yml`
- If you want to stay on the free trial, then you need to register verified numbers that can _receive_ these SMS. [Verified Caller IDs](https://www.twilio.com/console/phone-numbers/verified)

#### Running locally:
- Download `python3`
- Run `redis` locally
- Download the required packages:
`pip install -r requirements.txt`
- Fill out your `config.yml` appropriately
- `python3 app.py`

**Note**: This will run for as long as you leave it running on your local machine. But, what if we want to run this remotely so that it doesn't eat up your computer battery and you can close your computer in the night?

#### Running remotely with AWS:

- Create an EC2 instance
- SSH into your EC2 instance
- Clone this github repo to your EC2 instance
- SCP your personal `config.yml` file from your local computer to the repo on your EC2 instance
- Install all required packages via `pip install -r requirements.txt`
- Run `redis-server` on EC2 instance and daemonize it (so it's always running)
- Install `tmux`, our favorite terminal multiplexer
- Hop into a new `tmux` window, and run the app with `python3 app.py`
- boom.
