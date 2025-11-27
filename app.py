import streamlit as st
import pandas as pd
import os

# --- Konfiguration ---
CSV_DATEI = 'artikel.csv'
SEPARATOR = ';'

st.set_page_config(page_title="Quick-Copy Artikel", page_icon="📋")

# --- CSS für "sauberes" Aussehen (optional) ---
# Versteckt das Hamburger-Menü und den Footer für einen App-Look
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# --- Funktionen ---
@st.cache_data
def lade_daten():
    if not os.path.exists(CSV_DATEI):
        return None
    try:
        # dtype=str hält die Nummern als Text (wichtig für führende Nullen)
        df = pd.read_csv(CSV_DATEI, sep=SEPARATOR, dtype=str)
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"Fehler in der CSV: {e}")
        return None

# --- Hauptanwendung ---
def main():
    st.subheader("🔎 Artikel-Scanner")
    
    df = lade_daten()

    if df is None:
        st.error(f"Datei '{CSV_DATEI}' fehlt im Repository.")
        st.stop()

    # Eingabefeld (Drücke Enter zum Suchen)
    suche = st.text_input("Artikelnummer eingeben:", placeholder="Nummer tippen und Enter drücken...")

    if suche:
        suche_bereinigt = suche.strip()
        
        # Suche nach exaktem Match
        ergebnis = df[df['Artikelnummer'] == suche_bereinigt]

        if not ergebnis.empty:
            # Den Namen holen
            artikel_name = ergebnis.iloc[0]['Artikelname']
            
            st.success("Gefunden! Klicke rechts auf das Symbol zum Kopieren:")
            
            # TRICK: st.code zeigt den Text in einer Box mit Kopier-Button
            st.code(artikel_name, language=None)
            
        else:
            st.error(f"❌ Nichts gefunden für: {suche_bereinigt}")

if __name__ == "__main__":
    main()
