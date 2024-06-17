###
### SUPPORT?CONFIG DATA FOR METRICS SCRIPTS
###
### All of the lists of names for faculties, equipment types, rooms, etc. are set here
### The metrics scripts break when things in Libcal are altered (e.g. someone alters 
### the name for a piece of equipment or a space, adds new equipment to the system, 
### or makes changes to booking forms.
###
### Often these errors only appear when running the script, and then it's a game of hunt
### and peck to figure out what in this config file needs to be updated.
###

import hashlib

# Our outputData dictionaries. These dictionaries are gonna have a TON of data points 
# in them eventually....
equipmentOutputData = {}
spacesOutputData = {}

## These values are specific to the Scott MCL instance of LibCal's Spaces and Equipment modules. 
## FYI, these IDs can be found in the LibCal admin web interface (you'll have to generate a clientSecret in the API module though)
locationID =                                  # This is the system's location ID for the Scott MCL, which can be seen in the web-based admin for Libcal
clientID =                                     # Libapps client ID for the yorku account
clientSecret = '' # Access password, generated using the admin interface for libcal (API module)

#locationID = SET_THIS     # This is the system's location ID for the Scott MCL, which can be seen in the web-based admin for Libcal
#clientID = SET_THIS       # Libapps client ID for the yorku account
#clientSecret = 'SET_THIS' # Access password, generated using the admin interface for libcal (API module)


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
             "School of Continuing Studies (SCS)",
             "YUELI",
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
                   "VR Equipment",
                   "Art Tools"
                  ]

itemNames = ["Blue Yeti Nano, Premium USB Microphone",
             "Audio-Technica AT2005USB, Cardioid Microphone",
             "Apex176 Hypercardioid Shotgun Microphone",
             "Shure SM58, Vocal Microphone",
             "Power DeWise Lavalier Microphone",
             "Rode Wireless Go, Wireless & Wearable Microphone System",
             "Saramonic UwMic9 Kit 2, UHF Wireless & Wearable Microphone System",
             
             "Canon EOS M50, Mirrorless Camera",
             "Canon EOS M50 Mark II, Mirrorless Camera",
             "Canon EF-M 55-200 mm, Camera Lens",
             "Canon EF-M 32 mm, Camera Lens",
             
             "Insta360 One R (360 Edition), 360-Degree Camera",
             "Insta360 One R (Twin Edition), 360-Degree & 4K Wide-Angle Camera",
             "MeFoto RoadTrip Air, Tripod & Selfie Stick",
             "Manfrotto BeFree Advanced, Travel Tripod",
             "SmallRig Mini Tripod",
             "Ulanzi Phone Mount",
             
             "Neewer Lighting Kit (2 Lights, 2 Stands, & 2 Softboxes)",
             "Neewer Lighting Kit Without Softboxes",
             "Aputure Amaran AL-H198, LED Light Panel",
             "Neewer Lighting Single Panel",
             "Vbestlife W49, Mini Dimmable LED Light Panel",
             
             "DJI Osmo Mobile 6, Gimbal for Smartphones",
             "Zhiyun Weebill 3, Gimbal for Mirrorless Cameras",
             "Meta Quest 2 (128 GB), VR Headset & Controllers",
             "Meta Quest 2 (256 GB), VR Headset & Controllers",
             "Meta Quest 3",
             "Meta Quest, VR Headset & Controllers",
             "Sennheiser HD 280 Pro, Dynamic Headphones",

             "Zoom H4n Pro, Audio Recorder",
             "Zoom H6, Audio Recorder",
             "Windscreen for Zoom H4n Pro",
             
             "Zoom LiveTrak L8, 8-Channel Mixer",

             "Puluz 25 cm Foldable LED Ring Light Studio, Portable Lightbox",
             "Puluz 40 cm Foldable LED Ring Light Studio Box, Portable Lightbox",
             "Wacom Intuos Medium, Bluetooth Pen Tablet"
             ]


# Spaces module data
spaceCategories = ["Computer Labs",
                   "Studio Spaces",
                   "VR Rooms",
                   "Meeting Rooms and Demo Spaces"
                  ]

spaceNames = ["207 Editing Lab",
              "203E VR/Podcasting Room",
              "203G VR Room",
              "203K Audio Recording Studio",
              "204 Flex Studio",
              "Scott 206 Demo Space",
              '207C Audio Recording Studio',
              "Meeting Rooms and Demo Spaces"
             ]

