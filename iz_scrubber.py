import os
import sys
import json

from selenium import webdriver
import time
from datetime import datetime, timedelta
from tabulate import tabulate
import helpers

# Define variables...
validationboxeslist = []
validationtable = ["Box", "Status"]
validationdic = {}
accountvalid = True
running = True
totalriskscore = 0
customersscrubbed = 0
now = datetime.now()
timestarted = now
timestartedformated = now.strftime("%H:%M:%S")
timescrubbed = now.strftime("%H:%M:%S")

# Updates the current risk score for the selected customer


def updateriskscore():
    global totalriskscore
    try:
        risktext = driver.find_element_by_xpath(
            "//*[@id='master-content']/div[2]/div[2]/div[6]").text
        totalriskscore = int(risktext[1:])
        print("[*] Risk Score: " + str(totalriskscore))
    except:
        try:
            risktext = driver.find_element_by_xpath(
                "//*[@id='master-content']/div[2]/div[2]/div[2]").text
            totalriskscore = int(risktext[1:])
        except:
            skipbutton()

# Just navigates to the scrubbing, and inputs the corrects dates based on today's date.


def navigatetoscrubbingwindow():
    # Find current month
    fda = timedelta(days=5)
    today = datetime.today()
    first = today.replace(day=1)
    lastMonth = first - timedelta(days=1)
    todayrange = today - fda
    datem = str(datetime(todayrange.year, lastMonth.month, 1))
    curmonth = datem[0:10]
    print("[?] Current month: %r" % (curmonth))
    # If you wanna put in a certain date:
    # curmonth = "2020-05-31"

    # Find date five days ago
    fivedaysagodate = str(today - fda)
    fivedaysagodate = fivedaysagodate[0:10]
    print("[?] Date five days go: %r" % (fivedaysagodate))
    # If you wanna put in a certain date:
    # fivedaysagodate = "2020-05-31"

    filterURL = "https://www.internetzoo.dk/support/members/signup-screening?email=&name=&partner=&microsite=&bin=&last_4_digits=&address=&date_from=%s&date_to=%s&concept=&screening_status=pending&sortby=id-asc" % (
        curmonth, fivedaysagodate)
    return filterURL

# Goes through each of the 8 validation boxes, takes the data from each one, and inputs it into two dictionaries:
# 'validationboxeslist' is only used to later give a visual representation in the console of the status of each validation box
# 'validationdic' is a dictionary filled with the current customers information, which will later be passed into the
# 'helpers.py' file to be processed.


