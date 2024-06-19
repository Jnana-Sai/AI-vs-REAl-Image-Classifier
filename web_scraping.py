import bs4
import requests
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

#creating a directory to save images
folder_name = 'images'
if not os.path.isdir(folder_name):
    os.makedirs(folder_name)

parent_folder_name = folder_name
# Define the names of the subdirectories
subfolder_1 = os.path.join(parent_folder_name, "FAKE")
subfolder_2 = os.path.join(parent_folder_name, "REAL")

# Check if the subdirectories exist and create them if they don't
if not os.path.isdir(subfolder_1):
    os.makedirs(subfolder_1)

if not os.path.isdir(subfolder_2):
    os.makedirs(subfolder_2)


def download_image(url, folder_name, num, name):

    # write image to file
    reponse = requests.get(url)
    if reponse.status_code==200:
        with open(os.path.join(folder_name,name+str(num)+".jpg"), 'wb') as file:
            file.write(reponse.content)



#chromePath=r'c:\Users\jnana\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe'
driver=webdriver.Chrome()

search_URL = "https://www.google.com/search?q=ai+generated+images&tbm=isch"
driver.get(search_URL)

#//*[@id="rso"]/div/div/div[1]/div/div/div[25]
#//*[@id="rso"]/div/div/div[1]/div/div/div[50]
#//*[@id="rso"]/div/div/div[1]/div/div/div[75]
print(0)

a = input("Waiting...")
#Scrolling all the way up
driver.execute_script("window.scrollTo(0, 0);")
print(1)
page_html = driver.page_source
pageSoup = bs4.BeautifulSoup(page_html, 'html.parser')
containers = pageSoup.findAll('div', {'class':"eA0Zlc WghbWd FnEtTd mkpRId m3LIae RLdvSe qyKxnc ivg-i PZPZlf GMCzAd"} )
print(2)
print(len(containers))

len_containers = len(containers)
print(3)
print("Now lets start downloading images with search key word as ai generated images")
for i in range(1, len_containers+1):
    if i % 25 == 0:
        continue

    xPath = """//*[@id="rso"]/div/div/div[1]/div/div/div[%s]"""%(i)

    previewImageXPath = """//*[@id="rso"]/div/div/div[1]/div/div/div[%s]/div[2]/h3/a/div/div/div/g-img/img"""%(i)
    previewImageElement = driver.find_element(By.XPATH,previewImageXPath)
    previewImageURL = previewImageElement.get_attribute("src")
    #print("preview URL", previewImageURL)


    #print(xPath)


    driver.find_element(By.XPATH,xPath).click()
    #time.sleep(3)

    #//*[@id="islrg"]/div[1]/div[16]/a[1]/div[1]/img

    #input('waawgawg another wait')

    # page = driver.page_source
    # soup = bs4.BeautifulSoup(page, 'html.parser')
    # ImgTags = soup.findAll('img', {'class': 'n3VNCb', 'jsname': 'HiaYvf', 'data-noaft': '1'})
    # print("number of the ROI tags", len(ImgTags))
    # link = ImgTags[1].get('src')
    # #print(len(ImgTags))
    # #print(link)
    #
    # n=0
    # for tag in ImgTags:
    #     print(n, tag)
    #     n+=1
    # print(len(ImgTags))

    #/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[2]/div[1]/a/img

    #It's all about the wait

    timeStarted = time.time()
    while True:
        #//*[@id="Sva75c"]/div[2]/div[2]/div[2]/div[2]/c-wiz/div/div/div/div/div[2]/div/a/img[1]
        #//*[@id="dimg_161"]
        #//*[@id="Sva75c"]/div[2]/div[2]/div[2]/div[2]/c-wiz/div/div/div/div/div[3]/div[1]/a/img[1]
        #imageElement = driver.find_element(By.XPATH,"""//*[@id="Sva75c"]/div[2]/div[2]/div[2]/div[2]/c-wiz/div/div/div/div/div[3]/div[1]/a/img[1]""")
        #imageURL= imageElement.get_attribute('src')
        try:
        # Wait for the element to be present in the DOM and be visible
        #//*[@id="Sva75c"]/div[2]/div[2]/div[2]/div[2]/c-wiz/div/div[3]/div[1]/a/img[1]
            imageElement = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, """//*[@id="Sva75c"]/div[2]/div[2]/div[2]/div[2]/c-wiz/div/div[3]/div[1]/a/img[1]"""))
            )
            #print("Element found")
            imageURL= imageElement.get_attribute('src')
        except selenium.common.exceptions.TimeoutException:
            break
        except selenium.common.exceptions.NoSuchElementException:
            break
        if imageURL != previewImageURL:
            #print("actual URL", imageURL)
            break

        else:
            #making a timeout if the full res image can't be loaded
            currentTime = time.time()

            if currentTime - timeStarted > 10:
                print("Timeout! Will download a lower resolution image and move onto the next one")
                break


    #Downloading image
    try:
        download_image(imageURL, subfolder_1, i, "ai_art")
        print("Downloaded element %s out of %s total. URL: %s" % (i, len_containers + 1, imageURL))
    except:
        print("Couldn't download an image %s, continuing downloading the next one"%(i))
        print(imageURL)

    #//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[2]/div[1]/a/img
    #//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[2]/div[1]/a/img

driver.quit()

