import streamlit as st
import urllib.request
import re
from bs4 import BeautifulSoup

st.set_page_config(page_title="마케팅 카피 자동 생성기", page_icon="⚡")

st.title("⚡ 숏폼 대본 & 마케팅 카피 추출기")
st.write("분석할 링크(URL)를 입력하면 마케팅 핵심 포인트와 쇼츠 대본용 프롬프트를 자동으로 추출합니다.")

url = st.text_input("🔗 분석할 웹사이트 링크 입력", placeholder="https://...")

def get_page_text(target_url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(target_url, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as response:
        html = response.read().decode('utf-8', errors='ignore')
    soup = BeautifulSoup(html, 'html.parser')
    for el in soup(['script', 'style', 'header', 'footer', 'nav', 'iframe']):
        el.extract()
    text = soup.get_text(separator=' ', strip=True)
    return re.sub(r'\s+', ' ', text)[:2500]

if st.button("🚀 분석 시작"):
    if not url.startswith("http"):
        st.error("https:// 형식의 올바른 링크를 입력해 주세요.")
    else:
        with st.spinner("웹페이지 내용을 수집하는 중입니다..."):
            try:
                content = get_page_text(url)
                st.success("수집 완료!")
                
                prompt = f"""다음 웹페이지 내용을 바탕으로 마케팅 카피라이팅과 숏폼 대본을 작성해줘.

[상품/사이트 내용]
{content}

[요청사항]
1. 타겟 고객층 (3부류)
2. 핵심 소구점 (3가지)
3. SNS 광고 카피 (후킹 멘트 3개 + 본문 캡션)
4. 30초 숏폼/쇼츠 영상 스크립트 (후킹-문제제기-CTA)"""

                st.subheader("📋 생성된 결과 프롬프트")
                st.code(prompt, language="text")
            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")
                