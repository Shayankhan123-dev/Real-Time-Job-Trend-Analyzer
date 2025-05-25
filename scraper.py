from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time
from datetime import datetime

def scrape_linkedin_jobs(username, password, search_term="Python Developer", location="Pakistan", num_jobs=100):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)

    # Step 1: Login
    driver.get("https://www.linkedin.com/login")
    time.sleep(2)

    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "password").send_keys(Keys.RETURN)
    time.sleep(3)

    # Step 2: Search jobs
    search_url = f"https://www.linkedin.com/jobs/search/?keywords={search_term}&location="

    driver.get(search_url)
    time.sleep(5)

    jobs = []
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    listings = soup.select("ul.jobs-search__results-list li")[:num_jobs]

    for job in listings:
        try:
            title = job.select_one("h3").get_text(strip=True)
            company = job.select_one("h4").get_text(strip=True)
            loc = job.select_one("span.job-search-card__location").get_text(strip=True)
            date_posted = job.select_one("time").get("datetime")
            job_url = job.select_one("a")["href"]

            jobs.append({
                "title": title,
                "company": company,
                "location": loc,
                "date_posted": date_posted,
                "job_url": job_url,
                "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        except Exception as e:
            print(f"Skipping one due to error: {e}")

    driver.quit()

    df = pd.DataFrame(jobs)
    df.to_csv("linkedin_jobs.csv", index=False)
    print(f"[✓] Scraped {len(jobs)} jobs to linkedin_jobs.csv")

if __name__ == "__main__":
    # Replace with your LinkedIn credentials
    linkedin_user = "your_email@example.com"
    linkedin_pass = "your_password"
    scrape_linkedin_jobs(linkedin_user, linkedin_pass)
