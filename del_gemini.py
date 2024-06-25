import google.generativeai as genai
import requests

GOOGLE_API_KEY="AIzaSyCenQlwQ1J5JnDwT5oyRKroGv4ILcuzBqw"
genai.configure(api_key=GOOGLE_API_KEY)

async def main():
    async def fetch_url_content(url):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raises an HTTPError for bad responses
            return response.text
        except requests.RequestException as e:
            return str(e)

    model = genai.GenerativeModel('gemini-1.5-flash')
    url = await fetch_url_content("https://www.mall.cz/zpusoby-doruceni")
    response = model.generate_content(["What is this", url])
    print(response.text)


