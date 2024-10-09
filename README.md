# NLP-retrieval-of-xml-doc
draft


This is a python-only NLP search. It relies on a facebook embedding model to turn english language segments into a 1024-dimension vector, although the code is flexible enough to allow different embedding sizes.

It does what it's supposed to do, but be mindful of how much text you're inputting because it can be slow to generate the embeddings, which is why I comment that line out while I've already generated the data.

If I were going to make it faster, I would use speed up the vector search by using other modules, such as faiss or another vector-search application.

I opted for something slightly user-friendly in this draft, which is to output to HTML. I wanted to make it so that people don't have to stare at a terminal. Although the HTML slightly complicates things insofar as using this in the cloud, you could easily host a webserver that points to the output.html file that is generated and read it each time. You could also put the search inside a function and call it from the server to do everything in one call.

If you're still reading, you must be interested. I'm using the Canadian Tax Act's sections as the text segments to see if anything useful comes from it. It's a lot of text and even on my NVidia 3070, it takes about 15 minutes to create all of the embeddings.
