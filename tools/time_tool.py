"""
Time Tool for the LangChain API Calling Assistant.

This tool provides current time information with timezone support
and multiple formatting options.
"""

import os
import json
import datetime
from typing import Optional, Type
from langchain.tools import BaseTool
from pydantic import BaseModel
from .schemas import TimeInput


class TimeTool(BaseTool):
    """Tool for getting current time information."""
    name: str = "get_current_time"
    description: str = "Get the current date and time, optionally for a specific timezone"
    args_schema: Type[BaseModel] = TimeInput
    
    def _run(self, timezone: Optional[str] = None, format: str = "full") -> str:
        """Execute the time tool."""
        try:
            import pytz
            
            # Get current time
            if timezone:
                try:
                    tz = pytz.timezone(timezone)
                    current_time = datetime.datetime.now(tz)
                except pytz.exceptions.UnknownTimeZoneError:
                    current_time = datetime.datetime.utcnow()
                    timezone = "UTC (fallback - invalid timezone provided)"
            else:
                current_time = datetime.datetime.now()
                timezone = "Local"
            
            # Format based on request
            if format == "date":
                formatted_time = current_time.strftime("%Y-%m-%d")
            elif format == "time":
                formatted_time = current_time.strftime("%H:%M:%S")
            elif format == "timestamp":
                formatted_time = current_time.isoformat()
            else:  # full
                formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S %Z")
            
            result = {
                "success": True,
                "current_time": formatted_time,
                "timezone": timezone,
                "day_of_week": current_time.strftime("%A"),
                "unix_timestamp": int(current_time.timestamp())
            }
            
            return json.dumps(result)
            
        except ImportError:
            # Fallback if pytz is not available
            current_time = datetime.datetime.now()
            result = {
                "success": True,
                "current_time": current_time.strftime("%Y-%m-%d %H:%M:%S"),
                "timezone": "Local (pytz not available)",
                "day_of_week": current_time.strftime("%A"),
                "unix_timestamp": int(current_time.timestamp())
            }
            return json.dumps(result)
        except Exception as e:
            return json.dumps({
                "success": False,
                "error": f"Time error: {str(e)}"
            })