import streamlit as st
import pandas as pd

st.set_page_config(page_title="Jerez Fragance RD — Catálogo", page_icon="🧪", layout="centered")

st.title("🧪 JEREZ FRAGANCE RD")
st.subheader("Esencia de elegancia en cada gota 💧")
st.caption("📍 Tienda Física en Los Alcarrizos, Santo Domingo | 100% Originales")

st.divider()

# Enlace .csv directo de tu Google Sheets
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRZ_gpjbEJM_KcPR5jDowP3c4N4kFbIq7rF3W4ub9ly7GSQKpe5keGMB-4sKw1Y16Q3oigJe63sp4tQ/pub?gid=0&single=true&output=csv"

@st.cache_data(ttl=60)  # Se actualiza solo cada 60 segundos
def cargar_datos():
    df = pd.read_csv(SHEET_URL)
    return df

try:
    df = cargar_datos()

    categoria = st.selectbox(
        "Filtrar por categoría:",
        ["Todos"] + list(df["categoria"].dropna().unique())
    )

    st.write("### 🛍️ Perfumes Disponibles")

    # Filtrar según selección
    if categoria != "Todos":
        df_filtrado = df[df["categoria"] == categoria]
    else:
        df_filtrado = df

    for _, p in df_filtrado.iterrows():
        col1, col2 = st.columns([1, 2])
        
        with col1:
            if pd.notna(p["imagen"]) and str(p["imagen"]).startswith("http"):
                st.image(p["imagen"], use_container_width=True)
            else:
                st.info("📷 Foto no disponible")
            
        with col2:
            st.markdown(f"### {p['nombre']}")
            st.caption(f"**Marca:** {p['marca']} | **Categoría:** {p['categoria']}")
            st.write(f"🧪 **Notas:** {p['notas']}")
            st.markdown(f"💰 **Precio:** `{p['precio']}`")
            
            mensaje_wa = f"Hola, vi en el catálogo web el perfume '{p['nombre']}' y quiero más información."
            url_wa = f"https://api.whatsapp.com/send?phone=18098807994&text={mensaje_wa.replace(' ', '%20')}"
            
            st.link_button("💬 Pedir por WhatsApp", url_wa)
        
        st.divider()

except Exception as e:
    st.error("Cargando catálogo... Si persiste, verifica la hoja de cálculo.")