def validationboxescheck():
    global validationdic
    global validationboxeslist
    validationboxeslist = []
    validationdic = {}

    customerID = driver.find_element_by_xpath(
        "//*[@id='master-content']/table/tbody/tr[2]/td[1]/a")
    validationboxeslist.append(["CustomerID", customerID.text])

    issuerhealth = str(
        driver.find_element_by_xpath("//*[@id='master-content']/div[2]/div[1]/div/div[1]/div/h5/i").get_attribute(
            "class"))
    status = validationcheck(issuerhealth)
    validationboxeslist.append(["issuerhealth", status])
    validationdic.update({'issuerhealth': {'Status': status, 'Message': driver.find_element_by_xpath(
        "//*[@id='master-content']/div[2]/div[1]/div/div[1]/div/dl/dd").text}})
    # print("issuerhealth: " + issuerhealth)

    creditcardhealth = str(
        driver.find_element_by_xpath("//*[@id='master-content']/div[2]/div[1]/div/div[2]/div/h5/i").get_attribute(
            "class"))
    status = validationcheck(creditcardhealth)
    validationboxeslist.append(["creditcardhealth", status])
    validationdic.update({'creditcardhealth': {'Status': status, 'Message': driver.find_element_by_xpath(
        "//*[@id='master-content']/div[2]/div[1]/div/div[2]/div/dl/dd").text}})
    # print("creditcardhealth: " + creditcardhealth)

    completionspeed = str(
        driver.find_element_by_xpath("//*[@id='master-content']/div[2]/div[1]/div/div[3]/div/h5/i").get_attribute(
            "class"))
    status = validationcheck(completionspeed)
    validationboxeslist.append(["completionspeed", status])
    validationdic.update({'completionspeed': {'Status': status, 'Message': driver.find_element_by_xpath(
        "//*[@id='master-content']/div[2]/div[1]/div/div[3]/div/dl/dd").text}})
    # print("completionspeed: " + completionspeed)

    prepaidcard = str(
        driver.find_element_by_xpath("//*[@id='master-content']/div[2]/div[1]/div/div[4]/div/h5/i").get_attribute(
            "class"))
    status = validationcheck(prepaidcard)
    validationboxeslist.append(["prepaidcard", status])
    validationdic.update({'prepaidcard': {'Status': status, 'Message': driver.find_element_by_xpath(
        "//*[@id='master-content']/div[2]/div[1]/div/div[4]/div/dl/dd").text}})
    # print("prepaidcard: " + prepaidcard)

    refundcheck = str(
        driver.find_element_by_xpath("//*[@id='master-content']/div[2]/div[1]/div/div[5]/div/h5/i").get_attribute(
            "class"))
    status = validationcheck(refundcheck)
    validationboxeslist.append(["refundcheck", status])
    validationdic.update({'refundcheck': {'Status': status, 'Message': driver.find_element_by_xpath(
        "//*[@id='master-content']/div[2]/div[1]/div/div[5]/div/dl/dd").text}})
    # print("refundcheck: " + refundcheck)

    subscriptionstatus = str(
        driver.find_element_by_xpath("//*[@id='master-content']/div[2]/div[1]/div/div[6]/div/h5/i").get_attribute(
            "class"))
    status = validationcheck(subscriptionstatus)
    validationboxeslist.append(["subscriptionstatus", status])
    validationdic.update({'subscriptionstatus': {'Status': status, 'Message': driver.find_element_by_xpath(
        "//*[@id='master-content']/div[2]/div[1]/div/div[6]/div/dl/dd").text}})
    # print("subscriptionstatus: " + subscriptionstatus)

    geocheck = str(
        driver.find_element_by_xpath("//*[@id='master-content']/div[2]/div[1]/div/div[7]/div/h5/i").get_attribute(
            "class"))
    status = validationcheck(geocheck)
    validationboxeslist.append(["geocheck", status])
    validationdic.update({'geocheck': {'Status': status, 'Message': driver.find_element_by_xpath(
        "//*[@id='master-content']/div[2]/div[1]/div/div[7]/div/dl/dd").text}})
    # print("geocheck: " + geocheck)

    ipblocklistcheck = str(
        driver.find_element_by_xpath("//*[@id='master-content']/div[2]/div[1]/div/div[8]/div/h5/i").get_attribute(
            "class"))
    status = validationcheck(ipblocklistcheck)
    validationboxeslist.append(["ipblocklistcheck", status])
    validationdic.update({'ipblocklistcheck': {'Status': status, 'Message': driver.find_element_by_xpath(
        "//*[@id='master-content']/div[2]/div[1]/div/div[8]/div/dl/dd").text}})
    # print("ipblocklistcheck: " + ipblocklistcheck)

# Checks if a validation box is red or green, ergo checking the status


def validationcheck(value):
    if value == 'fa fa-check':
        return True
    else:
        return False

# clicks the approve button.


def approvebutton():
    driver.find_element_by_xpath(
        "//*[@id='master-content']/div[3]/a[1]").click()

# clicks the deny button.

# TODO Need to incorporate the block function to IP and Stolen CC


def denybutton():
    driver.find_element_by_xpath(
        "//*[@id='master-content']/div[3]/a[2]").click()
    time.sleep(0.3)
    driver.find_element_by_xpath(
        "//*[@id='decline-modal']/div/form/div/div[3]/button[2]").click()

# clicks the skip button.


def skipbutton():
    driver.find_element_by_xpath(
        "//*[@id='master-content']/div[3]/a[3]").click()

# FOR TESTING. If you comment out the 'button' definition calls in the 'verdict(number)' definition, and uncomment the
# userinput() in the 'while(running)' loop. Then you can manually input approves and fails with 1,2,3,4


