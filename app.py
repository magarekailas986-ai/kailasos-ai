from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

API_KEY = os.getenv("OPENROUTER_API_KEY")

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>KailasOS AI</title>
<meta name='viewport' content='width=device-width, initial-scale=1.0'>

<style>
body{
    margin:0;
    padding:0;
    background:#020b2d;
    font-family:Arial;
    color:white;
}

.container{
    width:90%;
    margin:auto;
    padding-top:40px;
    padding-bottom:40px;
}

.title{
    text-align:center;
    font-size:60px;
    font-weight:bold;
    background:linear-gradient(90deg,#00d4ff,#7b61ff);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}

.subtitle{
    text-align:center;
    font-size:22px;
    margin-top:10px;
    color:#ddd;
}

.card{
    background:#06154a;
    padding:25px;
    border-radius:25px;
    margin-top:30px;
    box-shadow:0 0 25px rgba(0,200,255,0.25);
}

input, textarea{
    width:100%;
    background:#0c1f63;
    border:none;
    outline:none;
    color:white;
    font-size:22px;
    border-radius:20px;
    padding:20px;
    margin-top:20px;
    box-sizing:border-box;
}

textarea{
    height:180px;
    resize:none;
}

button{
    width:100%;
    margin-top:25px;
    padding:22px;
    border:none;
    border-radius:50px;
    font-size:30px;
    font-weight:bold;
    color:white;
    cursor:pointer;
    background:linear-gradient(90deg,#00d4ff,#ff00ff);
}

.result-card{
    background:#05113b;
    padding:25px;
    border-radius:25px;
    margin-top:25px;
    box-shadow:0 0 20px rgba(0,200,255,0.2);
}

.result-title{
    font-size:28px;
    color:#00d4ff;
    font-weight:bold;
}

.result-text{
    font-size:22px;
    margin-top:20px;
    line-height:1.6;
    white-space:pre-wrap;
}

.copy-btn{
    margin-top:20px;
    padding:18px;
    border:none;
    border-radius:20px;
    font-size:22px;
    font-weight:bold;
    color:white;
    cursor:pointer;
    background:linear-gradient(90deg,#7b2cff,#c85cff);
}

.footer{
    text-align:center;
    margin-top:40px;
    font-size:22px;
    color:#bbb;
}

.loader{
    display:none;
    text-align:center;
    margin-top:20px;
    font-size:24px;
    color:#00d4ff;
}
</style>
</head>

<body>

<div class='container'>

<div class='title'>KailasOS AI</div>
<div class='subtitle'>Generate Viral Captions, Hooks, Hashtags & Bios 🚀</div>

<div class='card'>

<input type='text' id='topic' placeholder='Enter Topic'>

<textarea id='prompt' placeholder='Describe what you want...'></textarea>

<button onclick='generateContent()'>Generate AI Content</button>

<div class='loader' id='loader'>Generating Viral Content... 🚀</div>

</div>

<div id='results'></div>

<div class='footer'>Powered By KailasOS AI ⚡</div>

</div>

<script>

function copyText(text){
    navigator.clipboard.writeText(text)
    .then(()=>{
        alert('Copied Successfully ✅')
    })
}

async function generateContent(){

    let topic = document.getElementById('topic').value
    let prompt = document.getElementById('prompt').value

    document.getElementById('loader').style.display='block'

    let response = await fetch('/generate',{
        method:'POST',
        headers:{
            'Content-Type':'application/json'
        },
        body:JSON.stringify({
            topic:topic,
            prompt:prompt
        })
    })

    let data = await response.json()

    document.getElementById('loader').style.display='none'

    let content = data.content

    let sections = content.split('###')

    let html = ''

    sections.forEach(section=>{

        section = section.trim()

        if(section.length>0){

            let lines = section.split('\n')

            let title = lines[0]

            let text = lines.slice(1).join('\n')

            html += `
            <div class='result-card'>
                <div class='result-title'>${title}</div>
                <div class='result-text'>${text}</div>
                <button class='copy-btn' onclick='copyText(${JSON.stringify(text)})'>Copy</button>
            </div>
            `
        }
    })

    document.getElementById('results').innerHTML = html
}

</script>

</body>
</html>
"""

@app.route('/')
def home():
    return HTML

@app.route('/generate', methods=['POST'])
def generate():

    data = request.json

    topic = data.get('topic', '')
    prompt = data.get('prompt', '')

    final_prompt = f'''
Create premium social media content for:

Topic: {topic}
Description: {prompt}

Return ONLY this format:

### 🔥 Viral Caption
(write one powerful viral caption)

### 🎯 Hook
(write one attention grabbing hook)

### 🏷️ Hashtags
(write 15 trending hashtags)

### 👤 Instagram Bio
(write stylish instagram bio)
'''

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {
                "role": "user",
                "content": final_prompt
            }
        ]
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=payload
    )

    result = response.json()

    print(result)

    if 'choices' in result:
        content = result['choices'][0]['message']['content']
    else:
        content = str(result)

    return jsonify({
        'content': content
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
