import requests
import json

url = "https://api.perplexity.ai/chat/completions"

payload = {
    "model": "llama-3.1-sonar-large-128k-chat",
    "messages": [
        {
            "role": "system",
            "content": "Be precise and concise."
        },
        {
            "role": "user",
            "content": "How many stars are there in our galaxy?"
        }
    ],
    "max_tokens": "10000",
    "temperature": 0.2,
    "top_p": 0.9,
    "return_citations": True,
    "search_domain_filter": ["perplexity.ai"],
    "return_images": False,
    "return_related_questions": False,
    "search_recency_filter": "month",
    "top_k": 0,
    "stream": False,
    "presence_penalty": 0,
    "frequency_penalty": 1
}
headers = {
    "Authorization": "Bearer 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",
    "Content-Type": "application/json"
}

response = requests.request("POST", url, json=payload, headers=headers)

print(response.text)

message = json.load(response.text)

print(message)