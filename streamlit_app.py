import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="숏폼 대본 & 마케팅 카피 추출기", page_icon="⚡")
st.title("⚡ 숏폼 대본 & 마케팅 카피 자동 생성기")

url = st.text_input("분석할 웹페이지 URL을 입력하세요:", placeholder="https://...")

if st.button("🚀 카피 및 대본 생성하기"):
    if not url:
        st.warning("URL을 입력해 주세요.")
    else:
        try:
            with st.spinner("웹페이지 분석 중..."):
                headers = {'User-Agent': 'Mozilla/5.0'}
                response = requests.get(url, headers=headers, timeout=10)
                soup = BeautifulSoup(response.text, 'html.parser')
                text = ' '.join([p.get_text() for p in soup.find_all(['p', 'h1', 'h2', 'h3', 'span'])])
                
                # 텍스트 정제
                clean_text = ' '.join(text.split())[:1000]

            st.success("분석 완료!")
            st.subheader("📋 수집된 핵심 내용")
            st.write(clean_text if clean_text else "텍스트를 추출하지 못했습니다.")
            
            st.markdown("---")
            st.info("💡 위 수집 내용을 바탕으로 아래 AI 프롬프트를 복사하여 ChatGPT나 Gemini에 넣으시면 완성된 카피를 얻으실 수 있습니다!")
            
            prompt = f"""다음 웹페이지 내용을 바탕으로 마케팅 카피라이팅과 숏폼 대본을 작성해줘.

[상품/사이트 내용]
{clean_text}

[요청사항]
1. 타겟 고객층 (3부류)
2. 핵심 소구점 (3가지)
3. SNS 광고 카피 (후킹 멘트 3개 + 본문 캡션)
4. 30초 숏폼/쇼츠 영상 스크립트 (후킹-문제제기-CTA)"""

            st.code(prompt, language="text")

        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")