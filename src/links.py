import requests
import re
import os

url = 'https://api.github.com/repositories?since=800000000'  # This is an example grabbing repos with id nums greater than 800000000
headers = {'Accept': 'application/vnd.github+json', 'X-GitHub-Api-Version': '2022-11-28'}  # Bearer token can be added here to increase limit on number of repos requested
batches = 200

try:
    f = open('links.txt', 'w')
except FileNotFoundError:
    os.makedirs('links.txt')
    f = open('links.txt' , 'w')

for i in range(batches):
    r = requests.get(url, headers=headers)  # Using github api to retrieve next batch of urls
    url = re.search(r"(?<=<).*\d(?=>)", r.headers.get('Link'))[0]  # Getting the url for the next page of repo urls
    for obj in r.json():
        f.write(str(obj.get("html_url")) + '\n')  # Writing the returned urls to a file

f.write(url + '\n')
f.close()

