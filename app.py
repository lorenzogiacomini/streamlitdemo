import streamlit as st
import openai
from anthropic import Anthropic
import os
from datetime import datetime
import streamlit_authenticator as stauth

# Configurazione pagina
st.set_page_config(
    page_title="LLM Chat",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inizializza authenticator
def get_authenticator():
    """Crea e restituisce l'authenticator con credenziali da secrets"""
    # Ottieni credenziali da secrets
    users = st.secrets.get("users", {})

    # Crea la configurazione per streamlit-authenticator
    # Genera hash delle password
    credentials = {
        "usernames": {}
    }

    for username, password in users.items():
        # Usa la password direttamente hashata
        hashed_password = stauth.Hasher([password]).generate()[0]
        credentials["usernames"][username] = {
            "name": username,
            "password": hashed_password
        }

    # Configurazione authenticator
    config = {
        "credentials": credentials,
        "cookie": {
            "name": "llm_chat_auth",
            "key": "random_signature_key_12345",  # Chiave per firmare i cookie
            "expiry_days": 7
        },
        "preauthorized": {
            "emails": []
        }
    }

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days']
    )

    return authenticator

# Funzione per inizializzare la chat
def init_chat():
    """Inizializza lo stato della chat"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "api_key" not in st.session_state:
        st.session_state.api_key = ""
    if "provider" not in st.session_state:
        st.session_state.provider = "OpenAI"
    if "model" not in st.session_state:
        st.session_state.model = "gpt-4o-mini"

# Funzione per chiamare OpenAI
def call_openai(messages, api_key, model):
    """Effettua chiamata a OpenAI API"""
    try:
        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7,
            stream=True
        )
        return response
    except Exception as e:
        st.error(f"Errore OpenAI: {str(e)}")
        return None

# Funzione per chiamare Anthropic
def call_anthropic(messages, api_key, model):
    """Effettua chiamata a Anthropic API"""
    try:
        client = Anthropic(api_key=api_key)

        # Converti messaggi al formato Anthropic
        system_message = ""
        anthropic_messages = []

        for msg in messages:
            if msg["role"] == "system":
                system_message = msg["content"]
            else:
                anthropic_messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })

        # Chiamata streaming
        # Costruisci parametri dinamicamente
        stream_params = {
            "model": model,
            "max_tokens": 4096,
            "messages": anthropic_messages,
            "temperature": 0.7
        }

        # Aggiungi system solo se presente
        if system_message:
            stream_params["system"] = system_message

        with client.messages.stream(**stream_params) as stream:
            for text in stream.text_stream:
                yield text

    except Exception as e:
        st.error(f"Errore Anthropic: {str(e)}")
        return None

# Funzione principale
def main():
    # Inizializza authenticator
    authenticator = get_authenticator()

    # Login
    name, authentication_status, username = authenticator.login(location='main')

    # Gestione stati di autenticazione
    if authentication_status == False:
        st.error('❌ Username o password non validi')
        return

    if authentication_status == None:
        st.warning('👋 Inserisci username e password per accedere')
        return

    # Utente autenticato - salva username in session_state
    if "current_user" not in st.session_state:
        st.session_state["current_user"] = username

    # Inizializza chat
    init_chat()

    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("💬 LLM Chat")
    with col2:
        authenticator.logout('Logout', 'main')

    st.markdown("---")

    # Sidebar per configurazione
    with st.sidebar:
        st.header("⚙️ Configurazione")

        # Selezione provider
        provider = st.selectbox(
            "Provider LLM",
            ["OpenAI", "Anthropic"],
            key="provider_select"
        )

        # Selezione modello in base al provider
        if provider == "OpenAI":
            models = ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo"]
            default_model = "gpt-4o-mini"
        else:  # Anthropic
            models = ["claude-3-5-sonnet-20241022", "claude-3-5-haiku-20241022", "claude-3-opus-20240229"]
            default_model = "claude-3-5-sonnet-20241022"

        model = st.selectbox(
            "Modello",
            models,
            index=models.index(default_model) if default_model in models else 0
        )

        # Input API Key
        api_key = st.text_input(
            "API Key",
            type="password",
            help="Inserisci la tua API key personale"
        )

        st.markdown("---")

        # Pulsante per pulire la chat
        if st.button("🗑️ Pulisci Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

        # Info utente
        st.markdown("---")
        st.caption(f"👤 Utente: {st.session_state.get('current_user', 'N/A')}")
        st.caption(f"📅 {datetime.now().strftime('%d/%m/%Y %H:%M')}")

        # Statistiche chat
        st.markdown("---")
        st.metric("Messaggi", len(st.session_state.messages))

    # Area principale chat
    # Mostra messaggi esistenti
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input utente
    if prompt := st.chat_input("Scrivi il tuo messaggio..."):
        # Verifica che l'API key sia stata inserita
        if not api_key:
            st.error("⚠️ Inserisci la tua API key nella sidebar")
            return

        # Aggiungi messaggio utente
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Genera risposta
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            # Prepara messaggi per l'API
            api_messages = st.session_state.messages.copy()

            try:
                if provider == "OpenAI":
                    # Chiamata OpenAI
                    response = call_openai(api_messages, api_key, model)
                    if response:
                        for chunk in response:
                            if chunk.choices[0].delta.content is not None:
                                full_response += chunk.choices[0].delta.content
                                message_placeholder.markdown(full_response + "▌")
                        message_placeholder.markdown(full_response)

                else:  # Anthropic
                    # Chiamata Anthropic
                    for text in call_anthropic(api_messages, api_key, model):
                        if text:
                            full_response += text
                            message_placeholder.markdown(full_response + "▌")
                    message_placeholder.markdown(full_response)

                # Salva risposta
                if full_response:
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": full_response
                    })

            except Exception as e:
                st.error(f"Errore durante la generazione: {str(e)}")

if __name__ == "__main__":
    main()
