from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from time import sleep
import pandas as pd
import random
from xpath import xpath



def generate_leads(business, location, max_results=100):
    
    options = Options()
    options.add_argument("--lang=en-GB")
    # options.add_argument('--headless')

    service = Service(executable_path='./chromedriver.exe')

    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    driver.implicitly_wait(4)

    url = f'https://www.google.com/search?q={business.replace(" ", "+")}+in+{location}+google+maps'
    driver.get(url)

    driver.find_element(by='xpath', value=xpath["more_locations"]).click()
    businesses = driver.find_elements(by='xpath', value=xpath["businesses"])
    print(len(businesses))

    current_page = 1 #holds the current page
    processed = 0
    infos = ['name', 'rating', 'reviews_count', 'description', 'address']
    data = {
        'name': [],
        'rating': [],
        'reviews_count': [],
        'description': [],
        'address': [],
        'phone_number': [],
        'website': [],
    }

    while processed <= max_results:

        for business in businesses:

            if processed == max_results:
                break

            print('for loop')

            business.location_once_scrolled_into_view
            business.click()
            sleep(random.randint(1,2))

            for info in infos:
                try:
                    info_data = driver.find_element(by='xpath', value=xpath[info]).text
                    data[info].append(info_data)
                except:
                    data[info].append('NaN')

            try:
                website = driver.find_element(by='xpath', value=xpath['website']).get_attribute('href')
                data['website'].append(website)
            except:
                data['website'].append('NaN')

            try:
                phone_number = driver.find_element(by='xpath', value=xpath['phone_number']).get_attribute('data-phone-number').replace('+', '')
                data['phone_number'].append(phone_number)
            except:
                data['phone_number'].append('NaN')
            

            processed += 1

            print(f'{processed}/{max_results}')

        if processed == max_results:
            break
        # move the next page
        driver.find_element(by='xpath', value='//div[@aria-label="Local results pagination"]').location_once_scrolled_into_view

        try:
            driver.find_element(by='xpath', value=f'//a[@aria-label="Page {current_page + 1}"]/span').click()
        except:
            print('max pages exceeds...')
            break
        
        current_page += 1
        sleep(random.randint(2,3))
        businesses = driver.find_elements(by='xpath', value=xpath["businesses"])

    pd.DataFrame(data).to_csv('./results.csv', index_label=False, index=False)