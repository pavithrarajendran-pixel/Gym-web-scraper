import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Optional: If using OpenAI for AI summaries
# import openai
# openai.api_key = st.secrets.get("OPENAI_API_KEY")

def scrape_membership_fees():
    url = "https://www.planetfitness.com/membership-types"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')

    fees = []
    cards = soup.select(".pf-plans-card")

    for card in cards:
        plan = card.select_one(".pf-plans-card-title").get_text(strip=True) if card.select_one(".pf-plans-card-title") else "N/A"
        price = card.select_one(".pf-plans-card-price").get_text(strip=True) if card.select_one(".pf-plans-card-price") else "N/A"
        desc = card.select_one(".pf-plans-card-copy").get_text(strip=True) if card.select_one(".pf-plans-card-copy") else "N/A"
        fees.append({
            "Plan": plan,
            "Price": price,
            "Description": desc
        })

    return pd.DataFrame(fees)

# Optional: GPT summary enhancement
def enhance_data(df):
    if 'Description' not in df.columns:
        st.warning("No 'Description' column found in data.")
        return df

    summaries = []
    for desc in df['Description']:
        summary = f"Summary: {desc[:50]}..."
        response = openai.ChatCompletion.create(
             model="gpt-3.5-turbo",
             messages=[
                 {"role": "system", "content": "Summarize the gym plan in 1 sentence."},
                 {"role": "user", "content": desc}
             ]
         )
         summary = response['choices'][0]['message']['content']
        summaries.append(summary)

    df['AI Summary'] = summaries
    return df

def run_dashboard():
    st.title("🏋️ Smart Gym Web Scraper Bot")

    st.info("Scraping Planet Fitness membership types...")
    df = scrape_membership_fees()
    st.success("Scraped successfully!")

    st.subheader("💳 Membership Plans")
    st.dataframe(df)

    if st.checkbox("✨ Enhance with AI summaries"):
        df = enhance_data(df)
        st.subheader("🔍 With AI Summary")
        st.dataframe(df)

if __name__ == "__main__":
    run_dashboard()
