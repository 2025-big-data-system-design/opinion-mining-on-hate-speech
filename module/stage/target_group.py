# GRP 필드가 존재하고 OFF가 True인 문서만 필터링하는 match 단계 반환  
def match_offensive_group():
    return {
        "$match": {
            "GRP": {
                "$type": "string",
                "$not": {"$regex": "&"}  # "&" 포함된 GRP 제외
                },
            "offensive_score": {"$exists": True}
        }
    }

# gender, politics와 같은 category와 gender-LGBTQ+, gender-female과 같은 subgroup을 분리한다
def project_category_and_subgroup():
    return {
        "$project": {
            "offensive_score": 1,
            "grp_parts": {
                "$regexFind": {
                    "input": "$GRP",
                    "regex": r"^(gender|race|politics|religion|others)[-_](.+)$",
                    "options": "i"
                }
            }
        }
    }
    
def extract_category_and_subgroup():
    return {
        "$project": {
            "offensive_score": 1,
            "category": {
                "$cond": {
                    "if": {"$ne": ["$grp_parts", None]},
                    "then": {
                        "$toLower": {
                            "$arrayElemAt": ["$grp_parts.captures", 0]
                        }
                    },
                    "else": "others"
                }
            },
            "subgroup": {
                "$cond": {
                    "if": {"$ne": ["$grp_parts", None]},
                    "then": {
                        "$arrayElemAt": ["$grp_parts.captures", 1]
                    },
                    "else": "$GRP"
                }
            }
        }
    }

    
def group_by_category_and_subgroup():
    return {
        "$group": {
            "_id": {
                "category": "$category",
                "subgroup": "$subgroup"
            },
            "count": {"$sum": 1},
            "offensive_score": {"$avg": "$offensive_score"}
        }
    }
    
def project_result():
    return {
        "$project": {
            "_id": 0,
            "category": "$_id.category",
            "subgroup": "$_id.subgroup",
            "count": 1,
            "offensive_score": 1
        }
    }