#!/usr/bin/env python
# coding: utf-

import requests, json, csv, calendar, datetime, math, collections, hashlib
from datetime import *
import pandas as pd

##########
## INPUT variable
##########

# Set this to the year and month for which data will be gathered, in yyy-mm-dd format. dd should always be 01
# This is also the date format LibCal's API expects for the API calls
datadate = "2022-03-01"


##########
## Variable initializations and constants
##########


# Our outputData dictionary. This dictionary is gonna have a TON of data points in it eventually....
equipmentOutputData = {}
spacesOutputData = {}

# We'll need an accurate number of days in the month to make a proper call to the API (get 30 days of data for some months, 31 for others, and 28 for one special month)
[year, month, day] = datadate.split("-")
daysInMonth = calendar.monthrange(int(year), int(month))[1]

## These values are specific to the Scott MCL instance of LibCal's Spaces and Equipment modules. 
## FYI, these IDs can be found in the LibCal admin web interface (you'll have to generate a clientSecret in the API module though)
locationID = SET_THIS     # This is the system's location ID for the Scott MCL, which can be seen in the web-based admin for Libcal
clientID = SET_THIS       # Libapps client ID for the yorku account
clientSecret = 'SET_THIS' # Access password, generated using the admin interface for libcal (API module)

# The "faculties" and "rlationship" values here mirror the possible values used in the custom booking forms for Scott MCL spaces and equipment.
# Any changes there should be reflected here.

# The same is true for the constants outlined in the Spaces and Equipment values listed below -- they must match possible options
# in the LibCal setup. 

faculties = ["Arts, Media, Performance and Design (AMPD)",
             "Education (ED)",
             "Environmental & Urban Change (EUC)",
             "Glendon (GL)",
             "Graduate Studies (FGS)",
             "Health (HH)",
             "Lassonde School of Engineering (LE)",
             "Liberal Arts & Professional Studies (LA&PS)",
             "Libraries (YUL)",
             "Schulich School of Business (SB)",
             "Science (SC)",
             "Other Faculty or No Faculty"
            ]

relationshipCategories = ["Graduate Student",
                          "Undergraduate Student",
                          "Faculty Member",
                          "Staff Member",
                          "Community Partner",
                          "Librarian/Archivist",
                          "Other Relationship"
                         ]

# Lab operating hours for tallying frequencies
# Currently running in the range 8AM-8PM; may need asjustment later
# Can also put days of the week in here to hold daily tallies
hours = ["08AM",
         "09AM",
         "10AM",
         "11AM",
         "12PM",
         "01PM",
         "02PM",
         "03PM",
         "04PM",
         "05PM",
         "06PM",
         "07PM",
         "08PM",
         "Monday",
         "Tuesday",
         "Wednesday",
         "Thursday",
         "Friday",
         "Saturday",
         "Sunday"
        ]

# Equipment module data 
equipmentCategories = ["Audio Equipment",
                   "Video Equipment",
                   "VR Equipment"
                  ]

itemNames = ["Blue Yeti Nano, Premium USB Microphone",
             "Canon EOS M50, Mirrorless Camera",
             "Insta360 One R (360 Edition), 360-Degree Camera",
             "Insta360 One R (Twin Edition), 360-Degree & 4K Wide-Angle Camera",
             "MeFoto RoadTrip Air, Tripod & Selfie Stick",
             "Neewer Lighting Kit (2 Lights, 2 Stands, & 2 Softboxes)",
             "Oculus Quest 2, VR Headset & Controllers",
             "Oculus Quest, VR Headset & Controllers",
             "Rode Wireless Go, Wireless & Wearable Microphone System",
             "Sennheiser HD 280 Pro, Dynamic Headphones",
             "Vbestlife W49, Mini Dimmable LED Light Panel",
             "Zoom H4n Pro, Audio Recorder",
             "Zoom LiveTrak L8, 8-Channel Mixer"
             ]



# Spaces module data
spaceCategories = ["Computer Labs",
                   "Studio Spaces",
                   "VR Rooms"
                  ]

spaceNames = ["207 Editing Lab",
              "203A VR Room",
              "203B VR Room",
              "203K Audio Recording Studio",
              "204 Flex Studio",
             ]

