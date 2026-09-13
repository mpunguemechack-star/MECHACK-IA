import streamlit as st
from groq import Groq
from streamlit_mic_recorder import speech_to_text

st.set_page_config(page_title="Assistant IA Universel", page_icon="🤖", layout="centered")

st.title("🤖 Assistant IA Universel — Mechack IA")
st.write("Posez vos questions par texte ou à la voix !")

# Clé API Groq dans la barre latérale
api_key = st.sidebar.text_input("Clé API Groq", type="password", value="", help="Entrez votre clé gsk_...")

# Sélection dynamique avec les modèles recommandés par Groq
model_choice = st.sidebar.selectbox(
    "Modèle IA",
    [
        "openai/gpt-oss-20b",
        "openai/gpt-oss-120b",
        "qwen/qwen3.6-27b"
    ],
    index=0
)

if not api_key:
    st.info("💡 Veuillez entrer votre clé API Groq (MECHACK_IA) dans le panneau de gauche pour commencer.", icon="🔑")
else:
    client = Groq(api_key=api_key)

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "Tu es un assistant IA polyvalent, intelligent et très précis."}
        ]

    # Historique de conversation
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Entrée vocale (Micro)
    st.write("🎤 **Parler à l'assistant :**")
    text_from_voice = speech_to_text(
        language='fr',
        start_prompt="🔴 Appuyez pour parler",
        stop_prompt="⏹️ Arrêter l'enregistrement",
        key='voice_input'
    )

    # Entrée texte
    text_from_chat = st.chat_input("Ou tapez votre question ici...")

    prompt = text_from_voice if text_from_voice else text_from_chat

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                chat_completion = client.chat.completions.create(
                    messages=st.session_state.messages,
                    model=model_choice,
                )
                response = chat_completion.choices[0].message.content
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Erreur : {e}")
