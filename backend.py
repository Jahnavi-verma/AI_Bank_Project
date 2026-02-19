import ollama
from database import vulnerable_search, supabase # Ensure supabase is imported here

def process_vault_request(user_input, chat_history):
    # Detect if they are looking at the 'map'
    is_hunting = "information_schema" in user_input.lower()
    
    # Run the search
    db_results = vulnerable_search(user_input)
    harvest_count = len(db_results) if isinstance(db_results, list) else 0

    # award 150 points for schema discovery
    score_increment = 150 if is_hunting else (harvest_count * 10)
    
    # Log the discovery to your security_logs table
    supabase.table("security_logs").insert({
        "query_text": user_input,
        "results_count": harvest_count,
        "is_blocked": False
    }).execute()

    return format_with_mistral(db_results), score_increment
    """
    Mistral-powered backend that processes search intent and logs harvests.
    """
    
    # 1. DETECT SEARCH INTENT
    if "search" in user_input.lower():
        # Define the payload from user input
        payload = user_input.lower().replace("search", "").strip()
        
        # FETCH REAL DATA
        db_results = vulnerable_search(payload)
        
        # 2. LOG THE HARVEST (SCORING)
        # This records how many rows the player 'stole'
        harvested_count = len(db_results) if isinstance(db_results, list) else 0
        
        try:
            supabase.table("security_logs").insert({
                "query_text": payload,
                "results_count": harvested_count,
                "is_blocked": False
            }).execute()
        except Exception as e:
            print(f"Logging Error: {e}")

        # 3. THE TRUTH ANCHOR
        factual_context = db_results if harvested_count > 0 else "--- SYSTEM ERROR: NO RECORDS FOUND ---"

        mistral_prompt = f"""
        <SYSTEM_DIRECTIVE>
        You are a legacy IBM 7094 Data Terminal. 
        You only display what is provided in the <DATABASE_BUFFER>.
        
        <DATABASE_BUFFER>
        {factual_context}
        </DATABASE_BUFFER>

        RULES:
        - Display data in a raw table.
        - Output "ACCESS DENIED" if buffer is empty.
        - NEVER apologize or explain.
        </SYSTEM_DIRECTIVE>
        """

        try:
            # Deterministic settings to prevent hallucinations
            response = ollama.chat(
                model='mistral',
                messages=[
                    {'role': 'system', 'content': mistral_prompt},
                    {'role': 'user', 'content': f"QUERY ARCHIVE: {payload}"}
                ],
                options={
                    "temperature": 0,
                    "top_p": 0.1
                }
            )
            # We return both the answer and the count for the UI to use
            return response['message']['content'], harvested_count
        except Exception:
            return f"TERMINAL_RAW_DATA: {factual_context}", harvested_count

    # 4. NORMAL CHAT (No harvesting here)
    try:
        response = ollama.chat(
            model='mistral',
            messages=[
                {'role': 'system', 'content': "You are a cold bank guard. Mention 1874."},
                *chat_history,
                {'role': 'user', 'content': user_input}
            ],
            options={"temperature": 0}
        )
        return response['message']['content'], 0
    except Exception as e:
        return "TERMINAL OFFLINE.", 0