labWorkstations = ["Workstation 1 (Dell G7 with Adobe CC)",
                   "Workstation 2 (Dell G7)",
                   "Workstation 3 (Dell G7)",
                   "Workstation 4 (Dell G7)",
                   "Workstation 5 (Dell G7 with Hindenburg Pro)",
                   "Workstation 6 (27-in iMac with Adobe CC)",
                   "Workstation 7 (Dell 7060)"
                  ]


spaceDataCategories = [faculties, relationshipCategories, hours, spaceCategories, spaceNames, labWorkstations]
equipmentDataCategories = [faculties, relationshipCategories, hours, equipmentCategories, itemNames]

for category in [spaceDataCategories, equipmentDataCategories]:
    # Initialize all these data values to zero
    for index in range(len(category)):
        for entry in category[index]:
            if category == spaceDataCategories:
                spacesOutputData[entry] = 0
            else:
                equipmentOutputData[entry] = 0


# Ignore all staff-originated bookings. Side note: encourage staff to NOT use a bunch of different email addresses
adminEmails = ["example@email.com", 
              ]

# hash these email addresses so they match info in our processed CSV data 
# (all email addresses are obscured with hashes for privacy)
for index in range(len(adminEmails)):
    adminEmails[index] = hashlib.md5(adminEmails[index].encode()).hexdigest()

##########
## Gather data from LibCal and clean it
##########

## Get a token for API access
    
# URLs and data structures for API calls are all listed in the admin pages for the Libapps API module
url = 'https://yorku.libcal.com/1.1/oauth/token'
myRequestData = {'client_id': clientID,
        'client_secret': clientSecret,
        'grant_type': 'client_credentials'}

# send the request
call = requests.post(url, data = myRequestData)

# API authorization is returned in a JSON object, and we need to grab/store our access token, which
# is used to validate API calls for getting/setting data
authorizationData = call.json()
accessToken = authorizationData['access_token']



## Send API request to gather data

equipURL = 'https://yorku.libcal.com/1.1/equipment/bookings'
spaceURL = 'https://yorku.libcal.com/1.1/space/bookings'

# NOTE for the following: the MAXIMUM record limit for the LibCal API is 500, meaning 500 rows of data. No issues currently, but in the future
# this may become a problem that needs to be dealt with. A month that contains more than 500 records would have data truncated.
equipData = {'date': datadate,
        'days': daysInMonth,
        'limit': 500,
        'formAnswers': 1}
spaceData = {'date': datadate,
        'lid': locationID,  
        'days': daysInMonth,
        'limit': 500,
        'formAnswers': 1}


headers = {'Authorization':'Bearer '+accessToken}

# get Equipment module data for the month
response = requests.get(equipURL, headers=headers, params=equipData)
equipAPIData = response.json()

# get Spaces module data for the month
response = requests.get(spaceURL, headers=headers, params=spaceData)
spacesAPIData = response.json()



## First-pass data cleaning (for raw CSV output)

# List of field names for which data may be missing (due to booking form variations etc.
# for example, if no "cancellation" of a booking occurred, there is no 'cancelled' data in the record.
# This is mostly for space data. Equioment data only has "cancelled" as a possible missing field
possiblyMissingFields = ['cancelled', 'q2579', 'q2669', 'seat_id', 'seat_name', 'check_in_code']

# Basic cleaning for Equipment API data
for entry in equipAPIData:
    if "cancelled" in entry:
        if entry['cancelled'] == "":
            entry['cancelled'] = "null"
    else:
        entry["cancelled"] = "null"

    if ('q2489' not in entry.keys()) or (entry["q2489"]) == "":
        entry["q2489"] = "null"
    if ('q2490' not in entry.keys()) or (entry["q2490"]) == "":
        entry["q2490"] = "null"
    if ('q2491' not in entry.keys()) or (entry["q2491"]) == "":
        entry["q2491"] = "null"
        
    #Change key names for custom question fields
    entry["relpToYork"] = entry.pop("q2489")
    entry["faculty"] = entry.pop("q2490")
    entry["project"] = entry.pop("q2491")
    
    # Remove identifying patron information
    entry.pop("firstName") 
    entry.pop("lastName")
    entry.pop("account")
    entry["email"] = hashlib.md5(entry["email"].encode()).hexdigest()
    

    # Handle cases where the 'Other' field value might cause problems with stats (since it's a possible answer for
    # two different questions on booking forms
    if entry["relpToYork"] == "Other": entry["relpToYork"] = "Other Relationship" 
    if entry["faculty"] == "Other": entry["faculty"] = "Other Faculty or No Faculty"

