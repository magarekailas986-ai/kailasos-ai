from flask import Flask, request, jsonify, render_template_string
import requests
import os

app = Flask(__name__)

API_KEY = os.getenv("OPENROUTER_API_KEY")

HTML = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">

<title>KailasOS AI</title>

<style>

body{
    margin:0;
    padding:20px;
    background:#020617;
    color:white;
    font-family:Arial;
    text-align:center;
}

h1{
    font-size:60px;
    background:linear-gradient(90deg,#00e5ff,#7c3aed);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    margin-top:20px;
}

.subtitle{
    font-size:20px;
    color:#cbd5e1;
    margin-bottom:30px;
}

.container{
    max-width:850px;
    margin:auto;
    background:#0f172a;
    padding:25px;
    border-radius:25px;
    box-shadow:0 0 40px rgba(0,255,255,0.15);
}

input, textarea{
    width:90%;
    padding:18px;
    margin:15px 0;
    border:none;
    border-radius:15px;
    background:#111827;
    color:white;
    font-size:18px;
    outline:none;
}

button{
    padding:18px 40px;
    border:none;
    border-radius:15px;
    font-size:22px;
    font-weight:bold;
    color:white;
    cursor:pointer;
    background:linear-gradient(90deg,#00e5ff,#d400ff);
    transition:0.3s;
}

button:hover{
    transform:scale(1.05);
}

.loading{
    margin-top:20px;
    font-size:22px;
    color:#00e5ff;
}

.card{
    background:#111827;
    margin-top:25px;
    padding:20px;
    border-radius:20px;
    text-align:left;
    box-shadow:0 0 20px rgba(0,255,255,0.1);
}

.card h2{
    color:#00e5ff;
}

.copy-btn{
    margin-top:15px;
    padding:10px 20px;
    border:none;
    border-radius:10px;
    background:#7c3aed;
    color:white;
    cursor:pointer;
}

.footer{
    margin-top:40px;
    color:#94a3b8;
}

</style>
</head>

<body>

<h1>KailasOS AI</h1>

<div class="subtitle">
Generate Viral Captions, Hooks, Hashtags & Bios 🚀
</div>

<div class="container">

<input type="text" id="category" placeholder="Enter category">

<textarea id="prompt" rows="6" placeholder="Describe what you want..."></textarea>

<br>

<button onclick="generateContent()">
Generate AI Content
</button>

<div class="loading" id="loading"></div>

<div id="result"></div>

</div>

<div class="footer">
Powered By KailasOS AI ⚡
</div>

<script>

function copyText(text){
    navigator.clipboard.writeText(text);
    alert("Copied!");
}

async function generateContent(){

    document.getElementById("loading").innerHTML =
    "Generating Viral Content... 🚀";

    document.getElementById("result").innerHTML = "";

    let category =
    document.getElementById("category").value;

    let prompt =
    document.getElementById("prompt").value;

    let response = await fetch("/generate",{
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify({
            category:category,
            prompt:prompt
        })
    });

    let data = await response.json();

    document.getElementById("loading").innerHTML = "";

    document.getElementById("result").innerHTML = `
    
    <div class="card">
        <h2>🔥 Viral Caption</h2>
        <p>${data.caption}</p>
        <button class="copy-btn"
        onclick="copyText(\`${data.caption}\`)">
        Copy
        </button>
    </div>

    <div class="card">
        <h2>🎯 Hook</h2>
        <p>${data.hook}</p>
        <button class="copy-btn"
        onclick="copyText(\`${data.hook}\`)">
        Copy
        </button>
    </div>

    <div class="card">
        <h2>🏷️ Hashtags</h2>
        <p>${data.hashtags}</p>
        <button class="copy-btn"
        onclick="copyText(\`${data.hashtags}\`)">
        Copy
        </button>
    </div>

    <div class="card">
        <h2>👤 Bio</h2>
        <p>${data.bio}</p>
        <button class="copy-btn"
        onclick="copyText(\`${data.bio}\`)">
        Copy
        </button>
    </div>

    `;
}

</script>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/generate", methods=["POST"])
def generate():

    data = request.json

    category = data.get("category","")
    prompt = data.get("prompt","")

    final_prompt = f'''
    Category: {category}

    User Request:
    {prompt}

    Give response in EXACT format:

    Caption:
    ...

    Hook:
    ...

    Hashtags:
    ...

    Bio:
    ...
    '''

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type":"application/json"
        },
        json={
            "model":"openai/gpt-3.5-turbo",
            "messages":[
                {
                    "role":"user",
                    "content":final_prompt
                }
            ]
        }
    )

    result = response.json()

    print(result)

    if "choices" in result:

        text = result["choices"][0]["message"]["content"]

        caption = ""
        hook = ""
        hashtags = ""
        bio = ""

        parts = text.split("\\n")

        current = ""

        for line in parts:

            if "Caption:" in line:
                current = "caption"
                continue

            elif "Hook:" in line:
                current = "hook"
                continue

            elif "Hashtags:" in line:
                current = "hashtags"
                continue

            elif "Bio:" in line:
                current = "bio"
                continue

            if current == "caption":
                caption += line + " "

            elif current == "hook":
                hook += line + " "

            elif current == "hashtags":
                hashtags += line + " "

            elif current == "bio":
                bio += line + " "

        return jsonify({
            "caption": caption,
            "hook": hook,
            "hashtags": hashtags,
            "bio": bio
        })

    else:

        return jsonify({
            "caption":"API Error",
            "hook":"API Error",
            "hashtags":str(result),
            "bio":"API Error"
        })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
