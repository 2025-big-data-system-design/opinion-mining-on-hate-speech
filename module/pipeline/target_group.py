# MongoDB 집계 단계(stage) 관련 import
from module.stage.target_group import (  
    match_offensive_group,  # 공격성 + GRP 존재 필터링 단계  
    add_parsed_target_fields,  # category/subgroup 필드 분리 단계  
    group_by_category_and_subgroup,  # category-subgroup 기준 집계 단계  
    project_target_group_stats  # 출력 필드 정리 단계  
)

# 타겟 그룹 집계를 위한 파이프라인 반환
def get_target_group_pipeline():
    return [
        match_offensive_group(),  # 공격성 + GRP 존재 필터링 단계  
        add_parsed_target_fields(),  # category/subgroup 필드 분리 단계  
        group_by_category_and_subgroup(),  # category-subgroup 기준 집계 단계  
        project_target_group_stats()  # 출력 필드 정리 단계  
    ]