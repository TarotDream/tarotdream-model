from selenium import webdriver
import time
from selenium.webdriver.common.by import By

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=chrome_options)
# driver = webdriver.Chrome(executable_path=r'/usr/bin/chromedriver', chrome_options=chrome_options)
driver.maximize_window()

def kor_to_eng_translation(text) :
    try : 
        driver.get('https://papago.naver.com/?sk=ko&tk=en&st='+text)
        time.sleep(1)
        trans = driver.find_element(By.XPATH, '//*[@id="txtTarget"]').text
    except :
        driver.get('https://papago.naver.com/?sk=ko&tk=en')
        time.sleep(1)
        driver.find_element(By.XPATH, '//*[@id="txtSource"]').send_keys(text)
        # driver.find_element_by_xpath('//*[@id="txtSource"]').send_keys(text)
        # trans = driver.find_element_by_xpath('//*[@id="txtTarget"]').text
        trans = driver.find_element(By.XPATH, '//*[@id="txtTarget"]').text
    return trans

def eng_to_kor_translation(text) :
    try:
        driver.get('https://papago.naver.com/?sk=en&tk=ko&st='+text)
        time.sleep(1)
        trans = driver.find_element(By.XPATH, '//*[@id="txtTarget"]').text
    except:
        driver.get('https://papago.naver.com/?sk=en&tk=ko')
        time.sleep(1)
        driver.find_element(By.XPATH, '//*[@id="txtSource"]').send_keys(text)
        trans = driver.find_element(By.XPATH, '//*[@id="txtTarget"]').text   
    return trans