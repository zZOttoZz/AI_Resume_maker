import streamlit as st
import openai

st.set_page_config(page_title="AI Resume Optimizer", layout="centered")

st.title("📄 AI Resume Optimizer")
st.markdown("**Ladda upp jobbannonsen och svara på några enkla frågor – vi skapar ett AI-genererat CV i mallformat.**")

# API-nyckel (från .streamlit/secrets.toml)
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Inputs från användaren
job_text = st.text_area("📋 Klistra in jobbannonsen här")
name = st.text_input("👤 Ditt namn")
role = st.text_input("🎓 Din nuvarande roll")
skills = st.text_area("🛠️ Vad är du bra på?")
achievements = st.text_area("🏆 Vad är du mest stolt över?")

if st.button("🚀 Generera CV"):
    with st.spinner("Skapar ditt CV..."):

        prompt = f"""
Du är en professionell CV-skrivare. Använd informationen nedan för att skapa ett CV enligt denna struktur:

---
{name}
Stockholm | kontakt@mail.se | linkedin.com/in/profil

PROFIL
Skriv en 2-3 meningars summering av kandidatens bakgrund, baserat på deras nuvarande roll, prestationer och kompetenser.

ARBETSLIVSERFARENHET
{role} – Företag, Stad (År–År)
• 2–3 prestationer baserat på kandidatens input och jobbannonsen.

UTBILDNING
Exempel: Ekonomie kandidat – Stockholms universitet (2016–2019)

KOMPETENSER
• Lista 5–8 matchande kompetenser från både jobbannons och kandidatens svar.

Jobbannons:
{job_text}

Kandidatens input:
- Kompetenser: {skills}
- Prestationer: {achievements}

Generera CV:t i ren text enligt formatet ovan.
"""

        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        generated_cv = response['choices'][0]['message']['content']
        st.success("✅ Klart!")
        st.markdown("### ✨ Ditt genererade CV:")
        st.code(generated_cv, language='markdown')
