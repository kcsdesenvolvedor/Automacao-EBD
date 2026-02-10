import streamlit as st
import os
from scraper import fetch_lesson_data
from image_gen import generate_card

# Page Config
st.set_page_config(page_title="EBD Automation", page_icon="📖", layout="centered")

st.title("📖 EBD Automation Tool")
st.markdown("Gerador de posts para a Escola Bíblica Dominical (Betel)")

# Sidebar for Inputs
with st.sidebar:
    st.header("Configurações")
    professor_name = st.text_input("Nome do Professor", value="Pr. Kleber")
    santa_ceia = st.checkbox("Culto de Santa Ceia?", value=False)
    
    st.info("Se for Santa Ceia, o aviso de Café da Manhã não será exibido.")

# Main Area
if st.button("🔍 Buscar Dados da Lição"):
    with st.spinner("Buscando dados no blog..."):
        data = fetch_lesson_data()
        
    if data:
        st.session_state['lesson_data'] = data
        st.success(f"Lição {data['lesson_number']} encontrada!")
    else:
        st.error("Não foi possível encontrar a lição. Verifique o blog.")

# Display Data if Fetched
if 'lesson_data' in st.session_state:
    data = st.session_state['lesson_data']
    
    st.subheader("Dados Encontrados:")
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Tema", value=data['theme'], disabled=True)
    with col2:
        st.text_input("Hinos", value=data['hymns'], disabled=True)
        
    st.markdown("---")
    
    # Generate Image Button
    if st.button("🎨 Gerar Imagem"):
        has_breakfast = not santa_ceia
        
        with st.spinner("Gerando imagem..."):
            success = generate_card(data, professor_name, has_breakfast)
            
        if success:
            image_path = os.path.join("output", f"ebd_licao_{data['lesson_number']}.png")
            st.image(image_path, caption="Imagem Gerada", use_column_width=True)
            
            # Download Button
            with open(image_path, "rb") as file:
                btn = st.download_button(
                    label="📥 Baixar Imagem PNG",
                    data=file,
                    file_name=f"ebd_licao_{data['lesson_number']}.png",
                    mime="image/png"
                )
        else:
            st.error("Erro ao gerar a imagem. Verifique o template.")
