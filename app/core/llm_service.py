# app/core/llm_service.py

import google.generativeai as genai
import os
import re  # <-- IMPORT THE REGULAR EXPRESSION MODULE
import traceback
from dotenv import load_dotenv
from app.core.db_service import get_db_schema

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found. Please set it in your .env file.")
genai.configure(api_key=api_key)


def get_sql_from_question(question: str):
    """Converts a natural language question into a SQL query using Gemini."""
    
    schema = get_db_schema()
    
    prompt = f"""
    You are an expert SQL data analyst. Your task is to convert a natural language question into a single, executable SQL query for a SQLite database.
    You must only respond with the SQL query and nothing else. Do not include any explanations, markdown formatting, or any text other than the SQL query itself.

    Database Schema:
    {schema}

    Column Clarifications:
    - 'ad_sales.ad_sales' is the revenue generated from ads.
    - 'ad_sales.ad_spend' is the cost of the ads.
    - 'total_sales.total_sales' is the total revenue for a product, including ad and organic sales.
    - RoAS (Return on Ad Spend) is calculated as: SUM(ad_sales) / SUM(ad_spend).
    - CPC (Cost Per Click) is calculated as: SUM(ad_spend) / SUM(clicks).

    ---
    **CRUCIAL RULE:** For any question asking for a ranking (like "top 5", "highest", "lowest", "which"), your query MUST select both the identifier (e.g., item_id) AND the calculated value that was used for the ranking. For example, for "highest CPC", you must select both `item_id` and the calculated `cpc`.
    ---

    Question:
    "{question}"

    SQL Query:
    """
    
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    
    response = model.generate_content(prompt)
    
    try:
        response_text = response.text
    except Exception as e:
        print(f"Error getting text from model response: {e}")
        print(f"Full response: {response}")
        if hasattr(response, 'prompt_feedback'):
             print(f"Prompt Feedback: {response.prompt_feedback}")
        raise ValueError("The AI model did not return a valid text response. It might have been blocked due to safety settings.")

    # --- NEW ROBUST CLEANING LOGIC ---
    # Use regex to find the content inside ```sql ... ```
    sql_match = re.search(r"```sql\s*(.*?)\s*```", response_text, re.DOTALL)
    
    if sql_match:
        # If a markdown block is found, extract the SQL from it
        sql_query = sql_match.group(1)
    else:
        # Otherwise, assume the entire response is the SQL query
        sql_query = response_text
        
    return sql_query.strip()
