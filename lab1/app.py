import os
from flask import Flask, render_template, request, jsonify
from chef import ChefChatbot 

from dotenv import load_dotenv

load_dotenv() 

app = Flask(__name__)
my_bot = ChefChatbot()

@app.route('/')
def home():
    my_bot.reset_chat() 
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    txt = request.form.get('text', '')
    img_file = request.files.get('image')
    temp_val = float(request.form.get('creativity', 0.7)) 
    size = request.form.get('length', 'concise') 
    
    final_answer = my_bot.ask_chef(txt, img_file, temp_val, size)
    
    return jsonify({"answer": final_answer})

if __name__ == '__main__':
    app.run(debug=True)