# MongoDB 집계 단계(stage) 관련 import
from module.stage import (
    match_offensive_with_group,  # 공격성 댓글 + 그룹 조건 필터링 단계
    project_basic_fields  # 기본 필드(project) 단계
)

# 공격성 관련 집계 파이프라인 반환
def get_offensive_pipeline():
    return [
        match_offensive_with_group(),  # 공격성 댓글 + 그룹 조건 필터링 단계
        project_basic_fields()  # 기본 필드(project) 단계
    ]
