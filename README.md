# Locale

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red.svg)
![Google ADK](https://img.shields.io/badge/Google_ADK-Latest-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Overview

Locale is an intelligent event discovery application that helps users find activities and events based on their location, date preferences, and personal interests. Powered by Google's Agent Development Kit (ADK) and Gemini AI, the application provides personalized recommendations for things to do in a specified area and timeframe.



## ✨ Key Features

- **Location-Based Search**: Find events and activities in any specified location
- **Date Selection**: Choose a single day or a date range for event discovery
- **Interest Customization**: Add personal interests and hobbies for tailored recommendations
- **AI-Powered Recommendations**: Utilizes Google's Gemini AI to provide relevant suggestions
- **Interactive UI**: Clean, user-friendly interface built with Streamlit
- **Categorized Results**: Organizes recommendations by interest category
- **Detailed Event Information**: Provides event names, dates, times, descriptions, and source links

## 🛠️ Technologies Used

- **Python**: Core programming language
- **Streamlit**: Web application framework for the user interface
- **Google ADK (Agent Development Kit)**: Framework for building AI agents
- **Google Gemini AI**: Large language model for natural language processing
- **Google Search API**: For retrieving real-time event information
- **Python-dotenv**: For environment variable management
- **Asyncio**: For handling asynchronous operations
- **Nest-asyncio**: For managing nested event loops

## 📦 Installation

### Prerequisites

- Python 3.9 or higher
- Google API Key with access to Gemini API and Search API

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/locale.git
   cd locale
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory with your Google API key:
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   ```

## 🚀 Usage

1. Start the application:
   ```bash
   python main.py
   ```

2. The Streamlit interface will open in your default web browser (typically at http://localhost:8501)

3. In the sidebar:
   - Enter your location (e.g., "Firenze, Italia")
   - Select a date or date range
   - Toggle "Select Multiple Days" if needed

4. In the main panel:
   - Add your interests using the multiselect dropdown
   - You can select from predefined options or add custom interests

5. Click the "Search" button to generate recommendations

6. Review the AI-generated list of activities and events matching your criteria

## 🔌 API Integration

The application uses the following Google APIs:

- **Google Gemini API**: Powers the AI agent for natural language understanding and generation
- **Google Search API**: Retrieves real-time information about events and activities

To use these APIs, you need a valid Google API key with appropriate permissions.

## 📊 Project Structure

```
locale/
├── .env                  # Environment variables (create this file)
├── .gitignore            # Git ignore file
├── __init__.py           # Package initialization
├── main.py               # Application entry point
├── README.md             # Project documentation
├── requirements.txt      # Project dependencies
├── .streamlit/           # Streamlit configuration
├── agents/               # ADK agent definitions
│   ├── __init__.py
│   ├── chat_agent.py     # Conversational agent
│   └── search_agent.py   # Search functionality agent
├── config/               # Configuration settings
│   ├── __init__.py
│   └── settings.py       # Application settings
├── services/             # Service integrations
│   ├── __init__.py
│   └── adk_service.py    # Google ADK service integration
├── tools/                # Custom tools for agents
│   ├── __init__.py
│   └── chat_tools.py     # Tools for the chat agent
├── ui/                   # User interface components
│   ├── __init__.py
│   └── streamlit_ui.py   # Streamlit UI implementation
└── utils/                # Utility functions
    ├── __init__.py
    └── helpers.py        # Helper functions
```

## 🚢 Deployment

### Local Deployment

Follow the installation and usage instructions above to run the application locally.

### Cloud Deployment

The application can be deployed to various cloud platforms that support Python applications:

#### Streamlit Cloud

1. Push your code to a GitHub repository
2. Sign up for [Streamlit Cloud](https://streamlit.io/cloud)
3. Connect your GitHub repository
4. Configure your secrets (GOOGLE_API_KEY)
5. Deploy the application

#### Heroku

1. Create a `Procfile` with the following content:
   ```
   web: streamlit run main.py
   ```
2. Push your code to Heroku:
   ```bash
   heroku create
   heroku config:set GOOGLE_API_KEY=your_google_api_key_here
   git push heroku main
   ```

## 🤝 Contributing

Contributions are welcome! Here's how you can contribute to the project:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature-name`)
3. Make your changes
4. Run tests if available
5. Commit your changes (`git commit -m 'Add some feature'`)
6. Push to the branch (`git push origin feature/your-feature-name`)
7. Open a Pull Request

Please ensure your code follows the project's coding style and includes appropriate documentation.

## 🧪 Testing

Currently, the project does not include automated tests. Future development plans include adding:

- Unit tests for individual components
- Integration tests for API interactions
- End-to-end tests for the complete application flow

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Developed by Charles Crocicchia & Alex Fratoni
- Powered by Google's Agent Development Kit (ADK) and Gemini AI
- Built with Streamlit for the web interface

## 📞 Contact

For questions, feedback, or collaboration opportunities, please contact:

- Charles Crocicchia - [GitHub Profile](https://github.com/charlescro)

---

**Note**: This application is currently in development. Future updates will include a map feature and additional functionality.