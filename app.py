import streamlit as st

st.set_page_config(page_title="Jerez Fragance RD — Catálogo", page_icon="🧪", layout="centered")

st.title("🧪 JEREZ FRAGANCE RD")
st.subheader("Esencia de elegancia en cada gota 💧")
st.caption("📍 Tienda Física en Los Alcarrizos, Santo Domingo | 100% Originales")

st.divider()

categoria = st.selectbox(
    "Filtrar por categoría:",
    ["Todos", "Masculinos", "Femeninos", "Unisex", "Decants / Muestras"]
)

# Lista con enlaces a imágenes reales (puedes usar enlaces de PostImage, Imgur o Unsplash)
perfumes = [
    {
        "nombre": "Club de Nuit Intense Man",
        "marca": "Armaf",
        "categoria": "Masculinos",
        "precio": "RD$ 3,500",
        "notas": "Cítrico, Amaderado, Cueros",
        "imagen": "https://images.unsplash.com/photo-1594035910387-fea47794261f?w=500"
    },
    {
        "nombre": "Y EDP",
        "marca": "Yves Saint Laurent",
        "categoria": "Masculinos",
        "precio": "RD$ 7,200",
        "notas": "Manzana verde, Salvia, Habatonka",
        "imagen": "https://images.unsplash.com/photo-1523293182086-7651a899d37f?w=500"
    },
    {
        "nombre": "Decant / Muestra 10ml - Sauvage Elixir",
        "marca": "Dior",
        "categoria": "Decants / Muestras",
        "precio": "RD$ 950",
        "notas": "Especiado, Lavanda, Maderas",
        "imagen": "https://images.unsplash.com/photo-1588405748880-12d1d2a59f75?w=500"
    }
]

st.write("### 🛍️ Perfumes Disponibles")

for p in perfumes:
    if categoria == "Todos" or p["categoria"] == categoria:
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.image(p["imagen"], use_container_width=True)
            
        with col2:
            st.markdown(f"### {p['nombre']}")
            st.caption(f"**Marca:** {p['marca']} | **Categoría:** {p['categoria']}")
            st.write(f"🧪 **Notas:** {p['notas']}")
            st.markdown(f"💰 **Precio:** `{p['precio']}`")
            
            mensaje_wa = f"Hola, vi en el catálogo web el perfume '{p['nombre']}' y quiero más información."
            url_wa = f"https://api.whatsapp.com/send?phone=18098807994&text={mensaje_wa.replace(' ', '%20')}"
            
            st.link_button("💬 Pedir por WhatsApp", url_wa)
        
        st.divider()