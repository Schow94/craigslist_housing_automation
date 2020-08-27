from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os
import time

# from selenium.webdriver import Firefox
from send_email import test_sendmail

# driver = webdriver.Chrome('./chromedriver')
options = Options()
options.headless = True
driver = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver", options=options)

# driver = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver")

# driver = Firefox()
# CHANGE URL IF YOU WANT TO USE A DIFFERENT LOCATION
url = 'https://sfbay.craigslist.org/d/housing/search/hhh'
driver.get(url)

# MODIFY THESE PARAMETERS TO YOUR PREFERENCE
county = Select(driver.find_element_by_id('subArea'))
county.select_by_visible_text('san francisco')

max_price = driver.find_element_by_name('max_price')
max_price.send_keys('850')

# Open up category radio inputs to deselect categories
show_housing = driver.find_element_by_class_name('closed').click()

# Deselect these categories
office = driver.find_element_by_id('cat_off').click()
parking = driver.find_element_by_id('cat_prk').click()
real_estate = driver.find_element_by_id('cat_rea').click()
vacation = driver.find_element_by_id('cat_vac').click()
wanted_real_estate = driver.find_element_by_id('cat_rew').click()
swap = driver.find_element_by_id('cat_swp').click()

# Hit enter key/Submit changes
max_price.send_keys(Keys.RETURN)

items = []
count = 0


def find_housing():
    # Return titles of each posting for now
    listings = driver.find_elements_by_class_name("result-title")
    # print(os.environ.get('EMAIL'))
    # Print out title for each listing
    # Iterate through only first 4 links to save time
    for listing in listings:
        # Get all URLs
        link = listing.get_attribute('href')
        # # Open new tab
        driver.execute_script(f"window.open('{link}');")
        # # Switch focus to last opened tab
        driver.switch_to.window(driver.window_handles[-1])
        # # Do what you need to on that tab
        if driver.find_elements_by_class_name('price'):
            price = driver.find_element_by_class_name('price').text
        else:
            price = ''

        if driver.find_element_by_id('postingbody').text:
            description = driver.find_element_by_id('postingbody').text
        else:
            description = ''

        # Close tab & skip if no reply button
        if driver.find_elements_by_xpath('//*[@class="reply-button js-only"]'):
            # Adding periodic pauses in attempt to not overload Craigslist by sending too many
            # emails - Too many emails means emails won't send
            time.sleep(5)
            # # Select reply btn
            reply = driver.find_element_by_xpath('//*[@class="reply-button js-only"]')
            # # Click on reply btn
            reply.click()

            time.sleep(5)

            # # Wait for email info dialog to open up
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".reply-flap")))
            # # Grab email from dialog
            if driver.find_elements_by_class_name('mailapp'):
                email_url = driver.find_element_by_class_name('mailapp').get_attribute('innerHTML')

                print(link)

                item = dict({'price': price, 'email': email_url, 'description': description})
                global items
                items.append(item)
                global count
                count += 1

                # Send email to poster 
                # TAILOR MESSAGE TO YOUR LIKING
                test_sendmail(email_url, f"Hi, I'm interested in the room \n {link} \n \n Best, S")

                # Close tab after sending email
            driver.execute_script("window.close('" + link + "');")
            # Switch back to main tab & open a new tab
            driver.switch_to.window(driver.window_handles[0])
        else:
            print('reply button not found')
            driver.execute_script("window.close('" + link + "');")
            driver.switch_to.window(driver.window_handles[0])

    if driver.find_elements_by_class_name('next') and driver.find_element_by_class_name('next').get_attribute('href'):
        next_btn = driver.find_element_by_class_name('next')
        next_btn.click()
        find_housing()
    else:
        print('Next button not clickable')
        return


find_housing()


with open('items.py', 'w') as f:
    print(items, file=f)

print(f'Responded to {count} housing postings')
# Close driver/browser
driver.close()        
