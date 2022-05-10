import sys

import requests
from bs4 import BeautifulSoup
import json


# run the web crawler
def run(url, depth):
    links = get_links(url, depth)
    for i in range(len(links)):
        for j in links[i]:
            get_images(j, i)


# get all the images of the url and write to a JSON file of specific depth
def get_images(url, depth):
    urls = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    img_tags = soup.find_all('img')
    with open('results.json', 'a') as f:
        for img in img_tags:
            if img.has_attr('src'):
                urls.append(img['src'])
                result = {
                    "imageUrl": img['src'],
                    "sourceUrl": url,
                    "depth": depth,
                }
            f.write(json.dumps(result))
            f.write('\n')


# getting all the links of specific url within depth
def get_links(url, depth):
    url_list_depth = [[] for i in range(0, depth +1)]
    url_list_depth[0].append(url)
    for depth_i in range(0, depth):
        for links in url_list_depth[depth_i]:
            response = requests.get(links)
            soup = BeautifulSoup(response.text, 'html.parser')
            links_tags = soup.find_all('a')
            for link in links_tags:
                url_new = link.get('href')
                flag = False
                for item in url_list_depth:
                    for l in item:
                        if url_new == l:
                            flag = True
                if url_new is not None and "http" in url_new and flag is False:
                    url_list_depth[depth_i + 1].append(url_new)
    return url_list_depth


def main():
    run(sys.argv[1], int(sys.argv[2]))


if __name__ == '__main__':
    main()
