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
    font-family:Arial;
    color:white;
}

.container{
    width:90%;
    margin:auto;
    padding-top:40px;
    padding-bottom:50px;
}

.title{
    text-align:center;
    font-size:60px;
    font-weight:bold;
    background:linear-gradient(90deg,#00e5ff,#7c4dff);
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
    background:#06133d;
    border-radius:30px;
    padding:25px;
    margin-top:30px;
    box-shadow:0 0 25px rgba(0,255,255,0.2);
}

input, textarea{
    width:100%;
    background:#0b1b4f;
    border:none;
    color:white;
    padding:18px;
    border-radius:20px;
    font-size:22px;
    margin-top:15px;
    box-sizing:border-box;
}

textarea{
    height:180px;
    resize:none;
}

button{
    width:100%;
    border:none;
    margin-top:25px;
    padding:22px;
    border-radius:20px;
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
    font-size:26px;
    font-weight:bold;
    color:#00d9ff;
    margin-bottom:15px;
}

.result-text{
    font-size:20px;
    line-height:1.5;
    white-space:pre-wrap;
}

.copy-btn{
    margin-top:20px;
    background:linear-gradient(90deg,#7c3aed,#a855f7);
    padding:16px;
    border-radius:18px;
    text-align:center;
    font-size:22px;
    font-weight:bold;
}

.loading{
    text-align:center;
    margin-top:20px;
    font-size:22px;
    color:#00e5ff;
    display:none;
}

.footer{
    text-align:center;
    margin-top:40px;
    color:#aaa;
    font-size:20px;
}

@media(max-width:600px){
    .title{
        font-size:48px;
    }

    .subtitle{
        font-size:18px;
    }

    input, textarea{
        font-size:20px;
    }

    button{
        font-size:22px;
    }
}
</style>
</head>

<body>

<div class="container">

<div class="title">KailasOS AI</div>
<div class="subtitle">Generate Viral Captions, Hooks, Hashtags & Bios 🚀</div>

<div class="card">

<input type="text" id="niche" placeholder="Enter niche e.g Gaming">

<textarea id="prompt" placeholder="Describe what you want..."></textarea>

<button onclick="generateContent()">Generate AI Content</button>

<div class="loading" id="loading">
Generating Viral Content... 🚀
</div>

<div id="results"></div>

</div>

<div class="footer">
Powered By KailasOS AI ⚡
</div>

</div>

<script>

function copyText(id){
    const element = document.getElementById(id);

    if(!element){
        alert("Content not found");
        return;
    }

    const text = element.innerText;

    navigator.clipboard.writeText(text)
    .then(()=>{
        alert("Copied Successfully ✅");
    })
    .catch(()=>{
        alert("Copy Failed ❌");
    });
}

async function generateContent(){

    let niche = document.getElementById("niche").value;
    let prompt = document.getElementById("prompt").value;

    document.getElementById("loading").style.display = "block";

    const response = await fetch("/generate",{
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify({
            niche:niche,
            prompt:prompt
        })
    });

    const data = await response.json();

    document.getElementById("loading").style.display = "none";

    document.getElementById("results").innerHTML = `

    <div class="result-box">
        <div class="result-title">🔥 Viral Caption</div>
        <div class="result-text" id="captionText">${data.caption}</div>
        <button class="copy-btn" onclick="copyText('captionText')">Copy</button>
    </div>

    <div class="result-box">
        <div class="result-title">🎯 Hook</div>
        <div class="result-text" id="hookText">${data.hook}</div>
        <button class="copy-btn" onclick="copyText('hookText')">Copy</button>
    </div>

    <div class="result-box">
        <div class="result-title">🏷️ Hashtags</div>
        <div class="result-text" id="hashtagText">${data.hashtags}</div>
        <button class="copy-btn" onclick="copyText('hashtagText')">Copy</button>
    </div>

    <div class="result-box">
        <div class="result-title">👤 Instagram Bio</div>
        <div class="result-text" id="bioText">${data.bio}</div>
        <button class="copy-btn" onclick="copyText('bioText')">Copy</button>
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

    data = request.get_json()

    niche = data.get("niche")
    prompt = data.get("prompt")

    final_prompt = f'''
    Niche: {niche}

    User Request:
    {prompt}

    Generate:
    1 Viral Caption
    1 Hook
    20 Hashtags
    1 Instagram Bio

    Make everything highly viral and attractive.
    '''

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "openai/gpt-3.5-turbo",
            "messages": [
                {
                    "role": "user",
                    "content": final_prompt
                }
            ]
        }
    )

    result = response.json()

    print(result)

    if "choices" in result:
        content = result["choices"][0]["message"]["content"]
    else:
        return jsonify({
            "caption":"API Error",
            "hook":"API Error",
            "hashtags":"API Error",
            "bio":"API Error"
        })

    lines = content.split("\n")

    caption = ""
    hook = ""
    hashtags = ""
    bio = ""

    mode = ""

    for line in lines:

        low = line.lower()

        if "caption" in low:
            mode = "caption"
            continue

        elif "hook" in low:
            mode = "hook"
            continue

        elif "hashtag" in low:
            mode = "hashtags"
            continue

        elif "bio" in low:
            mode = "bio"
            continue

        if mode == "caption":
            caption += line + "\n"

        elif mode == "hook":
            hook += line + "\n"

        elif mode == "hashtags":
            hashtags += line + "\n"

        elif mode == "bio":
            bio += line + "\n"

    return jsonify({
        "caption": caption,
        "hook": hook,
        "hashtags": hashtags,
        "bio": bio
    })

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
