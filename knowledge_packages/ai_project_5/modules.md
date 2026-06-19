# Modules

## Module 1: Data Collection & Ingestion
**Description:** Responsible for gathering text data from social media sources. This can involve connecting to live APIs (if accessible) or ingesting pre-collected CSV/JSON datasets.
**Dependencies:** None

## Module 2: Text Preprocessing Pipeline
**Description:** Cleans the raw text data to prepare it for machine learning models. This involves removing URLs, special characters, and stop-words, handling emojis, and performing tokenization and lemmatization.
**Dependencies:** Module 1

## Module 3: Sentiment Classification Model
**Description:** The core AI module that takes the preprocessed text and outputs a sentiment label (Positive, Negative, Neutral) along with a confidence score.
**Dependencies:** Module 2

## Module 4: Trend Analysis & Aggregation
**Description:** Groups the classified data by time intervals (e.g., hourly, daily) or topics/keywords to calculate overall sentiment trends and volume.
**Dependencies:** Module 3

## Module 5: Interactive Dashboard
**Description:** Provides the user interface for monitoring the sentiment trends. It reads the aggregated data and renders charts, metrics, and data tables for end-users.
**Dependencies:** Module 4
