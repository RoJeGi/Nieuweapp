
import streamlit as st
import pandas as pd

st.title("Besteladvies App – Per Artikel en Week")

@st.cache_data
def load_data():
    df = pd.read_excel("Verkoopanalyse_met_besteladvies_correct.xlsx")
    return df

df = load_data()

# Keuze artikelnummer
artikel = st.selectbox("Kies artikelnummer:", sorted(df['Referentie'].dropna().unique()))

# Invoer huidige week
huidige_week = st.number_input("Voer huidige week in:", min_value=1, max_value=52, value=15, step=1)

# Filter op artikel
filtered = df[df['Referentie'] == artikel].copy()

# Bereken dynamisch het besteladvies
filtered['Bestellen'] = (
    (filtered['Bestelweek'] == huidige_week) &
    (filtered['Aantal geleverd'] > filtered['Aanwezige voorraad'])
).map({True: 'ja', False: 'nee'})

# Toon resultaten
result = filtered[filtered['Huidige week'] == huidige_week]

if not result.empty:
    st.subheader("Resultaten voor artikel:")
    st.dataframe(result[['Week', 'Aantal geleverd', 'Aanwezige voorraad', 'Levertijd in weken',
                         'Bestelweek', 'Bestellen']])
    advies = result['Bestellen'].iloc[0]
    st.markdown(f"### Bestellen: **{advies.upper()}**")
else:
    st.warning("Geen gegevens gevonden voor dit artikel in deze week.")