def userinput():
    # raw_input returns the empty string for "enter"
    print('\n[!] Please enter one of the following numbers:'
          '\n    1 = Approve'
          '\n    2 = Deny'
          '\n    3 = Skip'
          '\n    4 = Exit Program')
    approve = {'1', 'yes', 'y', 'ye', ''}
    deny = {'2', 'no', 'n'}
    skip = {'3', 'skip'}
    stop = {'4', 'stop'}

    choice = input().lower()
    if choice in approve:
        approvebutton()
        return
    elif choice in deny:
        denybutton()
        return
    elif choice in skip:
        skipbutton()
        return
    elif choice in stop:
        global running
        running = False
        return
    else:
        sys.stdout.write("Please respond with 'yes' or 'no'")

# Takes the number recieved from the 'help.py' file and makes a decision based on the risk score.
# if the total risk is 110 or greater, it's a hard fail regardless.
# if the number is 3, it's also a hard fail
# if the number is 2, it's a soft fail, meaning that a risk greater than 90 is required to deny the customer
# if the number is 1, one of the validation boxes was red, yet the error message was one we do not recognize. The program
# skips this customer for a human (me) to deal with later
# if the number is 0, and none of the other parameters are met, the customer is approved.


def verdict(number):
    if totalriskscore >= 110:
        print("[!] Hard fail based on risk score. Recommend 'Deny'.")
        denybutton()
        return
    elif number == 3:
        print("[!] Hard fail. Recommend 'Deny'.")
        denybutton()
        return
    elif number == 2 and totalriskscore > 90:
        print(
            "[!] Soft fail. Recommend 'Deny' based on Risk Score being higher than 90.")
        denybutton()
        return
    elif number == 1:
        print("[!] Unsure... Skipping so a human and decide :) ")
        skipbutton()
        return
    elif number == 0:
        print("[!] No problems found, recommend accepting.")
        approvebutton()
    else:
        print("[!] Not enough information to deny, so recommend approving.")
        approvebutton()

# Keeps track of how long the program has been running


def updatetime():
    global timestarted
    global timestartedformated
    global timescrubbed

    totaltime = datetime.now() - timestarted
    # timescrubbed = totaltime.strftime("%H:%M:%S")

    print('[*] Program started: ' + timestartedformated)
    print('[*] Total Run Time: ' + str(totaltime))


cur_directory = os.getcwd()
driver = webdriver.Chrome(
    cur_directory+"\\chromedriver_win32\\chromedriver.exe")

# Starts up the IZ website, and then logs in
print('[*] Navigating to the startup page...')
startupURL = "https://www.internetzoo.dk/auth/login"
driver.get(startupURL)
driver.find_element_by_id("email").send_keys("steventeglman@gmail.com")
driver.find_element_by_id("password").send_keys("123123123")
time.sleep(1)
print('[*] Logging in...')
driver.find_element_by_xpath(
    "//button[@type='submit' and @class='btn btn-primary']").click()
time.sleep(1)

print('[*] Finding the Range...')
driver.get(navigatetoscrubbingwindow())

print('[*] Starting Scrub...')
driver.find_element_by_xpath("//*[@id='master-content']/div[1]/div/a").click()

# Runs the program indefinitely until it runs out of customers to scrub. At which point, it will throw an exception.
# This should obviously be put in a try/catch block for a more elegant solution, yet for now it works.
while running:

    validationboxescheck()
    print(tabulate(validationboxeslist, headers=validationtable, tablefmt='psql'))
    updateriskscore()

    # helpers.analyzestatus runs looks at all of the messages retrieved from the 'validationdic' and searches to see
    # if there are any matches in the 'errors.json' file, to see if any messages correspond with any of the errors in
    # that list
    failnumber = helpers.analyzestatus(validationdic)
    verdict(failnumber)
    print('\n')
    # Uncomment to manually approve or deny customers.
    # userinput()
    customersscrubbed = customersscrubbed + 1
    updatetime()
    print('[*] Customers scrubbed: ' + str(customersscrubbed))
    print('\n')

    # TODO rename everything to use snake case (eg. with underscores between words) as apparently that's Python syntax
    # TODO Enable the quarentine check boxes?
    # TODO Make something for when the program ends. Like a final statistics box or something.
    # TODO Create a timer and Scrub counter
    # TODO Save scrubbing session data (times, etc) into log files.
    # TODO Look into the "summary of risks" section
    # TODO Log all approves and declines with the reason and customer ID
