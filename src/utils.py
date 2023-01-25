
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

from time import sleep
from selenium.webdriver.common.by import By
import re
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

def get_driver():
    s = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=s, options=options)
    return driver

def click_by_text(css_selector, text, driver):
    driver.execute_script(f"""
    let elts = document.querySelectorAll('{css_selector}')
elts.forEach((elt)=>{{
  if(elt.innerText.includes('{text}'))
      elt.click()
}})""")

def navigate_by_text(css_selector, text, driver):
    click_by_text(css_selector, text, driver)
    sleep(0.5)

def click(css_selector, driver):
    driver.execute_script(f"""
    let elt = document.querySelector('{css_selector}')
    elt.click()
    """)
    # driver.find_element(By.CSS_SELECTOR, css_selector).click()

def set_select_value(css_selector, value, driver):
    from selenium.webdriver.support.ui import Select
    #driver.execute_script(f"""let elt = document.querySelector('{css_selector}')
    #elt.value = '{value}'""")
    s = Select(driver.find_element(By.CSS_SELECTOR, css_selector))
    s.select_by_value(value)

def element_exists(css_selector, regexp, driver):
    browser = driver
    elts = browser.execute_script(f"return document.querySelectorAll('{css_selector}')")
    cmp = re.compile(regexp)
    for elt in elts:
        if cmp.match(elt.text):
            return True
    return False

def send_keys(css_selector, text, driver):
    driver.find_element(By.CSS_SELECTOR, css_selector).send_keys(text)
