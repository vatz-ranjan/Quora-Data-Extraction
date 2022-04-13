from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver import Keys
import json
from selenium.webdriver.common.by import By


class WebScraper:

    def __init__(self):
        self.__topic = None
        self.__allUrls = []
        self.__answers = {
            'topic': None,
            'mainEntity': []
        }

    def search(self, topic, chrome_driver_path='E:/Application/ChromeDriver/chromedriver.exe'):
        self.__topic = topic
        search_val = self.__topic + ' quora'
        base_url = 'https://www.google.com/'
        option = webdriver.ChromeOptions()
        option.add_argument('headless')
        driver = webdriver.Chrome(chrome_driver_path, options=option)
        driver.get(base_url)
        search = driver.find_element_by_name("q")
        search.send_keys(search_val)
        search.send_keys(Keys.ENTER)
        # url = driver.find_element_by_tag_name('HTML')
        url = driver.find_element(by=By.TAG_NAME, value='HTML').get_attribute('baseURI')
        req = requests.get(url)
        soup = BeautifulSoup(req.content, 'html.parser')
        entries = soup.findAll('div', attrs={'class': 'ZINbbc luh4tb xpd O9g5cc uUPGi'})
        for entry in entries:
            req_info = entry.findAll('a')[0].attrs['href']
            req_url = req_info[req_info.find('=') + 1:req_info.find('&')]
            if 'https://www.quora.com/' in req_url:
                self.__allUrls.append(req_url)
        driver.close()

    def scrape(self):
        self.__answers['topic'] = self.__topic
        for url in self.__allUrls:
            cur_info = {}
            print("Scanning {}".format(url))
            req = requests.get(url)
            soup = BeautifulSoup(req.content, 'html.parser')
            try:
                script = soup.find_all('script', attrs={'type': 'application/ld+json'})[0]
                entries = str(script)
                entries = entries.replace('</script>', '')
                entries = entries.replace('<script type="application/ld+json">', '')
                entries = json.loads(entries.strip())
            except:
                # print("Error!!! \nWebsite not found...")
                continue
            cur_info['question'] = entries['mainEntity']['name']
            cur_info['url'] = url
            cur_info['suggestedAnswer'] = []

            if entries is not None:
                for entry in entries['mainEntity']['suggestedAnswer']:
                    author_info = entry.get('author', None)
                    if author_info is not None:
                        author_name = author_info.get('name', None)
                        author_url = author_info.get('url', None)
                        author_description = author_info.get('description', None)
                    else:
                        author_name = None
                        author_url = None
                        author_description = None
                    text = entry['text']

                    cur_info_answer = {
                        'authorName': author_name,
                        'authorUrl': author_url,
                        'authorDescription': author_description,
                        'text': text
                    }
                    cur_info['suggestedAnswer'].append(cur_info_answer)
            self.__answers['mainEntity'].append(cur_info)

    def load_json(self, file_loc):
        connection = open(file_loc, 'w')
        # json.dump(self.__answers, connection, indent=4, ensure_ascii=False)
        json.dump(self.__answers, connection, indent=4)
        connection.close()