# Basic cleaning for Spaces API data
for entry in spacesAPIData:
    
    # Go through list of 'possibly missing' fields to see if they're in the data; if so and empty,
    # set to null. Without this, the output CSV file will be missing some fields and data won't line up with headers
    for possiblyMissing in possiblyMissingFields:
        if possiblyMissing in entry:
            if str(entry[possiblyMissing]) == "":
                entry[possiblyMissing] = "null"
        else:
            entry[possiblyMissing] = "null"

    # These are the custom questions, which are occasionally not filled out; 
    # empty questions result in mal-formatted CSV output so I set to null if nonexistent in a record
    if ('q2489' not in entry.keys()) or (entry["q2489"]) == "":
        entry["q2489"] = "null"
    if ('q2490' not in entry.keys()) or (entry["q2490"]) == "":
        entry["q2490"] = "null"
    if ('q2491' not in entry.keys()) or (entry["q2491"]) == "":
        entry["q2491"] = "null"
    if ('q2669' not in entry.keys()) or (entry["q2669"]) == "":
        entry["q2669"] = "null"
    
    #Change key names for custom question fields
    entry["relpToYork"] = entry.pop("q2489")
    entry["faculty"] = entry.pop("q2490")
    entry["project"] = entry.pop("q2491")
    entry["VRexperience"] = entry.pop("q2579")
    entry["flexStudioUse"] = entry.pop("q2669")
    
    # Remove identifying patron information
    entry.pop("firstName") 
    entry.pop("lastName")
    entry.pop("account")
    entry["email"] = hashlib.md5(entry["email"].encode()).hexdigest()
    
    # Handle cases where the 'Other' field value might cause problems with stats (since it's a possible answer for
    # two different questions on booking forms
    if entry["relpToYork"] == "Other": entry["relpToYork"] = "Other Relationship" 
    if entry["faculty"] == "Other": entry["faculty"] = "Other Faculty or No Faculty"
    

## Writing Data to a CSV file

## OUTPUT: Equipment data

csvOut = open("data/"+datadate+"_equip.csv", 'w')

# Equipment data field names in the order I want
equipFieldnames = ['bookId', 'id', 'eid', 'cid', 'lid',
             'fromDate', 'toDate', 'created',
             'email', 'status', 'location_name', 'category_name', 'item_name',
             'barcode', 'cancelled', 'relpToYork', 'faculty', 'project']

# create the csv writer object
csv_writer = csv.DictWriter(csvOut, fieldnames=equipFieldnames)

# Output the header first
csv_writer.writeheader()
 
for record in equipAPIData:
    csv_writer.writerow(record)
 
csvOut.close()

## OUTPUT: Space data

csvOut = open("data/"+datadate+"_space.csv", 'w')

# Spaces data field names in the order I want
spacesFieldnames = ['bookId', 'id', 'eid', 'cid', 'lid',
             'fromDate', 'toDate', 'created',
             'email', 'status', 'location_name', 'category_name', 'item_name',
              'seat_id', 'seat_name', 'check_in_code', 'cancelled', 'relpToYork', 'faculty', 'project', 'VRexperience', 'flexStudioUse']

# create the csv writer object
csv_writer = csv.DictWriter(csvOut, fieldnames=spacesFieldnames)

# Output the header first
csv_writer.writeheader()

 
for record in spacesAPIData:
    csv_writer.writerow(record)
 
csvOut.close()


## Pull in CSV data for final processing

# Hey, so those files we literally just created? Let's read 'em into Pandas Dataframes! 
# Why is this so obtuse, you ask?
# Because this was originally a separate script and I should consider converting the dict from earlier 
# in THIS script into a DataFrame but TBH I think the raw CSV files are still valuable and so this is ok by me

# Anyway, since we built the CSV files in the previous step, the format of them should be reliable 
# and we can simply read them into Pandas

spacesData = pd.read_csv("data/"+datadate+"_space.csv", index_col='id')
equipData = pd.read_csv("data/"+datadate+"_equip.csv", index_col='id')



##########
# Metrics and Stats Processing
##########

## Cancelled vs Actual Bookings

# Drop staff-affiliated bookings right off the top, so numbers all match; 
# otherwise the counts of cancellations, etc. get thrown off
for address in adminEmails:
    spacesData.drop(spacesData.index[(spacesData["email"] == address)],axis=0,inplace=True)
    equipData.drop(equipData.index[(equipData["email"] == address)],axis=0,inplace=True)

