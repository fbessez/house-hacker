import os
from yaml         import load as yaml_load, FullLoader
from time         import sleep
from pytz         import timezone
from redis        import Redis
from craigslist   import CraigslistHousing
from twilio.rest  import Client as TwilioClient
from attrdict     import AttrDict
from datetime     import datetime, timedelta

config = open("config.yml", "r")
config = yaml_load(config, Loader=FullLoader)
config = AttrDict(config)

redisClient  = Redis(host=os.environ.get('REDIS_HOST', config.redis.host),
                     port=os.environ.get('REDIS_PORT', config.redis.port),
                     db=0)
clistClient  = CraigslistHousing(site=config.craigslist.site,
                                 area=config.craigslist.area,
                                 filters=config.craigslist.filters)
twilioClient = TwilioClient(config.twilio.sid,
                            config.twilio.token)

def getApartmentOptions():
    results = []

    try:
        results = clistClient.get_results(sort_by=config.craigslist.search.sort_by,
                                          limit=config.craigslist.search.limit)
    except:
        print('Failed to fetch posts from Craigslist.')

    return results

def parseApartment(apartment):
    if redisClient.sismember(config.redis.key_names.seen, apartment['id']):
        return [None, None]

    post_id   = apartment['id']
    post_name = apartment['name']
    post_cost = apartment['price']
    post_loc  = apartment['where']
    post_time = apartment['datetime']
    post_url  = apartment['url']

    message  = '-'
    message += '\n\n' + post_name + '\n\n'
    message += 'price: %s\n\n'  % post_cost
    message += 'location: %s\n\n'    % post_loc
    message += 'posted: %s\n\n' % post_time
    message += post_url

    return [post_id, message]

def sendSms(to_number, apartment_id, message_body):
    if not to_number or not apartment_id:
        return
    try:
        print("Sending SMS to %s for ID: %s" % (to_number, apartment_id))
        twilioClient.messages.create(to=to_number,
                                     from_=config.twilio.from_number,
                                     body=message_body)

        redisClient.sadd(config.redis.key_names.seen, apartment_id)
    except:
        print("SMS delivery failed to %s for ID: %s" % (to_number, apartment_id))

def getCurrentTime():
    tz = timezone(config.timing.timezone)
    return datetime.now(tz)

def getCurrentHour():
    return getCurrentTime().hour

def isBlackoutHours():
    blackout_start, blackout_end = config.timing.blackout_start, config.timing.blackout_end
    currentHour = getCurrentHour()

    return currentHour >= blackout_start or currentHour < blackout_end

def hoursToSleep():
    HOURS_IN_DAY = 24

    currentHour = getCurrentHour()
    if currentHour >= config.timing.blackout_start:
        return HOURS_IN_DAY - currentHour + config.timing.blackout_end
    else:
        return config.timing.blackout_end - currentHour

def waitIntervalTime():
    sleep_time_in_seconds = config.timing.interval * 60 * 60
    sleeping_til = getCurrentTime() + timedelta(0, sleep_time_in_seconds)
    print("sleeping til %s..." % sleeping_til.strftime("%H:%M:%S"))
    sleep(sleep_time_in_seconds)

def main():
    while True:
        if isBlackoutHours():
            print("We are in a blackour hour!")
            print("Sleeping for %d hours..." % hoursToSleep())

            sleep(hoursToSleep() * 60 * 60) # seconds
            continue

        apartments = getApartmentOptions()
        for apartment in apartments:
            apartment_id, message_body = parseApartment(apartment)

            contacts = config.twilio.contacts
            for contact in config.twilio.contacts:
                number = config.twilio.contacts[contact]
                sendSms(number, apartment_id, message_body)

        waitIntervalTime()

main()
