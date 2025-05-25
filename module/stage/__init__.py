from .base import (
    match_offensive_with_group,
    project_basic_fields
)

from .gender import (
    match_gender_group,
    extract_gender_field,
    extract_gender_and_year,
    group_by_gender_year,
    project_gender_year_count
)

from .politics import (
    match_politics_group,
    extract_politics_field,
    extract_politics_and_year,
    group_by_politics_year,
    project_politics_year_count
)

from .race import (
    match_race_group,
    extract_race_field,
    explode_race,
    extract_race_and_year,
    group_by_race_year,
    project_race_year_count,
    extract_race,
    group_by_race,
    project_race_count
)

from .target_group import (
    match_offensive_group,
    project_final
)
