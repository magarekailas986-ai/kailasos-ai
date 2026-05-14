from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return """
<!DOCTYPE html>
<html>
<head>

<title>KailasOS AI</title>

<meta name="viewport" content="width=device-width, initial-scale=1.0">

<style>

body{
    margin:0;
    padding:0;
    background:#020b2b;
    font-family:Arial,sans-serif;
    color:white;
}

.container{
    width:90%;
    max-width:700px;
    margin:auto;
    padding:20px;
}

.title{
    text-align:center;
    font-size:55px;
    font-weight:bold;
    margin-top:40px;
    background:linear-gradient(90deg,#00d2ff,#7f5cff);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}

.subtitle{
    text-align:center;
    font-size:20px;
    margin-top:10px;
    color:#cccccc;
}

.card{
    background:#07133f;
    padding:25px;
    border-radius:25px;
    margin-top:35px;
    box-shadow:0 0 25px rgba(0,200,255,0.15);
}

input, textarea{
    width:100%;
    box-sizing:border-box;
    background:#0b1a52;
    border:none;
    border-radius:20px;
    padding:18px;
    color:white;
    font-size:20px;
    margin-bottom:20px;
    outline:none;
}

textarea{
    height:180px;
    resize:none;
}

.main-btn{
    width:100%;
    border:none;
    padding:20px;
    border-radius:20px;
    font-size:22px;
    font-weight:bold;
    color:white;
    cursor:pointer;
    background:linear-gradient(90deg,#00d2ff,#d400ff);
}

.result-card{
    background:#06103a;
    padding:25px;
    border-radius:25px;
    margin-top:30px;
    box-shadow:0 0 18px rgba(0,255,255,0.08);
}

.result-title{
    font-size:28px;
    font-weight:bold;
    color:#00d2ff;
    margin-bottom:15px;
}

.result-text{
    font-size:22px;
    line-height:1.7;
    white-space:pre-wrap;
    word-wrap:break-word;
}

.copy-btn{
    width:100%;
    margin-top:20px;
    border:none;
    padding:16px;
    border-radius:18px;
    font-size:20px;
    font-weight:bold;
    color:white;
    cursor:pointer;
    background:linear-gradient(90deg,#6a11cb,#a044ff);
}

.footer{
    text-align:center;
    margin-top:40px;
    margin-bottom:30px;
    color:#cccccc;
    font-size:18px;
}

.loading{
    text-align:center;
    font-size:22px;
    margin-top:25px;
    color:#00d2ff;
}

</style>

</head>

<body>

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
id="topic"
placeholder="Enter Topic"
/>

<textarea
id="prompt"
placeholder="Describe what you want..."
></textarea>

<button
class="main-btn"
onclick="generateContent()">
Generate AI Content
</button>

</div>

<div id="loading"></div>

<div id="results"></div>

<div class="footer">
Powered By KailasOS AI ⚡
</div>

</div>

<script>

function copyText(text){

    navigator.clipboard.writeText(text)
    .then(function(){
        alert("Copied Successfully!");
    });

}

async function generateContent(){

    let topic = document.getElementById("topic").value;

    let prompt = document.getElementById("prompt").value;

    document.getElementById("loading").innerHTML =
    '<div class="loading">Generating AI Content... 🚀</div>';

    document.getElementById("results").innerHTML = "";

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

    document.getElementById("loading").innerHTML = "";

    document.getElementById("results").innerHTML = `

    <div class="result-card">

        <div class="result-title">
        🔥 Viral Caption
        </div>

        <div class="result-text">
        ${data.caption}
        </div>

        <button
        class="copy-btn"
        onclick='copyText(${JSON.stringify("CAPTION_PLACEHOLDER")})'>
        Copy
        </button>

    </div>

    <div class="result-card">

        <div class="result-title">
        🎯 Hook
        </div>

        <div class="result-text">
        ${data.hook}
        </div>

        <button
        class="copy-btn"
        onclick='copyText(${JSON.stringify("HOOK_PLACEHOLDER")})'>
        Copy
        </button>

    </div>

    <div class="result-card">

        <div class="result-title">
        🏷️ Hashtags
        </div>

        <div class="result-text">
        ${data.hashtags}
        </div>

        <button
        class="copy-btn"
        onclick='copyText(${JSON.stringify("HASHTAGS_PLACEHOLDER")})'>
        Copy
        </button>

    </div>

    <div class="result-card">

        <div class="result-title">
        👤 Instagram Bio
        </div>

        <div class="result-text">
        ${data.bio}
        </div>

        <button
        class="copy-btn"
        onclick='copyText(${JSON.stringify("BIO_PLACEHOLDER")})'>
        Copy
        </button>

    </div>

    `;

    document.querySelectorAll(".copy-btn")[0]
    .setAttribute(
        "onclick",
        "copyText(" + JSON.stringify(data.caption) + ")"
    );

    document.querySelectorAll(".copy-btn")[1]
    .setAttribute(
        "onclick",
        "copyText(" + JSON.stringify(data.hook) + ")"
    );

    document.querySelectorAll(".copy-btn")[2]
    .setAttribute(
        "onclick",
        "copyText(" + JSON.stringify(data.hashtags) + ")"
    );

    document.querySelectorAll(".copy-btn")[3]
    .setAttribute(
        "onclick",
        "copyText(" + JSON.stringify(data.bio) + ")"
    );

}

</script>

</body>
</html>
"""

@app.route("/generate", methods=["POST"])
def generate():

    data = request.json

    topic = data.get("topic","")
    prompt = data.get("prompt","")

    caption = f"Dare to stand out in the world of {topic}! 🚀🔥"

    hook = f"Stop scrolling! The future of {topic} starts here 😎⚡"

    hashtags = f'''
#{topic.replace(" ","")}
#Viral
#Trending
#InstaFamous
#ContentCreator
#ExplorePage
#Reels
#SocialMedia
#Growth
#AI
'''

    bio = f'''
🚀 Passionate about {topic}

🔥 Creating viral content daily

⚡ Helping creators grow faster

📩 DM for collaborations

🌎 Dream Big. Create Bigger.
'''

    return jsonify({
        "caption":caption,
        "hook":hook,
        "hashtags":hashtags,
        "bio":bio
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
