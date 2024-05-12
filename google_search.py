from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def initialize_driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    return driver

def go_to_google_site(driver):
    driver.get("https://www.google.com/")
    title = driver.title
    assert "Google" in title, "Failed to navigate to Google site."

def search_for_keyword(driver, keyword):
    time.sleep(2)  
    search_input = driver.find_element(By.CSS_SELECTOR, 'textarea[name="q"]')
    search_input.send_keys(keyword)
    
    # Wait for the search button to be clickable
    search_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[value="Google Search"]')))
    search_button.click()
    
    title = driver.title
    assert keyword in title, f'Failed to search for the keyword "{keyword}".'

def select_udemy_course_link(driver):
    udemy_link = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//span[text()="Udemy"]')))
    udemy_link.click()

def verify_udemy_site(driver):
    time.sleep(2) 
    udemy_logo = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'img[alt="Udemy"]')))
    assert udemy_logo, 'Udemy page is not opened'

def search_for_bdd_with_cucumber(driver, keyword):
    time.sleep(2)  
    search_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-testid="search-input"]')))
    search_input.send_keys(keyword)
    print(f"Search for '{keyword}'")
    search_and_verify_course_page(driver)

def search_and_verify_course_page(driver):
    WebDriverWait(driver, 80).until(EC.presence_of_element_located((By.ID, 'challenge-stage')))
def click_on_course_with_highest_rating(driver):
    # Wait for the search results page to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h1[data-purpose="safely-set-inner-html:search:query"]')))
    
    # Find all course cards
    course_cards = driver.find_elements(By.CSS_SELECTOR, '.course-card-module--container--3oS-F')
    max_rating = 0
    max_rating_course_index = -1
    
    # Iterate through each course card to find the one with the highest rating
    for i, course_card in enumerate(course_cards):
        rating_element = course_card.find_element(By.CSS_SELECTOR, 'span[data-purpose="rating-number"]')
        rating = float(rating_element.text)
        if rating > max_rating:
            max_rating = rating
            max_rating_course_index = i
    
    if max_rating_course_index != -1:
        # Click on the course with the highest rating
        course_cards[max_rating_course_index].click()
        print(f"Step 6: Clicked on the course with the highest rating ({max_rating})")
    else:
        print('Step 6: No courses found')

def verify_course_page(driver, expected_course_name):
    time.sleep(10)
    WebDriverWait(driver, 30).until(EC.url_contains('/course/'))
    
    # Get the course title element
    course_title_element = driver.find_element(By.CSS_SELECTOR, 'h1[data-purpose="lead-title"]')
    assert course_title_element, 'Course title element not found'
    course_title = course_title_element.text
    assert expected_course_name in course_title, f'Course name does not contain "{expected_course_name}"'
    print(f"Step 7: Verified that the course page is opened and the course name contains \"{expected_course_name}\"")

def run_google_search_test():
    try:
        driver = initialize_driver()
        go_to_google_site(driver)
        search_for_keyword(driver, "Test Automation Learning")
        select_udemy_course_link(driver)
        verify_udemy_site(driver)
        search_for_bdd_with_cucumber(driver, "BDD with Cucumber")
        click_on_course_with_highest_rating(driver)
        verify_course_page(driver, "BDD with Cucumber")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_google_search_test()
