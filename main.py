import streamlit as st
from scrape import scrape_website, clean_body_content, extract_body_content, split_dom_content
from parse_with_ai import parse_with_cloudflare

# Cloudflare credentials configuration
if 'CLOUDFLARE_ACCOUNT_ID' not in st.secrets:
    st.error("Please set up your Cloudflare credentials in the secrets.toml file")
    st.stop()

# page title
st.title("AI Web Scraper")

# URL input with example
st.markdown("""
Enter the website URL below. Examples:
- `example.com`
- `https://example.com`
- `www.example.com/page`
""")
url = st.text_input("Enter the Website URL:")

# Step 1: Scrape the Website
if st.button("Scrape Website"):
    if not url:
        st.error("Please enter a URL")
    else:
        try:
            with st.spinner("Scraping the website..."):
                # Scrape the website
                dom_content = scrape_website(url)
                body_content = extract_body_content(dom_content)
                cleaned_content = clean_body_content(body_content)

                # Store the DOM content in Streamlit session state
                st.session_state.dom_content = cleaned_content

                # Display the DOM content in an expandable text box
                with st.expander("View DOM Content"):
                    st.text_area("DOM Content", cleaned_content, height=300)
                
                st.success("Website scraped successfully!")
                
        except ValueError as e:
            st.error(f"Invalid URL: {str(e)}")
        except Exception as e:
            st.error(f"Error: {str(e)}")

# Step 2: Ask Questions About the DOM Content
if "dom_content" in st.session_state:
    st.markdown("---")
    st.subheader("Analyze Content")
    parse_description = st.text_area(
        "What would you like to know about this content?",
        help="Describe what information you want to extract or analyze from the scraped content."
    )

    if st.button("Analyze"):
        if not parse_description:
            st.warning("Please enter what you'd like to analyze about the content.")
        else:
            try:
                with st.spinner("Analyzing content..."):
                    # Parse the content with Cloudflare Workers AI
                    dom_chunks = split_dom_content(st.session_state.dom_content)
                    parsed_result = parse_with_cloudflare(
                        dom_chunks, 
                        parse_description,
                        st.secrets["CLOUDFLARE_ACCOUNT_ID"],
                        st.secrets["CLOUDFLARE_API_TOKEN"]
                    )
                    st.write(parsed_result)
            except Exception as e:
                st.error(f"Error analyzing content: {str(e)}")