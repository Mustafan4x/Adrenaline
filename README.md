# Adrenaline

An ML-powered UFC fight prediction platform built with real fighter statistics scraped from UFCStats.com. Select any two fighters or browse upcoming events to get AI-driven predictions with detailed breakdowns, stat comparisons, and confidence ratings.

## Goal

Adrenaline goes beyond simple win/loss guessing. It scrapes real fighter data (striking output, takedown accuracy, defense, reach, age, win streaks, and more), trains an XGBoost model on historical fight outcomes, and presents predictions through a clean, dark-themed UI inspired by professional fight apps. Every prediction comes with feature importance analysis, tale-of-the-tape comparisons, radar charts, and a breakdown of why the model favors one fighter over the other.

## Features

- Full card predictions for upcoming UFC events
- Custom matchup predictions between any two fighters in the database
- Fighter profile pages with physical attributes, career stats, and fight history
- Expandable fight history with detailed per-fight stats scraped live from UFCStats
- Live UFC/MMA news feed with categorized articles
- Fighter profile cards with images pulled from UFC.com
- HTML/CSS visualizations: confidence bars, feature importance, tale of the tape, radar charts, and recent form
- Style matchup analysis describing how fighting styles interact
- One-click data updates after new UFC events
- Dark theme UI with smooth transitions

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Mustafan4x/Adrenaline.git
   cd Adrenaline
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate        # Linux / Mac
   # .venv\Scripts\activate          # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Launch Adrenaline

Fighter data and fight history are included in the repo, so no setup is needed:

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`.

### Keeping Data Up to Date

After a new UFC event, click the **Update Data** expander at the top of the app and hit the button. This scrapes only the latest event results and updates affected fighter stats (takes 1-2 minutes).

### Make Predictions

- **Full Card Predictions** -- Predict every fight on the upcoming card at once.
- **Custom Matchup** -- Select any two fighters from the dropdown menus and click Predict Matchup.
- **Fighter Profile** -- Look up any fighter's stats, fight history, and upcoming bouts. Click on past fights to see detailed round-by-round breakdowns.
- **News** -- Browse the latest UFC/MMA news categorized by past fights, upcoming fights, fighter news, and organization updates.

## Tech Stack

- **Data Collection**: requests, BeautifulSoup, lxml
- **ML Model**: XGBoost with scikit-learn cross-validation
- **Frontend**: Streamlit with custom HTML/CSS (Russo One + Nunito Sans fonts, dark theme)
- **Fighter Images**: Scraped from UFC.com and cached locally
- **News Feed**: Google News RSS

## Project Structure

```
app.py              - Streamlit web application (UI + HTML visualizations)
scraper.py          - Data scraper (fighters, fights, upcoming events, incremental updates)
preprocessing.py    - Data cleaning, feature engineering, style classification
model.py            - XGBoost prediction model with feature importance
data/fighters.csv   - Pre-scraped fighter database
data/fights.csv     - Pre-scraped fight history for model training
data/logos/         - Branding assets
```
