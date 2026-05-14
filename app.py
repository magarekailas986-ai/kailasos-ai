from flask import Flask, request, jsonify, render_template_string
import requests
import os

app = Flask(__name__)

API_KEY = os.getenv("OPENROUTER_API_KEY")

HTML = """

<!DOCTYPE html>
<html>

<head>

<title>KailasOS AI</title>

<meta name="viewport" content="width=device-width, initial-scale=1.0">

<style>

body{
background:#020b24;
font-family:Arial;
color:white;
padding:20px;
margin:0;
}

.title{
font-size:60px;
font-weight:bold;
text-align:center;
background:linear-gradient(90deg,#00d4ff,#8b5cf6);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
margin-top:40px;
}

.subtitle{
text-align:center;
font-size:22px;
color:#d1d5db;
margin-top:20px;
margin-bottom:40px;
}

.box{
background:#08122e;
padding:30px;
border-radius:30px;
box-shadow:0 0 25px rgba(0,255,255,0.2);
max-width:700px;
margin:auto;
}

input, textarea{
width:100%;
background:#0f172a;
border:none;
border-radius:20px;
padding:20px;
font-size:22px;
color:white;
margin-bottom:20px;
box-sizing:border-box;
}

textarea{
height:200px;
resize:none;
}

button{
width:100%;
padding:22px;
border:none;
border-radius:20px;
font-size:22px;
font-weight:bold;
color:white;
cursor:pointer;
background:linear-gradient(90deg,#22d3ee,#d946ef);
}

button:hover{
opacity:0.9;
}

.result-box{
background:#08122e;
padding:25px;
border-radius:25px;
margin-top:25px;
box-shadow:0 0 20px rgba(0,255,255,0.15);
}

.result-title{
font-size:22px;
font-weight:bold;
margin-bottom:15px;
color:#00d4ff;
}

.copy-btn{
margin-top:15px;
padding:12px 20px;
border:none;
border-radius:12px;
background:#7c3aed;
color:white;
font-size:18px;
cursor:pointer;
}

.footer{
text-align:center;
margin-top:50px;
font-size:18px;
color:#d1d5db;
}

.loading{
text-align:center;
font-size:24px;
margin-top:20px;
color:#00ffff;
display:none;
}

</style>

</head>

<body>

<div class="title">KailasOS AI</div>

<div class="subtitle">
Generate Viral Captions, Hooks, Hashtags & Bios 🚀
</div>

<div class="box">

<input type="text" id="topic" placeholder="Enter Topic">

<textarea id="prompt" placeholder="Describe what you want..."></textarea>

<button onclick="generateContent()">
Generate AI Content
</button>

<div class="loading" id="loading">
Generating Viral Content... 🚀
</div>

<div id="results"></div>

</div>

<div class="footer">
Powered By KailasOS AI ⚡
</div>

<script>

async function generateContent(){

let topic = document.getElementById("topic").value;
let prompt = document.getElementById("prompt").value;

document.getElementById("loading").style.display = "block";

let response = await fetch("/generate",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({
topic:topic,
prompt:prompt
})

});

let data = await response.json();

document.getElementById("loading").style.display = "none";

document.getElementById("results").innerHTML = `

<div class="result-box">
<div class="result-title">🔥 Viral Caption</div>
<div>${data.caption}</div>
<button class="copy-btn" onclick="copyText(\`${data.caption}\`)">Copy</button>
</div>

<div class="result-box">
<div class="result-title">🎯 Hook</div>
<div>${data.hook}</div>
<button class="copy-btn" onclick="copyText(\`${data.hook}\`)">Copy</button>
</div>

<div class="result-box">
<div class="result-title">🏷️ Hashtags</div>
<div>${data.hashtags}</div>
<button class="copy-btn" onclick="copyText(\`${data.hashtags}\`)">Copy</button>
</div>

<div class="result-box">
<div class="result-title">👤 Bio</div>
<div>${data.bio}</div>
<button class="copy-btn" onclick="copyText(\`${data.bio}\`)">Copy</button>
</div>

`;

}

function copyText(text){

navigator.clipboard.writeText(text);

alert("Copied Successfully 🚀");

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

    topic = data["topic"]
    prompt = data["prompt"]

    final_prompt = f"""

Topic: {topic}

User Request:
{prompt}

Create:

1 Viral Caption
1 Hook
1 Hashtags section
1 Instagram Bio

Format exactly like this:

Caption:
...

Hook:
...

Hashtags:
...

Bio:
...

"""

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

    text = result["choices"][0]["message"]["content"]

    caption = ""
    hook = ""
    hashtags = ""
    bio = ""

    try:

        part1 = text.split("Hook:")
        caption = part1[0].replace("Caption:", "").strip()

        part2 = part1[1].split("Hashtags:")
        hook = part2[0].strip()

        part3 = part2[1].split("Bio:")
        hashtags = part3[0].strip()

        bio = part3[1].strip()

    except:

        caption = text
        hook = text
        hashtags = text
        bio = text

    return jsonify({

        "caption": caption,
        "hook": hook,
        "hashtags": hashtags,
        "bio": bio

    })

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
