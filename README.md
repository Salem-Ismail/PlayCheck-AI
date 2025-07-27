# PlayCheck AI - Football Rules Assistant

An AI-powered football rules assistant that helps referees, players, and fans understand FIFA's Laws of the Game through intelligent search and interpretation.

## Features

- Intelligent Rule Search: TF-IDF semantic search through FIFA laws
- AI-Powered Interpretation: GPT-4 analysis with rule context
- Confidence Scoring: Shows how certain the system is about answers
- Modern Chat Interface: Clean, responsive design
- Real-time Responses: Instant rule clarification and analysis

## Quick Start

### Prerequisites
- Python 3.8+
- OpenAI API key

### Installation

1. Clone the repository
   ```bash
   git clone https://github.com/YOUR_USERNAME/PlayCheck-AI.git
   cd PlayCheck-AI
   ```

2. Install Python dependencies
   ```bash
   cd Backend
   pip install -r requirements.txt
   ```

3. Set up environment variables
   ```bash
   # Copy the example file
   cp env.example .env
   
   # Edit .env and add your OpenAI API key
   OPENAI_API_KEY=your_actual_api_key_here
   ```

4. Start the backend
   ```bash
   python app.py
   ```

5. Open the frontend
   - Navigate to `Frontend/src/chat.html`
   - Open in your web browser
   - Start asking questions!

## Usage Examples

### Basic Rule Queries
```
"What happens if a player handles the ball in the penalty area?"
"What's the restart if the ball hits the referee?"
```

### Complex Scenarios
```
"A defender deliberately handles the ball in the penalty area with no attempt to play the ball. Does the referee award a penalty and issue a red card for denying a goal?"
```

*Note: This project is in its early stages and is subject to significant changes, including updates to the feature set and tech stack.*