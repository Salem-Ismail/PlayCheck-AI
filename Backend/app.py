import json
from flask import Flask, request, jsonify
from search_laws import search_law, load_fifa_laws
from database import DatabaseManager
import os
import openai
from dotenv import load_dotenv
from flask_cors import CORS
import logging
import urllib.parse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Initialize database manager
import os
print(f"Current working directory: {os.getcwd()}")
print(f"Database file exists: {os.path.exists('playcheck.db')}")
db_manager = DatabaseManager()
db_manager.connect()

# Database connected for FIFA laws (AI chat functionality)

# Load FIFA Laws from database
fifa_laws = {"laws": db_manager.get_all_laws()}

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

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy", "message": "Backend server is running"})

@app.route("/get_rule", methods=["POST"])
def get_rule():
    try:
        logger.info("Received request to /get_rule")
        data = request.get_json()
        user_query = data.get("query", "")
        logger.debug(f"User query: {user_query}")

        if not user_query:
            logger.warning("No query provided in request")
            return jsonify({"error": "No query provided"}), 400

        logger.info("Searching for relevant laws...")
        # Retrieve multiple relevant laws
        relevant_laws_with_scores = search_law(user_query, laws, top_n=3)
        logger.info(f"Found {len(relevant_laws_with_scores)} relevant laws")

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
        logger.info("Calling OpenAI API...")
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": ai_prompt}],
                temperature=0.2
            )
            logger.info("OpenAI API call successful")
        except Exception as api_error:
            logger.error(f"OpenAI API error: {api_error}")
            raise api_error

        # Handle edge cases where OpenAI might return an empty response
        if response.choices and response.choices[0].message:
            answer = response.choices[0].message.content.strip()
        else:
            answer = "I'm sorry, I couldn't generate a response."
            
        logger.debug(f"Generated answer: {answer[:100]}...")  # Only log first 100 chars in debug mode


        return jsonify({"response": answer})

    except Exception as e:
        logger.error(f"Error in get_rule: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route("/feedback", methods=["POST"])
def receive_feedback():
    try:
        data = request.get_json()
        question = data.get("question", "")
        response = data.get("response", "")
        rating = data.get("rating", "")
        timestamp = data.get("timestamp", "")
        
        # Decode URL-encoded response text
        decoded_response = urllib.parse.unquote(response)
        
        # Log feedback to file with better formatting
        feedback_entry = f"""
=== FEEDBACK ===
Time: {timestamp}
Rating: {rating.upper()}
Question: {question}

Response: {decoded_response}

========================
"""
        
        with open("feedback_log.txt", "a", encoding="utf-8") as f:
            f.write(feedback_entry)
        
        logger.info(f"Feedback received: {rating} rating")
        return jsonify({"status": "success"})
        
    except Exception as e:
        logger.error(f"Error processing feedback: {str(e)}")
        return jsonify({"error": str(e)}), 500


# Scenario endpoints removed - using simple frontend JavaScript instead


if __name__ == "__main__":
    app.run(debug=True)
