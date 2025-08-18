# KrishiSevak - AI-Powered Agricultural Assistant 🌾

## Overview

KrishiSevak is an intelligent agricultural advisory system that helps farmers make informed decisions through voice interactions, disease detection, and personalized recommendations in multiple Indian languages.

## 🌟 Key Features

- **Voice Interface**: Natural language conversations in multiple languages
- **Disease Detection**: AI-powered plant disease identification 
- **Weather Integration**: Real-time forecasts and alerts
- **Market Prices**: Live agricultural commodity prices
- **Government Schemes**: Information about farming programs
- **Offline Support**: Core features work without internet

## 🏗️ Project Structure

```
KrishiSevak/
├── backend/                 # Python FastAPI Server
│   ├── app/
│   │   ├── agents/         # AI Decision Agents
│   │   ├── services/       # Core Services (LLM, RAG, STT/TTS)
│   │   ├── tools/         # Utility Tools
│   │   ├── config.py      # Configuration
│   │   └── main.py       # FastAPI Application
│   └── requirements.txt
│
├── frontend/               # Android Application
│   ├── app/
│   │   ├── src/
│   │   │   ├── main/     # Kotlin Source Files
│   │   │   └── res/      # Resources
│   │   └── build.gradle.kts
│   └── gradle/
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- Python 3.13+
- Android Studio Arctic Fox+
- JDK 17
- Node.js 18+

### Backend Setup

```bash
# Create and activate virtual environment
cd backend
python -m venv myenv
source myenv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys
```

### Frontend Setup

```bash
cd frontend
./gradlew build
```

## 💻 Development

### Running Backend

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 --log-level debug
```

### Running Frontend

```bash
cd frontend
./gradlew installDebug
```

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest
```

### Frontend Tests

```bash
cd frontend
./gradlew test
./gradlew connectedAndroidTest
```

## 📦 Deployment

### Backend

```bash
cd backend
docker build -t krishisevak-backend .
docker run -p 8000:8000 krishisevak-backend
```

### Frontend

```bash
cd frontend
./gradlew assembleRelease
```

## 📚 Documentation

- Backend API: http://localhost:8000/docs
- Frontend Wiki: [/docs/frontend.md](/docs/frontend.md)

## 🔒 Environment Setup

### Backend (.env)
```plaintext
OPENAI_API_KEY=your_key_here
CLAUDE_API_KEY=your_key_here
WEATHER_API_KEY=your_key_here
DATABASE_URL=postgresql://user:pass@localhost/db
```

### Frontend (local.properties)
```plaintext
sdk.dir=/Users/username/Library/Android/sdk
backend.url=http://10.0.2.2:8000
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request
## 👥 Team

- **Vicky Besra** 
- **Adesh Ghadage**
- **Ayan Singha**
- **Kartikeya Nari**

## 🙏 Acknowledgments

- OpenAI/Claude for LLM capabilities
- TensorFlow for ML models
- FastAPI framework
- Android Jetpack libraries