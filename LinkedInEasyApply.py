import time
import json
import pickle
import JobData
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
'''
Reference: https://stackoverflow.com/questions/37088589/selenium-wont-open-a-new-url-in-a-new-tab-python-chrome
https://stackoverflow.com/questions/28431765/open-web-in-new-tab-selenium-python
https://stackoverflow.com/questions/39281806/python-opening-multiple-tabs-using-selenium
'''
username =  "# your email here"
password =  "# your password here"

def init_driver():
    driver = webdriver.Chrome(executable_path = "./chromedriver")
    driver.wait = WebDriverWait(driver, 10)
    return driver
#enddef

def login(driver, username, password):
    driver.get("https://www.linkedin.com/")
    try:
        user_field = driver.find_element_by_class_name("login-email")
        pw_field = driver.find_element_by_class_name("login-password")
        login_button = driver.find_element_by_id("login-submit")
        user_field.send_keys(username)
        user_field.send_keys(Keys.TAB)
        time.sleep(1)
        pw_field.send_keys(password)
        time.sleep(1)
        login_button.click()
    except TimeoutException:
        print("TimeoutException! Username/password field or login button not found on glassdoor.com")
#enddef

def isElementPresentByClassName(driver, classname):
    try:
        driver.find_element_by_class_name(classname)
    except:
        print ('No such thing')
        return False
    return True

def gotojobs(driver):
    driver.get("https://www.linkedin.com/jobs")
    a=[]
    a = driver.find_elements_by_class_name("ember-text-field")
    for i in a:
        print i.get_attribute("id")
    jobDescField = a[0]
    locField = a[1]
    search_button = driver.find_element_by_class_name("submit-button")
    jobDescField.send_keys("Software Developer") # Desired Job Title
    jobDescField.send_keys(Keys.TAB)
    time.sleep(1)
    locField.send_keys("San Francisco Bay Area") # Desired Location
    time.sleep(1)
    search_button.click()
    time.sleep(2)   
    j=0
    linkslist = []
    while True:
        scheight = .1
        while scheight < 9.9:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight/%s);" % scheight)
            scheight += .01
        alljobsonpage = driver.find_elements_by_class_name("card-list__item")
        for i in alljobsonpage:
            try:
                easyapply = i.find_element_by_class_name("job-card__easy-apply-text")
                link = i.find_element_by_class_name("job-card__link-wrapper")
                print(link.get_attribute('href'))
                linkslist.append(link.get_attribute('href'))
            except:
                print("Not Easy Apply")
            print("____________________________")
        loopThroughJobs(driver,linkslist)
        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            print("Next Button")
            
            nextButton = driver.find_element_by_class_name('next')
            nextButton.click()
            del linkslist[:]
        except:
            break
        
    print("____________________________")


def loopThroughJobs(driver,jobsList):
    for i in jobsList:
        if(applyToJob(driver,i)):
            continue
    allwindows = driver.window_handles
    if(len(allwindows) == 2):
        driver.switch_to_window(allwindows[1])
        driver.close()
        driver.switch_to_window(allwindows[0])


def applyToJob(driver,job):
    
    window_before = driver.window_handles[0]
    execScript = "window.open('"+job+"', 'CurrJob');"
    driver.execute_script(execScript)
    window_after = driver.window_handles[1]
    driver.switch_to_window(window_after)
    time.sleep(3)
    # Dont Change This setting
    scheight = 4
    while scheight < 9.9:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/%s);" % scheight)
        scheight += 4

    driver.execute_script("window.scrollTo(0, 0);")
    try:
        div = driver.find_element_by_class_name("jobs-details-top-card__actions")
        applyButton = div.find_element_by_class_name("jobs-s-apply__button")
        applyButton.click()
        time.sleep(2)
    except:
        print("Found None")


    try:
        driver.find_element_by_css_selector('input[type="file"]').clear()
        driver.find_element_by_css_selector('input[type="file"]').send_keys("/Users/narenuday/Desktop/Active Resume/Uday Resume.docx")
        time.sleep(3)
        submitButton = driver.find_element_by_class_name('jobs-apply-form__submit-button')
        submitButton.click()
        time.sleep(1)
        return True
        
    except:
        allwindows = driver.window_handles
        if(len(allwindows) == 3):
            currWindow  = allwindows[2]
            driver.switch_to_window(currWindow)
            driver.close()
            driver.switch_to_window(window_after)
        return False
    driver.close()
    return False

if __name__ == "__main__":
    driver = init_driver()
    time.sleep(3)
    print "Logging into Linkedin account ..."
    login(driver, username, password)
    time.sleep(1)
    gotojobs(driver)



