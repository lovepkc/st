import openai
import streamlit as st 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import db

openai.api_key = st.secrets['OPENAI_API_KEY']


def retrive_docs(query, docs, k=2):
    vectorizer = TfidfVectorizer()
    doc_vectors = vectorizer.fit_transform(docs + [query])
    query_vec = doc_vectors[-1]
    doc_vectors = doc_vectors[:-1]
    similarities = cosine_similarity(query_vec, doc_vectors).flatten()
    top_indices = similarities.argsort()[::-1][:k]

    return [docs[i] for i in top_indices]


def get_reply(user_input):
    retrived = retrive_docs(user_input, db.DOCUMENTS, k=2)
    context = "\n".join(retrived)

    full_prompt = (
        f"다음 정보를 참고하여 대답하세요:\n\n{context}\n\n"
        f"{user_input}"
    )

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role":"system", "content":db.INSTRUCTION}, {"role":"user", "content":full_prompt}],           
    )
        
    reply = response.choices[0].message.content
    
    return reply
        