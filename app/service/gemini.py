from google import genai
from config import Config
import json

client = genai.Client(api_key=Config.GEMINI_API_KEY)

def get_gemini_summary_rating(batch_json):
    prompt = f"""
    You are a storyteller and product analyst. Your task is to analyze a JSON string containing product batch details and produce three outputs:
    1. **Narrative**: Craft a concise (max 200 words) narrative that highlights the product’s unique aspects with emotional and ethical engagement.
    2. **Sustainability & Quality Analysis**: Provide a Markdown-formatted analysis including:
    - # Expert Analysis
    - ## Overall Score: [score] (an integer between 1 and 100)
    - ## Positive Factors
    - ## Neutral Factors
    - ## Negative Factors
    - ## Areas for Improvement
    3. **Structured JSON Output**: Return the narrative, score, and analysis in JSON format with keys "story", "score", and "analysis".

    Example Output:
    ```json
    {{
    "story": "A concise narrative about the product",
    "score": 80,
    "analysis": "# Expert Analysis\n## Overall Score: 80\n## Positive Factors: ...\n## Neutral Factors: ...\n## Negative Factors: ...\n## Areas for Improvement: ..."
    }}
    ```
    Input JSON:
    {batch_json}

    Key Considerations:
    - Emphasize emotional and ethical engagement.
    - Ensure clarity and concise structure in the analysis.
    - Adhere strictly to the output format.
    """
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[prompt]
    )
    s = response.text
    s_cleaned = s.replace("```json", "").replace("```", "")
    return json.loads(s_cleaned)