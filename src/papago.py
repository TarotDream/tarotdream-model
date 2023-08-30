from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# driver = webdriver.Chrome(options=chrome_options)
# driver = webdriver.Chrome(executable_path=r'/usr/bin/chromedriver', chrome_options=chrome_options)
# driver.maximize_window()

def kor_to_eng_translation(text) :
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    try : 
        
        driver.get('https://papago.naver.com/?sk=ko&tk=en&st='+text)
        time.sleep(5)  # Increase sleep time to allow for page load
        trans_element = driver.find_element(By.XPATH, '//*[@id="txtTarget"]')
        trans = trans_element.text
    except :
        driver.get('https://papago.naver.com/?sk=ko&tk=en')
        time.sleep(5)  # Increase sleep time to allow for page load
        source_element = driver.find_element(By.XPATH, '//*[@id="txtSource"]')
        source_element.send_keys(text + Keys.RETURN)  # Pressing Enter after input
        trans_element = driver.find_element(By.XPATH, '//*[@id="txtTarget"]')
        trans = trans_element.text
    driver.quit()
    return trans

def eng_to_kor_translation(text):
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    try:
        driver.get('https://papago.naver.com/?sk=en&tk=ko&st=' + text)
        time.sleep(5)
        trans_element = driver.find_element(By.XPATH, '//*[@id="txtTarget"]')
        trans = trans_element.text
    except:
        driver.get('https://papago.naver.com/?sk=en&tk=ko')
        time.sleep(5)
        source_element = driver.find_element(By.XPATH, '//*[@id="txtSource"]')
        source_element.send_keys(text + Keys.RETURN)  # Pressing Enter after input
        trans_element = driver.find_element(By.XPATH, '//*[@id="txtTarget"]')
        trans = trans_element.text
    driver.quit()
    return trans