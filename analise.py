import json
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from stop_words import get_stop_words

with open("result.json", "r") as f:
    data = json.load(f)

def analyse_areas(data):
    areas = []
    for k, v in data.items():
        for field in v:
            if field[0] == "dc.description.department":
                areas.append(field[1])
    dict_count = dict(Counter(areas))
    dict_count = {k: v for k, v in sorted(dict_count.items(), key=lambda item: item[1])}
    
    total = 0
    for k, v in dict_count.items():
        total += v
    print(total)

    plt.barh(range(len(dict_count)), list(dict_count.values()), align='center')
    plt.yticks(range(len(dict_count)), list(dict_count.keys()))
    plt.show()

def analyse_words(data):
    words = []
    for k, v in data.items():
        for field in v:
            if field[0] == "dc.title":
                words += field[1].split()
    text = " ".join(words)
    stopwords = get_stop_words('pt')
    wc = WordCloud(stopwords=stopwords, background_color="black", width=1600*2, height=800*2).generate(text)

    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    plt.show()

analyse_words(data)
analyse_areas(data)