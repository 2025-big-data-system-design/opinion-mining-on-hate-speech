# MongoDB 집계 단계(stage) 관련 import
from module.stage import (
    match_offensive_with_group,  # 공격성 댓글 + 그룹 조건 필터링 단계
    project_basic_fields,  # 기본 필드(project) 단계
    match_religion_group,  # race 관련 그룹 조건 필터링 단계
    extract_religion_field,  # race 필드 추출 단계
    explode_religion,  # 다중 race 항목 분리 단계
    extract_religion,  # race 추출 단계
    group_by_religion,  # race 기준 그룹화 단계
    project_religion_count  # race 수(project) 단계
)

# 인종-연도별 집계 파이프라인 반환
def get_religion_pipeline():
    return [
        match_offensive_with_group(),  # 공격성 댓글 + 그룹 조건 필터링 단계
        project_basic_fields(),  # 기본 필드(project) 단계
        match_religion_group(),  # race 관련 그룹 조건 필터링 단계
        extract_religion_field(),  # race 필드 추출 단계
        explode_religion(),  # 다중 race 항목 분리 단계
        extract_religion(),  # race 추출 단계
        group_by_religion(),  # race 기준 그룹화 단계
        project_religion_count()  # race 수(project) 단계
    ]