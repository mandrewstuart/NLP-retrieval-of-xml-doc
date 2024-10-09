import html2text
import json
from llama_cpp import Llama
from uuid import uuid4


gguf_path = "/home/andrew/Downloads/bge-large-en-v1.5-f32.gguf"
model = Llama(gguf_path, embedding=True)


def make_data():
    file = open("I-3.3.xml", "r").read()
    s = 0
    RELATED = "<Section"
    CLOSE_RELATED = "</Section"
    texts = []
    embeds = []
    IDs = {}
    count = 0
    h = html2text.HTML2Text()
    h.ignore_links = True
    while s < 13588884 and s > -1:
        s = file.find(RELATED, s) + len(RELATED)
        e = file.find(CLOSE_RELATED, s)
        text = h.handle(file[s:e])
        IDs[str(count)] = {"order": count, "text": text, "embed": model.embed(text)}
        count += 1
        print(count)

    open("all_data", "w").write(json.dumps(IDs))



# make_data()

def get_data():
    return json.loads(open("all_data", "r").read())


IDs = get_data()


def get_closest(query):
    embedding = model.embed(query)
    distances = []
    for embed_index in range(len(IDs)):
        distances.append([sum([(IDs[str(embed_index)]["embed"][i] - embedding[i])**2 for i in range(len(IDs[str(embed_index)]["embed"]))])**0.5, IDs[str(embed_index)]])
    distances.sort()
    return {"results": [t[1] for t in distances[:20]], "query": query}


output = get_closest("I own a property as my primary residence and I do business from my study. Do I pay taxes on that part of my home?")


open("output.html", "w").write("<html><body><h1>Query: " + output["query"] + "</h1><h3>related sections</h3><ol>")
for i in output["results"]:
    open("output.html", "a").write("<li>" + str(i["order"]) + ": " + i["text"] + "</li><hr>")


open("output.html", "a").write("</ol></body></html>")
