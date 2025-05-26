# 타겟 스코어 구간화 집계 파이프라인 반환 (하드코딩 버전)
def get_target_score_bin_pipeline():
    return [
        # 뉴스 제목, 댓글, 타겟 정보, 공격성 정보 등을 추출하는 $project 단계
        {
            "$project": {
                "news_title": "$title", # 뉴스 제목 필드 매핑 
                "comment_text": "$comment", # 댓글 텍스트 필드 매핑
                "target_type": "$TGT", # 타겟 유형 (예: group, individual 등)
                "target_group": "$GRP", # 특정 타겟 그룹 (예: 여성, 정치인 등)
                "offensive_phrase": "$OFF_span", # 공격적인 문구가 포함된 부분
                "offensive_score": "$offensive_score", # 공격성 점수 (0~1 사이의 수치)
                "date": "$date", # 댓글 작성 날짜
                "OFF": 1, # 공격성 여부 표시
                "_id": 0 # _id 필드는 제외
            }
        },
        # 타겟 유형별로 공격성 점수를 구간별로 집계하는 병렬 파이프라인 단계
        {
            "$facet": {
                # group 타겟에 대해 공격성 점수를 버킷으로 집계하는 파이프라인 단계
                "group": [
                    {
                        "$match": {
                            "OFF": True, # 공격성 표시가 True인 문서만 필터링
                            "target_type": "group", # 타겟 유형이 "group"인 문서만 선택
                            "offensive_score": { "$ne": None } # 공격성 점수가 존재하는 문서만 필터링
                        }
                    },
                    {
                        "$bucket": {
                            "groupBy": "$offensive_score", # 공격성 점수를 기준으로 버킷 생성
                            "boundaries": [0.0, 0.2, 0.4, 0.6, 0.8, 1.0], # 점수 구간 정의
                            "default": "other", # 지정 구간에 속하지 않으면 "other"로 분류
                            "output": {
                                "count": { "$sum": 1 }, # 각 버킷별 문서 수 집계
                                "target_type": { "$first": "group" } # 각 버킷에 대해 "group" 값을 기록
                            }
                        }
                    }
                ],
                # individual 타겟에 대해 공격성 점수를 버킷으로 집계하는 파이프라인 단계
                "individual": [
                    {
                        "$match": {
                            "OFF": True, # 공격성 표시가 True인 문서만 필터링
                            "target_type": "individual", # 타겟 유형이 "indvidual"인 문서만 선택
                            "offensive_score": { "$ne": None } # 공격성 점수가 존재하는 문서만 필터링
                        }
                    },
                    {
                        "$bucket": {
                            "groupBy": "$offensive_score", # 공격성 점수를 기준으로 버킷 생성
                            "boundaries": [0.0, 0.2, 0.4, 0.6, 0.8, 1.0], # 점수 구간 정의
                            "default": "other", # 지정 구간에 속하지 않으면 "other"로 분류
                            "output": {
                                "count": { "$sum": 1 }, # 각 버킷별 문서 수 집계
                                "target_type": { "$first": "individual" } # 각 버킷에 대해 "individual" 값을 기록
                            }
                        }
                    }
                ],
                # untargeted 타겟에 대해 공격성 점수르 버킷으로 집계하는 파이프라인 단계
                "untargeted": [
                    {
                        "$match": {
                            "OFF": True, # 공격성 표시가 True인 문서만 필터링
                            "target_type": "untargeted", # 타겟 유형이 "untargeted"인 문서만 선택
                            "offensive_score": { "$ne": None } # 공격성 점수가 존재하는 문서만 필터링
                        }
                    },
                    {
                        "$bucket": {
                            "groupBy": "$offensive_score", # 공격성 점수를 기준으로 버킷 생성
                            "boundaries": [0.0, 0.2, 0.4, 0.6, 0.8, 1.0], # 점수 구간 정의
                            "default": "other", # 지정 구간에 속하지 않으면 "other"로 분류
                            "output": { 
                                "count": { "$sum": 1 }, # 각 버킷별 문서 수 집계
                                "target_type": { "$first": "untargeted" } # 각 버킷에 대해 "untargeted" 값을 기록
                            }
                        }
                    }
                ],
                # other 타겟에 대해 공격성 점수를 버킷으로 집계하는 파이프라인 단계
                "other": [
                    {
                        "$match": {
                            "OFF": True, # 공격성 표시가 True인 문서만 필터링
                            "target_type": "other", #  타겟 유형이 "other"인 문서만 선택
                            "offensive_score": { "$ne": None } # 공격성 점수가 존재하는 문서만 필터링
                        }
                    },
                    {
                        "$bucket": {
                            "groupBy": "$offensive_score", # 공격성 점수를 기준으로 버킷 생성 
                            "boundaries": [0.0, 0.2, 0.4, 0.6, 0.8, 1.0], # 점수 구간 정의
                            "default": "other", # 지정 구간에 속하지 않으면 "other"로 분류
                            "output": {
                                "count": { "$sum": 1 }, # 각 버킷별 문서 수 집계
                                "target_type": { "$first": "other" } # 각 버킷에 대해 "other" 값을 기록
                            }
                        }
                    }
                ]
            }
        },
        # facet 결과로부터 각 타겟 유형의 결과를 하나의 배열로 병합하는 단계
        {
            "$project": {
                "merged": {
                    "$concatArrays": [
                        "$group", # group 타겟 결과 배열
                        "$individual", # individual 타겟 결과 배열
                        "$untargeted", # untargeted 타렛 결과 배열
                        "$other" # other 타겟 결과 배열
                    ]
                }
            }
        },
        # 병합된 배열을 개별 문서로 분해하고, 각 요소를 루트로 설정한 뒤 정렬하는 단계
        { "$unwind": "$merged" }, # merged 배열을 요소 단위로 분해
        { 
            "$replaceRoot": { "newRoot": "$merged" }  # 분해된 요소를 새로운 문서의 루트로 설정
        },
        { 
            "$sort": { 
                "target_type": 1,  # target_type 기준 오름차순 정렬
                "_id": 1           # 동일한 target_type 내에서는 _id 기준 정렬
            }
        }
    ]
