from flask import Flask, request, jsonify, render_template_string
import requests
import json

app = Flask(__name__)

API_KEY = " "

HTML = """

<!DOCTYPE html>
<html>
<head>

<title>KailasOS AI Generator</title>

<meta name="viewport" content="width=device-width, initial-scale=1.0">

<style>

body{
margin:0;
padding:0;
background:#050816;
font-family:Arial;
color:white;
overflow-x:hidden;
}

.container{
max-width:700px;
margin:auto;
padding:20px;
}

.title{
font-size:50px;
font-weight:bold;
text-align:center;
margin-top:40px;
background:linear-gradient(90deg,#00f5ff,#8a2be2);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
}

.subtitle{
text-align:center;
font-size:20px;
color:#bbb;
margin-top:15px;
margin-bottom:40px;
}

.card{
background:rgba(255,255,255,0.05);
padding:25px;
border-radius:30px;
backdrop-filter:blur(12px);
box-shadow:0 0 40px rgba(0,255,255,0.12);
}

input, textarea{
width:100%;
padding:18px;
margin-top:15px;
margin-bottom:20px;
border:none;
outline:none;
border-radius:18px;
background:#0f172a;
color:white;
font-size:18px;
box-sizing:border-box;
}

textarea{
min-height:180px;
resize:none;
}

button{
width:100%;
padding:18px;
border:none;
border-radius:18px;
font-size:22px;
font-weight:bold;
cursor:pointer;
background:linear-gradient(90deg,#00f5ff,#0044ff,#b100ff);
color:white;
transition:0.3s;
}

button:hover{
transform:scale(1.03);
}

.loading{
display:none;
text-align:center;
font-size:20px;
margin-top:25px;
color:cyan;
animation:pulse 1s infinite;
}

@keyframes pulse{
0%{opacity:0.3;}
50%{opacity:1;}
100%{opacity:0.3;}
}

.result-card{
margin-top:35px;
padding:25px;
border-radius:30px;
background:rgba(255,255,255,0.05);
border:1px solid rgba(255,255,255,0.1);
box-shadow:0 0 30px rgba(0,255,255,0.12);
animation:fade 0.5s ease;
}

@keyframes fade{
from{
opacity:0;
transform:translateY(25px);
}
to{
opacity:1;
transform:translateY(0);
}
}

.result-title{
font-size:28px;
font-weight:bold;
margin-bottom:20px;
color:#00f5ff;
}

.copy-btn{
margin-top:25px;
padding:14px;
font-size:18px;
background:linear-gradient(90deg,#00f5ff,#8a2be2);
}

.footer{
text-align:center;
margin-top:50px;
margin-bottom:40px;
font-size:18px;
color:#888;
}

.glow{
position:fixed;
width:300px;
height:300px;
background:cyan;
filter:blur(160px);
opacity:0.08;
top:-50px;
left:-50px;
z-index:-1;
}

.glow2{
position:fixed;
width:300px;
height:300px;
background:purple;
filter:blur(160px);
opacity:0.08;
bottom:-50px;
right:-50px;
z-index:-1;
}

</style>

</head>

<body>

<div class="glow"></div>
<div class="glow2"></div>

<div class="container">

<div class="title">
KailasOS AI
</div>

<div class="subtitle">
Generate Viral Captions, Hooks, Hashtags & Bios 🚀
</div>

<div class="card">

<input
type="text"
id="style"
placeholder="Enter category (Example: Gaming Reel, Crypto Page, Dentist Clinic...)"
/>

<textarea
id="idea"
placeholder="Describe your content idea..."
></textarea>

<button onclick="generateContent()">
Generate AI Content
</button>

<div class="loading" id="loading">
Generating Viral Content... 🚀
</div>

</div>

<div id="result"></div>

<div class="footer">
Powered By KailasOS AI ⚡
</div>

</div>

<script>

async function generateContent(){

const style=document.getElementById("style").value;
const idea=document.getElementById("idea").value;

if(style.trim()=="" || idea.trim()==""){
alert("Please fill all fields 😄");
return;
}

document.getElementById("loading").style.display="block";
document.getElementById("result").innerHTML="";

const response=await fetch("/generate",{
method:"POST",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify({
style:style,
idea:idea
})
});

const data=await response.json();

document.getElementById("loading").style.display="none";

document.getElementById("result").innerHTML=`

<div class="result-card">

<div class="result-title">
🔥 AI Generated Content
</div>

<div id="contentText"
style="
white-space:pre-wrap;
line-height:1.8;
font-size:18px;
color:#eee;
">
${data.content}
</div>

<button class="copy-btn" onclick="copyContent()">
Copy Content 📋
</button>

</div>

`;

}

function copyContent(){

const text=document.getElementById("contentText").innerText;

navigator.clipboard.writeText(text);

alert("Content Copied Successfully 🚀");

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

    style = data["style"]
    idea = data["idea"]

    prompt = f"""
Create a premium viral social media content package.

Category:
{style}

Idea:
{idea}

Include:

1. Viral Hook
2. Instagram Caption
3. Trending Hashtags
4. Instagram Bio
5. Call To Action

Make the content:
- modern
- emotional
- premium
- viral
- highly engaging

Use emojis beautifully.
"""

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        data=json.dumps({
            "model":"inclusionai/ring-2.6-1t:free",
            "messages":[
                {
                    "role":"user",
                    "content":prompt
                }
            ]
        })
    )

    result = response.json()

    content = result["choices"][0]["message"]["content"]

    return jsonify({
        "content":content
    })

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
