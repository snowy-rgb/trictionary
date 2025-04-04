import requests
from bs4 import BeautifulSoup
import os
import json

KEYWORD_FILE = "inSys/keywords.txt"
ENTRIES_DIR = "entries"
OUTPUT_JSON = "inSys/entry_list.json"

def fetch_namu_page(keyword, idx):

        url = f"https://namu.moe/w/{keyword}"
        wiki_url = f"https://namu.wiki/w/{keyword}"  # 이건 공식 위키용 링크
        char_url = f"https://namu.wiki/w/{keyword}(트릭컬%20리바이브)" # 캐릭터용 문서
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://namu.moe/",
            "Accept-Language": "ko-KR,ko;q=0.9"
        }
    
        try:
            res = requests.get(url, headers=headers)
            
            if res.status_code != 200:
                print(f"[!] '{keyword}' 문서를 찾을 수 없습니다. (status: {res.status_code})")
                return False

            soup = BeautifulSoup(res.text, "html.parser")
            article = soup.find("article")
            summary = article.find("p").text.strip() if article and article.find("p") else "요약 정보 없음"
    
            code = f"{idx+1:04}"  # 0001, 0002, ...
            html_content = f"""
            <!DOCTYPE html>
            <html lang="ko">
            <head><meta charset="UTF-8"><title>{keyword}</title></head>
            <body>
            <h1>{keyword}</h1>
            <p>{summary}</p>
            <p><strong>코드: code[{code}]</strong></p>
            <p><a href="{url}" target="_blank">[나무위키 원문 보기]</a></p>
            </body></html>
            """
    
            with open(os.path.join(ENTRIES_DIR, f"{keyword}.html"), "w", encoding="utf-8") as f:
                f.write(html_content)
    
            print(f"[✓] '{keyword}' 저장 완료")
            return True
    
        except Exception as e:
            print(f"[!] '{keyword}' 처리 중 오류 발생: {e}")
            return False

def generate_entry_list():
    files = os.listdir(ENTRIES_DIR)
    entries = [f.replace(".html", "") for f in files if f.endswith(".html")]

    # ✅ 여기서 정렬 추가!
    entries.sort()  # 가나다 또는 code[0001] 순서로 정렬됨

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)

    print(f"[✓] entry_list.json 생성 완료 ({len(entries)}개 항목)")


def main():
    os.makedirs(ENTRIES_DIR, exist_ok=True)

    if not os.path.exists(KEYWORD_FILE):
        print(f"[X] '{KEYWORD_FILE}' 파일이 없습니다.")
        return

    with open(KEYWORD_FILE, "r", encoding="utf-8") as f:
        keywords = [line.strip() for line in f if line.strip()]
        
    # del
    # for kw in keywords:
    #     fetch_namu_page(kw)

    for idx, kw in enumerate(keywords):
        fetch_namu_page(kw, idx)

    generate_entry_list()
    print("[🎉] 자동 빌드 완료!")

if __name__ == "__main__":
    main()

