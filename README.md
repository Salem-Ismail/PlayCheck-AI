# PlayCheck AI - Football Rules Assistant

An AI-powered football rules assistant that helps referees, players, and fans understand FIFA's Laws of the Game through intelligent search and interpretation.

## Features

- Intelligent Rule Search: TF-IDF semantic search through FIFA laws
- AI-Powered Interpretation: GPT-4 analysis with rule context
- Confidence Scoring: Shows how certain the system is about answers
- Modern Chat Interface: Clean, responsive design
- Real-time Responses: Instant rule clarification and analysis

## Live App

- Backend + Frontend (served by Flask): `https://playcheck-ai.onrender.com/`
- Key routes:
  - `/` → Home
  - `/chat` → Chat interface
  - `/trees` → Decision Trees
  - `/training` → Training (Coming Soon)
  - `/tools` → Reference Tools
  - `/quick-reference` → Quick Reference Cards

## Quick Start (Local)

### Prerequisites
- Python 3.10 (recommended)
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
   # from Backend/
   python app.py
   ```

5. Open the app locally
   - Visit `http://127.0.0.1:5000/` for Home
   - Chat at `http://127.0.0.1:5000/chat`
   - Other pages: `/trees`, `/training`, `/tools`, `/quick-reference`

## Deployment (Render)

1. Create a new Web Service on Render and point it to this repo
2. Build command: `pip install -r Backend/requirements.txt`
3. Start command: `cd Backend && gunicorn app:app --workers 2 --timeout 120`
4. Environment Variables:
   - `OPENAI_API_KEY` = your OpenAI key
   - `FLASK_DEBUG` = False
   - `PYTHON_VERSION` = 3.10.12

Notes:
- The Flask backend serves the static frontend pages directly via clean routes.
- API endpoints used by the frontend: `/get_rule`, `/health`, `/feedback`.

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