# app/api/endpoints.py (Corrected and Production-Ready)

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import asyncio
import json
import traceback

from app.core.llm_service import get_sql_from_question
from app.core.db_service import execute_query
from app.core.chart_service import generate_chart 

router = APIRouter()

async def stream_response_generator(question: str):
    """Generator for streaming the response with the correct data keys and robust error handling."""
    sql_query = None  # Initialize sql_query to be safe
    try:
        # 1. Generate SQL from the question
        yield f"event: message\ndata: {json.dumps({'log': 'Generating SQL query...'})}\n\n"
        sql_query = get_sql_from_question(question)
        yield f"event: message\ndata: {json.dumps({'log': f'Executing query: `{sql_query}`'})}\n\n"
        await asyncio.sleep(0.5) # This delay is good for demos

        # 2. Execute the query against the database
        result_df, error = execute_query(sql_query)
        
        if error:
            error_message = f"Error executing SQL query: {error}"
            # FIX #1: Consistently include the 'sql' key in the payload.
            yield f"event: final_response\ndata: {json.dumps({'answer': error_message, 'sql': sql_query, 'chart_data': None})}\n\n"
            return

        # 3. Prepare the final text answer and generate the chart
        answer_text = "Here is the data you requested:\n\n" + result_df.to_string(index=False)
        chart_json = generate_chart(result_df, question)  

        full_response_data = {'answer': answer_text, 'sql': sql_query, 'chart_data': chart_json}
        
        # 4. Send the final, complete payload
        yield f"event: final_response\ndata: {json.dumps(full_response_data)}\n\n"

    except Exception as e:
        print(f"An unhandled error occurred in the generator: {e}")
        traceback.print_exc()
        error_str = str(e).lower()
        if "429" in error_str and "quota" in error_str:
            user_friendly_error = "I've been quite busy today and have reached my daily analysis limit. Please try again tomorrow. Thank you for your understanding!"
        else:
            user_friendly_error = "An unexpected server error occurred. Please ask your administrator to check the logs."
        
        # --- CRITICAL FIX #2 ---
        # Use the correct variable `user_friendly_error` instead of the non-existent `error_message`.
        yield f"event: final_response\ndata: {json.dumps({'answer': user_friendly_error, 'sql': sql_query, 'chart_data': None})}\n\n"


@router.get("/ask")
async def ask_question(question: str):
    return StreamingResponse(
        stream_response_generator(question),
        media_type="text/event-stream"
    )