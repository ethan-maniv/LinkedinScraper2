import pandas as pd
import requests
from dotenv import load_dotenv
import os
import tempfile


# Set up your Google Custom Search Engine (CSE) and obtain an API key
# Add your  


API_KEY = ''
CSE_ID = ''

input_file = 'input.csv'

df = pd.read_csv(input_file)

def splitName(name):
     text = name.split()
     if "." in name:
        name = text[0] + " " + text[2]
     firstName = name[0: name.index(" ")]
     lastName = name[name.index(" ")+1 : len(name)]
     return firstName + " " + lastName 

#function to check if the name is contained in the link
def checkLink(link,name):
     text = name.split()
     if "." in name:
        name = text[0] + " " + text[2]
     firstName = name[0: name.index(" ")]
     lastName = name[name.index(" ")+1 : len(name)]
     firstName = firstName.lower()
     lastName = lastName.lower()

     if firstName in link and lastName in link:
          return True
     else:
          return False


# Function to search Google Custom Search and extract LinkedIn URL
def search_and_get_linkedin_profile(Name, Major, Year):
    linkedin_url = "NOT FOUND"
    linkedin_url1 = ""
    linkedin_url2 = ""
    Name = splitName(Name)
    search_query = f"{Name} {Major} {Year} Purdue LinkedIn"
    api_url = f"https://www.googleapis.com/customsearch/v1?q={search_query}&key={API_KEY}&cx={CSE_ID}"

    try:
        response = requests.get(api_url)
        data = response.json()
        # Extract the first LinkedIn URL from the search results (if available)
        if 'items' in data and len(data['items']) > 0:
            linkedin_url = data['items'][0]['link']
            if checkLink(linkedin_url, Name) is False : #handles if u got a link but its the wrong one
                 search_query = f"{Name} {Major} Purdue LinkedIn"
                 api_url = f"https://www.googleapis.com/customsearch/v1?q={search_query}&key={API_KEY}&cx={CSE_ID}"
                 response = requests.get(api_url)
                 data = response.json()
                 if 'items' in data and len(data['items']) > 0:
                    linkedin_url = data['items'][0]['link']
                    if checkLink(linkedin_url, Name) is False:
                        search_query = f"{Name}"
                        api_url = f"https://www.googleapis.com/customsearch/v1?q={search_query}&key={API_KEY}&cx={CSE_ID}"
                        response = requests.get(api_url)
                        data = response.json()
                        #getting first 3 instead of 1 bc when u j search name theres more chance of inaccuracy
                        if 'items' in data and len(data['items']) > 0:
                                linkedin_url = data['items'][0]['link']
                                linkedin_url1 = data['items'][1]['link']
                                linkedin_url2 = data['items'][2]['link']


                        if(checkLink(linkedin_url, Name)) is True:
                              linkedin_url = linkedin_url #continue
                        elif(checkLink(linkedin_url1, Name)) is True:
                              linkedin_url = linkedin_url1
                        elif(checkLink(linkedin_url2, Name)) is True:
                              linkedin_url = linkedin_url2
                        else:
                                linkedin_url = "NOT FOUND"
                
        else: #handles if you didn't get a link
            search_query = f"{Name} {Major} Purdue LinkedIn"
            api_url = f"https://www.googleapis.com/customsearch/v1?q={search_query}&key={API_KEY}&cx={CSE_ID}"
            response = requests.get(api_url)
            data = response.json()
            if 'items' in data and len(data['items']) > 0:
                    linkedin_url = data['items'][0]['link']
            if checkLink(linkedin_url, Name) is False:
                        search_query = f"{Name}"
                        api_url = f"https://www.googleapis.com/customsearch/v1?q={search_query}&key={API_KEY}&cx={CSE_ID}"
                        response = requests.get(api_url)
                        data = response.json()
                        if 'items' in data and len(data['items']) > 0:
                                linkedin_url = data['items'][0]['link']
                                linkedin_url1 = data['items'][1]['link']
                                linkedin_url2 = data['items'][2]['link']

                        if(checkLink(linkedin_url, Name)) is True:
                              linkedin_url = linkedin_url #continue
                        elif(checkLink(linkedin_url1, Name)) is True:
                              linkedin_url = linkedin_url1
                        elif(checkLink(linkedin_url2, Name)) is True:
                              linkedin_url = linkedin_url2
                        else:
                                linkedin_url = "NOT FOUND"
            

    except Exception as e:
        print(f"Error: {e}")
        linkedin_url = ""
    
    return linkedin_url


    
         
# Add a new 'LinkedIn' column with profile URLs to the input.csv file
df['LinkedIn'] = df.apply(lambda row: search_and_get_linkedin_profile(row['Name'], row['Major'], row['Year']), axis=1)

df.to_csv(input_file, index=False)
