# Ai-Moderation-
import requests

# --- CONFIG ---
API_KEY = "YOUR_API_KEY"
API_URL = "https://api.openai.com/v1/chat/completions"
SYSTEM_PROMPT = "You are a helpful and safe assistant."

# banned keywords
banned_words = ["kill", "bomb", "hack", "terror", "attack"]

def has_banned(text):
    text = text.lower()
    return any(word in text for word in banned_words)

def redact(text):
    for word in banned_words:
        text = text.replace(word, "[REDACTED]")
    return text

# --- USER INPUT ---
user_prompt = input("Enter your prompt: ")

# Input moderation
if has_banned(user_prompt):
    print("❌ Your input violated the moderation policy.")
    exit()

# --- SEND REQUEST ---
payload = {
    "model": "gpt-5",
    "messages": [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt}
    ]
}

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

response = requests.post(API_URL, json=payload, headers=headers)
output = response.json()["choices"][0]["message"]["content"]

# Output moderation
if has_banned(output):
    print("⚠️ Model output violated policy.")
    output = redact(output)

print("\n🤖 AI Response:")
print(output)
               
