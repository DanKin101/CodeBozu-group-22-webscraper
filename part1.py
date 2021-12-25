from bs4 import BeautifulSoup
import requests
import pandas as pd


def birthplace():
    politician_birthplace_list = []
    birthplace_links = politician_data[born].find_all("a")
    if len(birthplace_links) == 0 or len(birthplace_links) == 1:
        if len(data) == 5:
            politician_birthplace = data[3].text + data[4]
        elif len(data) == 6:
            politician_birthplace = data[5].text
        elif len(data) == 7:
            politician_birthplace = data[5].text + data[6]
        elif len(data) == 8:
            politician_birthplace = data[6].text + data[7]

    else:
        for link in birthplace_links:
            politician_birthplace_list.append(link.text)
        politician_birthplace = " , ".join(politician_birthplace_list)

    return politician_birthplace

def store_info():
    info = {
        "Name": politician_name,
        "Fullname": politician_fullname,
        "Birthday": politician_birthday,
        "Birthlpace": politician_birthplace,
        "Political Party": politician_party,
    }
    president_info.append(info)

president_info = []
centuries = ["19th","20th","21st"]

for century in centuries:
    wiki_page = requests.get(
        f"https://en.wikipedia.org/wiki/Category:{century}-century_presidents_of_the_United_States").text
    wiki_soup = BeautifulSoup(wiki_page, "lxml")
    politicians_container = wiki_soup.find_all("div", class_="mw-content-ltr")
    politicians_links = politicians_container[1].find_all("a")

    for president in politicians_links:
        bio_data = requests.get(f"https://en.wikipedia.org{president['href']}").text

        data_soup = BeautifulSoup(bio_data, "lxml")
        data_card = data_soup.find("table", class_="infobox vcard")

        politician_data = data_card.find_all("td", class_="infobox-data")
        politician_label = data_card.find_all("th", class_="infobox-label")

        for label in politician_label:
            if label.text == "Born":
                born = politician_label.index(label)
            elif label.text == "Political party":
                party = politician_label.index(label)

        data = politician_data[born].contents

        if data[0].find("span") is None:
            politician_name = data_card.find("th", class_="infobox-above").text
            politician_fullname = data[0].text
            politician_birthday = data[3].text
            politician_party = politician_data[party].find("a").text
            politician_birthplace = birthplace()
            store_info()
        else:
            politician_name = data_card.find("th", class_="infobox-above").text
            politician_fullname = politician_name
            politician_birthday = data[1]
            politician_party = politician_data[party].find("a").text
            politician_birthplace = birthplace()
            store_info()


df = pd.DataFrame(president_info)
df.to_csv("data.csv")