# Grab a Series of just Status Column
spacesBookingStatus = spacesData["status"]
equipmentBookingStatus = equipData["status"]

# How many do we have?
spacesOutputData["totalBookings"] = len(spacesBookingStatus)
equipmentOutputData["totalBookings"] = len(equipmentBookingStatus)

spacesOutputData["cancelledByUsers"] = len(spacesBookingStatus[spacesBookingStatus.str.startswith('Cancelled by User')])
equipmentOutputData["cancelledByUsers"] = len(equipmentBookingStatus[equipmentBookingStatus.str.startswith('Cancelled by User')])

spacesOutputData["cancelledBySystem"] = len(spacesBookingStatus[spacesBookingStatus.str.startswith('Cancelled by System')])
equipmentOutputData["cancelledBySystem"] = len(equipmentBookingStatus[equipmentBookingStatus.str.startswith('Cancelled by System')])

spacesOutputData["cancelledByAdmin"] = len(spacesBookingStatus[spacesBookingStatus.str.startswith('Cancelled by Admin')])
equipmentOutputData["cancelledByAdmin"] = len(equipmentBookingStatus[equipmentBookingStatus.str.startswith('Cancelled by Admin')])

spacesOutputData["totalActualBookings"] = spacesOutputData["totalBookings"]-spacesOutputData["cancelledByUsers"]-spacesOutputData["cancelledBySystem"]-spacesOutputData["cancelledByAdmin"]
equipmentOutputData["totalActualBookings"] = equipmentOutputData["totalBookings"]-equipmentOutputData["cancelledByUsers"]-equipmentOutputData["cancelledBySystem"]-equipmentOutputData["cancelledByAdmin"]

print("SPACES DATA")
print("Total bookings made:", spacesOutputData["totalBookings"])
print("Cancelled by users:", spacesOutputData["cancelledByUsers"]) 
print("Cancelled for late checkin:", spacesOutputData["cancelledBySystem"])
print("Cancelled by staff:", spacesOutputData["cancelledByAdmin"])
print("Total actual bookings:", spacesOutputData["totalActualBookings"])

print("EQUIPMENT DATA")
print("Total bookings made:", equipmentOutputData["totalBookings"])
print("Cancelled by users:", equipmentOutputData["cancelledByUsers"]) 
print("Cancelled for late checkin:", equipmentOutputData["cancelledBySystem"])
print("Cancelled by staff:", equipmentOutputData["cancelledByAdmin"])
print("Total actual bookings:", equipmentOutputData["totalActualBookings"])



## Drop unwanted data

# Drop bookings canceled by User and by System
spacesData.drop(spacesData.index[(spacesData["status"] == 'Cancelled by User')],axis=0,inplace=True)
equipData.drop(equipData.index[(equipData["status"] == 'Cancelled by User')],axis=0,inplace=True)

spacesData.drop(spacesData.index[(spacesData["status"] == 'Cancelled by System')],axis=0,inplace=True)
equipData.drop(equipData.index[(equipData["status"] == 'Cancelled by System')],axis=0,inplace=True)

spacesData.drop(spacesData.index[(spacesData["status"].str.startswith('Cancelled by Admin'))],axis=0,inplace=True)
equipData.drop(equipData.index[(equipData["status"].str.startswith('Cancelled by Admin'))],axis=0,inplace=True)



## Data: Unique projects, VR content choices, and Flex Studio uses

# Set up a string translation table to remove newline characters from "project" entry fields
# Since the string is built by casting a LIST as a STRING, we can also remove
# the [ and ] characters that Python would use to show the sdata is in a list
strTranslation = str.maketrans('', '' ,'\r\n[]')

# First we can grab project field data and calculate the number of "unique" projects found within it
spacesOutputData["uniqueProjects"] = len(spacesData['project'].unique())-1
spacesOutputData["projectList"] = str(spacesData['project'].unique()).replace("nan ","") #remove Pandas NaN values from the string
spacesOutputData["projectList"] = spacesOutputData["projectList"].translate(strTranslation)

equipmentOutputData["uniqueProjects"] = len(equipData['project'].unique())-1
equipmentOutputData["projectList"] = str(equipData['project'].unique()).replace("nan ","") #remove Pandas NaN values from the string
equipmentOutputData["projectList"] = equipmentOutputData["projectList"].translate(strTranslation)

