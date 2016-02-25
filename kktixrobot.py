#!/usr/bin/env python

import argparse
import ConfigParser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# read and check config
config = ConfigParser.ConfigParser()
config.read(["./info.ini"])
person_info = config.items("person")
buying_info = dict(config.items("ticket"))
for sec in ["ticket-wanted", "number-wanted"]:
    buying_info[sec] = [ int(x) for x in buying_info[sec].split(',') ]
assert sum(buying_info["number-wanted"]) + 1 == len(person_info)
landing_url = buying_info["url"]

# landing
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)
driver.get(landing_url)

# click the right button for ticket reservation
    # the button seems to be one of class "btn-point" or "btn-ticket"
    # but the urls always give the same trailing path
all_hrefs = driver.find_elements_by_xpath("//*[@href]")
all_links = [ link.get_attribute("href") for link in all_hrefs ]
link_for_reserve = [ x for x in all_links if "/registrations/new" in x ][0]
driver.get(link_for_reserve)

# handle pop-up for non-member user
popup = wait.until(EC.presence_of_element_located((By.ID, "guestModalLabel")))
popup = driver.switch_to_active_element()
popup.click() # registration pop-up: No for now

# handle checkbox of Terms of Services
terms_agree = wait.until(EC.element_to_be_clickable((By.ID, "person_agree_terms")))
terms_agree.click()

# add tickets
tickets = driver.find_elements_by_css_selector(".ticket-unit")
for t, n in zip(buying_info["ticket-wanted"], buying_info["number-wanted"]):
    tickets_wanted = tickets[t-1]
    btn_add_ticket = tickets_wanted.find_element_by_css_selector(".btn-default.plus")
    for i in xrange(n):
        btn_add_ticket.click()

# go to info fill-out page
btn_next_step = driver.find_element_by_css_selector("button.btn.btn-primary")
btn_next_step.click()

# fill-in information
form = driver.find_elements_by_css_selector(".col-6.ng-pristine.ng-valid")
pinfo = [ p[1].split(',') for p in person_info ]
for f, v in zip(form, [ p for subl in pinfo for p in subl ]):
    f.send_keys(v)

# confirm form
btn_confirm = driver.find_element_by_css_selector("a.btn.btn-primary.btn-lg")
# btn_confirm.click()



