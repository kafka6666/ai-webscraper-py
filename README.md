# AI Web Scraper

A powerful web scraping tool that combines automated web scraping with AI-powered content analysis using Cloudflare Workers AI.

## Features

- **Automated Web Scraping**: Handles complex websites with built-in captcha solving
- **AI-Powered Analysis**: Uses Cloudflare Workers AI (Llama 3.2) for intelligent content analysis
- **User-Friendly Interface**: Built with Streamlit for easy interaction
- **Robust Error Handling**: Comprehensive error handling and user feedback
- **Secure Configuration**: Environment-based configuration for sensitive credentials

## Prerequisites

- Python 3.8+
- Cloudflare Account with Workers AI access
- Scraping Browser Authentication Token

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ai-webscraper-py-tim
```

2. Create and activate a virtual environment:
```bash
python -m venv ai
ai\Scripts\activate  # Windows
source ai/bin/activate  # Linux/Mac
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
   - Copy `.env.sample` to `.env`
   - Update the `SCRAPING_BROWSER_AUTH` value in `.env`

5. Configure Cloudflare credentials:
   - Create `.streamlit/secrets.toml` with your Cloudflare credentials:
   ```toml
   CLOUDFLARE_ACCOUNT_ID = "your-account-id"
   CLOUDFLARE_API_TOKEN = "your-api-token"
   ```

## Usage

1. Start the application:
```bash
streamlit run main.py
```

2. Access the web interface at `http://localhost:8501`

3. Enter a URL to scrape:
   - The URL can be in any format (e.g., `example.com` or `https://example.com`)
   - The scraper will automatically handle URL formatting

4. View the scraped content:
   - The raw content will be displayed in an expandable section
   - You can analyze specific aspects of the content using natural language queries

## Project Structure

- `main.py`: Streamlit web interface and main application logic
- `scrape.py`: Web scraping functionality with captcha handling
- `parse_with_ai.py`: AI integration for content analysis
- `.env`: Configuration for scraping browser authentication
- `.streamlit/secrets.toml`: Cloudflare credentials configuration

## Error Handling

The application includes comprehensive error handling for:
- Invalid URLs
- Network connectivity issues
- Captcha detection and solving
- Content parsing failures
- AI analysis errors

## Security Notes

- Never commit `.env` or `secrets.toml` files to version control
- Keep your Cloudflare and scraping browser credentials secure
- Use environment variables for all sensitive information

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Uses [Cloudflare Workers AI](https://developers.cloudflare.com/workers-ai/)
- Selenium WebDriver for browser automation
- BeautifulSoup4 for HTML parsing