from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from bs4 import BeautifulSoup
from selenium.common.exceptions import WebDriverException, TimeoutException
from urllib.parse import urlparse
import os
from dotenv import load_dotenv
import time

# Load environment variables from .env file
load_dotenv()

# Get authentication from environment variables with error handling
AUTH = os.getenv('SCRAPING_BROWSER_AUTH')
if not AUTH or AUTH == 'your-auth-token-here':
    raise ValueError(
        "Please set the SCRAPING_BROWSER_AUTH environment variable in your .env file "
        "with your actual scraping browser authentication token"
    )

SBR_WEBDRIVER = f'https://{AUTH}@brd.superproxy.io:9515'

def validate_url(url):
    """
    Validate and format the URL properly.
    
    Args:
        url (str): The URL to validate
        
    Returns:
        str: The properly formatted URL
        
    Raises:
        ValueError: If the URL is invalid
    """
    if not url:
        raise ValueError("URL cannot be empty")
        
    # Add scheme if missing
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
        
    try:
        result = urlparse(url)
        if not all([result.scheme, result.netloc]):
            raise ValueError("Invalid URL format")
        return url
    except Exception as e:
        raise ValueError(f"Invalid URL: {str(e)}")

def scrape_website(website_url, captcha_timeout=60):
    """
    Scrape a website using Selenium and handle captchas.
    
    Args:
        website_url (str): The URL to scrape
        captcha_timeout (int): Maximum time to wait for captcha solving in seconds
        
    Returns:
        str: The HTML content of the page
        
    Raises:
        ValueError: If the URL is invalid
        TimeoutException: If captcha solving times out
        Exception: For other scraping errors
    """
    try:
        # Validate and format the URL
        website_url = validate_url(website_url)
        print(f'Validated URL: {website_url}')
        
        print('Connecting to Scraping Browser...')
        options = ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-extensions')
        
        sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')
        with Remote(sbr_connection, options=options) as driver:
            print('Connected! Navigating...')
            try:
                driver.get(website_url)
            except WebDriverException as e:
                if "Could not resolve host" in str(e):
                    raise ValueError(f"Could not resolve the host for {website_url}. Please check if the URL is correct and accessible.")
                raise
            
            print("Checking for captcha...")
            start_time = time.time()
            captcha_detected = False
            
            while time.time() - start_time < captcha_timeout:
                try:
                    solve_res = driver.execute(
                        "executeCdpCommand",
                        {
                            "cmd": "Captcha.waitForSolve",
                            "params": {"detectTimeout": 5000},
                        },
                    )
                    status = solve_res.get("value", {}).get("status")
                    print("Captcha solve status:", status)
                    
                    if status == "solve_finished":
                        print("Captcha solved successfully!")
                        break
                    elif status == "not_detected":
                        # If captcha is not detected for a while, assume page is ready
                        if time.time() - start_time > 10 and not captcha_detected:
                            print("No captcha detected, proceeding with scraping...")
                            break
                    else:
                        captcha_detected = True
                        
                except Exception as e:
                    print(f"Warning: Captcha check failed: {str(e)}")
                    # If we've been checking for a while with no success, try to proceed
                    if time.time() - start_time > 15 and not captcha_detected:
                        print("No captcha detected after multiple checks, proceeding with scraping...")
                        break
                
                time.sleep(2)
            
            if time.time() - start_time >= captcha_timeout:
                if not captcha_detected:
                    print("Timeout reached but no captcha was detected, proceeding with scraping...")
                else:
                    raise TimeoutException(
                        f"Captcha solving timed out after {captcha_timeout} seconds"
                    )

            print("Scraping page content...")
            # Add a small delay to ensure page is fully loaded
            time.sleep(3)
            html = driver.page_source
            if not html:
                raise Exception("Failed to get page source")
                
            if len(html) < 100:  # Basic check for valid content
                raise Exception("Retrieved page seems empty or invalid")
                
            return html

    except ValueError as e:
        # Re-raise ValueError for invalid URLs
        raise
    except WebDriverException as e:
        raise Exception(f"Browser automation error: {str(e)}")
    except Exception as e:
        raise Exception(f"Failed to scrape website: {str(e)}")


def extract_body_content(html_content):
    """
    Extract the body content from HTML.
    
    Args:
        html_content (str): The HTML content to parse
        
    Returns:
        str: The body content or None if not found
    """
    if not html_content:
        return None
    try:
        soup = BeautifulSoup(html_content, "html.parser")
        body_content = soup.body
        if body_content:
            return str(body_content)
        return None
    except Exception as e:
        print(f"Error extracting body content: {str(e)}")
        return None


def clean_body_content(body_content):
    """
    Clean the body content by removing scripts, styles, and extra whitespace.
    
    Args:
        body_content (str): The body content to clean
        
    Returns:
        str: The cleaned content
    """
    if not body_content:
        return "No content was found on the page."
    
    try:
        soup = BeautifulSoup(body_content, "html.parser")

        # Remove script and style elements
        for script_or_style in soup(["script", "style"]):
            script_or_style.extract()

        # Get text and clean it
        cleaned_content = soup.get_text(separator="\n")
        cleaned_content = "\n".join(
            line.strip() for line in cleaned_content.splitlines() if line.strip()
        )

        if not cleaned_content:
            return "Content was found but contained no text after cleaning."

        print("DOM content extracted and cleaned successfully!")
        return cleaned_content

    except Exception as e:
        print(f"Error cleaning body content: {str(e)}")
        return "Error occurred while cleaning the content."


def split_dom_content(dom_content, max_length=6000):
    """
    Split the DOM content into chunks of specified maximum length.
    
    Args:
        dom_content (str): The content to split
        max_length (int): Maximum length of each chunk
        
    Returns:
        list: List of content chunks
    """
    if not dom_content:
        return []
        
    try:
        return [
            dom_content[i : i + max_length] 
            for i in range(0, len(dom_content), max_length)
        ]
    except Exception as e:
        print(f"Error splitting DOM content: {str(e)}")
        return [dom_content]  # Return the full content as a single chunk if splitting fails