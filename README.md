# LinkedInJobScraper
Give Job title and Location, get valuable job insights for both job seekers and providers

This is a Python script that scrapes job listings from LinkedIn based on the job title and location provided as system inputs. It uses the requests and BeautifulSoup libraries to scrape and parse HTML content from LinkedIn. It also uses the pandas library to store the scraped data as CSV files, and the nltk library to perform text analysis on the job descriptions.
Usage

To use this script, run it in the command line and provide the job title and location as system inputs. For example:

python

    python jobs.py "Data Analyst" "San Francisco, CA"

The script will scrape the first 250 job listings that match the provided search criteria (25 listings per page, up to 10 pages) and extract the following information for each job:

    Job title
    Company name
    Job location
    Job description
    Hiring person's name
    Link to message the recruiter
    Number of applicants
    Job posting time

The scraped data will be stored in two CSV files: jobs.csv and common_jd_words.csv.

The jobs.csv file will contain all of the scraped job information, with each row representing a single job listing.

The common_jd_words.csv file will contain the 100 most common words found in the job descriptions, along with their frequency.
Dependencies

This script requires the following Python libraries:

    requests
    beautifulsoup4
    pandas
    nltk

These can be installed using pip:

pip install requests beautifulsoup4 pandas nltk



