# Troubleshooting

## Issue 1: API Rate Limits and Authentication Errors
**Cause:** Social media APIs (like Twitter API) have strict rate limits on the number of requests per 15-minute window or require paid tiers.
**Solution:** 
- Implement batch processing and `time.sleep()` logic to respect rate limits.
- If live data isn't strictly necessary for the development phase, use static Kaggle datasets or open-source libraries like `snscrape` / `ntscraper` which bypass official API restrictions.

## Issue 2: Poor Accuracy on Sarcasm or Slang
**Cause:** Traditional ML models (like Naive Bayes with TF-IDF) or basic lexicons (like VADER) fail to understand context, sarcasm, and modern internet slang.
**Solution:** 
- Upgrade the classification module to use a pre-trained Transformer model from Hugging Face (e.g., `cardiffnlp/twitter-roberta-base-sentiment`), which is trained specifically on social media text.
- Clean out excessive noise, but keep emojis using emoji-aware tokenizers.

## Issue 3: Emojis and Special Characters Breaking the Pipeline
**Cause:** Standard regular expression text cleaning often strips out emojis, which carry heavy sentiment value in social media.
**Solution:**
- Use the `emoji` Python library to translate emojis into text (e.g., `:)` becomes `smile_face`) before passing it to the sentiment model, or ensure the chosen Transformer model inherently supports emojis.

## Issue 4: Dashboard UI Freezing with Large Datasets
**Cause:** Trying to process and render a massive Pandas dataframe directly in Streamlit causes memory overload and browser lag.
**Solution:**
- Aggregate the data on the backend *before* passing it to the UI (e.g., calculate daily averages instead of plotting 100,000 individual scatter points).
- Use Streamlit's `@st.cache_data` decorator to cache the results of the preprocessing and model inference functions so they don't re-run on every UI interaction.
