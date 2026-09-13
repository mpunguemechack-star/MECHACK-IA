import streamlit as st
from groq import Groq
from streamlit_mic_recorder import speech_to_text
import base64

st.set_page_config(page_title="MECHACK-IA", page_icon="🤖", layout="wide")

st.title("🤖 IR-MECHACK-IA — Plateforme IA Complète")
st.caption("Assistant intelligent multi-modal : Texte, Voix, Vision & Analyse de fichiers")

# Barre latérale
api_key = st.sidebar.text_input("Clé API Groq", type="password", value="", help="Entrez votre clé gsk_...")

model_choice = st.sidebar.selectbox(
    "Modèle IA principal",
    [
        "openai/gpt-oss-20b",
        "openai/gpt-oss-120b",
        "qwen/qwen3.6-27b"
    ],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Aide** : Vous pouvez poser des questions par texte, parler directement avec le micro ou envoyer des images/captures d'écran.")

if not api_key:
    st.info("🔑 Veuillez entrer votre clé API Groq dans le panneau de gauche pour commencer.", icon="🔑")
else:
    client = Groq(api_key=api_key)

    # Initialisation de l'historique
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "system",
                "content": (
                    "Tu es IR-MECHACK-IA, un assistant virtuel polyvalent, extrêmement puissant et intelligent. "
                    "Tu as été créé et conçu par IR Mechack Mpungue. "
                    "Tu dois toujours te présenter exclusivement sous le nom IR-MECHACK-IA. "
                    "Tu aides les utilisateurs dans la programmation, l'analyse d'images, la rédaction et la résolution de problèmes techniques."
                )
            }
        ]

    # Affichage de l'historique
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    st.markdown("---")
    
    # Zone de contrôle des entrées
    col_vocal, col_file = st.columns([1, 1])

    with col_vocal:
        st.write("🎤 **Entrée Vocale :**")
        text_from_voice = speech_to_text(
            language='fr',
            start_prompt="🔴 Appuyez pour parler",
            stop_prompt="⏹️ Arrêter",
            key='voice_input'
        )

    with col_file:
        st.write("🖼️ **Envoyer une capture ou image :**")
        uploaded_file = st.file_uploader("Choisissez une image...", type=["png", "jpg", "jpeg"], label_visibility="collapsed")

    # Zone de saisie texte
    text_from_chat = st.chat_input("Posez votre question ou décrivez votre besoin...")

    # Déterminer la source du prompt
    prompt = text_from_voice if text_from_voice else text_from_chat

    if prompt or uploaded_file:
        # Traitement si une image est jointe
        if uploaded_file is not None:
            st.image(uploaded_file, caption="Image envoyée", use_column_width=True)
            prompt_content = prompt if prompt else "Analyse cette image ou cette capture d'écran et explique ce qu'elle contient."
            user_message = f"[Image transmise] {prompt_content}"
        else:
            user_message = prompt

        st.session_state.messages.append({"role": "user", "content": user_message})
        with st.chat_message("user"):
            st.markdown(user_message)

        with st.chat_message("assistant"):
            try:
                # Appel API à Groq
                chat_completion = client.chat.completions.create(
                    messages=st.session_state.messages,
                    model=model_choice,
                )
                response = chat_completion.choices[0].message.content
                st.markdown(response)
                
                # Option de téléchargement si du code Python est généré dans la réponse
                if "```python" in response:
                    code_block = response.split("```python")[1].split("```")[0]
                    st.download_button(
                        label="📥 Télécharger le fichier ",
                        data=code_block,
                        file_name="programme_mechack_ia.py",
                        mime="text/x-python"
                    )

                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Erreur : {e}")
