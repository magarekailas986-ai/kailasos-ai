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
background:#020617;
font-family:Arial;
margin:0;
padding:20px;
color:white;
}

.title{
font-size:60px;
font-weight:bold;
text-align:center;
margin-top:30px;

background:linear-gradient(90deg,#00e5ff,#8b5cf6);

-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
}

.subtitle{
text-align:center;
font-size:22px;
margin-top:20px;
margin-bottom:40px;
color:#cbd5e1;
}

.main-box{
background:#08122e;
padding:30px;
border-radius:30px;
max-width:800px;
margin:auto;
box-shadow:0 0 30px rgba(0,255,255,0.15);
}

input, textarea{

width:100%;
padding:20px;
border:none;
border-radius:20px;
background:#0f172a;
color:white;
font-size:20px;
margin-bottom:20px;
box-sizing:border-box;
outline:none;
}

textarea{
height:200px;
resize:none;
}

button{

width:100%;
padding:20px;
border:none;
border-radius:20px;
font-size:22px;
font-weight:bold;
cursor:pointer;
color:white;

background:linear-gradient(
90deg,
#06b6d4,
#8b5cf6
);

}

button:hover{
opacity:0.9;
}

.loading{
display:none;
text-align:center;
margin-top:20px;
font-size:22px;
color:#00ffff;
}

.card{

background:#0f172a;
padding:25px;
border-radius:25px;
margin-top:25px;

box-shadow:
0 0 20px rgba(0,255,255,0.08);
}

.card-title{

font-size:24px;
font-weight:bold;
margin-bottom:15px;
color:#22d3ee;
}

.copy-btn{

margin-top:15px;
padding:12px 20px;
border:none;
border-radius:12px;
cursor:pointer;
font-size:18px;
color:white;

background:#7c3aed;
}

.footer{
text-align:center;
margin-top:50px;
color:#94a3b8;
font-size:18px;
}

</style>

</head>

<body>

<div class="title">
KailasOS AI
</div>

<div class="subtitle">
Generate Viral Captions, Hooks, Hashtags & Bios 🚀
</div>

<div class="main-box">

<input
type="text"
id="topic"
placeholder="Enter Topic"
/>

<textarea
id="prompt"
placeholder="Describe what you want..."
></textarea>

<button onclick="generateAI()">
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

function copyText(text){

navigator.clipboard.writeText(text);

alert("Copied Successfully 🚀");

}

async function generateAI(){

let topic =
document.getElementById("topic").value;

let prompt =
document.getElementById("prompt").value;

document.getElementById(
"loading"
).style.display = "block";

document.getElementById(
"results"
).innerHTML = "";

let response = await fetch(
"/generate",
{
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

document.getElementById(
"loading"
).style.display = "none";

document.getElementById(
"results"
).innerHTML = `

<div class="card">

<div class="card-title">
🔥 Viral Caption
</div>

<div>
${data.caption}
</div>

<button
class="copy-btn"
onclick="copyText(\`${data.caption}\`)">

Copy

</button>

</div>

<div class="card">

<div class="card-title">
🎯 Hook
</div>

<div>
${data.hook}
</div>

<button
class="copy-btn"
onclick="copyText(\`${data.hook}\`)">

Copy

</button>

</div>

<div class="card">

<div class="card-title">
🏷️ Hashtags
</div>

<div>
${data.hashtags}
</div>

<button
class="copy-btn"
onclick="copyText(\`${data.hashtags}\`)">

Copy

</button>

</div>

<div class="card">

<div class="card-title">
👤 Instagram Bio
</div>

<div>
${data.bio}
</div>

<button
class="copy-btn"
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

    topic = data.get("topic","")
    prompt = data.get("prompt","")

    final_prompt = f"""

You are a viral Instagram content creator.

TOPIC:
{topic}

USER REQUEST:
{prompt}

Generate:

Caption:
A powerful emotional viral caption.

Hook:
A scroll stopping hook.

Hashtags:
30 trending hashtags.

Bio:
A premium Instagram bio.

IMPORTANT:
- Keep sections short and clean.
- Use modern viral style.
- Use emojis.
- Follow exact format.

"""

    response = requests.post(

        "https://openrouter.ai/api/v1/chat/completions",

        headers={

            "Authorization":
            f"Bearer {API_KEY}",

            "Content-Type":
            "application/json"

        },

        json={

            "model":
            "openai/gpt-3.5-turbo",

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

    caption = "No caption generated"
    hook = "No hook generated"
    hashtags = "No hashtags generated"
    bio = "No bio generated"

    try:

        text = result["choices"][0]["message"]["content"]

        sections = text.split("Hook:")

        caption = sections[0]\
        .replace("Caption:","")\
        .strip()

        hook_part = sections[1]

        sections2 = hook_part.split(
        "Hashtags:"
        )

        hook = sections2[0].strip()

        hashtags_part = sections2[1]

        sections3 = hashtags_part.split(
        "Bio:"
        )

        hashtags = sections3[0].strip()

        bio = sections3[1].strip()

    except Exception as e:

        print(e)

        caption = str(result)

    return jsonify({

        "caption":caption,
        "hook":hook,
        "hashtags":hashtags,
        "bio":bio

    })

if __name__ == "__main__":

    app.run(
        debug=True,
        host="0.0.0.0"
    )
