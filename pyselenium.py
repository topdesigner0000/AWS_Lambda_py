import json
import selenium
from selenium import webdriver
import requests
from io import BytesIO
from zipfile import ZipFile
import os.path

def DownUnzip(url, path):
    r = requests.get(url)

    f = ZipFile(BytesIO(r.content))
    f.extractall(path)

def lambda_handler(event, context):
    # TODO implement

    chromium_url = "https://github.com/adieuadieu/serverless-chrome/releases/download/v1.0.0-55/stable-headless-chromium-amazonlinux-2017-03.zip"
    DownUnzip(chromium_url, "/tmp/")

    chrdrv_url = "https://chromedriver.storage.googleapis.com/2.43/chromedriver_linux64.zip"
    DownUnzip(chrdrv_url, "/tmp/")

    print(os.path.isfile("chromedriver"))
    os.chmod("/tmp/chromedriver", stat.S_IRWXU | stat.S_IXUSR | stat.S_IXOTH)

    chromeoptions = webdriver.ChromeOptions()
    chromeoptions.add_argument("--no-sandbox")
    chromeoptions.add_argument("--ignore-certificate-errors")
    chromeoptions.add_argument("--ignore-ssl-errors")
    chromeoptions.add_argument("--system-developer-mode")
    chromeoptions.add_argument("--no-first-run")
    
    chromeoptions.binary_location = '/tmp/headless-chromium'

    driver = webdriver.Chrome("/tmp/chromedriver", options=chromeoptions)
    driver.implicitly_wait(5)
    driver.maximize_window()

    url = "https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html"
    driver.get(url)
    html = driver.page_source

    return html
