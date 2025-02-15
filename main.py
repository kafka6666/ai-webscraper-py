import streamlit as st

# page title
st.title("AI Web Scraper")
url = st.text_input("Enter the Website URL: ")

if st.button("Scrape Site"):
    st.write("Scraping the site...")

