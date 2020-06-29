# This is the main business logic. In the end, this method will
# return one of four results
# 4 = Hard Fail with CC Quarantine
# 3 = Hard Fail
# 2 = Soft Fail
# 1 = Unsure/Skip
# 0 = Pass
import json

data = {}
with open('errors.json') as json_file:
    data = json.load(json_file)


def analyzestatus(validationdic):
    status = 0

    newstatus = creditcardhealth(validationdic)
    if newstatus >= status:
        status = newstatus

    newstatus = prepaidcard(validationdic)
    if newstatus >= status:
        status = newstatus

    newstatus = subscriptionstatus(validationdic)
    if newstatus >= status:
        status = newstatus

    newstatus = geocheck(validationdic)
    if newstatus >= status:
        status = newstatus

    newstatus = ipblocklistcheck(validationdic)
    if newstatus >= status:
        status = newstatus

    return status


def issuerhealth(validationdic):
    pass


def creditcardhealth(validationdic):
    # TODO Add better logic to this so that it can actually read the days, as 30 days makes the box red, even though
    #  it shouldn't
    status = 0
    boxstatus = validationdic['creditcardhealth']['Status']
    boxmessage = validationdic['creditcardhealth']['Message']
    if not boxstatus:
        status = 1
        print('[!] CC HEALTH IS QUESTIONABLE!')
    return status


def completionspeed(validationdic):
    pass


def prepaidcard(validationdic):
    status = 0
    boxstatus = validationdic['prepaidcard']['Status']
    boxmessage = validationdic['prepaidcard']['Message']
    if not boxstatus:
        status = 3
        print('[!] CC IS PREPAID!: %s' % boxmessage)
    return status


def refundcheck(validationdic):
    pass


def subscriptionstatus(validationdic):
    status = 0
    boxstatus = validationdic['subscriptionstatus']['Status']
    boxmessage = validationdic['subscriptionstatus']['Message']
    if not boxstatus:
        status = 1
        if [ele for ele in data["quarantine"] if(ele in boxmessage)]:
            print('[!] SHIFTY CARD DETECTED: %s' % boxmessage)
            return 4
        elif [ele for ele in data["hardfails"] if(ele in boxmessage)]:
            print('[!] CC HARD FAIL: %s' % boxmessage)
            return 3
        elif [ele for ele in data["softfails"] if(ele in boxmessage)]:
            print('[!] CC SOFT FAIL: %s' % boxmessage)
            return 2
        elif 'Unsubscribed at' in boxmessage:
            status = 0
    return status


def geocheck(validationdic):
    status = 0
    boxstatus = validationdic['geocheck']['Status']
    boxmessage = validationdic['geocheck']['Message']
    if not boxstatus:
        print('[!] GEOCHECK FAILED!: %s' % boxmessage)
        return 3

    return status


def ipblocklistcheck(validationdic):
    status = 0
    boxstatus = validationdic['ipblocklistcheck']['Status']
    boxmessage = validationdic['ipblocklistcheck']['Message']
    if not boxstatus:
        status = 1
        print('[!] IP BLOCKLIST CHECK FAILED!: %s' % boxmessage)
    return status
