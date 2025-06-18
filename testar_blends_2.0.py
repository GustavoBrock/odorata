import pandas as pd
import re
import itertools

# 🔹 Carregar o arquivo Excel com a matriz de compatibilidade e classificação expandida
file_path_compatibilidade = "Tabela_Plantas_Ansiedade_Desempenho_ExpansaoTotal.xlsx"
df_dict = pd.read_excel(file_path_compatibilidade, sheet_name=None)

# 🔹 Identificar e carregar a aba de compatibilidade
def encontrar_aba_compatibilidade(df_dict):
    for nome_aba in df_dict.keys():
        if "compatibilidade" in nome_aba.lower():
            return nome_aba
    return None

tabela_compatibilidade = encontrar_aba_compatibilidade(df_dict)

if tabela_compatibilidade:
    df_compatibilidade = df_dict[tabela_compatibilidade]
else:
    print("⚠️ Erro: Nenhuma aba de compatibilidade encontrada no arquivo.")
    exit()

# 🔹 Normalizar os nomes das colunas e plantas na matriz de compatibilidade
df_compatibilidade.columns = [re.sub(r"\s*\(.*?\)", "", str(col)).strip().lower() for col in df_compatibilidade.columns]
df_compatibilidade.iloc[:, 0] = df_compatibilidade.iloc[:, 0].str.lower().str.strip()

# 🔹 Substituir valores NaN por 0
df_compatibilidade = df_compatibilidade.fillna(0)

# 🔹 Carregar a aba "Classificação Expandida" para buscar efeitos primários, secundários, yin-yang, temperamento e contraindicações
df_classificacao = df_dict.get("Classificação Expandida")
if df_classificacao is None:
    print("⚠️ Erro: Aba 'Classificação Expandida' não encontrada.")
    exit()

df_classificacao.columns = [col.lower().strip() for col in df_classificacao.columns]
df_classificacao["nome da planta"] = df_classificacao["nome da planta"].str.lower().str.strip()

# 🔹 Solicitar os efeitos desejados ao usuário, permitindo múltiplas seleções
efeitos_desejados = input("Digite os efeitos desejados para o blend (separados por vírgula, ex: Calmante, Estimulante): ").strip().lower()

# Converter a entrada do usuário em uma lista de efeitos
lista_efeitos = [efeito.strip() for efeito in efeitos_desejados.split(",")]

# 🔹 Filtrar plantas que possuem pelo menos um dos efeitos desejados, verificando efeitos primários e secundários
df_filtrado = df_classificacao[
    df_classificacao["efeito primário"].str.contains("|".join(lista_efeitos), na=False, case=False) |
    df_classificacao["efeito secundário"].str.contains("|".join(lista_efeitos), na=False, case=False)
]

# 📌 Verificar se o filtro encontrou alguma planta
if df_filtrado.empty:
    print(f"⚠️ Nenhuma planta encontrada para os efeitos desejados: {', '.join(lista_efeitos)}")
    exit()

print(f"📌 Número total de plantas encontradas para os efeitos '{', '.join(lista_efeitos)}': {len(df_filtrado)}")

# 🔹 Criar um conjunto para armazenar combinações únicas sem duplicatas
blends_unicos = set()
blends_completos = []

# Função para calcular a compatibilidade entre duas plantas
def calcular_compatibilidade(nome1, nome2):
    if nome1 in df_compatibilidade.iloc[:, 0].values and nome2 in df_compatibilidade.columns:
        return df_compatibilidade.loc[df_compatibilidade.iloc[:, 0] == nome1, nome2].values[0]
    return 0

# Função para coletar informações essenciais da planta
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

# Testar combinações de 2 e 3 plantas e calcular a compatibilidade
for combinacao in itertools.combinations(df_filtrado["nome da planta"], 2):
    nome1, nome2 = sorted(combinacao)
    if (nome1, nome2) not in blends_unicos:
        compatibilidade = calcular_compatibilidade(nome1, nome2)
        if compatibilidade >= 4:
            info1, info2 = obter_info_planta(nome1), obter_info_planta(nome2)
            blends_unicos.add((nome1, nome2))
            blends_completos.append({
                "Planta 1": nome1,
                "Planta 2": nome2,
                "Planta 3": "-",
                "Compatibilidade Média": compatibilidade,
                "Yin-Yang": ", ".join(sorted(set([info1["yin_yang"], info2["yin_yang"]]))).replace("Ambos, ", ""),
                "Temperamento": ", ".join(sorted(set([info1["temperamento"], info2["temperamento"]]))).replace("Não Especificado, ", ""),
                "Contraindicações": ", ".join(sorted(set(info1["contraindicações"] + info2["contraindicações"])))
            })

for combinacao in itertools.combinations(df_filtrado["nome da planta"], 3):
    nome1, nome2, nome3 = sorted(combinacao)
    if (nome1, nome2, nome3) not in blends_unicos:
        compatibilidade = (calcular_compatibilidade(nome1, nome2) + calcular_compatibilidade(nome1, nome3) + calcular_compatibilidade(nome2, nome3)) / 3
        if compatibilidade >= 4:
            info1, info2, info3 = obter_info_planta(nome1), obter_info_planta(nome2), obter_info_planta(nome3)
            blends_unicos.add((nome1, nome2, nome3))
            blends_completos.append({
                "Planta 1": nome1,
                "Planta 2": nome2,
                "Planta 3": nome3,
                "Compatibilidade Média": compatibilidade,
                "Yin-Yang": ", ".join(sorted(set([info1["yin_yang"], info2["yin_yang"], info3["yin_yang"]]))).replace("Ambos, ", ""),
                "Temperamento": ", ".join(sorted(set([info1["temperamento"], info2["temperamento"], info3["temperamento"]]))).replace("Não Especificado, ", ""),
                "Contraindicações": ", ".join(sorted(set(info1["contraindicações"] + info2["contraindicações"] + info3["contraindicações"])))
            })

# 🔹 Criar DataFrame e salvar
pd.DataFrame(blends_completos).to_excel("Blends_Corrigidos.xlsx", index=False)
print("✅ Blends gerados e salvos com sucesso!")