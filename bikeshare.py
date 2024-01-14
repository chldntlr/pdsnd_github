import time
import pandas as pd
import numpy as np
#도시 데이터 정보 파일을 딕셔너리로 저장함
CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv' }
#get_filters function은 도시와 월과 일을 입력 받아 처리 하는 function
def get_filters():
    print('안녕하세요! 미국 자전거공유 데이터를 탐색해봅시다!')
    #도시 입력
    while True:
        city = input("도시를 입력하세요 (chicago, new york city, washington): ").lower()
        if city in ['chicago', 'new york city', 'washington']:
            break
        else:
            print("잘못된 입력입니다. 올바른 도시를 입력하세요.")
    #월 입력
    while True:
        month = input("월을 입력하세요 (all, january, february, ... , june): ").lower()
        months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
        if month in months:
            break
        else:
            print("잘못된 입력입니다. 올바른 월을 입력하세요.")
    #요일 입력
    while True:
        day = input("요일을 입력하세요 (all, monday, tuesday, ... sunday): ").lower()
        days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        if day in days:
            break
        else:
            print("잘못된 입력입니다. 올바른 요일을 입력하세요.")

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    #city에 입력 받은 도시 불러오기
    file_name = CITY_DATA[city]
    df = pd.read_csv(file_name)

    #입력된 월을 숫자로 매핑하는 함수
    def map_month(month):
        months_dict = {
            'all': 0, 'january': 1, 'february': 2, 'march': 3,
            'april': 4, 'may': 5, 'june': 6
        }
        return months_dict.get(month.lower(), 0)

    #입력된 요일을 숫자로 매핑하는 함수
    def map_day(day):
        days_dict = {
            'all': 0, 'monday': 0, 'tuesday': 1, 'wednesday': 2,
            'thursday': 3, 'friday': 4, 'saturday': 5, 'sunday': 6
        }
        return days_dict.get(day.lower(), 0)

    # 'Start Time' 열을 날짜 및 시간 형식으로 변환
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # 월에 따라 데이터 필터링
    if month != 'all':
        selected_month = map_month(month)
        if selected_month != 0:
            df = df[df['Start Time'].dt.month == selected_month]

    # 요일에 따라 데이터 필터링
    if day != 'all':
        selected_day = map_day(day)
        if selected_day != 0:
            df = df[df['Start Time'].dt.dayofweek == selected_day]

    #기존 데이터 5줄 출력
    current_line = 0
    while current_line < len(df):
        for i in range(current_line, current_line + 5):
            if i < len(df):
                print(df.iloc[i])
            else:
                break
        more_time = input("더 많은 항목을 조회 하시겠습니까? (yes, no)")
        if more_time.lower() != "yes" or current_line >= len(df):
            break
        else:
            current_line += 5

        restart = input('도시, 월, 요일을 다시 입력하시겠습니까? (yes/no): ')
        if restart.lower() != 'yes':
            break
        else:
            city = input("도시를 입력하세요 (chicago, new york city, washington): ").lower()
            month = input("월을 입력하세요 (all, january, february, ... , june): ").lower()
            day = input("요일을 입력하세요 (all, monday, tuesday, ... sunday): ").lower()

    return df


def time_stats(df):
    start_time = time.time()

    #가장 많이 사용하는 월
    most_month = df['Start Time'].dt.month.mode()[0]
    print(f"가장 많이 사용되는 월은 {most_month}입니다.")

    #가장 많이 사용되는 요일
    most_day = df['Start Time'].dt.day.mode()[0]
    print(f"가장 많이 사용된 요일은 {most_day}입니다.")

def station_stats(df):
    print("----------------------------------------")

    start_time = time.time()

    #가장 많이 사용되는 시작 지점
    most_start_station = df['Start Station'].mode()[0]
    print(f"가장 많이 시작된 역은 {most_start_station} 역 입니다.")

    #가장 많이 사용되는 끝나는 지점
    most_end_station = df['End Station'].mode()[0]
    print(f"가장 믾이 끝나는 역은{most_end_station} 역 입니다.")

def trip_duration_stats(df):
    print("----------------------------------------")
    start_time = time.time()

    #총 여행시간
    total_time = df['Trip Duration'].sum()
    print(f"총 여행 시간은 {total_time}초 입니다.")

    #평균 여행시간
    mean_time = df['Trip Duration'].mean()
    print(f"평균 여행 시간은 {mean_time}초 입니다.")

def user_stats(df):
    print("----------------------------------------")
    start_time = time.time()

    #사용지 유형 별 대여량
    user_type = df['User Type'].value_counts()
    print("사용자 별 대여량은:")
    for user, count in user_type.items():
        print(f"{user} : {count}")
    print("----------------------------------------")

    #성별에 따른 대여량
    if 'Gender' in df:
        gender_count = df['Gender'].value_counts()
        print("성별에 따른 대여량은:")
        for gender, count in gender_count.items():
            print(f"{gender} : {count}")
    print("----------------------------------------")

    #출생 연도에 따른 가장 늙은 사람, 가장 젊은 사람, 평균 연도
    if 'Birth Year' in df:
        earliest_birth_year = df['Birth Year'].min()
        latest_birth_year = df['Birth Year'].max()
        average_year = int(df['Birth Year'].mean())

        print(f"가장 오래된 출생 연도는 {earliest_birth_year} 입니다.")
        print(f"가장 최근 출생 연도는 {latest_birth_year} 입니다.")
        print(f"평균 연도는 {average_year} 입니다.")
        print("----------------------------------------")

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\n다시 시작하시겠습니까? yes 또는 no로 입력하세요.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()