# Users also provide info on how they'll use the Flex Studio or VR Rooms as part of those forms, so grab that...
spacesOutputData["VRContentList"] = str(spacesData['VRexperience'].unique()).replace("nan","") #remove Pandas NaN values from the string
spacesOutputData["VRContentList"] = spacesOutputData["VRContentList"].translate(strTranslation)
spacesOutputData["flexStudioUseList"] = str(spacesData['flexStudioUse'].unique()).replace("nan","") #remove Pandas NaN values from the string
spacesOutputData["flexStudioUseList"] = spacesOutputData["flexStudioUseList"].translate(strTranslation)

print("Equipment projects:", equipmentOutputData["projectList"])
print("Number of unique equipment projects:", equipmentOutputData["uniqueProjects"])
print()
print("Spaces projects:", spacesOutputData["projectList"])
print("Number of unique spaces projects:", spacesOutputData["uniqueProjects"])
print("Flex Studio projects:", spacesOutputData["flexStudioUseList"])
print("VR Room experiences:", spacesOutputData["VRContentList"])



## Data: Frequencies / Counts for faculty, RTI, space categories and equipment categories

# Both the equipment and spaces data have info for faculty, RTI, space/equipment category and item, so we'll
# look through those to build tallies adn store them in the output data
for category in ["faculty", "relpToYork", "category_name", 'item_name']:
    spacesCategoryTallies = spacesData[category].value_counts(dropna=True).to_dict()
    equipmentCategoryTallies = equipData[category].value_counts(dropna=True).to_dict()
    for key in spacesCategoryTallies:
        spacesOutputData[key] = spacesCategoryTallies[key]
    for key in equipmentCategoryTallies:
        equipmentOutputData[key] = equipmentCategoryTallies[key]    

# The Spaces data has a unique "seat_name" category so we'll do this one separately...
workstationTallies = spacesData["seat_name"].value_counts(dropna=True).to_dict()
for key in workstationTallies:
    spacesOutputData[key] = workstationTallies[key] 
    

    
## Unique Users

# We can count unique users by looking at unique email addresses. As a note, I have seen that some students will
# use more than one address when booking, which makes one person appear as two (or three).... not sure there's
# much to be done about this
spacesOutputData["uniqueUsers"] = len(spacesData['email'].unique())
equipmentOutputData["uniqueUsers"] = len(equipData['email'].unique())

print("Number of unique space users:", spacesOutputData["uniqueUsers"])
print("Number of unique equipment users:", equipmentOutputData["uniqueUsers"])



## User access times

# the fromDate field is used in both modules to log the time a user checks out a piece of equipment OR checks in to a space
# In this section we'll run througb that data and pull out frequences by day of the week and hour of the day
spacesCheckInTimes = spacesData['fromDate'].unique()
spacesCheckInTimes = spacesCheckInTimes.tolist()

equipCheckInTimes = equipData['fromDate'].unique()
equipCheckInTimes = equipCheckInTimes.tolist()

# Run through each of the checkin times lists to steip out day and hour info, and populate
# the outputData structures for ewach of the equipment and spaces categories
for reportType in [spacesCheckInTimes, equipCheckInTimes]:
    
    #initialize array for hours-only data
    checkInHours = []
    checkInDays = []

    # Convert HH:MM info strings into hours                                    
    for entry in reportType:
        if isinstance(entry, str) == True:
            accessTime = datetime.strptime(entry, "%Y-%m-%dT%H:%M:%S%z")
            # Need to handle an case where bookings are added manually, in which
            # case the time is set to midnight. For now alter this to read 10AM (lab opening time)
            if accessTime.strftime("%I%p") == "12AM":
                checkInHours.append(accessTime.strftime("10AM"))
            else:
                checkInHours.append(accessTime.strftime("%I%p"))        
            checkInDays.append(accessTime.strftime("%A"))

    # set up a Counter object to do frequency counts for checking times (total for whole month)
    checkInHoursCount = collections.Counter(checkInHours)
    checkInDaysCount = collections.Counter(checkInDays)

    for item in [checkInHoursCount, checkInDaysCount]:

        # Store totals in our outputData
        for key, value in item.items():
            if reportType == spacesCheckInTimes:
                spacesOutputData[key] = value
                print(key, spacesOutputData[key])
            else:
                equipmentOutputData[key] = value
                print(key, equipmentOutputData[key])
                

                
