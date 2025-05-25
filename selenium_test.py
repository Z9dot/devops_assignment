import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--remote-debugging-port=9222")
chrome_options.add_argument("--user-data-dir=/tmp/chrome-user-data")

driver = webdriver.Chrome(options=chrome_options)

try:
    driver.get("http://localhost:5000")
    time.sleep(2)
    
    assert "Sample App" in driver.page_source, "Sample App not found in page"
    print("✓ Sample App found on page")
    
    input_field = driver.find_element(By.NAME, "item")
    input_field.send_keys("Test Item")
    
    driver.find_element(By.TAG_NAME, "button").click()
    time.sleep(2)
    
    driver.refresh()
    time.sleep(2)
    
    assert "Test Item" in driver.page_source, "Test Item not found after submission"
    print("✓ Test Item successfully added and found")
    
    print("All Selenium tests passed!")

except Exception as e:
    print(f"❌ Selenium test failed: {e}")
    raise

finally:
    driver.quit()
