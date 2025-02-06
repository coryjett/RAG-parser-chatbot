import ollama, chromadb, time, os
from utilities import readtext, getconfig
from mattsollamatools import chunk_text_by_sentences
import chromadb.utils.embedding_functions as embedding_functions

collectionname=getconfig()["collection_name"]

chroma = chromadb.HttpClient(host=getconfig()["chroma_host"], port=getconfig()["chroma_port"])
print(chroma.list_collections())
#if any(collection.name == collectionname for collection in chroma.list_collections()):
if (collectionname == chroma.get_collection(collectionname).name):
  print('deleting collection')
  chroma.delete_collection(collectionname)
collection = chroma.get_or_create_collection(name=collectionname, metadata={"hnsw:space": "cosine"})

embedmodel = getconfig()["embedding_model"]

ollama_ef = embedding_functions.OllamaEmbeddingFunction(
    url="http://"+getconfig()["ollama_host"]+":"+getconfig()["ollama_port"]+"/api/embeddings",
    model_name=embedmodel,
)

path = getconfig()["files_path"]
dir_list = os.listdir(path)
i=0
while True:
  i+=1
  starttime = time.time()

  for file in dir_list:
    filename = path + file
    text = readtext(filename)
    chunks = chunk_text_by_sentences(source_text=text, sentences_per_chunk=7, overlap=0)
    print(f"with {len(chunks)} chunks")
    for index, chunk in enumerate(chunks):
      chunk_hash = hash(chunk)

      if collection.get(where={"$and":[{'hash':chunk_hash},{'source':filename}]})['ids'] != []:
        continue

      embed = ollama_ef(chunk)
      print(".", end="", flush=True)
      collection.add(
        [filename+str(index)], 
        [embed][0], 
        documents=[chunk],
        metadatas={"source": filename, "hash":chunk_hash}
        )

  with open('sourcedocs.txt') as f:
    lines = f.readlines()
    for filename in lines:
      text = readtext(filename)
      chunks = chunk_text_by_sentences(source_text=text, sentences_per_chunk=7, overlap=0)
      print(f"with {len(chunks)} chunks")
      for index, chunk in enumerate(chunks):
        chunk_hash = hash(chunk)

        if collection.get(where={"$and":[{'hash':chunk_hash},{'source':filename}]})['ids'] != []:
          continue

        embed = ollama_ef(chunk)
        print(".", end="", flush=True)
        collection.add(
          [filename+str(index)], 
          [embed][0], 
          documents=[chunk], 
          metadatas={"source": filename, "hash":chunk_hash}
          )
    
    print("--- %s seconds ---" % (time.time() - starttime))
    print("Iteration "+str(i)+" completed.  Sleeping...")
    time.sleep(10)
