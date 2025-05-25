# MongoDB 집계 단계(stage) 관련 import
from module.stage.target_group import (  
    match_offensive_group,  # 공격성 존재 필터링 단계  
    project_final
)

# 타겟 그룹 집계를 위한 파이프라인 반환
def get_target_group_pipeline():
    return [
        match_offensive_group(),  # 공격성 존재 필터링 단계
        project_final()
    ]