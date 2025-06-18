import streamlit as st
import pandas as pd
import re
import itertools

# 🔹 Configuração da Página
st.set_page_config(page_title="Odorata - Herbal Tea Generator", layout="wide")

# 🔹 Carregar Estilos Externos
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# 🔹 Criar Navegação com Ícones
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
    """,
    unsafe_allow_html=True)

# 🔹 Capturar Página Selecionada
query_params = st.query_params
pagina_atual = query_params.get("page", "home")

# 🔹 Exibir Conteúdo da Página Selecionada
if pagina_atual == "home":
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

   # 🔹 Página do Gerador de Blends
elif pagina_atual == "blends":
    st.markdown("# 🍵 Gerador de Blends")

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

    # 🔹 Criar interface centralizada
    st.subheader("🔍 Escolha os efeitos desejados:")

    efeitos_desejados = st.text_input("Digite os efeitos (ex: Calmante, Estimulante)").strip().lower()
    yin_yang = st.selectbox("Selecione Yin-Yang:", ["Todos", "Yin", "Yang"])
    temperamento = st.selectbox("Selecione o Temperamento:", temperamentos_disponiveis)
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

                # 🔹 Função para obter informações da planta
                def obter_info_planta(nome):
                    info = df_classificacao[df_classificacao["nome da planta"] == nome]
                    if not info.empty:
                        info = info.iloc[0]
                        return {
                            "yin_yang": info["classificação yin-yang"],
                            "temperamento": info["temperamento insônia"],
                            "contraindicações": info["contraindicações"].split(", ")
                        }
                    return {"yin_yang": "", "temperamento": "", "contraindicações": []}

                # 🔹 Gerar blends de 2 e 3 plantas
                for num_plantas in [2, 3]:
                    for combinacao in itertools.combinations(df_filtrado["nome da planta"], num_plantas):
                        nomes = sorted(combinacao)
                        compatibilidade = sum(calcular_compatibilidade(nomes[i], nomes[j]) for i in range(len(nomes)) for j in range(i+1, len(nomes))) / (len(nomes) * (len(nomes)-1) / 2)

                        if compatibilidade >= 4:
                            infos = [obter_info_planta(nome) for nome in nomes]

                            # 🔹 Aplicar filtros Yin-Yang e Temperamento
                            if (yin_yang != "Todos" and not all(info["yin_yang"] == yin_yang for info in infos)) or \
                               (temperamento != "Todos" and not all(info["temperamento"] == temperamento for info in infos)):
                                continue

                            blends_completos.append({
                                "Planta 1": nomes[0],
                                "Planta 2": nomes[1] if len(nomes) > 1 else "-",
                                "Planta 3": nomes[2] if len(nomes) > 2 else "-",
                                "Compatibilidade Média": round(compatibilidade, 2),
                                "Yin-Yang": ", ".join(sorted(set(info["yin_yang"] for info in infos))),
                                "Temperamento": ", ".join(sorted(set(info["temperamento"] for info in infos))),
                                "Contraindicações": ", ".join(sorted(set(sum([info["contraindicações"] for info in infos], []))))
                            })

                if blends_completos:
                    df_resultado = pd.DataFrame(blends_completos)
                    st.write("💡 Blends sugeridos:")
                    st.dataframe(df_resultado)
                else:
                    st.error("⚠️ Nenhum blend compatível foi encontrado.")

elif pagina_atual == "plantas":
    st.markdown("# 📖 Lista de Plantas")
elif pagina_atual == "loja":
    st.markdown("# 🛒 Loja")
elif pagina_atual == "contato":
    st.markdown("# 📞 Contato & Sobre")
