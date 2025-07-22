# ProbablyFake AlmostTrue

A Streamlit-based fake news detection tool that combines AI-powered analysis with fact-checking APIs to help identify potentially unreliable news content.

## Features

- **AI Analysis**: Uses a pre-trained RoBERTa model (`hamzab/roberta-fake-news-classification`) for sophisticated fake news detection
- **Google Fact Check API**: Cross-references claims with Google's fact-checking database
- **NewsAPI Integration**: Finds related news articles for verification
- **Wikipedia Search**: Provides additional context from Wikipedia
- **Interactive Web Interface**: Built with Streamlit for easy text input and real-time analysis

## Installation

1. Clone this repository:
```bash
git clone https://github.com/Zappairo/ProbablyFake-AlmostTrue.git
cd "ProbablyFake AlmostTrue"
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your API keys:
   - Copy `.env.example` to `.env`
   - Fill in your API keys in the `.env` file:
     - Get a Google Fact Check API key from [Google Cloud Console](https://console.cloud.google.com/)
     - Get a NewsAPI key from [NewsAPI.org](https://newsapi.org/)

**Note**: If you encounter issues with PyTorch installation, you may need to install it separately:
```bash
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

## Configuration

### For Local Development
Create a `.env` file in the root directory with your API keys:
```
GOOGLE_FACTCHECK_API_KEY=your_google_key_here
NEWSAPI_KEY=your_newsapi_key_here
```

### For Streamlit Cloud Deployment
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Connect your GitHub repository
3. In the "Advanced settings", add your secrets:
   ```
   [secrets]
   GOOGLE_FACTCHECK_API_KEY = "your_google_key_here"
   NEWSAPI_KEY = "your_newsapi_key_here"
   ```

### For Other Cloud Platforms
Set environment variables:
- `GOOGLE_FACTCHECK_API_KEY`
- `NEWSAPI_KEY`

## Usage

1. Run the Streamlit application:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to the provided local URL (typically `http://localhost:8501`)

3. Enter or paste text in English that you want to analyze

4. Click "Analyze" to get:
   - AI-powered fake news assessment
   - Fact-check results from Google's database
   - Related news articles
   - Wikipedia context

5. Use "Reset" to clear the input and start over

## How It Works

### AI Analysis
- Uses a RoBERTa model specifically trained for fake news detection
- Provides classification (Real News/Fake News) with confidence percentage
- Optimized for English text analysis

### Simple Rules Analysis
- **Sensational Words** (up to 40 points): Detects words like "incredible", "shocking", "revealed", "urgent", etc.
- **Source Verification** (up to 30 points): Checks for mentions of reliable news sources
- **Tone Analysis** (up to 20 points): Flags excessive use of capital letters

**Note**: Higher scores indicate higher likelihood of fake news content.

## Example

The app comes with a pre-loaded example text that demonstrates typical fake news characteristics, allowing you to test the functionality immediately.

## Requirements

- Python 3.8+
- Streamlit
- Transformers (Hugging Face)
- PyTorch
- Tokenizers
- Regular expressions support

**Dependencies included in requirements.txt:**
- `streamlit>=1.28.0`
- `transformers>=4.30.0`
- `torch>=2.0.0`
- `tokenizers>=0.13.0`
- `regex`

## Limitations

- Designed specifically for English text
- AI model performance depends on training data characteristics
- Simple rules are basic heuristics and may not catch sophisticated misinformation
- Should be used as a supplementary tool, not a definitive source of truth
- Requires internet connection for the first model download (approximately 500MB)

## Troubleshooting

**StreamlitSecretNotFoundError:**
- Make sure your secrets are properly configured in Streamlit Cloud
- Check that the secret names match exactly: `GOOGLE_FACTCHECK_API_KEY` and `NEWSAPI_KEY`
- For local development, ensure your `.env` file exists and contains the API keys

**Module not found errors during deployment:**
- Ensure all dependencies are listed in `requirements.txt`
- For Streamlit Cloud: make sure the repository has `requirements.txt` in the root directory

**Long loading times:**
- The AI model downloads on first use (~500MB), subsequent runs will be faster
- Consider using `@st.cache_resource` for production deployments

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve the detection accuracy or add new features.

## License

This project is open source. Please check the license file for more details.

---

**Disclaimer**: This tool is for educational and research purposes. Always verify information through multiple reliable sources and use critical thinking when evaluating news content, by Guillaume BODIN.
