import requests
from bs4 import BeautifulSoup
import pandas as pd
import urllib
import nltk
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import RegexpTokenizer
from collections import Counter
import sys

job_links = []
jobs = []
jds = []
role = str(sys.argv[1])
location = str(sys.argv[2])

for i in range(10):
    base_url = 'https://www.linkedin.com/jobs/search/?'
    query_params = {
    'keywords': role,
    'location': location,
    'sortBy': 'R',
    'f_TPR': 'r604800', # Jobs posted in the last week
    'start': str((i+1)*25)
    }

    # Create the final URL by concatenating the base URL and the encoded query parameters
    url = base_url + urllib.parse.urlencode(query_params)
    response = requests.get(url)
    soup = BeautifulSoup(response.content,'html.parser')
    job_divs = soup.find_all('div', {'class': 'base-card'})

    for job_div in job_divs:
        job_link = job_div.find('a', {'class': 'base-card__full-link'})['href']
        job_links.append(job_link)

def get_job_info(url):
    # make a GET request to the URL
    response = requests.get(url)

    # parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")
    
    # extract the job title
    job_title_elem = soup.find("h1", class_="topcard__title")
    job_title = job_title_elem.get_text().strip() if job_title_elem else "Not available"
    # extract the company name
    company_name_elem = soup.find("a", class_="topcard__org-name-link")
    company_name = company_name_elem.get_text().strip() if company_name_elem else "Not available"

    # extract the job location
    job_location_elem = soup.find("span", class_="topcard__flavor topcard__flavor--bullet")
    job_location = job_location_elem.get_text().strip() if job_location_elem else "Not available"

    # extract the job description
    job_description_elem = soup.find("div", class_="show-more-less-html__markup show-more-less-html__markup--clamp-after-5")
    job_description = job_description_elem.get_text().strip() if job_description_elem else "Not available"

    # extract the hiring person's name
    hiring_person_elem = soup.find('a', {'class': 'message-the-recruiter__cta'})
    hiring_person = hiring_person_elem['aria-label'][8:] if hiring_person_elem else "Not available"

    # extract the link to message the recruiter
    message_recruiter_elem = soup.find('a', {'class': 'message-the-recruiter__cta'})
    message_recruiter_link = message_recruiter_elem['href'] if message_recruiter_elem else "Not available"
    
    
    # Extract the number of applicants
    num_applicants_elem = soup.find('span', {'class': 'topcard__flavor--metadata topcard__flavor--bullet num-applicants__caption'})
    num_applicants = num_applicants_elem.text.strip() if num_applicants_elem else "Not available"

    # Extract the job posting time
    job_posting_time_elem = soup.find('span', {'class': 'posted-time-ago__text'})
    job_posting_time = job_posting_time_elem.text.strip() if job_posting_time_elem else "Not available"
    
    # print the extracted information
    job = {}
    
    job["Job_Title"] =  job_title
    job["Company_Name"] =  company_name
    job["Job_Description"] = job_description
    job["Job_Location"] =  job_location
    job["Hiring_Person"] = hiring_person
    job["Message_Recruiter_Link"] = message_recruiter_link
    job["Time"] = job_posting_time
    job["Number_Of_Applicants"] = num_applicants
    job['link'] = url
    
    return job
    #print("Company Name:", company_name)
    #print("Job Location:", job_location)
    #print("Job Description:", job_description)
    #print("Hiring Person:", hiring_person)
    #print("Message Recruiter Link:", message_recruiter_link) 


for i in job_links:
    jobs.append(get_job_info(i))
    
for i in jobs:
    jds.append(i['Job_Description'])

string = "".join(jds)

# Remove non-letter symbols from the string using NLTK's RegexpTokenizer
tokenizer = RegexpTokenizer(r'\w+')
words = tokenizer.tokenize(string.lower())

# Remove stop words (generic words) from the list of words
stop_words = set(stopwords.words('english'))
words = [word for word in words if word not in stop_words]

# Count the frequency of each word
word_counts = Counter(words)

# Get the 10 most common words
most_common_words = word_counts.most_common(100)


pd.DataFrame(most_common_words,columns=['words','frequency']).to_csv('common_jd_words.csv')
pd.DataFrame(jobs).to_csv('jobs.csv')
