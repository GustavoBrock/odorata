import streamlit as st
import pandas as pd
import re
import itertools

# 🔹 Configuração da Página
st.set_page_config(page_title="Odorata - Herbal Tea Generator", layout="wide")

# 🔹 Estilos Visuais Melhorados
st.markdown("""
    <style>
        /* Esconde a tarja "Deploy" no canto superior */
        header {visibility: hidden;}

        /* Define a cor de fundo da página */
        .stApp {
            background-color: #E8E5D8 !important;
        }

        /* Mantém a barra superior fixa */
        .navbar {
            background-color: #4b5a35;
            padding: 15px;
            text-align: center;
            border-radius: 10px;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.2);
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            z-index: 1000;
            display: flex;
            justify-content: center;
            gap: 30px;
        }

        .navbar a {
            color: #E8E5D8;
            text-decoration: none;
            font-size: 22px;
            font-weight: bold;
            display: inline-flex;
            align-items: center;
            transition: color 0.3s ease-in-out;
        }

        .navbar a:hover {
            color: #d1cfc7;
        }

         .navbar img {
            width: 28px; /* Aumentamos o tamanho dos ícones */
            margin-right: 12px;
        }

       /* Ajusta o espaçamento do conteúdo para evitar sobreposição com a barra fixa */
        .content {
            padding-top: 110px; /* Ajustado para compensar o aumento da barra */
        }

        .header {
            text-align: center;
            font-size: 50px;
            font-family: 'DM Serif Display', serif;
            font-weight: bold;
            color: #4b5a35;
            padding-top: 10px;
        }

        .subheader {
            text-align: center;
            font-size: 22px;
            color: #5b7a58;
        }

        .separator {
            width: 100%;
            height: 2px;
            background-color: #4b5a35;
            margin: 10px auto;
        }

        .container {
            padding: 15px;
            background-color: #4b5a35;
            opacity: 1.0;
            border-radius: 15px;
            box-shadow: 3px 3px 10px rgba(0, 0, 0, 1);
            margin: 10px auto;
            width: 50%;
            text-align: left;
            color: #E8E5D8;
        }

        /* Corrige a cor dos botões */
        .stButton>button {
            background-color: #4b5a35 !important;
            color: #E8E5D8 !important;
            font-size: 5px;
            border-radius: 10px;
            padding: 10px;
            width: 100%;
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
            border: none !important;
        }

        .stButton>button:hover {
            background-color: #3b4a28 !important;
        }
        
        h3{
            text-align: center;
            }
            
    </style>
""", unsafe_allow_html=True)

# 🔹 Barra de Navegação Superior Fixa com Ícones Minimalistas (Carregando Online para Evitar Erros de Caminho)
st.markdown("""
    <div class="navbar">
        <a href="?page=home">
            <img src="https://cdn-icons-png.flaticon.com/128/7299/7299462.png"> Início
        </a>
        <a href="?page=blends">
            <img src="https://cdn-icons-png.flaticon.com/128/5303/5303997.png"> Gerador de Blends
        </a>
        <a href="?page=plantas">
            <img src="https://cdn-icons-png.flaticon.com/128/3812/3812789.png"> Lista de Plantas
        </a>
        <a href="?page=loja">
            <img src="https://cdn-icons-png.flaticon.com/128/1992/1992740.png"> Loja
        </a>
        <a href="?page=contato">
            <img src="https://cdn-icons-png.flaticon.com/128/4187/4187213.png"> Contato & Sobre
        </a>
    </div>
""", unsafe_allow_html=True)

# 🔹 Espaço para evitar sobreposição com a barra fixa
st.markdown('<div class="content">', unsafe_allow_html=True)

# 🔹 Criar uma linha de colunas vazias para centralizar o logo corretamente
col1, col2, col3 = st.columns([5, 5.5, 1])
with col2:
    st.image("image.png", width=150)  # Carregar corretamente a imagem do logo

# 🔹 Cabeçalho Principal
st.markdown('<div class="header">Odorata - Herbal Tea Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="subheader">Transforme a arte da fitoterapia em experiências únicas! </div>', unsafe_allow_html=True)

# 🔹 Linha Divisória
st.markdown('<div class="separator"></div>', unsafe_allow_html=True)

# 🔹 Seções Explicativas
st.markdown("""
    <div class="container">
        <h3>O que é a Odorata?</h3>
        <p>A <b>Odorata</b> é uma experiência inovadora que combina a tradição da fitoterapia com tecnologia para criar blends de chás personalizados.
            Aqui você aprenderá sobre como escolher os melhores chás para o seu biotipo e assim acabar com a ideia de que os fitoterápicos funcionam apenas como placebo.</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="container">
        <h3>Como Funciona?</h3>
        <p>Nosso sistema utiliza uma <b>base de dados científica</b> para sugerir as melhores combinações de ervas com base nos seus efeitos desejados.</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="container">
        <h3>Benefícios dos Blends</h3>
        <p><b>Relaxante:</b> Perfeito para aliviar o estresse e promover o sono.</p>
        <p><b>Energizante:</b> Estimula a mente e aumenta a disposição.</p>
        <p><b>Digestivo:</b> Auxilia na digestão e melhora o metabolismo.</p>
    </div>
""", unsafe_allow_html=True)

# 🔹 Botão para Acessar o Gerador de Blends
st.markdown('<div style="text-align: center; margin-top: 20px;">', unsafe_allow_html=True)
if st.button("✨ Criar Meu Blend Agora"):
    st.switch_page("🍵 Gerador de Blends")  # Levar para a página do gerador
st.markdown('</div>', unsafe_allow_html=True)

# 🔹 Fechar o espaço de correção da barra fixa
st.markdown('</div>', unsafe_allow_html=True)

