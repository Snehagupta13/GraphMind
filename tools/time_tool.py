from langchain_core.tools import tool
from datetime import datetime

@tool
def get_current_datetime(location: str = "local") -> str:
    """Return the current date and time in ISO format. Accepts an optional location hint."""
    now = datetime.now()
    return now.strftime("Current date and time [%Y-%m-%d %H:%M:%S]")
