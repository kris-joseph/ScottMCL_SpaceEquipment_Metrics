# ScottMCL_SpaceEquipment_Metrics
Script for polling Springshare LibCal's API to gather monthly metrics for the lab's space bookings and equipment loans.
 
As written, the script is tailored for the York University Libraries' environment and the specific set of metrics we wish to track for the use of our media creation lab spaces and equipment. It hinges on data pulled from the LibCal API module, and is configured with URLs that match our subscription and environment. To adapt the script for another environment, update the API URLs, location and client IDs, and "client secret" (which is used to authenticate access to the API; this API token can be generated in the admin interface for Springshare's LibCal API module). The "variables and constants" section would also have to be adapted to suit the space/equipment categories, seat names, and item names used in an environment other than ours. If time and the API allow, I may revise this to have the script pull that info dynamically.

## To use:

- Other than standard libraries, the only extra Python module required for this script is pandas

- You may execute either the Python notebook or the Python script. The script does not currently take any command line input. To execute it for any given month, set the "datadate" variable in the script before running. The variable expects a string in the form "yyyy-mm-dd"; "dd" is always "01" to reflect the first day of the month as the start data for data collection.

- To get a full month of data, do not execute the script before the end of the month for which data is needed. For example, do not gather June metrics until after July 1.

- The CSV output from this tool (yyyy-mm-dd_overall_finalStats.csv) can be opened in Excel and then be pasted directly into the DSI department metrics tracking spreadsheet for the Scott Media Creation Lab (MCL).

## Outputs:

The script will generate CSV files of "raw" data for equipment and space bookings, as well as a "final" set of tallies and metrics for each module, and one "combined" file with both modules' data together. As part of its work, the script will read and update the contents of three "Users" text files in the data subdirectory.

All outputs will appear in the data\ subdirectory, with filenames starting with the date info for the month processed (e.g. 2022-07-01_equip.csv....)

## Possible challenges:

There is not as much intelligence as there could be in the mechanism for tracking first-time users. "Test runs" of the script will update the files used to track known users of the lab, which can throw off actual metrics. To avoid this, make a backup copy of the three txt files in the data subdirectory before doing any testing or revisions.

Finally, the goal of this short project was to automate and minimize the time required to gather and report data on lab usage. The script is currently "brittle" in that any changes made to the lab setup (new equipment, new spaces or seats) or any changes made to our department's final tracking spreadsheets (where the output metrics will be added over time) will have to be reflected across all three sources: LibCal's configuration, this script, and the format of the final tracking spreadsheet.
