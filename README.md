# ProbablyFake AlmostTrue

A Streamlit-based fake news detection tool that combines AI-powered analysis with simple rule-based scoring to help identify potentially unreliable news content.

## Features

- **AI Analysis**: Uses a pre-trained RoBERTa model (`hamzab/roberta-fake-news-classification`) for sophisticated fake news detection
- **Simple Rules Analysis**: Implements basic heuristics to score text based on:
  - Sensational words detection
  - Absence of reliable sources
  - Excessive use of capital letters
- **Interactive Web Interface**: Built with Streamlit for easy text input and real-time analysis
- **Dual Scoring System**: Provides both AI confidence scores and rule-based scores (0-100)

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

**Note**: If you encounter issues with PyTorch installation, you may need to install it separately:
```bash
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

**For deployment on cloud platforms** (Streamlit Cloud, Heroku, etc.), make sure the `requirements.txt` file is in the root directory.

## Usage

1. Run the Streamlit application:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to the provided local URL (typically `http://localhost:8501`)

3. Enter or paste text in English that you want to analyze

4. Click "Analyze" to get both AI-powered and rule-based assessments

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
