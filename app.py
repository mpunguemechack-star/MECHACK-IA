import streamlit as st
from groq import Groq

st.set_page_config(page_title="Assistant IA Universel", page_icon="🤖", layout="centered")

st.title("🤖 Assistant IA Universel — Mechack IA")
st.write("Posez toutes vos questions, l'IA vous répond instantanément !")

# Saisie de la clé API
api_key = st.sidebar.text_input("Clé API Groq", type="password", value="", help="Entrez votre clé gsk_...")

if not api_key:
    st.info("💡 Veuillez entrer votre clé API Groq (MECHACK_IA) dans le panneau de gauche pour commencer.", icon="🔑")
else:
    client = Groq(api_key=api_key)

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "Tu es un assistant IA polyvalent, intelligent et très précis."}
        ]

    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input("Posez votre question ici..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                stream = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=st.session_state.messages,
                    stream=False,
                )
                response = stream.choices[0].message.content
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Erreur : {e}")
