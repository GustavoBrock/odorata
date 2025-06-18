import pandas as pd
import re

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

# 🔹 Carregar a aba "Classificação Expandida" para buscar efeitos primários, yin-yang, temperamento e contraindicações
df_classificacao = df_dict.get("Classificação Expandida")
if df_classificacao is None:
    print("⚠️ Erro: Aba 'Classificação Expandida' não encontrada.")
    exit()

df_classificacao.columns = [col.lower().strip() for col in df_classificacao.columns]
df_classificacao["nome da planta"] = df_classificacao["nome da planta"].str.lower().str.strip()

# 🔹 Verificar se a coluna "contraindicações" existe
if "contraindicações" not in df_classificacao.columns:
    print("⚠️ Erro: A coluna 'contraindicações' não foi encontrada na aba Classificação Expandida.")
    exit()

# 🔹 Solicitar o efeito desejado ao usuário
efeito_desejado = input("Digite o efeito desejado para o blend (ex: Calmante, Estimulante, Cognitivo): ").strip().lower()

# 🔹 Filtrar plantas que possuem o efeito desejado
df_filtrado = df_classificacao[df_classificacao["efeito primário"].str.contains(efeito_desejado, na=False, case=False)]

# 📌 Verificar se o filtro encontrou alguma planta
if df_filtrado.empty:
    print(f"⚠️ Nenhuma planta encontrada para o efeito desejado: {efeito_desejado}")
    exit()

print(f"📌 Número total de plantas encontradas para '{efeito_desejado}':", len(df_filtrado))

# 🔹 Criar DataFrame para armazenar combinações de plantas
blends_sugeridos = set()

# 🔹 Testar combinações de 2 ou 3 plantas
for i, planta1 in df_filtrado.iterrows():
    for j, planta2 in df_filtrado.iterrows():
        if planta1["nome da planta"] != planta2["nome da planta"]:
            nomes_2 = sorted([planta1["nome da planta"], planta2["nome da planta"]])
            nome1, nome2 = nomes_2

            # Verificar compatibilidade média para 2 plantas
            if nome1 in df_compatibilidade.iloc[:, 0].values and nome2 in df_compatibilidade.columns:
                peso1 = df_compatibilidade.loc[df_compatibilidade.iloc[:, 0] == nome1, nome2].values[0]
                media_compatibilidade_2 = peso1
            else:
                media_compatibilidade_2 = 0

            # 🔹 Coletar Yin-Yang, Temperamento e Contraindicações para blends de 2 plantas
            yin_yang_blend = set()
            temperamentos_blend = set()
            contraindicações_blend = set()

            for planta in [nome1, nome2]:
                yin_yang_valor = df_classificacao.loc[df_classificacao["nome da planta"] == planta, "classificação yin-yang"].values
                temp_valor = df_classificacao.loc[df_classificacao["nome da planta"] == planta, "temperamento insônia"].values
                contra_valor = df_classificacao.loc[df_classificacao["nome da planta"] == planta, "contraindicações"].values

                if len(yin_yang_valor) > 0:
                    yin_yang_blend.add(yin_yang_valor[0])
                if len(temp_valor) > 0:
                    temperamentos_blend.add(temp_valor[0])
                if len(contra_valor) > 0 and isinstance(contra_valor[0], str):
                    contraindicações_blend.update(re.split(r"; |, |\n", contra_valor[0]))

            yin_yang_final = "Ambos" if len(yin_yang_blend) > 1 else ", ".join(yin_yang_blend)
            temperamentos_final = ", ".join(sorted(temperamentos_blend)) if temperamentos_blend else "Não Especificado"
            contraindicações_final = ", ".join(sorted(contraindicações_blend)) if contraindicações_blend else "-"

            if media_compatibilidade_2 > 3.5:
                blends_sugeridos.add((nome1, nome2, "-", media_compatibilidade_2, yin_yang_final, temperamentos_final, contraindicações_final))

            for k, planta3 in df_filtrado.iterrows():
                if planta1["nome da planta"] != planta3["nome da planta"] and planta2["nome da planta"] != planta3["nome da planta"]:
                    nomes_3 = sorted([planta1["nome da planta"], planta2["nome da planta"], planta3["nome da planta"]])
                    nome1, nome2, nome3 = nomes_3

                    # Verificar compatibilidade média para 3 plantas
                    if nome1 in df_compatibilidade.iloc[:, 0].values and nome2 in df_compatibilidade.columns and nome3 in df_compatibilidade.columns:
                        peso1 = df_compatibilidade.loc[df_compatibilidade.iloc[:, 0] == nome1, nome2].values[0]
                        peso2 = df_compatibilidade.loc[df_compatibilidade.iloc[:, 0] == nome2, nome3].values[0]
                        peso3 = df_compatibilidade.loc[df_compatibilidade.iloc[:, 0] == nome1, nome3].values[0]
                        media_compatibilidade_3 = (peso1 + peso2 + peso3) / 3
                    else:
                        media_compatibilidade_3 = 0

                    # 🔹 Coletar contraindicações para blends de 3 plantas
                    contraindicações_blend.clear()
                    for planta in [nome1, nome2, nome3]:
                        contra_valor = df_classificacao.loc[df_classificacao["nome da planta"] == planta, "contraindicações"].values
                        if len(contra_valor) > 0 and isinstance(contra_valor[0], str):
                            contraindicações_blend.update(re.split(r"; |, |\n", contra_valor[0]))

                    contraindicações_final = ", ".join(sorted(contraindicações_blend)) if contraindicações_blend else "-"

                    if media_compatibilidade_3 > 3.5:
                        blends_sugeridos.add((nome1, nome2, nome3, media_compatibilidade_3, yin_yang_final, temperamentos_final, contraindicações_final))

# 🔹 Criar DataFrame com os blends gerados
df_blends = pd.DataFrame(blends_sugeridos, columns=["Planta 1", "Planta 2", "Planta 3", "Compatibilidade Média", "Yin-Yang", "Temperamento", "Contraindicações"])

# 🔹 Salvar em um novo arquivo Excel
file_path_blends = "Blends_Recomendados_Final.xlsx"
df_blends.to_excel(file_path_blends, sheet_name="Blends Recomendados", index=False)

# 🔹 Mensagem final
print(f"\n✅ Blends gerados com sucesso! Verifique o arquivo '{file_path_blends}'.")
