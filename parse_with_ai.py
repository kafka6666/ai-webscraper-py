import requests
from typing import List

class CloudflareAI:
    def __init__(self, account_id: str, api_token: str):
        self.account_id = account_id
        self.api_token = api_token
        self.base_url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run"
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }

    def generate_text(self, prompt: str, model: str = "@cf/meta/llama-3.2-3b-instruct") -> str:
        payload = {
            "messages": [{"role": "user", "content": prompt}]
        }
        
        response = requests.post(
            f"{self.base_url}/{model}",
            headers=self.headers,
            json=payload
        )
        
        if response.status_code == 200:
            return response.json()["result"]["response"]
        else:
            raise Exception(f"Error: {response.status_code}, {response.text}")

def parse_with_cloudflare(dom_chunks: List[str], parse_description: str, account_id: str, api_token: str) -> str:
    ai = CloudflareAI(account_id, api_token)
    
    # Create a more structured prompt for better results
    combined_prompt = f"""You are an AI assistant tasked with analyzing web content. Please follow these instructions carefully:

1. Analyze the following web content:
{' '.join(dom_chunks)}

2. Task: {parse_description}

3. Guidelines:
- Focus only on information relevant to the task
- Be clear and concise in your response
- If no relevant information is found, state that clearly
- Format the output in a readable way

Your response:"""

    try:
        response = ai.generate_text(combined_prompt)
        return response
    except Exception as e:
        return f"Error processing request: {str(e)}"