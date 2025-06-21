import streamlit as st
import requests

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

# Funktion för att anropa Hugging Face API
def call_llama3(prompt):
    url = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
    headers = {
        "Authorization": f"Bearer {st.secrets['HF_API_TOKEN']}"
    }
    response = requests.post(url, headers=headers, json={"inputs": prompt})

    if response.status_code == 200:
        try:
            return response.json()[0]["generated_text"]
        except Exception:
            return response.json()
    else:
        return f"Fel från API: {response.status_code} – {response.text}"

# Knapp för att generera CV
if st.button("🚀 Generera CV"):
    with st.spinner("AI jobbar..."):
        prompt = f"""
Du är en professionell CV-skapare. Använd informationen nedan för att skriva ett CV enligt den här mallen:

---
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

INFORMATION:
Jobbannons: {job_text}
Kompetenser: {skills}
Prestationer: {achievements}

Skriv CV:t i ren text enligt formatet ovan. Använd bara svenska.
"""

        result = call_llama3(prompt)
        st.success("✅ CV genererat!")
        st.markdown("### ✨ Resultat:")
        st.code(result, language="markdown")

        generated_cv = response['choices'][0]['message']['content']
        st.success("✅ Klart!")
        st.markdown("### ✨ Ditt genererade CV:")
        st.code(generated_cv, language='markdown')
