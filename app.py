import streamlit as st
from PIL import Image

with st.sidebar:
    st.title("Seguimi sui Social")
    st.write("Resta aggiornato sui miei test sulla Hyundai Inster:")
    st.link_button("YouTube", "https://youtube.com/@mginelli76?si=iuRHNZE4UOnIbivr")
    st.link_button("Instagram", "https://instagram.com/ocramgy/")
    st.link_button("TikTok", "https://www.tiktok.com/@ocramgy76?lang=en")
    st.link_button("Facebook", "https://facebook.com/marcoginelli")

try:
    image = Image.open('logo MGY social.jpg')
    st.image(image, width=200)
except:
    pass

st.title("EV CHARGE COST & TIME CALCULATOR powered by MGY")
st.write("Real Efficiency & Time Calculator - Calcolatore ricarica EV con efficienza e tempi reali offerto da MGY")

cap = st.number_input("Capacita Batteria (kWh)", value=49.0, step=1.0)

# Menu unico con tutti i profili richiesti
opzioni_profilo = [
    "Domestica 6A (~1.38 kW) - Eff. 85.5%",
    "Domestica 8A (~1.84 kW) - Eff. 89.1%",
    "Domestica 10A (~2.30 kW) - Eff. 91.3% (Schuko)",
    "Domestica 12A (~2.76 kW) - Eff. 92.7% (Benchmark MGY)",
    "Domestica 16A (~3.70 kW) - Eff. 92.7% (Limite contatore 3 kW)",
    "Domestica/Wallbox 32A (~7.40 kW) - Eff. 92.0% (Contatore 6+ kW)",
    "Pubblica Standard 16A Trifase (~11.00 kW) - Eff. 92.0%",
    "Pubblica Accelerata 32A Trifase (~22.00 kW) - Eff. 92.0%",
    "Fast DC (50 kW) - Eff. 95.0%",
    "Ultra-Fast DC (100 kW) - Eff. 95.0%",
    "Ultra-Fast DC (150+ kW) - Eff. 95.0%"
]

profilo = st.selectbox("Seleziona il tipo di ricarica", opzioni_profilo, index=3)

# Mappatura dati tecnici di default basati sulla scelta
if "6A" in profilo:
    kw, eff, prezzo_def = 1.38, 0.855, 0.192
elif "8A" in profilo:
    kw, eff, prezzo_def = 1.84, 0.891, 0.192
elif "10A" in profilo:
    kw, eff, prezzo_def = 2.30, 0.913, 0.192
elif "12A" in profilo:
    kw, eff, prezzo_def = 2.76, 0.927, 0.192
elif "16A (~3.7" in profilo:
    kw, eff, prezzo_def = 3.70, 0.927, 0.192
elif "32A (~7.4" in profilo:
    kw, eff, prezzo_def = 7.40, 0.920, 0.192
elif "11.00 kW" in profilo:
    kw, eff, prezzo_def = 11.00, 0.920, 0.65
elif "22.00 kW" in profilo:
    kw, eff, prezzo_def = 22.00, 0.920, 0.69
elif "50 kW" in profilo:
    kw, eff, prezzo_def = 50.00, 0.950, 0.85
elif "100 kW" in profilo:
    kw, eff, prezzo_def = 100.00, 0.950, 0.89
else: # 150+ kW
    kw, eff, prezzo_def = 150.00, 0.950, 0.89

if "ultimo_profilo" not in st.session_state or st.session_state.ultimo_profilo != profilo:
    st.session_state.ultimo_profilo = profilo
    st.session_state.prezzo_input = prezzo_def

prezzo = st.number_input(
    "Real Price - Inserire Costo reale (EUR/kWh)",
    value=st.session_state.prezzo_input,
    format="%.3f",
    key="prezzo_input"
)

col1, col2 = st.columns(2)
with col1:
    inizio = st.number_input("Battery Level Start (%)", value=20, min_value=0, max_value=100)
with col2:
    fine = st.number_input("Battery Level End (%)", value=80, min_value=0, max_value=100)

if st.button("Calculate now - CALCOLA ORA", use_container_width=True):
    if fine <= inizio:
        st.error("La percentuale finale deve essere maggiore!")
    else:
        # Calcolo energia e costi fisso per tutti
        kwh_netti = ((fine - inizio) / 100) * cap
        kwh_pagati = kwh_netti / eff
        costo = kwh_pagati * prezzo

        minuti_totali = 0
        kw_reali = kw * eff

        # Limitazione fisica di bordo dell'auto per la ricarica AC Pubblica (Max 11 kW per Inster)
        kw_ricarica_effettiva = kw
        if "Pubblica Accelerata 32A" in profilo:
            kw_ricarica_effettiva = 11.00  # L'auto accetta massimo 11 kW in AC anche su colonnine da 22 kW
            kw_reali = 11.00 * eff

        # Calcolo dinamico minuto per minuto basato sui kW effettivi immessi
        for p in range(int(inizio), int(fine)):
            kwh_singolo_percento = cap / 100
            
            # Gestione della curva di rallentamento protettivo sopra l'80% e l'85%
            if p >= 85:
                frazione_potenza = 0.38 if kw_ricarica_effettiva <= 22.0 else 0.22
            elif p >= 80:
                frazione_potenza = 0.65 if kw_ricarica_effettiva <= 22.0 else 0.45
            else:
                frazione_potenza = 1.0
                
            kw_istantanei = kw_ricarica_effettiva * frazione_potenza * eff
            ore_per_un_percento = kwh_singolo_percento / kw_istantanei
            minuti_totali += ore_per_un_percento * 60

        minuti_totali = int(round(minuti_totali))
        
        # CORREZIONE BUG: Variabili italianizzate e coerenti con la definizione iniziale
        ore = minuti_totali // 60
        minuti = minuti_totali % 60

        st.divider()
        
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Costo Totale", f"EUR {costo:.2f}")
        with c2:
            st.metric("Tempo Stimato", f"{ore}h {minuti}m")

        st.info(
            "Dettagli Tecnici:\n" +
            "- Modalità: " + profilo + "\n" +
            "- Energia netta erogata: " + str(round(kwh_netti, 2)) + " kWh\n" +
            "- Energia pagata (con perdite): " + str(round(kwh_pagati, 2)) + " kWh\n" +
            "- Potenza reale di picco: " + str(round(kw_reali, 2)) + " kW"
        )
