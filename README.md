# AI Resume Optimizer

Detta är en enkel Streamlit-app som genererar ett CV baserat på en jobbannons och dina egna uppgifter. Nu går det även att ladda upp ditt befintliga CV (PDF) för att skapa en kort sammanfattning som kan användas i prompten.

## Kom igång

1. Installera beroenden
   ```bash
   pip install -r requirements.txt
   ```
2. Skapa en `secrets.toml` med din Hugging Face-token:
   ```toml
   HF_API_TOKEN = "din-token-här"
   ```
3. Starta applikationen:
   ```bash
   streamlit run app.py
   ```

## Användning

1. Fyll i formulären med jobbannons, namn, roll, kompetenser och prestationer.
2. Ladda upp ett befintligt CV i PDF-format och klicka på **Sammanfatta CV** för att låta modellen skapa en kort summering.
3. Markera om du vill använda sammanfattningen i prompten och klicka sedan på **Generera CV**.

Det genererade CV:t visas i ren text och kan kopieras direkt.
