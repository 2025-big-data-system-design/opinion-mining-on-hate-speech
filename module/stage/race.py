# race- 접두어가 포함되며 'others'가 아닌 문서만 필터링하는 match 단계 반환
def match_race_group():
    return {
        "$match": {
            "target_group": {
                "$regex": "race-(?!others)"  # race- 접두사 포함 & race-others 제외
            },
            "date": { "$ne": None }
        }
    }

# target_group에서 race 정보를 추출해 race_matches 배열로 저장하는 addFields 단계 반환
def extract_race_field():
    return {
        "$addFields": {
            "race_matches": {
                "$regexFindAll": {
                    "input": "$target_group",
                    "regex": "race-(asian|black|white|indian|chinese|southeast_asian|korean_chinese)"  # others 제외
                }
            }
        }
    }

# race_matches 배열을 펼치는 unwind 단계 반환
def explode_race():
    return {
        "$unwind": "$race_matches"
    }

# race 값에서 접두사 제거 + 날짜에서 연도 정보 추출하는 addFields 단계 반환
def extract_race_and_year():
    return {
        "$addFields": {
            "race": { "$substr": ["$race_matches.match", 5, -1] },  # 'race-' 접두사 제거 (index 5부터)
            "year": { "$year": { "$toDate": "$date" } }
        }
    }

# race 값에서 접두사 제거
def extract_race():
    return {
        "$addFields": {
            "race": { "$substr": ["$race_matches.match", 5, -1] }  # 'race-' 접두사 제거 (index 5부터)
        }
    }

# 인종과 연도 기준으로 그룹화하여 개수를 집계하는 group 단계 반환
def group_by_race_year():
    return {
        "$group": {
            "_id": {
                "race": "$race",
                "year": "$year"
            },
            "count": { "$sum": 1 }
        }
    }

# 인종 기준으로 그룹화하여 개수를 집계하는 group 단계 반환
def group_by_race():
    return {
        "$group": {
            "_id": {
                "race": "$race",
            },
            "count": { "$sum": 1 }
        }
    }


# 최종 출력 필드를 구성하는 project 단계 반환
def project_race_year_count():
    return {
        "$project": {
            "race": "$_id.race",
            "year": { "$toString": "$_id.year" },
            "count": 1,
            "_id": 0
        }
    }

# 최종 출력 필드를 구성하는 project 단계 반환
def project_race_count():
    return {
        "$project": {
            "race": "$_id.race",
            "count": 1,
            "_id": 0
        }
    }