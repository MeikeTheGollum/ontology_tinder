import io
from urllib.request import urlretrieve

from playwright.sync_api import sync_playwright
import requests, zipfile
from concurrent.futures import ThreadPoolExecutor



urls= ["https://dl.fbaipublicfiles.com/fasttext/vectors-english/crawl-300d-2M.vec.zip",
       "https://nlp.stanford.edu/data/glove.6B.zip",
       "https://nlp.stanford.edu/data/glove.42B.300d.zip",
       "https://nlp.stanford.edu/data/glove.840B.300d.zip",
       "https://nlp.stanford.edu/data/glove.840B.300d.zip"]

def download_file(url):
    """
    Downloads the requested files given an url and saves them in the resources' folder.

    :param url: The url of the model
    """
    response = requests.get(url, stream=True)
    if "content-disposition" in response.headers:
        content_disposition = response.headers["content-disposition"]
        filename = content_disposition.split("filename=")[1]
    else:
        filename = url.split("/")[-1]
        with open(f"../resources/{filename}", mode="wb") as file:
            for chunk in response.iter_content(chunk_size=10*1024):
                file.write(chunk)
        print(f"Downloaded file {filename}")

def extract_model(url):
    """
    Extracts the previously downloaded zips into models folder.

    :param url: the url of the file to be extracted
    """
    filename = url.split("/")[-1]
    with zipfile.ZipFile(f"../resources/{filename}", 'r') as zip_ref:
        zip_ref.extractall("../resources/models")
        print(f"Extracted {filename} to models folder")

#def load_model(filename):


with ThreadPoolExecutor() as executor:
    executor.map(download_file, urls)
    executor.map(extract_model, urls)