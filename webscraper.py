import selenium
import json
import sys
import argparse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
# py scraper.py
# Arguments:
# --url, -u: Uri of the website to be scraped
# --size, -s: Number of pages to be scraped
# --help, -h: Prints help menu

data = {}
url = None
pages = 0

menu = '''
Required arguments: \n
\t--url, -u: Url of the website to be scraped \n
\t--size, -s: Number of pages to be scraped \n

Optional arguments: \n
--help, -h: Prints help menu \n
'''

parser = argparse.ArgumentParser(description=menu)

parser.add_argument("-u", "--url", help="Url of the website to be scraped")
parser.add_argument("-s", "--size", help="Number of pages to be scraped")


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get(url)


def get_reviews(url, pages):
    data = {}
    for x in range(20):
        try:
            elem = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CLASS_NAME, "Review")))

            review_element = driver.find_element(By.CLASS_NAME, "Review")
            review_element_id = review_element.get_attribute("data-review-id")

            review__header = review_element.find_elements(
                By.CLASS_NAME, "Review__header")
            review__container = review_element.find_elements(
                By.CLASS_NAME, "Review__container")
            review__dateSource = review_element.find_elements(
                By.CLASS_NAME, "Review__dateSource")

            review_name = review__header[0].text
            review_content = review__container[0].text
            review_date = review__dateSource[0].text

            re = review_content.replace("\n", " ")
            re = re.replace(review_date, "")

            data[f"Review No: {x}"] = {"Name": review_name,
                                       "Content": re, "Date Posted": review_date}

            driver.execute_script(
                '''document.getElementsByClassName("Review")[0].remove();''')
        except:
            driver.close()

    data[f"{pages}"] = data
    driver.implicitly_wait(10)


for p in range(pages):
    get_reviews(url, p)
    next_button = driver.find_element(By.LINK_TEXT, "»")
    next_button.click()

driver.close()

# Dump Data
with open('reviews.json', 'w') as outfile:
    json.dump(data, outfile)
