import ollama, chromadb, time, os
from utilities import readtext, getconfig
from mattsollamatools import chunk_text_by_sentences
import chromadb.utils.embedding_functions as embedding_functions

collectionname="buildragwithpython"

chroma = chromadb.HttpClient(host="localhost", port=8000)
print(chroma.list_collections())
if any(collection.name == collectionname for collection in chroma.list_collections()):
  print('deleting collection')
  chroma.delete_collection(collectionname)
collection = chroma.get_or_create_collection(name=collectionname, metadata={"hnsw:space": "cosine"})

embedmodel = getconfig()["embedmodel"]
ollama_ef = embedding_functions.OllamaEmbeddingFunction(
    url="http://localhost:11434/api/embeddings",
    model_name=embedmodel,
)

path = getconfig()["files_path"]
dir_list = os.listdir(path)
starttime = time.time()

for file in dir_list:
  filename = path + file
  text = readtext(filename)
  chunks = chunk_text_by_sentences(source_text=text, sentences_per_chunk=7, overlap=0 )
  print(f"with {len(chunks)} chunks")
  for index, chunk in enumerate(chunks):
    #Switch from direct ollama ebedding to chromadb embedding using ollama wrapper
    #https://docs.trychroma.com/embeddings/ollama
    embed = ollama.embeddings(model=embedmodel, prompt=chunk)['embedding']
    #embed = ollama_ef(chunk)
    print(".", end="", flush=True)
    #collection.add([filename+str(index)], [embed], documents=[chunk], metadatas={"source": filename})
    collection.add(
      [filename+str(index)], 
      [embed], 
      documents=[chunk],
      metadatas={"source": filename}
      )

with open('sourcedocs.txt') as f:
  lines = f.readlines()
  for filename in lines:
    text = readtext(filename)
    chunks = chunk_text_by_sentences(source_text=text, sentences_per_chunk=7, overlap=0 )
    print(f"with {len(chunks)} chunks")
    for index, chunk in enumerate(chunks):
      embed = ollama.embeddings(model=embedmodel, prompt=chunk)['embedding']
      print(".", end="", flush=True)
      collection.add(
        [filename+str(index)], 
        [embed], 
        documents=[chunk], 
        metadatas={"source": filename}
        )
  
  print("--- %s seconds ---" % (time.time() - starttime))

