# Viva

## Q1: Why did you choose Transformers (like BERT/RoBERTa) over traditional models like Naive Bayes or SVM for sentiment analysis?
**Answer:** Traditional models rely on TF-IDF or Bag of Words, which ignore the sequence and context of words. Social media text is highly contextual, relying on slang, sarcasm, and sentence structure. Transformers use an attention mechanism to understand the bidirectional context of a word within a sentence, yielding significantly higher accuracy for complex sentiments.

## Q2: How did you handle the imbalance in your dataset where neutral tweets vastly outnumbered positive or negative ones?
**Answer:** Class imbalance can cause the model to become biased toward predicting the majority class. We can handle this by either under-sampling the neutral class to balance the dataset, over-sampling the minority classes (using techniques like SMOTE for traditional ML), or applying class weights in the loss function during training to penalize misclassifications of the minority classes more heavily.

## Q3: Can you explain the text preprocessing steps applied to the social media data before feeding it to the model?
**Answer:** Social media text is noisy. The preprocessing pipeline typically includes:
1. Removing URLs, mentions (@user), and hashtags.
2. Converting text to lowercase to maintain uniformity.
3. Handling emojis (either removing them or converting them to textual meanings).
4. Removing stop-words (common words like "and", "the") if using traditional ML, though Transformers often benefit from keeping stop-words to preserve context.
5. Tokenization and lemmatization (reducing words to their base form).

## Q4: How does your system differentiate between real-time data streaming and static dataset analysis?
**Answer:** For static analysis, the system loads a CSV/JSON file into a Pandas dataframe, processes it in batch, and visualizes the results. For real-time streaming, the system connects to an API endpoint (e.g., Tweepy stream), processes individual text payloads on the fly as they arrive, and pushes the updated metrics to the dashboard dynamically.