print("Now lets start downloading images with search key word as midjourney generated images")
driver2=webdriver.Chrome()
search_URL = "https://www.google.com/search?q=midjourney+generated+images&tbm=isch"
driver2.get(search_URL)
a = input("Waiting...")
#Scrolling all the way up
driver2.execute_script("window.scrollTo(0, 0);")
page_html = driver2.page_source
pageSoup = bs4.BeautifulSoup(page_html, 'html.parser')
containers = pageSoup.findAll('div', {'class':"eA0Zlc WghbWd FnEtTd mkpRId m3LIae RLdvSe qyKxnc ivg-i PZPZlf GMCzAd"} )

print(len(containers))
len_containers = len(containers)
for i in range(1, len_containers+1):
    if i % 25 == 0:
        continue

    xPath = """//*[@id="rso"]/div/div/div[1]/div/div/div[%s]"""%(i)
    previewImageXPath = """//*[@id="rso"]/div/div/div[1]/div/div/div[%s]/div[2]/h3/a/div/div/div/g-img/img"""%(i)
    previewImageElement = driver2.find_element(By.XPATH,previewImageXPath)
    previewImageURL = previewImageElement.get_attribute("src")
    driver2.find_element(By.XPATH,xPath).click() 
    timeStarted = time.time()
    while True:
        try:
        # Wait for the element to be present in the DOM and be visible
            imageElement = WebDriverWait(driver2, 10).until(
                EC.presence_of_element_located((By.XPATH, """//*[@id="Sva75c"]/div[2]/div[2]/div[2]/div[2]/c-wiz/div/div/div/div/div[3]/div[1]/a/img[1]"""))
            )
            #print("Element found")
            imageURL= imageElement.get_attribute('src')
        except selenium.common.exceptions.TimeoutException:
            break
        except selenium.common.exceptions.NoSuchElementException:
            break
        if imageURL != previewImageURL:
            #print("actual URL", imageURL)
            break

        else:
            #making a timeout if the full res image can't be loaded
            currentTime = time.time()

            if currentTime - timeStarted > 10:
                print("Timeout! Will download a lower resolution image and move onto the next one")
                break


    #Downloading image
    try:
        download_image(imageURL, subfolder_1, i, "mid")
        print("Downloaded element %s out of %s total. URL: %s" % (i, len_containers + 1, imageURL))
    except:
        print("Couldn't download an image %s, continuing downloading the next one"%(i))

driver2.quit()

print("Now lets start downloading images with search key word as dalle2 generated images")
driver3=webdriver.Chrome()
search_URL = "https://www.google.com/search?q=dalle2+generated+images&tbm=isch"
driver3.get(search_URL)


print(0)

a = input("Waiting...")
#Scrolling all the way up
driver3.execute_script("window.scrollTo(0, 0);")
print(1)
page_html = driver3.page_source
pageSoup = bs4.BeautifulSoup(page_html, 'html.parser')
containers = pageSoup.findAll('div', {'class':"eA0Zlc WghbWd FnEtTd mkpRId m3LIae RLdvSe qyKxnc ivg-i PZPZlf GMCzAd"} )
print(2)
print(len(containers))

len_containers = len(containers)
print(3)
for i in range(1, len_containers+1):
    if i % 25 == 0:
        continue

    xPath = """//*[@id="rso"]/div/div/div[1]/div/div/div[%s]"""%(i)
    previewImageXPath = """//*[@id="rso"]/div/div/div[1]/div/div/div[%s]/div[2]/h3/a/div/div/div/g-img/img"""%(i)
    previewImageElement = driver3.find_element(By.XPATH,previewImageXPath)
    previewImageURL = previewImageElement.get_attribute("src")
    #print("preview URL", previewImageURL)


    #print(xPath)


    driver3.find_element(By.XPATH,xPath).click()
    timeStarted = time.time()
    while True:
        try:
        # Wait for the element to be present in the DOM and be visible
            imageElement = WebDriverWait(driver3, 10).until(
                EC.presence_of_element_located((By.XPATH, """//*[@id="Sva75c"]/div[2]/div[2]/div[2]/div[2]/c-wiz/div/div/div/div/div[3]/div[1]/a/img[1]"""))
            )
            #print("Element found")
            imageURL= imageElement.get_attribute('src')
        except selenium.common.exceptions.TimeoutException:
            break
        except selenium.common.exceptions.NoSuchElementException:
            break
        if imageURL != previewImageURL:
            #print("actual URL", imageURL)
            break

        else:
            #making a timeout if the full res image can't be loaded
            currentTime = time.time()

            if currentTime - timeStarted > 10:
                print("Timeout! Will download a lower resolution image and move onto the next one")
                break


    #Downloading image
    try:
        download_image(imageURL, subfolder_1, i, "dal")
        print("Downloaded element %s out of %s total. URL: %s" % (i, len_containers + 1, imageURL))
    except:
        print("Couldn't download an image %s, continuing downloading the next one"%(i))

driver3.quit() 


from pygoogle_image import image as pi
pi.download(keywords="ai generated art", limit=100, directory= subfolder_1)
pi.download(keywords='landscapes', limit=100, directory= subfolder_2)
pi.download(keywords='cityscapes', limit=100, directory= subfolder_2)
pi.download(keywords='animals', limit=100, directory= subfolder_2)
pi.download(keywords='vehicles', limit=50, directory= subfolder_2)
pi.download(keywords='traffic', limit=50, directory= subfolder_2)
pi.download(keywords='offices', limit=50, directory= subfolder_2)
pi.download(keywords='real food images', limit=50, directory= subfolder_2) 
