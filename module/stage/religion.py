# religion- 접두어가 포함되며 'others'가 아닌 문서만 필터링하는 match 단계 반환
def match_religion_group():
    return {
        "$match": {
            "target_group": {
                "$regex": "religion-(?!others)"  # religion- 접두사 포함 & religion-others 제외
            },
            "date": { "$ne": None }
        }
    }

# target_group에서 religion 정보를 추출해 religion_match 배열로 저장하는 addFields 단계 반환
def extract_religion_field():
    return {
        "$addFields": {
            "religion_matches": {
                "$regexFindAll": {
                    "input": "$target_group",
                    "regex": "religion-(islam|christian|catholic|buddhism)"  # others 제외
                }
            }
        }
    }

# religion_matches 배열을 펼치는 unwind 단계 반환
def explode_religion():
    return {
        "$unwind": "$religion_matches"
    }

# religion 값에서 접두사 제거
def extract_religion():
    return {
        "$addFields": {
            "religion": { "$substr": ["$religion_matches.match", 9, -1] }  # 'religion-' 접두사 제거 (index 5부터)
        }
    }

# 종교 기준으로 그룹화하여 개수를 집계하는 group 단계 반환
def group_by_religion():
    return {
        "$group": {
            "_id": {
                "religion": "$religion",
            },
            "count": { "$sum": 1 }
        }
    }

# 최종 출력 필드를 구성하는 project 단계 반환
def project_religion_count():
    return {
        "$project": {
            "religion": "$_id.religion",
            "count": 1,
            "_id": 0
        }
    }