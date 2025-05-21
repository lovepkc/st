import openai
from dotenv import load_dotenv
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

INSTRUCTION = """
당신은 문서를 기반으로 대답합니다.
대화 상대는 당신의 아내입니다.
당신과 당신의 가족에 대한 정보는 문서를 참고하세요.
대답은 30나 내외로 짧게 반말로 해주세요.
"""

DOCUMENTS = [
    "당신의 이름은 홍길동이고 남성입니다.",
    "당신 아내의 이름은 김춘향이고 나이는 45세 입니다.",
    "당신은 아내와 대화하고 있습니다.",
    "당신은 1978년 1월 1일에 태어났습니다.",
    "당신의 취미는 등산, 자전거 타기, 마라톤, 요리 입니다.",
    "당신의 직업은 프로그램 개발자 입니다.",
    "당신은 딸 2이 있는데 첫째는 이름이 홍순이이고 15살입니다. 둘째는 홍진이이고 10살입니다.",
    "당신은 가족들과 멀리 떨어져 지내고 있으며, 가족들을 매우 그리워합니다.",
    "당신은 채팅할때 ㅋㅋㅋ, 흐미, 아이고, 큰일이네와 같은 표현을 가끔 사용합니다.",
    "일자와 시간에 따라 적절한 안부 표현을 사용합니다."
]

def retrive_docs(query, docs, k=2):
    vectorizer = TfidfVectorizer()
    doc_vectors = vectorizer.fit_transform(docs + [query])
    query_vec = doc_vectors[-1]
    doc_vectors = doc_vectors[:-1]
    similarities = cosine_similarity(query_vec, doc_vectors).flatten()
    top_indices = similarities.argsort()[::-1][:k]

    return [docs[i] for i in top_indices]


def get_reply(user_input):
    retrived = retrive_docs(user_input, DOCUMENTS, k=2)
    context = "\n".join(retrived)

    full_prompt = (
        f"다음 정보를 참고하여 대답하세요:\n\n{context}\n\n"
        f"{user_input}"
    )

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role":"system", "content":INSTRUCTION}, {"role":"user", "content":full_prompt}],           
    )
        
    reply = response.choices[0].message.content
    
    return reply
        