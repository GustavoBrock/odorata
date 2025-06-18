import streamlit as st
import pandas as pd
import re
import itertools
import io

# 🔹 Configuração da Página
st.set_page_config(page_title="Odorata", layout="wide")

# 🔹 Carregar Estilos Externos (Correção do erro de codificação)
with open("style_3.6.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# 🔹 Criar Barra Lateral para Navegação com Ícones Unicode
st.sidebar.markdown('<div class="sidebar-logo-container">', unsafe_allow_html=True)
st.sidebar.image("image.png", width=200)  # Carregar corretamente a imagem da logo
st.sidebar.markdown('</div>', unsafe_allow_html=True)


# Criar opções com emojis diretamente no texto
menu_opcoes = {
    "🏡 Início": "home",
    "🌿 Gerador de Blends": "blends",
    "📚 Lista de Plantas": "plantas",
    "🛍️ Loja": "loja",
    "👥 Contato & Sobre": "contato"
}

# Criar menu lateral com os emojis destacados
pagina_atual = st.sidebar.radio("Escolha uma seção:", list(menu_opcoes.keys()))

# 🔹 Criar espaço abaixo da sidebar para o conteúdo
st.markdown('<div class="content">', unsafe_allow_html=True)

# 🔹 Criar conteúdo para cada página com a fonte "DM Serif Display"
if menu_opcoes[pagina_atual] == "home":
    st.markdown('<div class="page-title">Bem vindo a Odorata</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Transforme a arte da fitoterapia em experiências únicas! </div>', unsafe_allow_html=True)
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

elif menu_opcoes[pagina_atual] == "blends":
    st.markdown('<div class="page-title">Gerador de Blends</div>', unsafe_allow_html=True)
    
    # 🔹 Carregar a planilha de dados
    file_path = "Tabela_Plantas_Ansiedade_Desempenho_ExpansaoTotal.xlsx"
    df_dict = pd.read_excel(file_path, sheet_name=None)

    # 🔹 Identificar e carregar as abas
    def encontrar_aba(nome, df_dict):
        for aba in df_dict.keys():
            if nome.lower() in aba.lower():
                return aba
        return None

    tabela_compatibilidade = encontrar_aba("compatibilidade", df_dict)
    tabela_classificacao = encontrar_aba("Classificação Expandida", df_dict)

    if tabela_compatibilidade and tabela_classificacao:
        df_compatibilidade = df_dict[tabela_compatibilidade]
        df_classificacao = df_dict[tabela_classificacao]
    else:
        st.error("⚠️ Erro ao carregar a planilha.")
        st.stop()

    # 🔹 Normalizar os dados da planilha
    df_compatibilidade.columns = [re.sub(r"\s*\(.*?\)", "", str(col)).strip().lower() for col in df_compatibilidade.columns]
    df_compatibilidade.iloc[:, 0] = df_compatibilidade.iloc[:, 0].str.lower().str.strip()
    df_compatibilidade = df_compatibilidade.fillna(0)

    df_classificacao.columns = [col.lower().strip() for col in df_classificacao.columns]
    df_classificacao["nome da planta"] = df_classificacao["nome da planta"].str.lower().str.strip()

    # 🔹 Obter lista real de temperamentos da planilha
    temperamentos_disponiveis = df_classificacao["temperamento insônia"].dropna().unique().tolist()
    temperamentos_disponiveis.insert(0, "Todos")  # Adiciona opção "Todos"

    # 🔹 Apenas garantir que o código acesse o nome correto
    if "classificação lunae-solis" not in df_classificacao.columns:
        st.error("⚠️ A coluna 'classificação lunae-solis' não foi encontrada na planilha.")
        st.write("Colunas disponíveis:", df_classificacao.columns.tolist())  # Lista para depuração
        st.stop()

    # 🔹 Criar interface centralizada
    st.subheader("🔍 Escolha os efeitos desejados:")

    efeitos_desejados = st.text_input("Digite os efeitos (ex: Calmante, Estimulante)").strip().lower()
    Lunae_Solis = st.selectbox("Selecione Lunae-Solis:", ["Todos", "Lunae", "Solis"])
    temperamento = st.selectbox("Selecione o Temperamento:", ["Todos", "Sanguíneo", "Fleumático", "Colérico", "Melancólico"])
    evitar_contra = st.checkbox("Evitar Contraindicações")


    if st.button("Gerar Blend"):
        if not efeitos_desejados:
            st.warning("⚠️ Digite pelo menos um efeito.")
        else:
            lista_efeitos = [efeito.strip() for efeito in efeitos_desejados.split(",")]

            # 🔹 Filtrar plantas com base nos critérios
            df_filtrado = df_classificacao[
                df_classificacao["efeito primário"].str.contains("|".join(lista_efeitos), na=False, case=False) |
                df_classificacao["efeito secundário"].str.contains("|".join(lista_efeitos), na=False, case=False)
            ]

            if df_filtrado.empty:
                st.error(f"⚠️ Nenhuma planta encontrada para os efeitos desejados: {', '.join(lista_efeitos)}")
            else:
                st.success(f"✅ Número total de plantas encontradas: {len(df_filtrado)}")

                blends_completos = []

                # 🔹 Função para calcular compatibilidade
                def calcular_compatibilidade(nome1, nome2):
                    if nome1 in df_compatibilidade.iloc[:, 0].values and nome2 in df_compatibilidade.columns:
                        return df_compatibilidade.loc[df_compatibilidade.iloc[:, 0] == nome1, nome2].values[0]
                    return 0

                # 🔹 Função para obter informações da planta
                def obter_info_planta(nome):
                    info = df_classificacao[df_classificacao["nome da planta"] == nome]
                    if not info.empty:
                        info = info.iloc[0]
                        return {
                            "Lunae_Solis": info["classificação lunae-solis"],
                            "temperamento": info["temperamento insônia"],
                            "contraindicações": info["contraindicações"].split(", ")
                        }
                    return {"Lunae_Solis": "", "temperamento": "", "contraindicações": []}

                # 🔹 Gerar blends de 2 e 3 plantas
                for num_plantas in [2, 3]:
                    for combinacao in itertools.combinations(df_filtrado["nome da planta"], num_plantas):
                        nomes = sorted(combinacao)
                        compatibilidade = sum(calcular_compatibilidade(nomes[i], nomes[j]) for i in range(len(nomes)) for j in range(i+1, len(nomes))) / (len(nomes) * (len(nomes)-1) / 2)

                        if compatibilidade >= 4:
                            infos = [obter_info_planta(nome) for nome in nomes]

                            # 🔹 Aplicar filtros Yin-Yang e Temperamento
                            if (Lunae_Solis != "Todos" and not all(info["lunae_solis"] == Lunae_Solis for info in infos)) or \
                               (temperamento != "Todos" and not all(info["temperamento"] == temperamento for info in infos)):
                                continue

                            blends_completos.append({
                                "Planta 1": nomes[0],
                                "Planta 2": nomes[1] if len(nomes) > 1 else "-",
                                "Planta 3": nomes[2] if len(nomes) > 2 else "-",
                                "Compatibilidade Média": round(compatibilidade, 2),
                                "Lunae-Solis": ", ".join(sorted(set(info["Lunae_Solis"] for info in infos))),
                                "Temperamento": ", ".join(sorted(set(info["temperamento"] for info in infos))),
                                "Contraindicações": ", ".join(sorted(set(sum([info["contraindicações"] for info in infos], []))))
                            })

                if blends_completos:
                    df_resultado = pd.DataFrame(blends_completos)
                    st.markdown('<div class="page-subtitle">💡 Blends sugeridos:</div>', unsafe_allow_html=True)
                    # 🔹 Criar estilos CSS personalizados
                    custom_css = """
                    <style>
                        .scroll-container {
                            max-height: 400px; /* Altura máxima */
                            overflow-y: auto; /* Ativa rolagem vertical */
                            border-radius: 10px; /* Bordas arredondadas */
                            border: 2px solid #000000; /* Borda preta */
                            padding: 10px;
                            background-color: #f5e1c8; /* Fundo */
                        }
                        
                        .scroll-container table {
                            width: 100%;
                            border-collapse: separate;
                            border-spacing: 0px;
                            border-radius: 10px;
                        }

                        /* Estilização das células do cabeçalho */
                        .scroll-container th {
                            background-color: #4b5a35; /* Fundo verde escuro */
                            color: #FFFFFF; /* Texto branco */
                            border: 2px solid #000000; /* Borda preta */
                            padding: 8px;
                        }

                        /* Estilização das células da tabela */
                        .scroll-container td {
                            background-color: #bcc494; /* Fundo bege claro */
                            color: #000000; /* Texto preto */
                            border: 2px solid #000000; /* Borda preta */
                            padding: 8px;
                        }

                        /* Remove bordas duplas */
                        .scroll-container table, .scroll-container th, .scroll-container td {
                            border-collapse: collapse;
                        }
                    </style>
                    """

                    # 🔹 Aplicar CSS personalizado
                    st.markdown(custom_css, unsafe_allow_html=True)

                    # 🔹 Criar a tabela estilizada
                    styled_table = df_resultado.to_html(index=False, escape=False)

                    # 🔹 Exibir a tabela com a rolagem dentro de um `<div>`
                    st.markdown(
                        f"""
                        <div class="scroll-container">
                            {styled_table}
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )

                    # 🔹 Criar botão para download do Excel
                    def converter_para_excel(df):
                        output = io.BytesIO()
                        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                            df.to_excel(writer, index=False, sheet_name="Blends")
                        processed_data = output.getvalue()
                        return processed_data

                    st.markdown(
                            """
                            <style>
                                .stDownloadButton>button {
                                    background-color: #4b5a35 !important; /* Cor de fundo */
                                    color: #FFFFFF !important; /* Cor do texto */
                                    border-radius: 10px !important; /* Bordas arredondadas */
                                    border: 2px solid #000000 !important; /* Borda preta */
                                    padding: 8px 16px !important; /* Ajuste do padding interno */
                                    font-weight: bold !important; /* Deixa o texto em negrito */
                                }
                                
                                .stDownloadButton>button:hover {
                                    background-color: #3b4a25 !important; /* Cor ao passar o mouse */
                                    color: #FFFFFF !important; /* Mantém o texto branco */
                                }
                            </style>
                            """,
                            unsafe_allow_html=True
                        )


                    # 🔹 Criar botões de download
                    st.markdown('<div class="page-subtitle">Baixar Blends</div>', unsafe_allow_html=True)

                    col1, = st.columns(1)

                    with col1:
                        st.download_button(
                            label=".xlsx",
                            data=converter_para_excel(df_resultado),
                            file_name="blends_sugeridos.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )

         

                else:
                    st.error("⚠️ Nenhum blend compatível foi encontrado.")

elif menu_opcoes[pagina_atual] == "plantas":
    st.markdown('<div class="page-title">Lista de Plantas</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Aqui nós temos uma lista com as plantas usadas em nosso gerador de blends</div>', unsafe_allow_html=True)

elif menu_opcoes[pagina_atual] == "loja":
    st.markdown('<div class="page-title">Loja</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Aqui você pode explorar e comprar blends exclusivos.</div>', unsafe_allow_html=True)

elif menu_opcoes[pagina_atual] == "contato":
    st.markdown('<div class="page-title">Contato & Sobre</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Fale conosco e saiba mais sobre a Odorata.</div>', unsafe_allow_html=True)

