import streamlit as st
import pandas as pd
import re
import itertools

# 🔹 Configuração da Página
st.set_page_config(page_title="Odorata", layout="wide")

# 🔹 Fonte personalizada semelhante à "Quilin"
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&display=swap');

        body {
            background-color: #e8e5d8;
            font-family: 'Arial', sans-serif;
        }
        .header {
            text-align: center;
            font-size: 50px;
            font-family: 'DM Serif Display', serif;
            font-weight: bold;
            color: #3b5d42;
            padding-top: 10px;
        }
        .subheader {
            text-align: center;
            font-size: 22px;
            color: #5b7a58;
        }
        .separator {
            width: 80%;
            height: 2px;
            background-color: #3b5d42;
            margin: 15px auto;
        }
        .container {
            padding: 20px;
            background-color: #ffffff;
            border-radius: 15px;
            box-shadow: 4px 4px 15px rgba(0, 0, 0, 0.1);
            margin: auto;
            width: 80%;
        }
        .stButton>button {
            background-color: #5b7a58;
            color: white;
            font-size: 18px;
            border-radius: 10px;
            padding: 10px;
            width: 100%;
        }
        .stButton>button:hover {
            background-color: #3b5d42;
        }
    </style>
""", unsafe_allow_html=True)

# 🔹 Criar a Barra Lateral para Navegação
st.sidebar.image("image.png", width=120)
st.sidebar.markdown("# 🌿 Menu")
pagina = st.sidebar.radio(
    "Escolha uma seção:",
    ["🏠 Início", "🍵 Gerador de Blends", "📖 Lista de Plantas", "📞 Contato & Sobre"]
)

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

# 🔹 Criar conteúdo para cada página
if pagina == "🏠 Início":
    st.markdown('<div class="header">Bem-vindo à Odorata 🌿</div>', unsafe_allow_html=True)
    st.markdown('<div class="subheader">Explore a fitoterapia e descubra o poder das ervas na criação de blends perfeitos! 🍵</div>', unsafe_allow_html=True)
    st.image("image.png", width=200)
    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
    st.write("""
        A **Odorata** é um projeto que combina conhecimento ancestral com tecnologia moderna para criar blends de chás personalizados.
        Utilize o nosso **Gerador de Blends** para descobrir as melhores combinações de ervas com base em seus efeitos desejados.
    """)

elif pagina == "🍵 Gerador de Blends":
    st.markdown('<div class="header">Gerador de Blends 🍵</div>', unsafe_allow_html=True)
    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)

    # 🔹 Criar interface de seleção de blends
    with st.container():
        st.subheader("🔍 Escolha os efeitos desejados:")
        efeitos_desejados = st.text_input("Digite os efeitos (ex: Calmante, Estimulante)").strip().lower()
        yin_yang = st.selectbox("Selecione Yin-Yang:", ["Todos", "Yin", "Yang"])
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
                    st.success(f"📌 Número total de plantas encontradas: {len(df_filtrado)}")

                    blends_completos = []

                    # 🔹 Função para calcular compatibilidade
                    def calcular_compatibilidade(nome1, nome2):
                        if nome1 in df_compatibilidade.iloc[:, 0].values and nome2 in df_compatibilidade.columns:
                            return df_compatibilidade.loc[df_compatibilidade.iloc[:, 0] == nome1, nome2].values[0]
                        return 0

                    # 🔹 Gerar blends de 2 e 3 plantas
                    for num_plantas in [2, 3]:
                        for combinacao in itertools.combinations(df_filtrado["nome da planta"], num_plantas):
                            nomes = sorted(combinacao)
                            compatibilidade = sum(calcular_compatibilidade(nomes[i], nomes[j]) for i in range(len(nomes)) for j in range(i+1, len(nomes))) / (len(nomes) * (len(nomes)-1) / 2)

                            if compatibilidade >= 4:
                                blends_completos.append({
                                    "Planta 1": nomes[0],
                                    "Planta 2": nomes[1] if len(nomes) > 1 else "-",
                                    "Planta 3": nomes[2] if len(nomes) > 2 else "-",
                                    "Compatibilidade Média": round(compatibilidade, 2)
                                })

                    if blends_completos:
                        df_resultado = pd.DataFrame(blends_completos)
                        st.write("💡 Blends sugeridos:")
                        st.dataframe(df_resultado)
                    else:
                        st.error("⚠️ Nenhum blend compatível foi encontrado.")

elif pagina == "📖 Lista de Plantas":
    st.markdown('<div class="header">Lista de Plantas 🌱</div>', unsafe_allow_html=True)
    st.markdown('<div class="subheader">Veja as ervas disponíveis e seus efeitos terapêuticos</div>', unsafe_allow_html=True)
    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
    st.write("""
        Aqui você pode visualizar todas as plantas cadastradas, seus benefícios e contraindicações.
        Em breve adicionaremos uma busca interativa!
    """)

elif pagina == "📞 Contato & Sobre":
    st.markdown('<div class="header">Contato & Sobre 📞</div>', unsafe_allow_html=True)
    st.markdown('<div class="subheader">Fale conosco e saiba mais sobre a Odorata</div>', unsafe_allow_html=True)
    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
    st.write("""
        Caso tenha dúvidas ou sugestões, entre em contato conosco:
        - 📩 **E-mail:** contato@odorata.com
        - 📷 **Instagram:** @odorata_blends
        - 🌐 **Site:** www.odorata.com.br
    """)
