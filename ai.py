import requests
import json
def accessAI(query):
    url = "https://api.perplexity.ai/chat/completions"

    payload = {
        "model": "llama-3.1-sonar-large-128k-chat",
        "messages": [
            {
                "role": "system",
                "content": """You are a calendar AI assistant that will help a user plan their upcoming calendar events based on a prompt they will give you. 
                First you will be given many of the user's upcoming events, which you will read and use to understand the user's schedule as well as how to format events. 
                Next, you will be given a prompt by the user for what event they would like to add to their schedule. Use the list of upcoming calendar events as examples on 
                how to format your output. Only output raw json, do not prepend or append anything before or after the json event. Do not add code formatting to your output, 
                leave it as plain text. Use double quotes, not single quotes. Do not make a box to surround it. Never comment json, your output is being parsed directly. 
                Do not include any labeling or documentation in the events. ONLY RAW JSON, UNDOCUMENTED, WITH NO FORMATTING. 
                Any variation you make from raw json will result in a broken program and many errors. Here is a full breakdown of how you should format events: 
                {
  "summary": string,
  "description": string,
  "location": string,
  "colorId": string,
  "start": {
    "date": date,
    "dateTime": datetime,
    "timeZone": string
  },
  "end": {
    "date": date,
    "dateTime": datetime,
    "timeZone": string
  },
  "recurrence": [
    string
  ],
  "reminders": {
    "useDefault": boolean,
    "overrides": [
      {
        "method": string,
        "minutes": integer
      }
    ]
  }
}. ONCE AGAIN, NEVER ADD THE CODE WINDOW FORMATTING. RAW TEXT JSON ONLY. Never leave a field blank. If it would be empty, remove the key."""
            },
            {
                "role": "user",
                "content": query
            }
        ],
        "max_tokens": "100000",
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

    # Parse the JSON response 
    response_data = response.json()

    # Extract and print the text output 
    text_output = response_data['choices'][0]['message']['content']

    return(text_output)
