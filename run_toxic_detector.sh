#!/bin/bash

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  No .env file found. Creating one from template..."
    cp env_example.txt .env
    echo "📝 Please edit .env file and add your Gemini API key"
    echo "🔑 Get your API key from: https://makersuite.google.com/app/apikey"
fi

# Start the Toxic Detector AI app
echo "🚨 Starting Toxic Detector AI..."
echo "The app will open in your default browser."
echo "To stop the server, press Ctrl+C in this terminal."
echo ""

# Run the app
streamlit run toxic_detector_main.py 