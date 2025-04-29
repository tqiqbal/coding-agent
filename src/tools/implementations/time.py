"""Time-related tools."""
from datetime import datetime
import pytz
from ..base import Tool, tool

@tool(
    name="get_current_time",
    description="Get the current time in a specific timezone"
)
class CurrentTimeTool(Tool):
    parameters = {
        "type": "object",
        "properties": {
            "timezone": {
                "type": "string",
                "description": "Timezone name (e.g., 'America/New_York', 'UTC'). Defaults to UTC if not provided.",
                "default": "UTC"
            }
        },
        "required": [],
        "additionalProperties": False
    }

    async def execute(self, timezone: str = "UTC") -> str:
        """Get current time in the specified timezone.
        
        Args:
            timezone: Timezone name (e.g., 'America/New_York', 'UTC')
            
        Returns:
            Current time in the specified timezone
            
        Raises:
            ValueError: If timezone is invalid
        """
        try:
            tz = pytz.timezone(timezone)
            current_time = datetime.now(tz)
            return current_time.strftime("%Y-%m-%d %H:%M:%S %Z")
        except pytz.exceptions.UnknownTimeZoneError:
            raise ValueError(f"Invalid timezone: {timezone}")
