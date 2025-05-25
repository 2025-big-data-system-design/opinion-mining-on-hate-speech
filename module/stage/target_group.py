# GRP 필드가 존재하고 OFF가 True인 문서만 필터링하는 match 단계 반환  
def match_offensive_group():
    return {
        "$match": {
            "OFF": True,
            "TGT": {"$in": ["individual", "group", "untargeted", "other"]},
            "offensive_score": {"$ne": None}
        }
    }
    
def project_final():
    return {
        "$project": {
            "TGT": 1,
            "OFF": 1,
            "offensive_score": 1
        }
    }