## Data: First Time Users

spacesOutputData["firstTimeUsers"] = 0
equipmentOutputData["firstTimeUsers"] = 0
overallFirstTimeUsers = 0

# Read existing data files and build user lists
existingSpaceUserFile = open("data/existingSpaceUsers.txt", "r")
existingEquipmentUserFile = open("data/existingEquipmentUsers.txt", "r")
existingOverallUserFile = open("data/existingOverallUsers.txt", "r")

existingSpaceUserDataSet = existingSpaceUserFile.read()
existingSpaceUsers = existingSpaceUserDataSet.split("\n")

existingEquipmentUserDataSet = existingEquipmentUserFile.read()
existingEquipmentUsers = existingEquipmentUserDataSet.split("\n")

existingOverallUserDataSet = existingOverallUserFile.read()
existingOverallUsers = existingOverallUserDataSet.split("\n")

# Get a list of unique users for this month
spaceUniqueUsers = spacesData['email'].unique()
spaceUniqueUsers = spaceUniqueUsers.tolist()

equipUniqueUsers = equipData['email'].unique()
equipUniqueUsers = equipUniqueUsers.tolist()

overallUniqueUsers = list(set(spaceUniqueUsers + equipUniqueUsers))

for usergroup in [spaceUniqueUsers, equipUniqueUsers, overallUniqueUsers]:

    for userThisMonth in usergroup:
        
        if usergroup == spaceUniqueUsers:
            if userThisMonth not in existingSpaceUsers:
                spacesOutputData["firstTimeUsers"] += 1
                existingSpaceUsers.append(userThisMonth)
        elif usergroup == equipUniqueUsers:
            if userThisMonth not in existingEquipmentUsers:
                equipmentOutputData["firstTimeUsers"] += 1
                existingEquipmentUsers.append(userThisMonth)
        else:
            if userThisMonth not in existingOverallUsers:
                overallFirstTimeUsers += 1
                existingOverallUsers.append(userThisMonth)
        
existingOverallUsers = list(set(existingSpaceUsers + existingEquipmentUsers))  

# Dump the new existing user lists back to a file
with open("data/existingSpaceUsers.txt", "w") as existingSpaceUserFile:
    existingSpaceUserDataSet = "\n".join(existingSpaceUsers)
    existingSpaceUserFile.write(existingSpaceUserDataSet)

with open("data/existingEquipmentUsers.txt", "w") as existingEquipmentUserFile:
    existingEquipmentUserDataSet = "\n".join(existingEquipmentUsers)
    existingEquipmentUserFile.write(existingEquipmentUserDataSet)
    
with open("data/existingOverallUsers.txt", "w") as existingOverallUserFile:
    existingOverallUserDataSet = "\n".join(existingOverallUsers)
    existingOverallUserFile.write(existingOverallUserDataSet)

print("This month's number of new space users:", spacesOutputData["firstTimeUsers"])
print("This month's number of new equipment users:", equipmentOutputData["firstTimeUsers"])
print("This month's number of new overall users:", overallFirstTimeUsers)


#######
## Final Data Output
#######

# now we will open a file for writing
spaceCsvOut = open("data/"+datadate+"_space_finalStats.csv", 'w')
equipmentCsvOut = open("data/"+datadate+"_equipment_finalStats.csv", 'w')

# Field names in the order I want
spaceFieldnames = [
              # Overall booking stats
              'uniqueUsers', 'firstTimeUsers', 'Studio Spaces', 'Computer Labs', 'VR Rooms',
              'uniqueProjects', 'projectList', 'totalBookings', 'cancelledByUsers', 'cancelledBySystem',
              'cancelledByAdmin', 'totalActualBookings',
              # Bookings by Faculty
              'Arts, Media, Performance and Design (AMPD)', 'Education (ED)',
              'Environmental & Urban Change (EUC)', 'Glendon (GL)',
              'Graduate Studies (FGS)', 'Health (HH)', 'Lassonde School of Engineering (LE)',
              'Liberal Arts & Professional Studies (LA&PS)', 'Libraries (YUL)',
              'Schulich School of Business (SB)', 'Science (SC)', 'Other Faculty or No Faculty',
              # Bookings by Relp To Institution
              'Faculty Member', 'Staff Member', 'Graduate Student',
              'Undergraduate Student', 'Librarian/Archivist', 'Community Partner', 'Other Relationship',
              # Booking Times
              '08AM', '09AM', '10AM', '11AM', '12PM', '01PM', '02PM', '03PM', '04PM', '05PM',
              '06PM', '07PM', '08PM', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 
              'Saturday', 'Sunday',
              #Bookings by space/seat
              '203K Audio Recording Studio', '207 Editing Lab', 'Workstation 1 (Dell G7 with Adobe CC)',
              'Workstation 2 (Dell G7)', 'Workstation 3 (Dell G7)', 'Workstation 4 (Dell G7)',
              'Workstation 5 (Dell G7 with Hindenburg Pro)', 'Workstation 6 (27-in iMac with Adobe CC)',
              'Workstation 7 (Dell 7060)', '203A VR Room', '203B VR Room', '204 Flex Studio',  
              # Content choices
              'VRContentList', 'flexStudioUseList'
             ]

