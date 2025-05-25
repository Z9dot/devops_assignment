import time
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("http://localhost:5000")
time.sleep(1)

assert "Sample App" in driver.page_source

input_field = driver.find_element(By.NAME, "item")
input_field.send_keys("Test Item")
driver.find_element(By.TAG_NAME, "button").click()
time.sleep(1)

driver.refresh()
time.sleep(1)
assert "Test Item" in driver.page_source
driver.quit()
