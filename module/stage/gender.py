# 성별 관련 그룹만 필터링하고 날짜가 존재하는 문서만 추출하는 match 단계 반환  
def match_gender_group():  
    return {  
        "$match": {  
            "target_group": {  
                "$regex": "gender-(male|female|feminist|queer|others)"  # 성별 관련 그룹 정규표현식 필터  
            },  
            "date": { "$ne": None }  # 날짜 필드가 None이 아닌 문서만 필터링  
        }  
    }

# target_group에서 성별 정보를 추출해 gender_match 필드로 추가하는 addFields 단계 반환  
def extract_gender_field():  
    return {  
        "$addFields": {  
            "gender_match": {  
                "$regexFind": {  
                    "input": "$target_group",  # 정규식 적용 대상 필드  
                    "regex": "gender-(male|female|feminist|queer|others)"  # 성별 그룹 추출 정규표현식  
                }  
            }  
        }  
    }

# 날짜에서 연도를 추출하고 성별 문자열을 분리해 새로운 필드를 추가하는 addFields 단계 반환  
def extract_gender_and_year():  
    return {  
        "$addFields": {  
            "parsed_date": { "$toDate": "$date" },  # 문자열 형식의 date를 날짜 타입으로 변환  
            "gender": { "$substr": ["$gender_match.match", 7, -1] },  # 'gender-' 접두사를 제거하고 성별만 추출  
            "year": { "$year": { "$toDate": "$date" } }  # 날짜에서 연도 정보만 추출  
        }  
    }

# 성별과 연도 기준으로 그룹화하여 개수를 집계하는 group 단계 반환  
def group_by_gender_year():  
    return {  
        "$group": {  
            "_id": {  
                "gender": "$gender",  # 성별 기준 그룹  
                "year": "$year"  # 연도 기준 그룹  
            },  
            "count": { "$sum": 1 }  # 각 그룹별 문서 수 집계  
        }  
    }

# 그룹화된 성별-연도 정보를 출력 형식에 맞게 정리하는 project 단계 반환  
def project_gender_year_count():  
    return {  
        "$project": {  
            "gender": "$_id.gender",  # 성별 정보 출력  
            "year": { "$toString": "$_id.year" },  # 연도를 문자열로 변환하여 출력  
            "count": 1,  # 그룹별 댓글 수 출력  
            "_id": 0  # _id 필드는 출력에서 제외  
        }  
    }
