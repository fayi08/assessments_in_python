from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Initialize WebDriver
def initialize_driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    return driver

# Search for amazon basics
def search_amazon_basics(driver):
    driver.get("https://www.amazon.com/")
    search_input = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "twotabsearchtextbox")))
    search_input.send_keys("amazon basics")
    search_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "nav-search-submit-button")))
    search_button.click()

# Verify that the results for amazon basics are displayed on the top of the page
def verify_search_results(driver):
    search_results_text = WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CLASS_NAME, "a-color-state.a-text-bold"), "amazon basics"))
    assert search_results_text, "Search results for 'amazon basics' are displayed on the top of the page below the menu bar."

# Filter search results by Amazon Brands
def filter_by_amazon_brands(driver):
    checkbox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//li[@aria-label="Amazon Brands"]//input[@type="checkbox"]')))
    driver.execute_script("arguments[0].scrollIntoView();", checkbox)
    driver.execute_script("arguments[0].click();", checkbox)

# Verify if the checkbox is checked after clicking
def verify_checkbox_state(driver):
    checkbox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//li[@aria-label="Amazon Brands"]//input[@type="checkbox"]')))
    is_checked = checkbox.is_selected()
    assert is_checked, "Checkbox is checked after clicking."
    print("Is checkbox checked:", is_checked)

# Click on an Amazon Basics product
def click_amazon_basics_product(driver):
    product_link = driver.find_element(By.XPATH, '//a[contains(@href, "/Amazon-Basics-Freezer-Gallon-Count/dp/B093WPZF1Y")]')
    product_link.click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "add-to-cart-button")))


# Select the product size and verify
def select_and_verify_product_size(driver):
    button_element = driver.find_element(By.ID, "a-autoid-10")
    if "a-button-selected" not in button_element.get_attribute("class"):
        button_element.click()
        print("Clicked on Gallon (90 Count) button")
    button_element.click()

    size_element = driver.find_element(By.XPATH, '//span[@class="selection"]')
    selected_size = size_element.text
    expected_size = "Gallon (90 Count)"
    assert selected_size == expected_size, f"Expected size: '{expected_size}', Actual size: '{selected_size}'"
    print("Selected size verified:", selected_size)

# Add the product to the cart
def add_to_cart(driver):
    add_to_cart_button = driver.find_element(By.ID, "add-to-cart-button")
    add_to_cart_button.click()
    WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.ID, "nav-cart-count"), "1"))

# Navigate to the cart
def navigate_to_cart(driver):
    go_to_cart_button = driver.find_element(By.XPATH, '//a[@href="/cart?ref_=sw_gtc"]')
    go_to_cart_button.click()
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "sc-subtotal-amount-activecart")))

# Verify the subtotal
def verify_subtotal(driver):
    subtotal_element = driver.find_element(By.ID, "sc-subtotal-amount-activecart")
    subtotal_text = subtotal_element.text
    price = "$13.35"
    assert price in subtotal_text, f"Expected subtotal: '{price}', Actual subtotal: '{subtotal_text}'"
    print("9. Verify the subtotal:", subtotal_text)

def amazon_cart_test():
    
    try:
        driver = initialize_driver()
        search_amazon_basics(driver)
        verify_search_results(driver)
        filter_by_amazon_brands(driver)
        verify_checkbox_state(driver)
        click_amazon_basics_product(driver)
        select_and_verify_product_size(driver)
        add_to_cart(driver)
        navigate_to_cart(driver)
        verify_subtotal(driver)
    finally:
        driver.quit()

if __name__ == "__main__":
    amazon_cart_test()
