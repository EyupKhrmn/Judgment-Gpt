import re


def splitAnswer(answer):

    list = []
    sections = re.split(r'(?<=\n)([A-ZÇĞİÖŞÜ\s]+):', answer)

    result = {}
    for i in range(1, len(sections), 2):
        key = sections[i].strip()  # Başlık
        value = sections[i + 1].strip()  # İçerik
        result[key] = value

    for key, value in result.items():
        list.append([key, value])

    return list


from bs4 import BeautifulSoup


def clean_text(text):
    text = BeautifulSoup(text, "html.parser").get_text(separator=" ")

    text = re.sub(r'\s+', ' ', text)

    return text.strip()