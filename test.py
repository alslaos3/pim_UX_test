import random
import string
import requests

# 14자리의 무작위 문자열을 생성하는 함수
def generate_random_string(length):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))

# 매크로
def url_macro(base_url, num_trials):
    for _ in range(num_trials):
        random_string = generate_random_string(14)
        url = base_url + random_string
        response = requests.get(url)
        print(f"{_}")
        # 응답이 성공적이라면, URL을 출력하고 종료
        if response.status_code == 200:
            print(f"Found a valid URL: {url}")
            return

    print("No valid URL found")

# 매크로 실행
base_url = "https://user-app.krampoline.com/"
url_macro(base_url, 1000)
