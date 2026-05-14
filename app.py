from flask import Flask, request, jsonify, render_template_string
import requests
import os

app = Flask(__name__)

API_KEY = os.environ.get("OPENROUTER_API_KEY")

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>KailasOS AI</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<style>
body{
    margin:0;
    padding:0;
    background:#020b2d;
    font-family:Arial,sans-serif;
    color:white;
}

.container{
    width:90%;
    max-width:700px;
    margin:auto;
    padding-top:40px;
    padding-bottom:50px;
}

.title{
    text-align:center;
    font-size:62px;
    font-weight:bold;
    background:linear-gradient(90deg,#00e5ff,#7c4dff);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}

.subtitle{
    text-align:center;
    font-size:22px;
    color:#ddd;
    margin-top:10px;
}

.card{
    margin-top:30px;
    background:#06133d;
    padding:25px;
    border-radius:30px;
    box-shadow:0 0 35px rgba(0,255,255,0.15);
}

input,textarea{
    width:100%;
    background:#0b1b4f;
    border:none;
    outline:none;
    color:white;
    border-radius:22px;
    padding:20px;
    font-size:20px;
    box-sizing:border-box;
    margin-top:15px;
}

textarea{
    height:180px;
    resize:none;
    line-height:1.5;
}

.main-btn{
    width:100%;
    border:none;
    padding:22px;
    border-radius:20px;
    margin-top:25px;
    font-size:24px;
    font-weight:bold;
    color:white;
    cursor:pointer;
    background:linear-gradient(90deg,#00d9ff,#d500f9);
}

.result-box{
    margin-top:25px;
    background:#08143d;
    padding:25px;
    border-radius:25px;
}

.result-title{
    font-size:28px;
    font-weight:bold;
    color:#00d9ff;
    margin-bottom:15px;
}

.result-text{
    font-size:21px;
    line-height:1.6;
    white-space:pre-wrap;
    color:#f5f5f5;
}

.copy-btn{
    width:100%;
    border:none;
    padding:18px;
    margin-top:20px;
    border-radius:18px;
    font-size:22px;
    font-weight:bold;
    color:white;
    cursor:pointer;
    background:linear-gradient(90deg,#7c3aed,#a855f7);
}

.loading{
    display:none;
    text-align:center;
    margin-top:25px;
}

.spinner{
    width:60px;
    height:60px;
    border:6px solid rgba(255,255,255,0.2);
    border-top:6px solid #00e5ff;
    border-radius:50%;
    animation:spin 1s linear infinite;
    margin:auto;
}

.loading-text{
    margin-top:15px;
    font-size:22px;
    color:#00e5ff;
}

.footer{
    text-align:center;
    margin-top:40px;
    color:#aaa;
    font-size:20px;
}

@keyframes spin{
    100%{
        transform:rotate(360deg);
    }
}

@media(max-width:600px){

.title{
    font-size:48px;
}

.subtitle{
    font-size:18px;
}

input,textarea{
    font-size:18px;
}

.result-text{
    font-size:19px;
}

}

</style>
</head>
<body>

<div class="container">

<div class="title">KailasOS AI</div>
<div class="subtitle">Generate Viral Captions, Hooks, Hashtags & Bios 🚀</div>

<div class="card">

<input type="text" id="niche" placeholder="Enter niche e.g Gaming, Fitness, Motivation">

<textarea id="prompt" placeholder="Describe exactly what type of viral content you want..."></textarea>

<button class="main-btn" onclick="generateContent()">Generate AI Content</button>

<div class="loading" id="loading">
    <div class="spinner"></div>
    <div class="loading-text">Generating Viral Content... 🚀</div>
</div>

<div id="results"></div>

</div>

<div class="footer">
Powered By KailasOS AI ⚡
</div>

</div>

<script>

function copyText(id,button){

    const text=document.getElementById(id).innerText;

    navigator.clipboard.writeText(text)
    .then(()=>{
        const original=button.innerText;
        button.innerText="Copied ✅";

        setTimeout(()=>{
            button.innerText=original;
        },2000);
    });
}

async function generateContent(){

    const niche=document.getElementById("niche").value;
    const prompt=document.getElementById("prompt").value;

    document.getElementById("loading").style.display="block";
    document.getElementById("results").innerHTML="";

    const response=await fetch("/generate",{
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify({
            niche:niche,
            prompt:prompt
        })
    });

    const data=await response.json();

    document.getElementById("loading").style.display="none";

    document.getElementById("results").innerHTML=`

    <div class="result-box">
        <div class="result-title">🔥 Viral Caption</div>
        <div class="result-text" id="captionText">${data.caption}</div>
        <button class="copy-btn" onclick="copyText('captionText',this)">Copy</button>
    </div>

    <div class="result-box">
        <div class="result-title">🎯 Hook</div>
        <div class="result-text" id="hookText">${data.hook}</div>
        <button class="copy-btn" onclick="copyText('hookText',this)">Copy</button>
    </div>

    <div class="result-box">
        <div class="result-title">🏷️ Hashtags</div>
        <div class="result-text" id="hashtagText">${data.hashtags}</div>
        <button class="copy-btn" onclick="copyText('hashtagText',this)">Copy</button>
    </div>

    <div class="result-box">
        <div class="result-title">👤 Instagram Bio</div>
        <div class="result-text" id="bioText">${data.bio}</div>
        <button class="copy-btn" onclick="copyText('bioText',this)">Copy</button>
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

    data=request.get_json()

    niche=data.get("niche")
    prompt=data.get("prompt")

    final_prompt=f'''
You are a professional viral social media content creator.

Niche: {niche}

User Request:
{prompt}

Generate exactly in this format:

Caption:
(Short powerful viral caption maximum 2 lines)

Hook:
(Attention grabbing hook maximum 2 lines)

Hashtags:
(Only 15 trending hashtags)

Bio:
(Short premium Instagram bio)

Keep everything stylish, modern, emotional and viral.
Do not generate long paragraphs.
'''

    response=requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization":f"Bearer {API_KEY}",
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

    result=response.json()

    if "choices" not in result:
        return jsonify({
            "caption":"API Error",
            "hook":"API Error",
            "hashtags":"API Error",
            "bio":"API Error"
        })

    content=result["choices"][0]["message"]["content"]

    caption=""
    hook=""
    hashtags=""
    bio=""

    mode=""

    for line in content.split("
"):

        low=line.lower()

        if "caption" in low:
            mode="caption"
            continue

        elif "hook" in low:
            mode="hook"
            continue

        elif "hashtags" in low:
            mode="hashtags"
            continue

        elif "bio" in low:
            mode="bio"
            continue

        if mode=="caption":
            caption += line + "
"

        elif mode=="hook":
            hook += line + "
"

        elif mode=="hashtags":
            hashtags += line + "
"

        elif mode=="bio":
            bio += line + "
"

    return jsonify({
        "caption":caption.strip(),
        "hook":hook.strip(),
        "hashtags":hashtags.strip(),
        "bio":bio.strip()
    })

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
