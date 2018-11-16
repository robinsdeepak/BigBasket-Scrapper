from selenium import webdriver
from bs4 import BeautifulSoup as bs
import requests
import shutil
import time
import os
import json


# driver = webdriver.Chrome() # With Head
# Headless
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
driver = webdriver.Chrome(options=chrome_options)

links = open('links.txt', 'r')
url_list = links.readlines()
# print(url_list)
# exit()
for url in url_list[15:]:

    driver.get(url)
    # driver.get(url.replace('\n', ''))
    time.sleep(8)   # 2 Sec for ssh
    while True:
        try:
            driver.find_element_by_xpath("//button[@ng-click='vm.pagginator.showmorepage()']").click()
            time.sleep(2)
            print("Clicked Successfully")
        except:
            break
    html = driver.execute_script("return document.documentElement.outerHTML")
    soup = bs(html, 'html.parser')
    products = soup.findAll("div", {"qa": "product"})
    # print(len(products))
    directory = 'All_Data\\' + url.replace('https://www.bigbasket.com/pc/', '').replace('/?nc=bt\n', '').replace('/?nc=nb\n', '').replace('/?nc=cs\n', '').replace('/', '\\')
    # print(directory)
    try:
        os.makedirs(directory+'\\images\\large')
    except FileExistsError:
        pass
    try:
        os.makedirs(directory + '\\images\\small')
    except FileExistsError:
        pass
    # d_dir = os.path.join(directory, 'data')     # Data Directory
    data = open(os.path.join(directory, 'data.txt'), "w")
    data.write("[")
    # print(directory)
    for product in products:
        # break
        img = product.find("img")['src']
        image_small = img.replace('/media/uploads/p/mm/', '/media/uploads/p/s/')
        image_large = img.replace('/media/uploads/p/s/', '/media/uploads/p/l/').replace('/media/uploads/p/mm/', '/media/uploads/p/l/')
        del img

        Brand = product.find("div", {"qa": "product_name"}).find("h6").text
        Product = product.find("div", {"qa": "product_name"}).find("a").text
        Quantity = product.find("span", {"data-bind": "label"}).text
        Price = product.find("span", {"class": "discnt-price"}).text

        # Writing data jo json file
        data.write(json.dumps({
            'image': [{'small': image_small}, {'large': image_large}],
            'Brand': Brand,
            'Product': Product,
            'Quantity': Quantity,
            'Price': Price
        })+',\n\n')

        # copy image files
        try:
            image_small_raw = requests.get(image_small, stream=True)
            filename = os.path.basename(image_small)
            img_dir = os.path.join(directory, "images\\small", filename)
            with open(img_dir, "wb") as out_file:
                shutil.copyfileobj(image_small_raw.raw, out_file)
            del image_small_raw

            image_large_raw = requests.get(image_large, stream=True)
            time.sleep(1)
            filename = os.path.basename(image_large)
            img_dir = os.path.join(directory, "images\\large", filename)
            with open(img_dir, "wb") as out_file:
                shutil.copyfileobj(image_large_raw.raw, out_file)
            del image_large_raw
        except Exception as e:
            print(e)
        else:
            print("Successfully downloaded data from category url\n", url)
    data.write("]")
    data.close()
driver.quit()
links.close()
