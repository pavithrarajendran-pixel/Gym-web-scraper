# Smart Gym Scraper Bot with AI Enhancements

import requests
from bs4 import BeautifulSoup
import pandas as pd
import openai
import streamlit as st

# === CONFIG ===
openai.api_key = "your-api-key"  # Replace with your actual API key

# === SCRAPE CLASSES ===
def scrape_gym_classes():
    url = 'https://www.fit19.com/classes'  # Example site
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    class_sections = soup.find_all('div', class_='class-section')  # May need adjustment
    scraped_data = []

    for cls in class_sections:
        try:
            name = cls.find('h3').text.strip()
            desc = cls.find('p').text.strip()
            scraped_data.append({"Class Name": name, "Description": desc})
        except:
            continue

    return pd.DataFrame(scraped_data)

# === AI ENHANCEMENTS ===
def summarize_class(description):
    prompt = f"Summarize this gym class in one short, friendly sentence:\n\n{description}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

def categorize_class(description):
    prompt = f"What category does this gym class fall into? Choose one: [Cardio, Strength, Flexibility, Mindfulness, Mixed]:\n\n{description}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

# === PROCESS DATA ===
def enhance_data(df):
    summaries, categories = [], []
    for desc in df['Description']:
        summaries.append(summarize_class(desc))
        categories.append(categorize_class(desc))
    df['AI Summary'] = summaries
    df['Category'] = categories
    return df

# === STREAMLIT UI ===
def run_dashboard():
    st.title("🏋️ Smart Gym Class Assistant")
    df = scrape_gym_classes()
    st.subheader("🔍 Scraped Data")
    st.dataframe(df)

    if st.button("✨ Enhance with AI"):
        df = enhance_data(df)
        st.success("Enhanced with summaries and categories!")
        st.dataframe(df)
        st.download_button("📥 Download CSV", df.to_csv(index=False), "gym_classes_ai.csv")

if __name__ == '__main__':
    run_dashboard()
