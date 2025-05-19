# MongoDB 집계 단계(stage) 관련 import
from module.stage import (
    match_offensive_with_group,  # 공격성 댓글 + 그룹 조건 필터링 단계
    project_basic_fields,  # 기본 필드(project) 단계
    match_gender_group,  # 성별 관련 그룹 조건 필터링 단계
    extract_gender_field,  # 성별 필드 추출 단계
    extract_gender_and_year,  # 성별 및 연도 추출 단계
    group_by_gender_year,  # 성별-연도 기준 그룹화 단계
    project_gender_year_count  # 성별-연도별 수(project) 단계
)

# 성별-연도별 집계 파이프라인 반환
def get_gender_year_pipeline():
    return [
        match_offensive_with_group(),  # 공격성 댓글 + 그룹 조건 필터링 단계
        project_basic_fields(),  # 기본 필드(project) 단계
        match_gender_group(),  # 성별 관련 그룹 조건 필터링 단계
        extract_gender_field(),  # 성별 필드 추출 단계
        extract_gender_and_year(),  # 성별 및 연도 추출 단계
        group_by_gender_year(),  # 성별-연도 기준 그룹화 단계
        project_gender_year_count()  # 성별-연도별 수(project) 단계
    ]
