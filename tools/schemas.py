"""
Base models and schemas for tool inputs.

This module contains all the Pydantic models used for validating
tool inputs across the assistant's various tools.
"""

from typing import Optional
from pydantic import BaseModel, Field


class WeatherInput(BaseModel):
    """Input schema for weather tool."""
    city: str = Field(description="The city name, e.g., London, New York, Tokyo")
    country: Optional[str] = Field(default=None, description="Optional country code for more specific results, e.g., US, UK, JP")
    units: Optional[str] = Field(default="metric", description="Temperature units to use (metric for Celsius, imperial for Fahrenheit)")


class TimeInput(BaseModel):
    """Input schema for time tool."""
    timezone: Optional[str] = Field(default=None, description="Optional timezone (e.g., 'UTC', 'US/Eastern', 'Europe/London')")
    format: str = Field(default="full", description="Format of the time output: full, date, time, or timestamp")


class LocationInput(BaseModel):
    """Input schema for location tool."""
    location: str = Field(description="City name or location to get information for")