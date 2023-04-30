from flask import Flask, request, jsonify, Response
from werkzeug.utils import secure_filename
import os
import faiss
import openai
from flask_cors import CORS
import langchain



from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.docstore.document import Document
from langchain.vectorstores import FAISS, VectorStore
from llama_index import download_loader
from llama_index import SimpleDirectoryReader

openai.api_key = "your_openai_api_key"
docsearch = VectorStore()
history = []

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = './uploaded_files'

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    
    document = SimpleDirectoryReader(input_files=[file_path]).load_langchain_data()

    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=0)
    documents = text_splitter.split_documents(document)

    embeddings = OpenAIEmbeddings(openai_api_key=openai.api_key)
    docsearch = FAISS.from_documents(documents, embeddings)

    return jsonify({"message": "File uploaded and indexed successfully."})

@app.route('/query', methods=['POST'])
def query_index():
    question = request.json['question']

    relevant = docsearch.similarity_search(question, 3)
    contexts=[]
    for i, doc in enumerate(relevant):
        contexts.append(f"Context {i}:\n{doc.page_content}")
    context = "\n\n".join(contexts)

    system_prompt = f"""
    Please only use the following context to answer the question.

    context : '''{context}'''
    """

    return Response(query_openai_api(system_prompt, question), content_type='text/event-stream')

def query_openai_api(system_prompt,prompt):
    model = "text-davinci-002"  # Change to your preferred model
    history += [{"role":"user", "content":prompt}]
    response = openai.ChatCompletion.create(
        model = model,
        messages=[{"role":"system", "content":system_prompt}] + history + [{"role":"user", "content":prompt}],
        stream=True,
        max_tokens=50,  # You can adjust this value depending on the desired length of the response
        temperature=0,
    )
    completion_text = ''
    for line in response:
        if 'content' in line['choices'][0]['delta']:
            completion_text += line['choices'][0]['delta']['content']
            yield line['choices'][0]['delta']['content']
    history += [{"role":"assistant", "content":completion_text }]

if __name__ == '__main__':
    app.run(debug=True)
