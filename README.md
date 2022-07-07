# ScottMCL_SpaceEquipment_Metrics
Script for polling Springshare LibCal's API to gather monthly metrics for the lab's space bookings and equipment loans.
 
As written, the script is tailored for the York University Libraries' environment and the specific set of metrics we wish to track for the use of our media creation lab spaces and equipment. It hinges on data pulled from the LibCal API module, and is configured with URLs that match our subscription and environment. To adapt the script for another environment, updated the API URLs, location and client IDs, and "client secret" (which is used to authenticate access to the API; this API token can be generated in the admin interface for Springshare's LibCal API module. The "variables and constants" section owuld also have to be adapted to suit the space/equipment categories, seat names, and item names used in an environment other than ours.

## To use:

- Other than standard libraries, the only extra Python module required for this script is pandas

- You may execute either the Python notebook or the Python script. The script does not currently take any command line input. To execute it for any given month, set the "datadate" variable in the script before running. The variable expects a string in the form "yyyy-mm-dd"

- To get a full month of data, do not execute the script before the end of the month for which data is needed. For example, do not gather June metrics until after July 1.

- The CSV output form this tool can be opened in Excel and then be pasted directly into the DSI department metrics tracking spreadsheet for the Scott MCL, which is stored in YUL-DSI's Teams collection (in the Administration > Statistics Statistics Statistics folder)

## Outputs:

The script will generate CSV files of "raw" data for equipment and space bookings, as well as a "final" set of tallies and metrics for each module. As part of its work, the script will read and update the contents of three "Users" text files in the data subdirectory.

All outputs will appear in the data\ subdirectory, with filenames starting with the date info for the month processed (e.g. 2022-07-01_equipdata.csv....)

## Possible challenges:

There is not as much intelligence as there could be in the mechanism for tracking first-time users. "Test runs" of the script will update the files used to track known users of the lab, which can throw off actual metrics. To avoid this, make a backup copy of the three txt files in the data subdirectory before doing any testing or revisions.

I have set up the "final" outputs to uses hashes of patron email addresses, to preserve privacy... but the "raw" data pulled from LibCal does contain names and email addresses to. For now I have left this in place on the assumption that these files are transitory and will not be kept... but a later version of the script will likely drop the "name" fields and hash email addresses at that level of output, just to remove any possible exposure of individual patron data.

Finally, the goal of this project was to automate and minimize time requied to gather and report data on lab usage. The script is "brittle" in that any changes made to the lab setup (new quipment, new sapcwes or seats) or any changes made to our department's final tracking spreadsheets (where the output metrics will be added over time) will have to be reflected across all three sources: LibCal's comfiguration, this script, and the format of the final tracking spreadsheet.