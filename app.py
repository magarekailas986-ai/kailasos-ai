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
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <style>
        body{
            background:#050816;
            color:white;
            font-family:Arial;
            padding:20px;
            text-align:center;
        }

        h1{
            font-size:50px;
            background:linear-gradient(90deg,#00e5ff,#8a2be2);
            -webkit-background-clip:text;
            -webkit-text-fill-color:transparent;
        }

        .box{
            background:#0f172a;
            padding:20px;
            border-radius:20px;
            max-width:700px;
            margin:auto;
            box-shadow:0 0 20px rgba(0,255,255,0.2);
        }

        input, textarea{
            width:90%;
            padding:15px;
            margin:10px;
            border:none;
            border-radius:10px;
            background:#111827;
            color:white;
            font-size:18px;
        }

        button{
            padding:15px 30px;
            border:none;
            border-radius:12px;
            font-size:20px;
            color:white;
            cursor:pointer;
            background:linear-gradient(90deg,#00e5ff,#c800ff);
        }

        #result{
            margin-top:20px;
            white-space:pre-wrap;
            text-align:left;
        }
    </style>
</head>

<body>

<h1>KailasOS AI</h1>

<p>Generate Viral Captions, Hooks, Hashtags & Bios 🚀</p>

<div class="box">

<input type="text" id="category" placeholder="Category">

<textarea id="prompt" rows="6" placeholder="Type your idea..."></textarea>

<br><br>

<button onclick="generateContent()">Generate AI Content</button>

<div id="result"></div>

</div>

<script>
async function generateContent(){

    document.getElementById("result").innerHTML = "Generating... 🚀";

    let category = document.getElementById("category").value;
    let prompt = document.getElementById("prompt").value;

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

    document.getElementById("result").innerHTML = data.content;
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

    final_prompt = f"""
    Category: {category}

    User Request:
    {prompt}

    Generate:
    - Viral caption
    - Hook
    - Hashtags
    - Bio
    """

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
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
        content = result["choices"][0]["message"]["content"]
    else:
        content = str(result)

    return jsonify({
        "content": content
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
