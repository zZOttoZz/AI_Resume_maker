import streamlit as st
import requests
import fitz  # PyMuPDF for reading PDFs

# Sidinställningar
st.set_page_config(page_title="AI Resume Optimizer", layout="centered")

st.title("📄 AI Resume Optimizer (Gratis via Hugging Face)")
st.markdown("Fyll i formuläret nedan så genererar AI ett CV åt dig baserat på en fast mall.")

# Input-fält
job_text = st.text_area("📋 Klistra in jobbannonsen")
name = st.text_input("👤 Ditt namn")
role = st.text_input("🎓 Din nuvarande roll")
skills = st.text_area("🛠️ Vad är du bra på?")
achievements = st.text_area("🏆 Vad är du mest stolt över?")

# Ladda upp befintligt CV
cv_file = st.file_uploader("📑 Ladda upp ditt nuvarande CV (PDF)", type="pdf")
cv_summary = ""

# Läs texten från PDF och skapa en sammanfattning
def read_pdf(file) -> str:
    try:
        with fitz.open(stream=file.read(), filetype="pdf") as doc:
            text = "\n".join(page.get_text() for page in doc)
        return text
    except Exception as e:
        st.error(f"Kunde inte läsa PDF: {e}")
        return ""

def summarize_cv(text: str) -> str:
    summary_prompt = f"Sammanfatta följande CV i punktform:\n\n{text}"
    return call_llama3(summary_prompt)

if 'cv_summary' not in st.session_state:
    st.session_state['cv_summary'] = ''

if cv_file and st.button("📝 Sammanfatta CV"):
    with st.spinner("Läser och sammanfattar CV..."):
        cv_text = read_pdf(cv_file)
        if cv_text:
            st.session_state['cv_summary'] = summarize_cv(cv_text)

use_summary = False
if st.session_state['cv_summary']:
    st.markdown("### Sammanfattning av uppladdat CV")
    st.text_area("Kontrollera sammanfattningen", st.session_state['cv_summary'], height=150)
    use_summary = st.checkbox("Använd denna sammanfattning i prompten", value=True)

# Funktion för att anropa Hugging Face LLaMA 3 API
def call_llama3(prompt):
    url = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
    headers = {
        "Authorization": f"Bearer {st.secrets['HF_API_TOKEN']}"
    }
    response = requests.post(url, headers=headers, json={"inputs": prompt}, timeout=30)

    if response.status_code == 200:
        try:
            return response.json()[0]["generated_text"]
        except Exception as e:
            return f"⚠️ Kunde inte läsa svaret från modellen: {e}"
    else:
        return f"❌ API-fel ({response.status_code}): {response.text}"

# När användaren klickar på knappen
if st.button("🚀 Generera CV"):
    with st.spinner("AI jobbar..."):
        summary_section = f"Sammanfattning av tidigare CV:\n{st.session_state['cv_summary']}\n" if use_summary else ""

        # Prompten till modellen
        prompt = f'''Du är en professionell CV-skapare. Använd informationen nedan för att skriva ett CV enligt den här mallen:

{name}
Stockholm | kontakt@mail.se | linkedin.com/in/profil

PROFIL
En 2-3 meningars sammanfattning av kandidatens bakgrund och styrkor.

ARBETSLIVSERFARENHET
{role} – Företag, Stad (År–År)
• Punkt 1
• Punkt 2

UTBILDNING
Exempel: Ekonomie kandidat – Handelshögskolan (2016–2019)

KOMPETENSER
• Lista 5–8 färdigheter

INFORMATION FRÅN ANVÄNDAREN:
Jobbannons: {job_text}
Kompetenser: {skills}
Prestationer: {achievements}
{summary_section}

Skriv CV:t i ren text enligt formatet ovan. Använd bara svenska.
'''

        # Anropa AI:n
        generated_cv = call_llama3(prompt)

        # Visa resultat
        st.success("✅ CV genererat!")
        st.markdown("### ✨ Ditt genererade CV:")
        st.code(generated_cv, language='markdown')
