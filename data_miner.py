from bs4 import BeautifulSoup
import urllib.request
import time
import csv
import os
import string

#PLEASE AVOID RUNNING THIS CODE!
#Out of respect for the Bounty website and to avoid putting undue stress on their servers, please avoid running this code more times than necessary.

#The website we are scraping for data displays this error message when there are no more new names to display for a given letter. We will use it as our flag to move to the next letter.
error_flag="No matching names were found"

#We initialise the lists where we will append names, origins and genders of the names we find
names=["Names"]
origins=["Origins"]
genders=["Genders"]

#We pass every letter of the alphabet as an argument to the web page string
for start_letter in list(string.ascii_lowercase):
    print(start_letter)
    i=1

    #Dynamically generate page link
    names_link="http://www.bounty.com/pregnancy-and-birth/baby-names/baby-name-search/"+start_letter+"?PageNumber="+str(i)+"#ListingTop"
    names_html=urllib.request.urlopen(names_link)
    soup = BeautifulSoup(names_html, "html.parser")

    #Check if there are names on the page
    if error_flag in str(soup):
        valid_page=False
    else:
        valid_page=True

    #For each valid_page, execute the code in the while loop to pull the relevant data from it
    while valid_page:
        print(i)

        #Pull all names, origins and gender data from the current page using the BeautifulSoup find_all method, and append them to the central lists stripped of any html code
        pulled_names=soup.find_all(name='span',attrs={'class':'name'})
        for name in pulled_names:
            names.append(name.text)
        pulled_origins=soup.find_all(name='span',attrs={'class':'origin'})
        for origin in pulled_origins:
            origins.append(origin.text)
        pulled_genders=soup.find_all(name='span',attrs={"class":["gender hide-text female","gender hide-text male"]})
        for gender in pulled_genders:
            genders.append(gender.text)

        #Initialise and check if next page contains names, otherwise finalise loop
        i+=1
        names_link="http://www.bounty.com/pregnancy-and-birth/baby-names/baby-name-search/"+start_letter+"?PageNumber="+str(i)+"#ListingTop"
        names_html=urllib.request.urlopen(names_link)
        soup = BeautifulSoup(names_html, "html.parser")
        if error_flag in str(soup):
            valid_page=False

        #Hard-code a delay of one second before the next loop to prevent putting too much stress on the servers of the website being data-mined
        time.sleep(1)

#Remove the file to be written to if it exists, and create a new one where all the data is written to in csv format
os.remove(r'C:\Users\computer\Documents\Python\Names Gender\names.csv')
with open(r'C:\Users\computer\Documents\Python\Names Gender\names.csv', mode='w', newline='') as names_file:
    names_writer = csv.writer(names_file, delimiter=',')
    for index in range(len(names)):
        names_writer.writerow([names[index],genders[index],origins[index]])

print(names)
print(origins)
print(genders)
