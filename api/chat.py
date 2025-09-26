import azure.functions as func
import json
import os
import requests

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_json()
        prompt = req_body.get("prompt", "")

        # Azure OpenAI config
        endpoint = os.getenv("https://cr-ai900-openaiservice.openai.azure.com/")
        api_key = os.getenv("3ukNW7MRZLE218xiS7l7cuOwKam94jJBzxjag0FKCZ6gkqaL9xeJJQQJ99BIAC5RqLJXJ3w3AAABACOGlb2S")
        deployment = os.getenv("gpt-4")
        api_version = "2023-12-01-preview"

        url = f"{endpoint}/openai/deployments/{deployment}/chat/completions?api-version={api_version}"

        headers = {
            "Content-Type": "application/json",
            "api-key": api_key
        }

        data = {
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 100
        }

        r = requests.post(url, headers=headers, json=data)
        r.raise_for_status()
        result = r.json()
        ai_message = result["choices"][0]["message"]["content"]

        return func.HttpResponse(json.dumps({"response": ai_message}), mimetype="application/json")

    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500, mimetype="application/json")
