# 공격성(True)이며 그룹(GRP)가 존재하는 문서만 필터링하는 match 단계 반환  
def match_offensive_with_group():  
    return {  
        "$match": {  
            "OFF": True,  # 공격성 댓글만 대상  
            "GRP": {"$ne": None}  # GRP 필드가 None이 아닌 문서만 필터링  
        }  
    }

# 분석에 필요한 기본 필드만 추출하는 project 단계 반환  
def project_basic_fields():  
    return {  
        "$project": {  
            "news_title": "$title",  # 뉴스 제목  
            "comment_text": "$comment",  # 댓글 내용  
            "target_type": "$TGT",  # 타겟 유형 (예: gender, political 등)  
            "target_group": "$GRP",  # 타겟 그룹 (예: 여성, 보수 등)  
            "offensive_phrase": "$OFF_span",  # 공격성 문구  
            "date": "$date",  # 날짜  
            "_id": 0  # _id 필드는 제외  
        }  
    }
