import streamlit as st
import pandas as pd

# Configuración inicial para móvil y escritorio
st.set_page_config(
    page_title="Jerez Fragance RD — Catálogo", 
    page_icon="🛍️", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Estilos CSS personalizados (Efecto Treinta: Claro, Limpio, Minimalista)
st.markdown("""
<style>
    /* Fondo limpio claro */
    .stApp {
        background-color: #f8f9fa;
        color: #212529;
    }
    
    /* Header principal */
    .store-header {
        text-align: center;
        padding: 10px 0px 5px 0px;
    }
    .store-title {
        font-size: 1.8rem;
        font-weight: 900;
        letter-spacing: 1px;
        color: #111;
        margin-bottom: 2px;
    }
    .store-info {
        font-size: 0.85rem;
        color: #28a745;
        font-weight: 600;
    }
    .store-address {
        font-size: 0.8rem;
        color: #6c757d;
        margin-bottom: 15px;
    }
    
    /* Estilos de Tarjetas de Productos (Grid 2x2) */
    .product-card {
        background-color: #ffffff;
        border: 1px solid #e9ecef;
        border-radius: 12px;
        padding: 10px;
        text-align: center;
        margin-bottom: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    .product-price {
        font-size: 1.1rem;
        font-weight: 800;
        color: #212529;
        margin-top: 5px;
    }
    .out-of-stock {
        color: #dc3545;
        font-weight: 700;
        font-size: 0.85rem;
    }
    
    /* Botón flotante WhatsApp */
    .floating-wa {
        position: fixed;
        bottom: 20px;
        right: 20px;
        background-color: #25d366;
        color: white;
        border-radius: 50px;
        padding: 12px 20px;
        font-weight: bold;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        z-index: 999;
        text-decoration: none;
    }
</style>
""", unsafe_allow_html=True)

# Encabezado
st.markdown("""
    <div class="store-header">
        <div class="store-title">🛍️ JEREZ FRAGANCE RD</div>
        <div class="store-info">🟢 Abierto · 10:00 a. m. - 6:00 p. m.</div>
        <div class="store-address">📍 Calle 14 #59 Savica, Los Alcarrizos, Santo Domingo</div>
    </div>
""", unsafe_allow_html=True)

# Enlace de tu Google Sheets
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRZ_gpjbEJM_KCpRSjDowP3c4N4kFblq7rF3W4ub9ly7QSQKpe5keGMB-4sKw1Y16Q3olgJe63ap4tQ/pub?gid=0&single=true&output=csv"

@st.cache_data(ttl=5)
def cargar_datos():
    df = pd.read_csv(SHEET_URL)
    df.columns = df.columns.str.strip().str.lower()
    return df

try:
    df = cargar_datos()

    # Buscador principal
    busqueda = st.text_input("", placeholder="🔍 Buscar producto...", label_visibility="collapsed")

    # Filtros por categorías (Estilo botones)
    categorias = ["Ver todos"] + [str(c) for c in df["categoria"].dropna().unique()]
    cat_sel = st.radio("Categorías", categorias, horizontal=True, label_visibility="collapsed")

    # Filtrado dinámico
    df_filtrado = df.copy()
    if cat_sel != "Ver todos":
        df_filtrado = df_filtrado[df_filtrado["categoria"] == cat_sel]
    if busqueda:
        df_filtrado = df_filtrado[df_filtrado["nombre"].astype(str).str.contains(busqueda, case=False, na=False)]

    st.write("")

    # Generar Grid en 2 columnas (igual que la foto)
    cols = st.columns(2)
    for idx, (_, p) in enumerate(df_filtrado.iterrows()):
        col = cols[idx % 2]
        with col:
            with st.container():
                url_img = str(p["imagen"]).strip() if pd.notna(p["imagen"]) else ""
                if url_img.startswith("http"):
                    st.image(url_img, use_container_width=True)
                else:
                    st.caption("📷 Foto no disponible")
                
                st.markdown(f"**{p['nombre']}**")
                
                # Manejar precios o estado "Agotado"
                precio_str = str(p['precio'])
                if "agotado" in precio_str.lower():
                    st.markdown("<p class='out-of-stock'>Producto agotado</p>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<p class='product-price'>{precio_str}</p>", unsafe_allow_html=True)
                
                # Botón individual de pedido
                msg = f"Hola Jerez Fragance RD! Me interesa consultar por '{p['nombre']}'"
                url_wa = f"https://api.whatsapp.com/send?phone=18098807994&text={msg.replace(' ', '%20')}"
                st.link_button("💬 Pedir", url_wa, use_container_width=True)
                st.markdown("---")

except Exception as e:
    st.error("Cargando catálogo... Asegúrate de publicar la hoja de Google Sheets en la web.")