labWorkstations = ["Workstation 1 (Dell G7 with Adobe CC)",
                   "Workstation 2 (Dell G7 with Adobe CC)",
                   "Workstation 3 (Dell G7)",
                   "Workstation 4 (Dell G7)",
                   "Workstation 5 (Dell G7 with Hindenburg Pro)",
                   "Workstation 6 (27-in iMac with Adobe CC)",
                   "Workstation 7 (Mac Studio)"
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


# Ignore all staff-originated bookings by including their emil addresses in the list below. Side note: encourage staff to NOT use a bunch of different email addresses

adminEmails = ["example@email.com", 
              ]

# hash these email addresses so they match info in our processed CSV data 
# (all email addresses are obscured with hashes for privacy)
for index in range(len(adminEmails)):
    adminEmails[index] = hashlib.md5(adminEmails[index].encode()).hexdigest()

###
### The following two lists outline how the "raw" API data will be output
### to CSV for futher processing
###

# Spaces data field names in the order I want
spacesInputDataFieldnames = ['bookId', 'id', 'eid', 'cid', 'lid',
             'fromDate', 'toDate', 'created',
             'email', 'status', 'location_name', 'category_name', 'item_name', 'event',
             'seat_id', 'seat_name', 'check_in_code', 'cancelled', 'relpToYork', 
             'faculty', 'project', 'VRexperience', 'flexStudioUse', 
             'flexStudioPhotoCameraChoice', 'flexStudioVidCameraChoice', 'flexStudioBackgroundChoice',
             'groupBooking', 'groupSize', 'nickname']

# Equipment data field names in the order I want
equipInputDataFieldnames = ['bookId', 'id', 'eid', 'cid', 'lid',
             'fromDate', 'toDate', 'created',
             'email', 'status', 'location_name', 'category_name', 'item_name',
             'event', 'barcode', 'cancelled', 'relpToYork', 'faculty', 'project',
             'VRexperience', 'flexStudioUse', 'flexStudioPhotoCameraChoice', 'flexStudioVidCameraChoice', 'flexStudioBackgroundChoice', 'groupBooking', 'groupSize', 'nickname']

###
### The following two lists outline how the FINAL metrics data will be output
### to CSV files for updating the departmental metrics spreadsheets. The columns here
### must MATCH the columns in the sheets (Microsoft Teams: LIB-DSI -> Files -> Administration ->
### Statistics Statistics Statistics -> DSI Stats -> DSI Stats -MCL.xlsx

spacesFinalFieldnames = [
              # Overall booking stats
              'uniqueUsers', 'firstTimeUsers', 'Studio Spaces', 'Computer Labs', 'VR Rooms',
              'uniqueProjects', 'projectList', 'totalBookings', 
              'cancelledByUsers', 'cancelledBySystem',
              'cancelledByAdmin', 'totalActualBookings',
              # Bookings by Faculty
              'Arts, Media, Performance and Design (AMPD)', 'Education (ED)',
              'Environmental & Urban Change (EUC)', 'Glendon (GL)',
              'Graduate Studies (FGS)', 'Health (HH)', 'Lassonde School of Engineering (LE)',
              'Liberal Arts & Professional Studies (LA&PS)', 'Libraries (YUL)',
              'Schulich School of Business (SB)', 'Science (SC)', 
              'School of Continuing Studies (SCS)', 'YUELI',
              'Other Faculty or No Faculty',
              # Bookings by Relp To Institution
              'Faculty Member', 'Staff Member', 'Graduate Student',
              'Undergraduate Student', 'Librarian/Archivist', 'Community Partner', 
              'Other Relationship',
              # Booking Times
              '08AM', '09AM', '10AM', '11AM', '12PM', '01PM', '02PM', '03PM', '04PM', '05PM',
              '06PM', '07PM', '08PM', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 
              'Saturday', 'Sunday',
              #Bookings by space/seat
              '203K Audio Recording Studio', '207C Audio Recording Studio',
              '207 Editing Lab', 
              'Workstation 1 (Dell G7 with Adobe CC)',
              'Workstation 2 (Dell G7 with Adobe CC)', 'Workstation 3 (Dell G7)', 
              'Workstation 4 (Dell G7)',
              'Workstation 5 (Dell G7 with Hindenburg Pro)', 
              'Workstation 6 (27-in iMac with Adobe CC)',
              'Workstation 7 (Mac Studio)', '203E VR/Podcasting Room', '203G VR Room',  '204 Flex Studio',
              'Scott 205 Office Area', 'Scott 206 Demo Space', 'Meeting Rooms and Demo Spaces',
              'Audio Recording Rooms', 'Flex Studio Spaces', '203A VR Room',
              # Content choices
              'VRContentList', 'flexStudioUseList'
             ]

equipmentFinalFieldnames = [
              # Overall booking stats
              'uniqueUsers', 'firstTimeUsers', 'Audio Equipment', 'Video Equipment', 
              'VR Equipment', 'uniqueProjects', 'projectList', 'totalBookings',
              'cancelledByUsers', 'cancelledBySystem',
              'cancelledByAdmin', 'totalActualBookings',
              # Bookings by Faculty
              'Arts, Media, Performance and Design (AMPD)', 'Education (ED)',
              'Environmental & Urban Change (EUC)', 'Glendon (GL)',
              'Graduate Studies (FGS)', 'Health (HH)', 'Lassonde School of Engineering (LE)',
              'Liberal Arts & Professional Studies (LA&PS)', 'Libraries (YUL)',
              'Schulich School of Business (SB)', 'Science (SC)', 
              'School of Continuing Studies (SCS)', 'YUELI',
              'Other Faculty or No Faculty',
              # Bookings by Relp To Institution
              'Faculty Member', 'Staff Member', 'Graduate Student',
              'Undergraduate Student', 'Librarian/Archivist', 'Community Partner', 
              'Other Relationship',
              # Booking Times
              '08AM', '09AM', '10AM', '11AM', '12PM', '01PM', '02PM', '03PM', '04PM', '05PM',
              '06PM', '07PM', '08PM', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 
              'Saturday', 'Sunday',
              #Bookings by equipment type
              'Blue Yeti Nano, Premium USB Microphone',
              'Canon EOS M50, Mirrorless Camera',
              'Canon EOS M50 Mark II, Mirrorless Camera',
              'Canon EF-M 55-200 mm, Camera Lens',
              'Canon EF-M 32 mm, Camera Lens',
              'Insta360 One R (360 Edition), 360-Degree Camera',
              'Insta360 One R (Twin Edition), 360-Degree & 4K Wide-Angle Camera',
              'MeFoto RoadTrip Air, Tripod & Selfie Stick',
              'Manfrotto BeFree Advanced, Travel Tripod',
              'SmallRig Mini Tripod',
              'Ulanzi Phone Mount',
              'Neewer Lighting Kit (2 Lights, 2 Stands, & 2 Softboxes)',
              'Neewer Lighting Kit Without Softboxes',
              'Neewer Lighting Single Panel',
              'DJI Osmo Mobile 6, Gimbal for Smartphones',
              'Zhiyun Weebill 3, Gimbal for Mirrorless Cameras',
              'Meta Quest 3',
              'Meta Quest 2 (128 GB), VR Headset & Controllers',
              'Meta Quest 2 (256 GB), VR Headset & Controllers',
              'Meta Quest, VR Headset & Controllers',
              'Rode Wireless Go, Wireless & Wearable Microphone System',
              'Power DeWise Lavalier Microphone',
              'Sennheiser HD 280 Pro, Dynamic Headphones',
              'Vbestlife W49, Mini Dimmable LED Light Panel',
              'Zoom H4n Pro, Audio Recorder',
              'Zoom H6, Audio Recorder',
              'Zoom LiveTrak L8, 8-Channel Mixer',
              'Windscreen for Zoom H4n Pro', 
              'Aputure Amaran AL-H198, LED Light Panel', 
              'Saramonic UwMic9 Kit 2, UHF Wireless & Wearable Microphone System',
              'Shure SM58, Vocal Microphone',
              'Apex176 Hypercardioid Shotgun Microphone',
              'Audio-Technica AT2005USB, Cardioid Microphone',
              'Puluz 25 cm Foldable LED Ring Light Studio, Portable Lightbox', 
              'Puluz 40 cm Foldable LED Ring Light Studio Box, Portable Lightbox', 
              'Wacom Intuos Medium, Bluetooth Pen Tablet', 'Art Tools'
             ]
