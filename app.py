import streamlit as st
from PIL import Image

# Crea una barra laterale
with st.sidebar:
    st.title("Seguimi sui Social")
    st.write("Resta aggiornato sui miei test sulla Hyundai Inster:")
    
    # Link ai tuoi canali (sostituisci gli URL con i tuoi veri link)
    st.link_button("YouTube 📺", "https://youtube.com/@mginelli76?si=iuRHNZE4UOnIbivr")
    st.link_button("Instagram 📸", "https://instagram.com/ocramgy/")
    st.link_button("TikTok 🎵", "https://www.tiktok.com/@ocramgy76?lang=en")
    st.link_button("Facebook 📺", "https://facebook.com/marcoginelli")
  
# 1. Carica l'immagine dal tuo repository
image = Image.open('logo MGY social.jpg')

# 2. Visualizzala (puoi regolare la larghezza con width)
st.image(image, width=200)

st.title("⚡ EV CHARGE COST CALCULATOR powered by MGY")
st.write("Real Efficency Calculator - Calcolatore ricarica EV con efficienza reale offerto da MGY")

# 1. Input Capacità Batteria
cap = st.number_input("Capacità Batteria (kWh)", value=49.0, step=1.0)

# 2. Selezione Profilo
profilo = st.selectbox("Type - Tipo di ricarica", 
                      ["Charging Station - Colonnina (92% eff.)", "Home - Casa (85% eff.)"])

# Imposta valori in base al profilo
if "Charging Station - Colonnina" in profilo:
    prezzo_default = 0.81
    eff = 0.92
else:
    prezzo_default = 0.25
    eff = 0.85

# 3. Altri Input
prezzo = st.number_input("Real Price - Inserire Costo reale (€/kWh)", value=prezzo_default, format="%.2f")

col1, col2 = st.columns(2)
with col1:
    inizio = st.number_input("Battery Level Start - Batteria Inizio (%)", value=20, min_value=0, max_value=100)
with col2:
    fine = st.number_input("Battery Level End - Batteria Fine (%)", value=80, min_value=0, max_value=100)

# 4. Calcoli
if st.button("Calculate now - CALCOLA ORA", use_container_width=True):
    if fine <= inizio:
        st.error("La percentuale finale deve essere maggiore!")
    else:
        kwh_netti = ((fine - inizio) / 100) * cap
        kwh_pagati = kwh_netti / eff
        costo = kwh_pagati * prezzo
        
        # Risultati grafici
        st.divider()
        st.metric("Costo Totale", f"€ {costo:.2f}")
        
        st.info(f"""
        **Dettagli Tecnici:**
        - Net Energy - Energia netta: {kwh_netti:.2f} kWh
        - Payed Energy - Energia pagata ({int(eff*100)}% eff): {kwh_pagati:.2f} kWh

        """)












