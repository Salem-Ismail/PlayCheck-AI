import json
from flask import Flask, request, jsonify
from search_laws import search_law, load_fifa_laws
import os
import openai
from dotenv import load_dotenv
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Load FIFA Laws of the Game JSON
with open("fifa_laws.json", "r", encoding="utf-8") as file:
    fifa_laws = json.load(file)

laws = load_fifa_laws()["laws"]


def find_relevant_law(user_query):
    """
    Uses TF-IDF ranking to find the most relevant FIFA law.
    """
    law_title, law_summary = search_law(user_query, laws)
    return law_title, law_summary


@app.route("/")
def home():
    return """
    <h1>PlayCheck AI Football Rules Assistant</h1>
    <p>Backend is running successfully!</p>
    <p>Open <a href="../Frontend/src/chat.html">chat.html</a> to use the chat interface.</p>
    """

@app.route("/test", methods=["GET"])
def test():
    return jsonify({"message": "Backend is working!"})

@app.route("/get_rule", methods=["POST"])
def get_rule():
    try:
        print("Received request to /get_rule")
        data = request.get_json()
        user_query = data.get("query", "")
        print(f"User query: {user_query}")

        if not user_query:
            return jsonify({"error": "No query provided"}), 400

        print("Searching for relevant laws...")
        # Retrieve multiple relevant laws
        relevant_laws_with_scores = search_law(user_query, laws, top_n=3)
        print(f"Found {len(relevant_laws_with_scores)} relevant laws")

        # Format the laws for the AI
        law_context = "\n\n".join([
            f"Law {law_dict['number']}: {law_dict['title']} - {law_dict['summary']} (Confidence: {int(score*100)}%)" 
            for law_dict, score in relevant_laws_with_scores
        ])

        # Enhanced AI prompt with structured format
        ai_prompt = f"""
You are PlayCheck AI, an expert football referee assistant trained on FIFA's Laws of the Game. 
Your job is to analyze match scenarios and provide clear, structured explanations.

**Below are some potentially relevant FIFA Laws:**
{law_context}

**ANALYZE THIS SCENARIO:** "{user_query}"

**PROVIDE YOUR RESPONSE IN THIS EXACT STRUCTURED FORMAT:**

**SUMMARY:** [Provide a short 1-2 sentence summary of the applicable law(s)]

**SANCTIONS:** [List all applicable sanctions/cards - yellow cards, red cards, etc. Include multiple sanctions if multiple offenses occur]

**RESTART:** [Specify the exact restart method - free kick, penalty kick, throw-in, etc.]

**FINAL DECISION:** [Provide the clear final decision the referee should make]

If no specific FIFA Law covers this situation, respond with: "No specific FIFA Law covers this situation."

**IMPORTANT:** Be thorough - if multiple offenses occur, address each one. If multiple players are involved, specify sanctions for each.
"""

        # Call OpenAI API
        print("Calling OpenAI API...")
        try:
            response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": ai_prompt}],
            temperature=0.2
        )
            print("OpenAI API call successful")
        except Exception as api_error:
            print(f"OpenAI API error: {api_error}")
            raise api_error

        # Handle edge cases where OpenAI might return an empty response
        if response.choices and response.choices[0].message:
            answer = response.choices[0].message.content.strip()
        else:
            answer = "I'm sorry, I couldn't generate a response."
            
        print(f"Generated answer: {answer[:100]}...")  # Print first 100 chars


        return jsonify({"response": answer})

    except Exception as e:
        print(f"Error in get_rule: {str(e)}")  # Add this for debugging
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
