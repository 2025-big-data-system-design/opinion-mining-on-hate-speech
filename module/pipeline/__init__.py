from .base import get_offensive_pipeline
from .gender_year import get_gender_year_pipeline
from .politics_year import get_politics_year_pipeline
from .race_year import get_race_year_pipeline

__all__ = [
    "get_offensive_pipeline",
    "get_gender_year_pipeline",
    "get_politics_year_pipeline",
    "get_race_year_pipeline"
]
