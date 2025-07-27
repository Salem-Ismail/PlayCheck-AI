# PlayCheck AI - Football Rules Assistant

An AI-powered football rules assistant that helps referees, players, and fans understand FIFA's Laws of the Game through intelligent search and interpretation.

## ⚽ Features

- **Intelligent Rule Search**: TF-IDF semantic search through FIFA laws
- **AI-Powered Interpretation**: GPT-4 analysis with rule context
- **Confidence Scoring**: Shows how certain the system is about answers
- **Modern Chat Interface**: Clean, responsive design
- **Real-time Responses**: Instant rule clarification and analysis

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- OpenAI API key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/PlayCheck-AI.git
   cd PlayCheck-AI
   ```

2. **Install Python dependencies**
   ```bash
   cd Backend
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   # Copy the example file
   cp env.example .env
   
   # Edit .env and add your OpenAI API key
   OPENAI_API_KEY=your_actual_api_key_here
   ```

4. **Start the backend**
   ```bash
   python app.py
   ```

5. **Open the frontend**
   - Navigate to `Frontend/src/chat.html`
   - Open in your web browser
   - Start asking questions!

## 📖 Usage Examples

### Basic Rule Queries
```
"What happens if a player handles the ball in the penalty area?"
"Is this offside?"
"What's the restart if the ball hits the referee?"
```

### Complex Scenarios
```
"A defender deliberately handles the ball in the penalty area with no attempt to play the ball. Does the referee award a penalty and issue a red card for denying a goal?"
```

## 🏗️ Architecture

### Backend (Python/Flask)
- **Flask API**: RESTful endpoints for rule queries
- **TF-IDF Search**: Semantic search through FIFA laws
- **OpenAI Integration**: GPT-4 for intelligent interpretation
- **Confidence Scoring**: Similarity-based confidence levels

### Frontend (HTML/CSS/JavaScript)
- **Modern UI**: Clean, responsive design with Tailwind CSS
- **Real-time Chat**: Interactive chat interface
- **Error Handling**: User-friendly error messages
- **Mobile Responsive**: Works on all devices

### Data Layer
- **FIFA Laws Database**: Complete FIFA Laws of the Game
- **Structured Data**: JSON format with summaries and keywords
- **Semantic Search**: Intelligent matching of queries to laws

## 🔧 Technical Details

### Search Algorithm
The system uses TF-IDF (Term Frequency-Inverse Document Frequency) vectorization to find the most relevant FIFA laws for any given query. This ensures accurate rule matching even when users don't use exact legal terminology.

### AI Integration
PlayCheck AI combines semantic search with OpenAI's GPT-4 to provide intelligent rule interpretation. The system:
1. Finds relevant laws using TF-IDF search
2. Provides those laws as context to GPT-4
3. Generates human-readable explanations
4. Shows confidence scores for transparency

### Confidence Scoring
Each response includes a confidence score indicating how certain the system is about the relevant laws. This helps users understand the reliability of the information provided.

## 🎯 Use Cases

### For Referees
- **Pre-game preparation**: Rule clarification and scenario review
- **Training and education**: Learning complex rule interpretations
- **Post-game analysis**: Reviewing decisions and learning from mistakes
- **Quick reference**: Fast rule lookups during breaks

### For Players and Coaches
- **Rule education**: Understanding FIFA laws and interpretations
- **Scenario analysis**: Learning from specific game situations
- **Training support**: Educational tool for team training

### For Fans
- **Rule clarification**: Understanding referee decisions
- **Game analysis**: Better understanding of football rules
- **Learning tool**: Educational resource for football knowledge

## 🛠️ Development

### Project Structure
```
PlayCheck-AI/
├── Backend/
│   ├── app.py              # Flask application
│   ├── search_laws.py      # TF-IDF search implementation
│   ├── fifa_laws.json      # FIFA laws database
│   └── requirements.txt    # Python dependencies
├── Frontend/
│   └── src/
│       ├── chat.html       # Chat interface
│       ├── index.html      # Landing page
│       └── output.css      # Tailwind CSS
├── .gitignore             # Git ignore rules
├── env.example            # Environment variables template
└── README.md              # This file
```

### Contributing
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🚀 Roadmap

### Phase 1: Core Features ✅
- [x] Basic chat interface
- [x] TF-IDF search implementation
- [x] OpenAI integration
- [x] Confidence scoring

### Phase 2: Enhanced Features (In Progress)
- [ ] Video analysis platform
- [ ] Interactive training scenarios
- [ ] Progress tracking
- [ ] Mobile app

### Phase 3: Advanced Features (Planned)
- [ ] Voice input integration
- [ ] Smart watch compatibility
- [ ] Association management tools
- [ ] Multi-language support

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Support

- **Issues**: Report bugs and feature requests on GitHub
- **Discussions**: Join the community discussions
- **Email**: Contact for business inquiries

## 🙏 Acknowledgments

- FIFA for the Laws of the Game
- OpenAI for GPT-4 API
- The referee community for feedback and testing

---

**Built with ❤️ for the football community** 