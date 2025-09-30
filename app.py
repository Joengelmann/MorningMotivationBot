from flask import Flask, render_template, request
import openai
import os
from dotenv import load_dotenv
import re
from textblob import TextBlob

def analyze_sentiment(text):
    return TextBlob(text).sentiment.polarity  # Range: -1 (negative) to 1 (positive)

# Load environment variables
load_dotenv()

# Configure OpenAI client using new v1 API
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)

def get_motivation(user_input, tone):
    sentiment = analyze_sentiment(user_input)

    if sentiment < -0.3:
        mood = "You are a very supportive life coach. The user is feeling low today."
    elif sentiment < 0.3:
        mood = "You are an encouraging life coach. The user is feeling a bit off."
    else:
        mood = "You are a high-energy life coach. The user is already in a good mood!"

    prompt = (
        f"{mood} The user has just woken up and feels: '{user_input}'. "
        f"Write your entire response in a {tone.lower()} tone. "
        "Reply with a motivational message to explaining to them why they should excited for the day. "
        "Also Write a haiku that addresses the user's feelings and ends with optimism. "
        "Also give 3 actionable steps to help them improve their morning. "
        "Also include a cheerful, UNIQUE YouTube music video that fits for their feelings. "
        "PLEASE INCLUDE THE YOUTUBE URL ON A NEW LINE AT THE BOTTOM AND MAKE SURE THE VIDEO IS CURRENTLY AVAILABLE ON YOUTUBE. "
        "DO NOT CHOOSE A SONG WRITTEN BY RICK ASTLEY!"
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": mood},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.9
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("Error:", e)
        return "Sorry, I couldn't think of anything right now — but you're awesome!"

def generate_peaceful_image(user_input, tone):
    try:
        image_prompt = f"A morning scene to help convince someone to get out of bed who is feeling {user_input} with a {tone.lower()} tone"
        response = client.images.generate(
            model="dall-e-3",
            prompt=image_prompt,
            size="1024x1024",
            quality="standard",
            n=1
        )
        return response.data[0].url
    except Exception as e:
        print("Image generation error:", e)
        return None

def extract_youtube_video_id(text):
    match = re.search(r"(?:https?://)?(?:www\.)?youtu(?:be\.com/watch\?v=|\.be/)([\w\-]{11})", text)
    return match.group(1) if match else None

@app.route('/', methods=['GET', 'POST'])
def index():
    motivation = None
    video_id = None
    image_url = None
    if request.method == 'POST':
        user_input = request.form['feeling']
        tone = request.form['tone']
        motivation = get_motivation(user_input, tone)
        video_id = extract_youtube_video_id(motivation)
        image_url = generate_peaceful_image(user_input, tone)
    return render_template('index.html', response=motivation, video_id=video_id, image_url=image_url)
    
if __name__ == '__main__':
    app.run(debug=True)
