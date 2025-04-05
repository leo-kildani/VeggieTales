from google import genai
from config import Config
import json

client = genai.Client(api_key=Config.GEMINI_API_KEY)

def get_gemini_summary_rating(batch_json):
    prompt = f"""
        You are a storyteller and product analyst. You will be provided with a JSON string containing information about a product batch, including details on farming, delivery, and storage. Please follow the steps below:

        1. **Storytelling**: Craft a compelling narrative that brings the product to life. Focus on the unique aspects related to its farming, environmental impact, transport, or shelf experience. Highlight any elements that could emotionally or ethically engage the customer.

        2. **Sustainability & Quality Analysis**: Based on the provided data, assign a score between 1 and 100 that reflects the product's overall quality and sustainability. Justify your score by analyzing the relevant factors in the JSON. Your analysis should be clear, concise, and structured in Markdown format, only including the following sections:
        - # Expert Analysis
        - ## Overall Score: [score] (1-100)
        - ## Positive Factors
        - ## Neutral Factors
        - ## Negative Factors
        - ## Areas for Improvement

        3. **Return JSON Output**: Provide the story, score, and analysis in a structured JSON format with the keys "story", "score", and "analysis". Ensure the score is an integer between 1 and 100.

        Here is the JSON to analyze:
        ```json
        {batch_json}
        """
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[prompt]
    )
    s = response.text
    s_cleaned = s.replace("```json", "").replace("```", "")
    return json.loads(s_cleaned)