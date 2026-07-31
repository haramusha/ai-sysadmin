import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Wykrywacz logów",page_icon="🪵", layout="centered")

#Konfiguracja API
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

st.title("Wirtualny Asystent ds. Logów AI")

plik = st.file_uploader("Wgraj plik z logami", type=["txt"])

if st.button("Uruchom analizę AI"):
    if plik is not None:
        plik_tekst = plik.read().decode("utf-8")
        with st.spinner('Łączę się z chmurą i szukam dostępnego modelu...'):
            try:
                # 1. Pobieramy listę wszystkich modeli
                dostepne_modele = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]

                sukces = False

                # 2. Próbujemy każdy model po kolei
                for nazwa_modelu in dostepne_modele:
                    try:
                        model = genai.GenerativeModel(nazwa_modelu)
                        prompt_dla_ai = prompt_dla_ai = f"""Jesteś seniorem inżynierii systemów. Przeanalizuj poniższe logi serwera, znajdź w nich błędy i zaproponuj rozwiązanie.

                        WAŻNE ZASADY (MUSISZ ICH BEZWZGLĘDNIE PRZESTRZEGAĆ):
                        1. Wygeneruj CAŁĄ odpowiedź WYŁĄCZNIE w języku polskim (nawet jeśli logi są po angielsku).
                        2. Zwróć TYLKO ostateczny wynik analizy i 3 punkty z rozwiązaniem.
                        3. ZAKAZ tworzenia brudnopisów. NIE PISZ swojego procesu myślowego, notatek typu Self-Correction, sekcji Task ani tłumaczeń. Odpowiedź ma być gotowa do przeczytania przez klienta końcowego.

                        Oto logi do analizy:\n\n{plik_tekst}"""

                        # Próba wygenerowania tekstu
                        odpowiedz = model.generate_content(prompt_dla_ai)

                        # Jeśli doszliśmy tutaj, model zadziałał!
                        st.success(f"Sukces! Aplikacja automatycznie użyła modelu: {nazwa_modelu}")
                        st.write("### Wynik analizy:")
                        st.write(odpowiedz.text)

                        sukces = True
                        break  # Przerywamy pętlę, mamy wynik!

                    except Exception as e:
                        # Jeśli model zwrócił błąd 404 lub inny, ignorujemy go i pętla idzie do kolejnego
                        continue

                if not sukces:
                    st.error("Niestety, żaden z modeli dostępnych dla tego klucza nie zadziałał.")

            except Exception as główny_błąd:
                st.error(f"Problem z połączeniem do Google API: {główny_błąd}")
    else:
        st.warning("Najpierw wpisz jakiś tekst w polu wyżej!")
