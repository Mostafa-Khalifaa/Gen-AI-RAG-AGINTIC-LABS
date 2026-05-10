from flask import Flask, render_template, request, jsonify
import base64
from langchain.messages import HumanMessage
from agent import doctor
import os


app = Flask(__name__)

THREAD_ID = "web_session_01"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    text_message = data.get('text', '')
    image_base64 = data.get('image', None)
    
    messages = []
    
    if image_base64:
        if image_base64.startswith('data:image'):
            image_base64 = image_base64.split(',')[1]
            
        messages.append({
            "type": "text",
            "text": text_message if text_message else "Please diagnose this image."
        })
        messages.append({
            "type": "image",
            "base64": image_base64,
            "mime_type": "image/jpeg" 
        })
        
        human_msg = HumanMessage(content=messages)
    else:
        human_msg = HumanMessage(content=text_message)
        
    try:
        res = doctor.invoke(
            {"messages": [human_msg]},
            config={"configurable": {"thread_id": THREAD_ID}}
        )
        
        ai_response = res['messages'][-1].content
        return jsonify({"reply": ai_response})
    
    except Exception as e:
        print(f"Error during agent invocation: {e}")
        return jsonify({"reply": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
