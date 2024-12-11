from fastapi import HTTPException  # Added import for HTTPException

def check_usage_limit(user, api_name):
    # Placeholder function for usage limit enforcement
    if user.usage_count >= user.subscription_plan.usage_limit:
        raise HTTPException(status_code=403, detail="Usage limit reached")
