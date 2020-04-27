
INSTRUCTIONS FOR final_project_drafting.py

This program allows a user to choose a city in the United States 
and see the average rating (1-5) and average total number of user ratings 
for restaurants sorted by price level (1-4 or 0-4) from the Yelp Fusion Business Search API 
and the Google Places API, both linked below.

Yelp Fusion Business Search API: 
https://www.yelp.com/developers/documentation/v3/business_search 

Google Places API, specifically the Text Search Request capability: 
https://developers.google.com/places/web-service/search#TextSearchRequests

Both of these APIs require keys. Instructions for how to supply API keys to the program are available below. 

Users of this program can visualize data for restaurants in a given city with a total of 
four different plotly bar charts: one for each average (mean) the program calculates against 
the price level for each API.

Before supplying API keys to the program, be sure you have installed 
the required Python packages: requests and plotly. 

The json and sqlite3 packages should be built in, and thus there should be no need to install them.


SPECIAL INSTRUCTIONS FOR SUPPLYING API KEYS TO THE PROGRAM:

1) Create two Python files with the following names:

google_secrets.py

yelp_secrets.py

2) Acquire your unique API keys from the following APIs:

Yelp Fusion Business Search API: 
https://www.yelp.com/developers/documentation/v3/business_search 

Google Places API, specifically the Text Search Request capability: 
https://developers.google.com/places/web-service/search#TextSearchRequests

3) After acquiring the unique API keys from each API, open your google_secrets.py file.

4) Initialize a variable called google_api_key

5) Assign your Google API key to the variable as a string.

6) Open your yelp_secrets.py file.

7) Initialize two variables, respectively called yelp_client_id and yelp_api_key

8) Assign your Yelp Client ID and Yelp API key to each variable respectively, both as strings.

9) Save both files and close them.

10) Make sure both files are in the same directory as the one from which you will be running the program.


When running the program, the most important thing to keep in mind is to follow the command-line prompts closely.

Enjoy!


PLEASE SEE THE FOLLOWING VIDEO FOR A DETAILED WALKTHROUGH OF HOW TO INTERACT WITH THIS PROGRAM 
AFTER SUPPLYING YOUR API KEYS AND INSTALLING THE REQUIRED PACKAGES:

https://www.loom.com/share/92a92898d97141e396beb8f4cc566c59







