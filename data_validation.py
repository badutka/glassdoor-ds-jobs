import pandas as pd
from pydantic import BaseModel, Field, ValidationError, field_validator
from typing import List, Optional, Union
import numpy as np


class Person(BaseModel):
    """
    Pydantic model representing a person's job and company details.
    """
    # Job-related details
    job_title: str  # The job title of the person (required)
    rating: Optional[float]  # A star rating associated with the company (optional)

    # Company information
    company_name: Optional[str]  # Name of the company (optional)
    size: Optional[str]  # Company size (optional)
    founded: Optional[int]  # Year the company was founded (optional)
    type_of_ownership: Optional[str]  # Type of ownership (e.g., private, public) (optional)
    industry: Optional[str]  # Industry in which the company operates (optional)
    sector: Optional[str]  # Sector within the industry (optional)

    # Revenue details (can be integer or float)
    min_revenue: Optional[int | float]  # Minimum revenue; optional, can be int or float
    max_revenue: Optional[int | float]  # Maximum revenue; optional, can be int or float

    # Salary details (required)
    salary_min: int | float  # Minimum salary offered; must be int or float
    salary_max: int | float  # Maximum salary offered; must be int or float

    # Location details
    location_city: str  # City where the job is located (required)
    location_state: Optional[str]  # State where the job is located (optional)
    headquarters_city: Optional[str]  # Headquarters city of the company (optional)
    headquarters_state: Optional[str]  # Headquarters state of the company (optional)

    # Competition details
    num_competitors: Optional[int]  # Number of competitors (optional)

    @field_validator("location_state", mode="before")
    def nan_to_none(cls, value):
        """
        Validator for the 'location_state' field.
        Converts np.nan values (of type float) to None so that the field matches Optional[str].
        """
        if isinstance(value, float) and np.isnan(value):
            return None
        return value


def validate_row(row):
    """
    Validates a pandas DataFrame row against the Person model.

    Args:
        row (pd.Series): A row from a DataFrame containing the data to validate.

    Returns:
        tuple: (Person instance if validation succeeds, None)
               OR (None, error message string if validation fails)
    """
    try:
        # Convert the row to a dictionary and unpack it into the Person model
        return Person(**row.to_dict()), None
    except ValidationError as e:
        # If validation fails, return None and the error message
        return None, str(e)
