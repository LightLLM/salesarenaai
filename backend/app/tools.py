def detect_objection(objection_type: str, user_statement: str):
    """
    Call this tool when you introduce a major objection to see if the user handled it well.
    Args:
        objection_type: The category of objection (e.g. 'budget', 'competitor', 'timing', 'roi').
        user_statement: A summary of how the user tried to resolve it.
    """
    print(f"[TOOL] detect_objection called: {objection_type} - {user_statement}")
    return {"status": f"Objection {objection_type} logged. Adjusting pressure."}

def score_sales_skill(confidence: int, objection_handling: int, clarity: int, value_framing: int, closing: int, feedback: str):
    """
    Call this tool at the END of the conversation to provide a final scorecard.
    Args:
        confidence: Score 1-10.
        objection_handling: Score 1-10.
        clarity: Score 1-10.
        value_framing: Score 1-10.
        closing: Score 1-10.
        feedback: 2-3 sentences of actionable feedback for the user to improve.
    """
    print(f"[TOOL] score_sales_skill called. Confidence: {confidence}")
    return {"status": "Scorecard generated and saved."}
