# MongoDB 관련 import  
from module.db.db_connection import get_collection  # MongoDB 컬렉션 연결 함수  

# pandas 관련 import  
import pandas as pd  # 데이터프레임 및 데이터 처리 관련 기능 제공  

# 파이프라인 관련 import  
from module.pipeline import (  
    get_offensive_pipeline,  # 공격성 관련 집계 파이프라인 함수  
    get_gender_year_pipeline,  # 성별-연도별 집계 파이프라인 함수  
    get_politics_year_pipeline,  # 정치 성향-연도별 집계 파이프라인 함수 
    get_race_year_pipeline,  # 인종-연도별 집계 파이프라인 함수 
    get_target_group_pipeline  # 타겟 그룹 집계 파이프라인 함수 
)

# MongoDB에서 파이프라인 실행 후 결과를 DataFrame으로 반환
def run_pipeline(
    pipeline # MongoDB aggregate에 사용할 파이프라인 리스트
):
    # MongoDB 컬렉션 객체 가져오기
    collection = get_collection() 
    
    # 집계 결과를 리스트로 변환 후 DataFrame으로 변환
    return pd.DataFrame(list(collection.aggregate(pipeline)))

# 기본 데이터프레임 생성
def get_base_df():
    # 공격성 관련 파이프라인 실행 후 DataFrame 생성
    df = run_pipeline(get_offensive_pipeline())
    
    # 'date' 컬럼이 존재하는 경우
    if "date" in df.columns: 
        # 문자열을 datetime 형식으로 변환 (변환 실패 시 NaT 처리)
        df["date"] = pd.to_datetime(df["date"], errors="coerce")  

    # 전처리된 DataFrame 반환
    return df

# 성별-연도별 집계 데이터프레임 생성
def get_gender_year_df():
    # 성별-연도별 집계 파이프라인 실행 후 DataFrame 생성
    df = run_pipeline(get_gender_year_pipeline())
    
    # 결과 DataFrame 반환
    return df

# 정치 성향-연도별 집계 데이터프레임 생성
def get_politics_year_df():
    # 정치 성향-연도별 집계 파이프라인 실행 후 DataFrame 생성
    df = run_pipeline(get_politics_year_pipeline())
    
    # 결과 DataFrame 반환
    return df

# 인종-연도별 집계 데이터프레임 생성
def get_race_year_df():
    # 인종-연도별 집계 파이프라인 실행 후 DataFrame 생성
    df = run_pipeline(get_race_year_pipeline())
    
    # 결과 DataFrame 반환
    return df

# 타겟 그룹 집계 데이터프레임 생성
def get_target_group_df():
    # 타겟 그룹 집계 파이프라인 실행 후 DataFrame 생성
    df = run_pipeline(get_target_group_pipeline())
    
    # 결과 DataFrame 반환
    return df