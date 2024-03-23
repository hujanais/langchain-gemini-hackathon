from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
# from bs4 import BeautifulSoup
import time

# def scrape_bundeswehr_jobs(url):
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all job cards
        job_cards = soup.find_all("div", class_="infos")
        # print(job_cards)
        # Iterate over each job card and extract information
        job_data = []
        for job_card in job_cards:
            job_title_tag = job_card.find('h3', class_='jobtitle')
             # Extract job title and link
            job_title = job_title_tag.text.strip()
            
            job_link = job_title_tag.a.get("href")
            print(job_link)
            # print(job_link)
        # Print job title and link
        # print("Job Title:", job_title)
        # print("Job Link:", "https://www.bundeswehrkarriere.de" + job_link)
        # print()
        
        return job_data
    else:
        print("Failed to retrieve data from the URL:", url)
        return None

# URL of the website to scrape
url = 'https://www.bundeswehrkarriere.de/jobs/unsere-jobs'

# Scrape the job information
# jobs = scrape_bundeswehr_jobs(url)
# Simulate clicking the "Load More" button and scrape additional jobs
# Create a new instance of Chrome driver
custom_options = webdriver.ChromeOptions()
prefs = {
  "translate_whitelists": {"de":"en"},
  "translate":{"enabled":"true"}
}
custom_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(options=custom_options)
driver.get(url)

# Cookies
cookies = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div[2]/a[3]"))
)
time.sleep(5)
cookies.click()
  
# # Find the "Load More" button
load_more_button = WebDriverWait(driver, 40).until(
    EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/section/section/section/section[2]/div/div/div/div/div[3]/button"))
)

print(load_more_button.is_displayed())

# # Click the "Load More" button until it is not visible
# while load_more_button.is_displayed():
#     # Click the button to load more jobs
#     print(load_more_button.is_displayed())
#     time.sleep(10)
#     load_more_button.click()

    
#     # Scrape jobs from the current page

# Find all job titles with class name "jobtitle"
# job_titles = driver.find_elements(By.CLASS_NAME,"jobtitle")

# # Extract URLs from job titles
# job_urls = [title.find_element(By.TAG_NAME,"a").get_attribute("href") for title in job_titles]

len(job_titles)





job_id=1
for u in job_urls:
    print(u)
    driver.get(u)
    time.sleep(5)

    try:
        Page_title=driver.find_element(By.TAG_NAME, 'h1').text
        Page_paragraph=driver.find_element(By.TAG_NAME, 'p').text

        p0=driver.find_element(By.CLASS_NAME, 'field-items').find_elements(By.TAG_NAME, 'p')[0].text
        ul0=driver.find_element(By.CLASS_NAME, 'field-items').find_elements(By.TAG_NAME, 'ul')[0].text

        p1=driver.find_element(By.CLASS_NAME, 'field-items').find_elements(By.TAG_NAME, 'p')[1].text
        ul1=driver.find_element(By.CLASS_NAME, 'field-items').find_elements(By.TAG_NAME, 'ul')[1].text

        p2=driver.find_element(By.CLASS_NAME, 'field-items').find_elements(By.TAG_NAME, 'p')[2].text
        ul2=driver.find_element(By.CLASS_NAME, 'field-items').find_elements(By.TAG_NAME, 'ul')[2].text

        # File Saving
        file_name="C:/Users/sanmomin/Downloads/GenAI/German Job/Job " + str(job_id) + ".md"
        f=open(file_name, "a")
        f.write("**Title**")
        f.write("\n"+Page_title+"\n")
        f.write("\n"+Page_paragraph+"\n")

        f.write("\n**"+p0+"**\n")
        f.write("\n"+ "-\t"+ul0.replace("\n","\n-\t") +"\n")
        f.write("\n**"+p1+"**\n")
        f.write("\n"+ "-\t"+ul1.replace("\n","\n-\t") +"\n")
        f.write("\n**"+p2+"**\n")
        f.write("\n"+ "-\t"+ul2.replace("\n","\n-\t") +"\n")

        f.close()
        job_id=job_id+1
    except:
        job_id=job_id+1
        pass

# # # Close the browser
# scrape_bundeswehr_jobs(html_content)
# driver.quit()

# Print the scraped job information
# if jobs:
#     for job in jobs:
#         print(job)
