from flask import Flask, request, jsonify
import requests
import os
import json

app = Flask(__name__)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


@app.route("/")
def home():
    return open("index.html", encoding="utf-8").read()


@app.route("/generate", methods=["POST"])
def generate():

    try:
        data = request.json

        topic = data.get("topic", "")
        prompt = data.get("prompt", "")

        final_prompt = f"""
You are a viral social media expert.

Topic: {topic}

User Request:
{prompt}

Generate:
1 viral caption
1 viral hook
15 viral hashtags
1 attractive instagram bio

IMPORTANT:
Return ONLY valid JSON.

Example format:

{{
  "caption": "text here",
  "hook": "text here",
  "hashtags": "#tag1 #tag2 #tag3",
  "bio": "text here"
}}

Make everything:
- modern
- viral
- emotional
- engaging
- attractive
- social media optimized
"""

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "openai/gpt-4.1-mini",
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

        ai_text = result["choices"][0]["message"]["content"]

        # JSON CLEANUP
        ai_text = ai_text.replace("```json", "")
        ai_text = ai_text.replace("```", "")
        ai_text = ai_text.strip()

        parsed = json.loads(ai_text)

        return jsonify({
            "caption": parsed.get("caption", ""),
            "hook": parsed.get("hook", ""),
            "hashtags": parsed.get("hashtags", ""),
            "bio": parsed.get("bio", "")
        })

    except Exception as e:
        print("ERROR:", e)

        return jsonify({
            "caption": "Error generating caption",
            "hook": "Error generating hook",
            "hashtags": "#error",
            "bio": "Error generating bio"
        })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
