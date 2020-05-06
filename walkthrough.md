# Creating a Real Estate Agent

## Quick Background

I moved back home to NYC and needed to find a new spot. If you don't know, the New York housing market moves very quickly. A good apartment can be on and off the market in the blink of an eye. Once you find an apartment that _is_ still available, it's basically a race to the down payment.

I wanted to minimize the amount of time between an apartment listing going up and me being aware of it, so I wrote a little Craigslist Real Estate Agent.

## Craigslist Real Estate Agent

##### What does it do?

My real estate agent checks Craigslist for housing at some configured interval and shoots me (and my soon-to-be roommates) an SMS when it thinks it might be what I'm looking for.

##### How does it do that?

Super simple: a [craigslist API](https://github.com/juliomalegria/python-craigslist) client and a [Twilio](https://www.twilio.com/) client.

*Note*: You need to create a Twilio account and get a Twilio SID, Token and Active Number for this to work.

##### How is it deployed?

I really wanted to get this running on a Raspberry Pi but instead I went with something a bit more conventional: an EC2 instance.

At a high level, I just put the code on an EC2 instance and ran it. And, it'll continue to run 'til a) I find an apartment and I stop it or b) I cancel my credit card.

##### How is it being run on an EC2 instance?

I am nowhere near proficient enough at working with AWS so this was just a way for me to get a bit more familiar with the tools it has to offer.

*What is an EC2 instance?* Simply, it's just a virtual server with compute power.

So, I created one of those. Here's exactly how I went from creating it to having it work as my real estate agent.


###### Creating an EC2 Instance

1. Create an AWS account in your region of choice
2. Navigate to `EC2` or `Launch a virtual machine`
3. Choose your AMI. If you want this to be free, choose the free one - it's basically just a Linux template. If you want something more specific, choose that.
4. Choose your instance type. Again, free is good for this project. The instance type you choose will determine how much CPU, memory, storage and networking capacity your service has.
5. Configure security groups. This will control the traffic for your instance. It's basically a set of rules that dictate what is legal inbound and outbound traffic. For us, we want to be able to SSH into our EC2 instance so let's configure `Type: SSH | Protocol: TCP | Port Range: 22 | Source: My IP`
5. Skip the rest of the configuration and click `Launch`
6. This should prompt you with a pop-up regarding a `key pair`. Do this. It will generate a public and private key combo that you'll need to connect to your instance securely. Save the `.pem` file that you are given.
7. Okay, now you have an EC2 instance running and configured. nice.

###### SSHing into your EC2 Instance

1. Check out your EC2 running instances and find the one you just created.
2. Copy / Pasta the Public DNS. example: `ec2-18-122-333-77.us-east-2.compute.amazonaws.com`
3. Go find that `.pem` you saved earlier.
4. Run `ssh -i PATH_TO_PEM.pem ec2-user@YOUR_EC2_PUBLIC_DNS_GOES_HERE`
5. Then, make that an alias on your local machine if you think you'll need to do that often.
6. Boom, now you're on the remote EC2 instance. It's probably pretty bare so we're going to need to install a few things.

###### Clone your Real Estate Agent code onto your EC2 Instance

1. You should know how to do this. You may need to install `git` though.
2. If your repo is private, then you'll also need to configure `git` with a new ssh key for your EC2 instance to read from your Git.

###### Run your app

1. Assuming you've followed the README of the repo, you should be in good shape. If you haven't read that, go read that.
2. Install `tmux` on your EC2 instance and create a new thread.
3. Run the app `python app.py` on that thread and voila!

## What's left?

Well, this only covers listings on Craigslist and only sends SMS to myself for a manual review. If this real estate agent were any good, it would learn which apartments I tend to like and then be able to respond to their listings automagically. I'm hoping this will give me enough of an edge to help me find that perfect spot and quickly.