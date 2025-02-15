import streamlit as st
from scrape import scrape_website

# page title
st.title("AI Web Scraper")
url = st.text_input("Enter the Website URL: ")

# scrape button functionality
if st.button("Scrape Site"):
    st.write("Scraping the site...")
    scraped_content = scrape_website(url)
    print(scraped_content)
