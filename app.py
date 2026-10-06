import streamlit as st
import pandas as pd

# 1. Configuración de pantalla completa y título del navegador
st.set_page_config(
    page_title="Jerez Fragance RD — Catálogo VIP", 
    page_icon="✨", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Estilos CSS personalizados para estética de lujo
st.markdown("""
<style>
    /* Fondo oscuro estilizado */
    .stApp {
        background-color: #0e1117;
    }
    
    /* Encabezado principal */
    .main-header {
        text-align: center;
        padding: 10px 0px 20px 0px;
    }
    .main-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(45deg, #f3ec78, #af4261);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
    }
    .sub-title {
        color: #b0b3b8;
        font-size: 1.1rem;
        font-style: italic;
    }
    
    /* Botón de WhatsApp estilizado */
    div.stButton > button {
        background-color: #25D366 !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 25px !important;
        border: none !important;
        padding: 10px 20px !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
    }
    div.stButton > button:hover {
        background-color: #128C7E !important;
        transform: scale(1.02);
    }
</style>
""", unsafe_allow_html=True)

# 3. Banner superior con identidad de marca
st.markdown("""
    <div class="main-header">
        <h1 class="main-title">✨ JEREZ FRAGANCE RD ✨</h1>
        <p class="sub-title">Esencia de elegancia en cada gota 💧</p>
        <p style="color: #888; font-size: 0.9rem;">📍 Tienda Física en Los Alcarrizos, Santo Domingo | 100% Originales 🇩🇴</p>
    </div>
""", unsafe_allow_html=True)

st.divider()

# URL de la hoja de cálculo de Google Sheets publicada como CSV
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRZ_gpjbEJM_KCpRSjDowP3c4N4kFblq7rF3W4ub9ly7QSQKpe5keGMB-4sKw1Y16Q3olgJe63ap4tQ/pub?gid=0&single=true&output=csv"

@st.cache_data(ttl=10)
def cargar_datos():
    df = pd.read_csv(SHEET_URL)
    df.columns = df.columns.str.strip().str.lower()
    return df

try:
    df = cargar_datos()

    # Barra superior con Buscador y Filtro por categoría
    col_busqueda, col_filtro = st.columns([2, 1])
    
    with col_busqueda:
        busqueda = st.text_input("🔍 Buscar por perfume o marca:", placeholder="Ej. Club de Nuit, Dior, Armaf...")
        
    with col_filtro:
        categorias = ["Todas"] + [str(c) for c in df["categoria"].dropna().unique()]
        cat_seleccionada = st.selectbox("🏷️ Categoría:", categorias)

    # Filtrar catálogo dinámicamente
    df_filtrado = df.copy()
    
    if cat_seleccionada != "Todas":
        df_filtrado = df_filtrado[df_filtrado["categoria"] == cat_seleccionada]
        
    if busqueda:
        df_filtrado = df_filtrado[
            df_filtrado["nombre"].astype(str).str.contains(busqueda, case=False, na=False) |
            df_filtrado["marca"].astype(str).str.contains(busqueda, case=False, na=False)
        ]

    st.markdown(f"Mostrando **{len(df_filtrado)}** perfumes disponibles:")
    st.write("")

    # Generación de tarjetas para cada producto
    for _, p in df_filtrado.iterrows():
        with st.container():
            c1, c2 = st.columns([1, 2], gap="large")
            
            with c1:
                url_img = str(p["imagen"]).strip() if pd.notna(p["imagen"]) else ""
                if url_img.startswith("http"):
                    st.image(url_img, use_container_width=True)
                else:
                    st.info("📷 Foto no disponible")
                    
            with c2:
                st.markdown(f"## {p['nombre']}")
                st.markdown(f"**Marca:** `{p['marca']}` | **Categoría:** `{p['categoria']}`")
                st.write(f"🧪 **Notas Olfativas:** {p['notas']}")
                st.markdown(f"### 💰 `{p['precio']}`")
                
                # Mensaje dinámico para WhatsApp
                msg = f"Hola Jerez Fragance RD! 👋 Me interesa información sobre el perfume '{p['nombre']}' ({p['precio']})."
                url_wa = f"https://api.whatsapp.com/send?phone=18098807994&text={msg.replace(' ', '%20')}"
                
                st.link_button("💬 Pedir por WhatsApp", url_wa)
                
            st.divider()

except Exception as e:
    st.error("Cargando catálogo... Si persiste el mensaje, verifica que la hoja de Google Sheets esté pública.")
