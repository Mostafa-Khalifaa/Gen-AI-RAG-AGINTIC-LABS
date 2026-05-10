from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from document_handler import process_pdf
from llm_agent import get_answer

load_dotenv()

app = Flask(__name__)
global_db = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    global global_db
    
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded."}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected."}), 400
        
    file_path = "temp.pdf"
    file.save(file_path)
    
    try:
        global_db = process_pdf(file_path)
        return jsonify({"message": "File processed successfully! The database is ready."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/ask', methods=['POST'])
def ask_question():
    global global_db
    
    if not global_db:
        return jsonify({"error": "Please upload a PDF file first."}), 400
        
    data = request.json
    question = data.get('question')
    
    if not question:
        return jsonify({"error": "Please provide a question."}), 400
        
    try:
        result = get_answer(global_db, question)
        return jsonify({
            "answer": result["answer"],
            "sources": result["sources"]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)