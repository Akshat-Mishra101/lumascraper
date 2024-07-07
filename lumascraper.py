from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, JavascriptException, NoSuchElementException
import time, json, os
from dotenv import load_dotenv
import csv  # Added to handle CSV files

load_dotenv()



# Check if the file does not exist
if not os.path.exists('output.tsv'):
    with open('output.tsv', 'w') as file:
        # Write the header
        file.write("eventName\teventLink\tfullname\tprofileLink\tuserId\tdescription\tinstagram\ttwitter\tyoutube\ttiktok\tlinkedin\twebsite\n")



def save_to_tsv(data, file_path='output.tsv'):
    with open(file_path, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter='\t')
        writer.writerow(data)

def read_tsv_file(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            data.append(row)
    return data
def log(message):
    print(f"[LOG] {message}")


options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 5)



# Open the login page
print("logging in")
driver.get("https://lu.ma")


time.sleep(5)


cookie = {
    'name': os.environ.get("keyname"),
    'value': os.environ.get("keyvalue"),  # Make sure the LI_AT_COOKIE is set in your .env file
    'domain': '.lu.ma'
}


driver.add_cookie(cookie)

# Refresh or navigate to the target page after adding the cookie
driver.refresh() 

time.sleep(3)


data_array = read_tsv_file('lumalinks.tsv')



for row in data_array:
    time.sleep(4)
    print('This is the row')
    print(row)
    driver.get(row[0])
    time.sleep(3)


    eventName = driver.find_element(By.CSS_SELECTOR,'h1.jsx-140261309.title.text-primary.mb-0.long').text

    listButton = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div.jsx-2911588165.text-tinted.fs-sm.guests-string.animated")))
    listButton.click()

    time.sleep(3)

    lister= wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'div.jsx-531347415.flex-column.outer.overflow-auto')))


    #elements = list.find_elements(EC.presence_of_element_located("div.flex-center.gap-2.spread"))

    
    print('about to get links')
    elements = lister.find_elements(By.CSS_SELECTOR,"div.flex-center.gap-2.spread")


    print('Collecting Profile Links')
    profileLinks = []
    for element in elements:
        href = element.find_element(By.CSS_SELECTOR,"a")
        profileLinks.append(href.get_attribute('href'))
    print("Profile Links Collected")

    for element in profileLinks:
        # print(element.text)
        # href = element.find_element(By.CSS_SELECTOR,"a")
        # print(href.get_attribute('href'))
        driver.get(element)
        time.sleep(2)
        
        fullname = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"h1.jsx-3444256809.mb-0"))).text
        print(f'FullName: {fullname}')
        userId = 'N/A'
        try:
            userId = driver.find_element(By.CSS_SELECTOR,'div.jsx-3444256809.username.text-tertiary-alpha').text
            print(f'UserID: {userId}')
        except NoSuchElementException:
            print("The User Doesn't Have an ID")

        
        dataBox = driver.find_element(By.CSS_SELECTOR,'div.jsx-3444256809.flex-column.info')
        bio = 'N/A'
        try:
            bio = dataBox.find_element(By.CSS_SELECTOR,'div.text-secondary-alpha').text
            print(f'Profile Description: {bio}')
        except NoSuchElementException:
            print("The User Doesn't Have a Profile Description")



        socialdict = {'instagram': 'N/A', 'twitter': 'N/A', 'youtube': 'N/A', 'tiktok': 'N/A', 'linkedin': 'N/A', 'website': 'N/A'}

        try:
            socialsRow = dataBox.find_element(By.CSS_SELECTOR,'div.jsx-1428039309.social-links.flex-center.social-links.regular')
            socials = socialsRow.find_elements(By.CSS_SELECTOR,"div.jsx-2703338562.social-link.regular")

            for social in socials:
                href = social.find_element(By.CSS_SELECTOR,'a')
                socialLink = href.get_attribute('href')

                socialLink.startswith('https://instagram.com')

                if socialLink.startswith('https://instagram.com'):
                    socialdict['instagram'] = socialLink
                elif socialLink.startswith('https://twitter.com'):
                    socialdict['twitter'] = socialLink
                elif socialLink.startswith('https://youtube.com'):
                    socialdict['youtube'] = socialLink
                elif socialLink.startswith('https://tiktok.com'):
                    socialdict['tiktok'] = socialLink
                elif socialLink.startswith('https://linkedin.com'):
                    socialdict['linkedin'] = socialLink
                else:
                    socialdict['website'] = socialLink  # Assuming any non-specific link is a website

            
            print(socialdict)
            print(list(socialdict.values()))

            

            
            save_to_tsv([eventName, row[0], fullname, element, userId, bio] + list(socialdict.values()))
        except NoSuchElementException:
            print("No Socials Detected")
        print('\n\n\n')
        # Append row to TSV
        



    




    





