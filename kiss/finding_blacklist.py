import csv
import os
from googletrans import Translator

def get_idioms(file_path):
    os_path = os.getcwd()

    idiom_list = []
    with open(os_path + file_path, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            idiom_list.append(row[0])

    return set(idiom_list) 

file_path = '/kiss/data/KISS.csv'
idiom_set = get_idioms(file_path)

translator = Translator()
text = "안녕하세요"
trans = translator.translate(text, src='ko', dest='en')
print(trans.text)