equipmentFieldnames = [
              # Overall booking stats
              'uniqueUsers', 'firstTimeUsers', 'Audio Equipment', 'Video Equipment', 'VR Equipment',
              'uniqueProjects', 'projectList', 'totalBookings', 'cancelledByUsers', 'cancelledBySystem',
              'cancelledByAdmin', 'totalActualBookings',
              # Bookings by Faculty
              'Arts, Media, Performance and Design (AMPD)', 'Education (ED)',
              'Environmental & Urban Change (EUC)', 'Glendon (GL)',
              'Graduate Studies (FGS)', 'Health (HH)', 'Lassonde School of Engineering (LE)',
              'Liberal Arts & Professional Studies (LA&PS)', 'Libraries (YUL)',
              'Schulich School of Business (SB)', 'Science (SC)', 'Other Faculty or No Faculty',
              # Bookings by Relp To Institution
              'Faculty Member', 'Staff Member', 'Graduate Student',
              'Undergraduate Student', 'Librarian/Archivist', 'Community Partner', 'Other Relationship',
              # Booking Times
              '08AM', '09AM', '10AM', '11AM', '12PM', '01PM', '02PM', '03PM', '04PM', '05PM',
              '06PM', '07PM', '08PM', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 
              'Saturday', 'Sunday',
              #Bookings by equipment type
              'Blue Yeti Nano, Premium USB Microphone',
              'Canon EOS M50, Mirrorless Camera',
              'Insta360 One R (360 Edition), 360-Degree Camera',
              'Insta360 One R (Twin Edition), 360-Degree & 4K Wide-Angle Camera',
              'MeFoto RoadTrip Air, Tripod & Selfie Stick',
              'Neewer Lighting Kit (2 Lights, 2 Stands, & 2 Softboxes)',
              'Oculus Quest 2, VR Headset & Controllers',
              'Oculus Quest, VR Headset & Controllers',
              'Rode Wireless Go, Wireless & Wearable Microphone System',
              'Sennheiser HD 280 Pro, Dynamic Headphones',
              'Vbestlife W49, Mini Dimmable LED Light Panel',
              'Zoom H4n Pro, Audio Recorder',
              'Zoom LiveTrak L8, 8-Channel Mixer' 
             ]

# create the csv writer object
spaceCsvWriter = csv.DictWriter(spaceCsvOut, fieldnames=spaceFieldnames)
equipmentCsvWriter = csv.DictWriter(equipmentCsvOut, fieldnames=equipmentFieldnames)

# Output the header first
spaceCsvWriter.writeheader()
equipmentCsvWriter.writeheader()

spaceCsvWriter.writerow(spacesOutputData)
equipmentCsvWriter.writerow(equipmentOutputData)

spaceCsvOut.close()
equipmentCsvOut.close()



## Create combined file (one line of data for both modules)

finalEquipmentData = open("data/"+datadate+"_equipment_finalStats.csv", 'r')
finalSpaceData = open("data/"+datadate+"_space_finalStats.csv", 'r')

equipmentHeader = finalEquipmentData.readline().strip()
spacesHeader = finalSpaceData.readline().strip()
finalHeader = equipmentHeader+spacesHeader

equipmentData = finalEquipmentData.readline().strip()
spacesData = finalSpaceData.readline().strip()

finalData = equipmentData+spacesData

finalFullData = open("data/"+datadate+"_overall_finalStats.csv", 'w')

finalFullData.write(finalHeader+"\n")
finalFullData.write(finalData+"\n")