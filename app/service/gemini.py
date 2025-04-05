from google import genai
from config import Config
import json

client = genai.Client(api_key=Config.GEMINI_API_KEY)

def get_gemini_summary_rating(batch_json):
    prompt = f"""
    You are a storyteller and product analyst. You will be given a JSON string describing a product batch, including details about its farming, delivery, and storage.
    1. First, write a short but compelling story about the product. Highlight any unique aspects from the farm, environmental impact, transport, or shelf experience that would make a customer emotionally or ethically connected to it.
    2. Then, analyze all available information and assign a score between 1 and 100 for the product's overall quality and sustainability. Be transparent and concise in how you derive the score based on the values in the JSON, and include an analysis of key factors that influenced your rating. Consider every aspect of the data. Write the analysis in a clear and structured manner using Markdown format. 
    3. Finally, return the story, the score, and the score analysis in a JSON format with keys "story", "score", and "analysis". The score should be an integer between 1 and 100. 
    Here is the JSON:
    ```json
    {batch_json}
    ```
    """    
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[prompt]
    )
    s = response.text
    s_cleaned = s.replace("```json", "").replace("```", "")
    return json.loads(s_cleaned)