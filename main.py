import os
import requests
from bs4 import BeautifulSoup
import re

def fetch_image_urls(query: str, max_links_to_fetch: int):
    search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&q={}".format(query)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    image_urls = set()
    results = soup.find_all('img', {'src': True})

    for img in results[:max_links_to_fetch]:
        image_urls.add(img['src'])

    return image_urls

def persist_image(folder_path: str, url: str, counter):
    try:
        image_content = requests.get(url).content
    except Exception as e:
        print(f"ERROR - Could not download {url} - {e}")

    try:
        f = open(os.path.join(folder_path, f"image_{counter}.jpg"), 'wb')
        f.write(image_content)
        f.close()
        print(f"SUCCESS - saved {url} - as {folder_path}/image_{counter}.jpg")
    except Exception as e:
        print(f"ERROR - Could not save {url} - {e}")

def search_and_download(search_term: str, target_path='./images', number_images=10):
    target_folder = os.path.join(target_path, '_'.join(search_term.lower().split(' ')))

    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    image_urls = fetch_image_urls(search_term, number_images)

    counter = 0
    for elem in image_urls:
        persist_image(target_folder, elem, counter)
        counter += 1

# Example usage:
search_term = 'imran khan'
search_and_download(search_term=search_term, number_images=50)
