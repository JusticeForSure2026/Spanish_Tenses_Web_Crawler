import csv

import requests as requests
from bs4 import BeautifulSoup

import time

import pandas as pd
import xlsxwriter

reader = csv.DictReader(open('Verb List To Crawl.csv', newline='', encoding='utf-8'))

word_count = 0

delay = 1.25

verb_list = None
data_frame = None

headers = requests.utils.default_headers()
headers.update({'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0', })


def search_all_verbs():
    global word_count

    global verb_list
    global data_frame

    verb_list = []

    for row in reader:
        find_all_tenses_for_one_verb(row['Español'])
        word_count += 1

        print(row)

        # if word_count > 2:
        #     break

        time.sleep(delay)

    print(word_count)

    data_frame = pd.DataFrame(verb_list, columns=['0'] * 132)

    writer = pd.ExcelWriter('Output.xlsx', engine='xlsxwriter')
    data_frame.to_excel(writer, sheet_name='Output', index=False)

    writer._save()


def find_all_tenses_for_one_verb(verb):
    url = "https://conjugator.reverso.net/conjugation-spanish-verb-" + verb + ".html"

    soup = BeautifulSoup(requests.get(url, headers=headers).text, 'html.parser')

    termination_index = 0

    global word_count

    global verb_list

    print_all_verbs = False

    current_verb_list = []

    tense1 = []
    tense2 = []
    tense3 = []
    tense4 = []
    tense5 = []
    tense8 = []
    tense9 = []
    tense10 = []
    tense12 = []
    tense14 = []
    tense15 = []

    for div_element in soup.find_all("div", {"class": "blue-box-wrap"}):
        termination_index += 1

        item_count = 0

        long_version = False
        masculine = ""

        if termination_index in (6, 7, 11, 13, 16):
            continue

        if termination_index > 17:
            break

        tense_content = []

        for tense_item in div_element.find_all("li"):
            content = ""

            for tense_subelement in tense_item.find_all():
                tense_item_string = str(tense_subelement.text)

                if item_count == 0 and tense_item_string == "me ":
                    tense_item_string = "yo "
                elif item_count == 1 and tense_item_string == "te ":
                    tense_item_string = "tú "
                elif item_count == 2 and tense_item_string == "se ":
                    tense_item_string = "él/ella/Ud. "
                elif item_count == 3 and tense_item_string == "nos ":
                    tense_item_string = "nosotros "
                elif item_count == 4 and tense_item_string == "os ":
                    tense_item_string = "vosotros "
                elif item_count == 5 and tense_item_string == "se ":
                    tense_item_string = "ellos/ellas/Uds. "

                content += tense_item_string

            item_count += 1

            # print(content)

            # current_verb_list.append(content)
            # current_verb_list.append(",")
            tense_content.append(content)
            tense_content.append(",")

            if print_all_verbs:
                print(content)

        if termination_index == 1:
            tense1 = tense_content
        elif termination_index == 2:
            tense2 = tense_content
        elif termination_index == 3:
            tense3 = tense_content
        elif termination_index == 4:
            tense4 = tense_content
        elif termination_index == 5:
            tense5 = tense_content
        elif termination_index == 8:
            tense8 = tense_content
        elif termination_index == 9:
            tense9 = tense_content
        elif termination_index == 10:
            tense10 = tense_content
        elif termination_index == 12:
            tense12 = tense_content
        elif termination_index == 14:
            tense14 = tense_content
        elif termination_index == 15:
            tense15 = tense_content

    for element in tense1:
        current_verb_list.append(element)

    for element in tense10:
        current_verb_list.append(element)

    for element in tense3:
        current_verb_list.append(element)

    for element in tense4:
        current_verb_list.append(element)

    for element in tense5:
        current_verb_list.append(element)

    for element in tense2:
        current_verb_list.append(element)

    for element in tense9:
        current_verb_list.append(element)

    for element in tense8:
        current_verb_list.append(element)

    for element in tense12:
        current_verb_list.append(element)

    for element in tense14:
        current_verb_list.append(element)

    for element in tense15:
        current_verb_list.append(element)

    verb_list.append(current_verb_list)


search_all_verbs()
