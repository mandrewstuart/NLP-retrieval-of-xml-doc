import html2text
import json
from llama_cpp import Llama
from uuid import uuid4


# loading a model is fast these days but technically this should be a function because we don't want side effects in our modules.
gguf_path = "/home/andrew/Downloads/bge-large-en-v1.5-f32.gguf"
model = Llama(gguf_path, embedding=True)


def make_data():
    """We read the XML tax act and parse out the sections crudely.
    We add an order as index, the text and the embedding to the IDs varible (which is badly named.)
    We write all of the data to an all_data file using json.dumps so that it can be read again easily.
    """
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


# this is commented because I already have a copy of the data. if you don't, make your changes as necessary.
# make_data()

def get_data():
    """This one-liner reads the all_data file back into a dictionary."""
    return json.loads(open("all_data", "r").read())


# This is a side effect. If you're running this differently than as a script, I recommend making modifications.
IDs = get_data()


def get_closest(query):
    """This accepts a string and outputs a dictionary. The results value is a list and query returns the original query.
    This whole thing would be simple to put behind a get request and parse a query string.
    """
    embedding = model.embed(query)
    distances = []
    for embed_index in range(len(IDs)):
        distances.append([sum([(IDs[str(embed_index)]["embed"][i] - embedding[i])**2 for i in range(len(IDs[str(embed_index)]["embed"]))])**0.5, IDs[str(embed_index)]])
    distances.sort()
    return {"results": [t[1] for t in distances[:20]], "query": query}


# Side effects again. I don't recommend running this as a module outside of a function.
output = get_closest("I own a property as my primary residence and I do business from my study. Do I pay taxes on that part of my home?")
open("output.html", "w").write("<html><body><h1>Query: " + output["query"] + "</h1><h3>related sections</h3><ol>")
for i in output["results"]:
    open("output.html", "a").write("<li>" + str(i["order"]) + ": " + i["text"] + "</li><hr>")


open("output.html", "a").write("</ol></body></html>")

# this is good enough for now. it does what it's supposed to. It's a in the direction of extreme programming because there are no tests or anything frivolously extra.
