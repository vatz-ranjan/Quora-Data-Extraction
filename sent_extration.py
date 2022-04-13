import json
from time import sleep
import pandas as pd
from nltk.tokenize import sent_tokenize


class SentExtraction:

    def __init__(self):
        self.__topic = None
        self.__answer = None
        self.__sentences = []

    def read_json(self, file_loc):
        connection = open(file_loc, 'r')
        json_info = connection.read()
        sleep(1)
        connection.close()
        self.__answer = json.loads(json_info)

    def sentence_extraction(self):
        if self.__answer is not None:
            self.__topic = self.__answer['topic']
            entities = self.__answer['mainEntity']
            for entity in entities:
                cur_info = entity['suggestedAnswer']
                for answer in cur_info:
                    paragraph = answer['text']
                    sentences = sent_tokenize(paragraph)
                    for sentence in sentences:
                        self.__sentences.append(sentence)
                        self.__sentences.append("\n")

    def load_text(self, file_loc):
        if len(self.__sentences) < 1:
            return
        try:
            connection = open(file_loc, 'w')
            for sentence in self.__sentences:
                connection.write(sentence)
        except:
            connection = open(file_loc, 'wb')
            for sentence in self.__sentences:
                connection.write(sentence.encode('utf-8', 'ignore'))
        sleep(2)
        connection.close()

    def load_excel(self):
        if len(self.__sentences) < 1:
            return
        excel_file_loc = 'Topic.xlsx'
        dataset = list(set(self.__sentences))
        output_dataset = pd.DataFrame(pd.Series(dataset), columns=['Text'])
        writer = pd.ExcelWriter(excel_file_loc, engine='xlsxwriter')
        output_dataset.to_excel(writer, sheet_name=self.__topic.replace(' ', '_'), index=True, na_rep='NaN')

        '''
        for column in output_dataset:
            column_width = int(max(output_dataset[column].astype(str).map(len).max(), len(column)))
            col_idx = output_dataset.columns.get_loc(column)
            writer.sheets[self.__topic.replace(' ', '_')].set_column(col_idx, col_idx, column_width)
        '''

        writer.save()



