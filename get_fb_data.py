from bs4 import BeautifulSoup as Soup
from selenium import webdriver 
from selenium.common.exceptions import NoSuchElementException 
from selenium.webdriver.common.keys import Keys
import requests
import selenium.webdriver.support.ui as ui
import time
import random
import csv
from selenium.webdriver.common.action_chains import ActionChains 
import re
import traceback

def fetch_fb_details(user_details, username, passwd):
    
    print "Browser initiated don't play with the system for a while (Code may fail incase of slow internet!)"
    print "If code fails then run code again after a while."

    profile = webdriver.FirefoxProfile()
    browser = webdriver.Firefox(firefox_profile=profile)

    logiun_url = "http://www.facebook.com"
    browser.get(logiun_url)

    print "Logging in...."
    try:
        print "Entering email and passwd"
        elem = browser.find_element_by_name('email')
        elem.send_keys(username)
        ps = browser.find_element_by_name('pass')
        ps.send_keys(passwd + Keys.RETURN)
        time.sleep(1)
    except:
        print "Invalid credentials !"
        return
  
    print "Searching for username...."
    users_fb_url = []
    for each_user in user_details:
        try:
            time.sleep(1)
            print "Searching for " + each_user + " on facebook !"
            find_url = "http://www.facebook.com/search/str/results/?q=" + each_user
            browser.get(find_url)
            source = browser.page_source.encode('utf-8')
            soup = Soup(source,"html.parser")
            div = soup.find("div",attrs={"class":"_gll"})
            user_profiles = str(div)
            userid_pattern = re.compile('https://www.facebook.com/[0-9A-Za-z.]+[?]')
            user_ids = userid_pattern.findall(user_profiles)
            users_fb_url.append([each_user] + user_ids)
        except:
            users_fb_url.append([each_user] + [])
    
    writer = csv.writer(open("user_details.csv", "ab"))

    print "Getting user's public information...."
    for row in users_fb_url:
        try:
            url = row[1]
            detail = row[0]
            handle = str(url).split('/')[-1].replace('?', '')
            browser.get(url)
            source = browser.page_source.encode('utf-8')
            soup = Soup(source, "html.parser")
            raw = soup.find('div',{'class':'_1zw4 _1kny'})
            basic_info = raw.find_all('li')
            data = [detail, handle]
            print (handle)
            for each in basic_info:
                info = each.text.encode('utf-8')
                data.append(info)
            writer.writerow(data)
        except:
            traceback.print_exc()
            print "Can not open the profile !"
            pass
    
    browser.quit()
    print "Exploration done ! "
    print "Check user_details.csv for user's info."
    


if __name__ == '__main__':

    # username = 'nishasingh270492@gmail.com'
    # passwd = 'popjohn92'
    
    fp = open("credentials.txt","rU")
    lines = fp.readlines()
    fp.close()
    
    fp = open("user_search_info.txt", "rU")
    user_details = fp.readlines()
    fp.close()
    
    try:
        username = lines[0].strip()
        passwd = lines[1].strip()
        user_search_info = [detail.strip() for detail in user_details]
    except:
        print "Check the credentials file."

    fetch_fb_details(user_search_info, username, passwd)
