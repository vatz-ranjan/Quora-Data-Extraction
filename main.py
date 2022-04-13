import os
import warnings
from web_scraper import WebScraper
from sent_extration import SentExtraction


class Quora:

    def __init__(self, topic):
        self.__topic = topic
        self.__folderName = "Topics"
        os.makedirs(self.__folderName, exist_ok=True)
        jsonFileName = self.__topic.replace(' ', '_') + '.json'
        self.__jsonFileLoc = os.path.join(self.__folderName, jsonFileName)
        textFileName = self.__topic.replace(' ', '_') + '.txt'
        self.__textFileLoc = os.path.join(self.__folderName, textFileName)

    def extraction(self):
        chromeDriverPath = 'E:/Application/ChromeDriver/chromedriver.exe'
        scraper = WebScraper()
        scraper.search(topic=self.__topic, chrome_driver_path=chromeDriverPath)
        scraper.scrape()
        scraper.load_json(file_loc=self.__jsonFileLoc)

    def sentence_tokenization(self):
        print("Creating Text File...")
        sent_extract = SentExtraction()
        sent_extract.read_json(file_loc=self.__jsonFileLoc)
        sent_extract.sentence_extraction()
        sent_extract.load_text(file_loc=self.__textFileLoc)
        sent_extract.load_excel()


def task():
    topic_lis = ['post traumatic stress disorder', 'clinical depression', 'depression', 'depressive', 'health', 'world']
    while True:
        topic = topic_lis[1]
        # topic = input("Enter your query: ")
        if len(topic) < 1:
            continue
        else:
            break

    quora = Quora(topic=topic)
    quora.extraction()
    quora.sentence_tokenization()


if __name__ == '__main__':
    warnings.filterwarnings('ignore')
    task()
