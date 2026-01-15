# 💬 LLM Chat con Autenticazione

Una chat interattiva con modelli LLM (Large Language Models) costruita con Streamlit, dotata di sistema di autenticazione e supporto per multiple API.

## ✨ Caratteristiche

- **🔐 Autenticazione Utente**: Sistema sicuro di login con username/password
- **🤖 Multi-Provider LLM**: Supporto per OpenAI e Anthropic (Claude)
- **🔑 BYK (Bring Your Key)**: Gli utenti utilizzano le proprie API keys
- **💬 Chat Interattiva**: Interfaccia chat con streaming delle risposte
- **📱 Responsive**: Design ottimizzato per desktop e mobile
- **☁️ Cloud-Ready**: Pronto per il deploy su Streamlit Community Cloud

## 🚀 Quick Start Locale

### Prerequisiti

- Python 3.8 o superiore
- pip

### Installazione

1. Clona il repository:
```bash
git clone <repository-url>
cd streamlitdemo
```

2. Installa le dipendenze:
```bash
pip install -r requirements.txt
```

3. Configura gli utenti:
```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

4. Modifica `.streamlit/secrets.toml` con i tuoi utenti:
```toml
[users]
admin = "tuapassword"
utente1 = "password123"
```

5. Avvia l'applicazione:
```bash
streamlit run app.py
```

6. Apri il browser su `http://localhost:8501`

## ☁️ Deploy su Streamlit Community Cloud

### Step 1: Prepara il Repository

Assicurati che il tuo repository contenga:
- `app.py` (applicazione principale)
- `requirements.txt` (dipendenze)
- `.streamlit/config.toml` (configurazione)

### Step 2: Deploy su Streamlit Cloud

1. Vai su [share.streamlit.io](https://share.streamlit.io)
2. Fai login con il tuo account GitHub
3. Clicca su "New app"
4. Seleziona:
   - **Repository**: il tuo repository GitHub
   - **Branch**: main (o il branch desiderato)
   - **Main file path**: `app.py`
5. Clicca su "Deploy"

### Step 3: Configura i Secrets

1. Nell'interfaccia di Streamlit Cloud, vai su **Settings** > **Secrets**
2. Aggiungi i tuoi utenti nel formato TOML:

```toml
[users]
admin = "password_sicura_123"
user1 = "altra_password_456"
demo = "demo789"
```

3. Clicca su "Save"
4. L'app si riavvierà automaticamente

## 🔑 Come Ottenere le API Keys

### OpenAI

1. Vai su [platform.openai.com](https://platform.openai.com)
2. Crea un account o fai login
3. Vai su **API Keys**
4. Clicca su "Create new secret key"
5. Copia la chiave (non sarà più visibile!)

### Anthropic (Claude)

1. Vai su [console.anthropic.com](https://console.anthropic.com)
2. Crea un account o fai login
3. Vai su **API Keys**
4. Clicca su "Create Key"
5. Copia la chiave

## 📖 Utilizzo

1. **Login**: Inserisci username e password configurati nei secrets
2. **Configura**: Nella sidebar, seleziona:
   - Provider LLM (OpenAI o Anthropic)
   - Modello desiderato
   - Inserisci la tua API key personale
3. **Chatta**: Scrivi il tuo messaggio nella chat e ricevi risposte in streaming
4. **Gestisci**: Usa il pulsante "Pulisci Chat" per iniziare una nuova conversazione

## 🎯 Modelli Supportati

### OpenAI
- `gpt-4o` - Più potente e versatile
- `gpt-4o-mini` - Veloce ed economico (consigliato)
- `gpt-4-turbo` - Versione turbo di GPT-4
- `gpt-3.5-turbo` - Veloce e economico

### Anthropic (Claude)
- `claude-3-5-sonnet-20241022` - Bilanciato (consigliato)
- `claude-3-5-haiku-20241022` - Veloce ed economico
- `claude-3-opus-20240229` - Più potente

## 🔒 Sicurezza

- ⚠️ **Non committare mai il file `.streamlit/secrets.toml`**
- 🔑 Le API keys sono inserite dagli utenti e non memorizzate
- 🔐 Le password in `secrets.toml` dovrebbero essere forti
- 📝 Su produzione, considera l'uso di sistemi di autenticazione più robusti

## 🛠️ Personalizzazione

### Modificare il Tema

Edita `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#FF4B4B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
```

### Aggiungere Nuovi Provider

Modifica `app.py` per aggiungere supporto per altri provider LLM (es. Cohere, Hugging Face, etc.)

## 📊 Struttura del Progetto

```
streamlitdemo/
├── app.py                          # Applicazione principale
├── requirements.txt                # Dipendenze Python
├── .gitignore                      # File da ignorare in Git
├── README.md                       # Questo file
└── .streamlit/
    ├── config.toml                # Configurazione Streamlit
    └── secrets.toml.example       # Esempio secrets (non committare secrets.toml!)
```

## 🐛 Troubleshooting

### "API key non valida"
- Verifica che l'API key sia corretta e attiva
- Controlla di aver selezionato il provider giusto
- Verifica di avere crediti disponibili sull'account

### "Username o password non validi"
- Verifica i secrets configurati
- Su Streamlit Cloud, controlla Settings > Secrets
- Assicurati che il formato TOML sia corretto

### L'app non si avvia
- Verifica che tutte le dipendenze siano installate
- Controlla i log per errori specifici
- Assicurati che `secrets.toml` sia configurato correttamente

## 📝 Licenza

MIT License - Sentiti libero di utilizzare e modificare questo progetto.

## 🤝 Contributi

Contributi, issues e feature requests sono benvenuti!

## 👨‍💻 Autore

Creato con ❤️ per dimostrare l'integrazione di LLM con Streamlit
