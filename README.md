# 🌿 Odorata – Blends Fitoterápicos Inteligentes

Odorata é um projeto de inovação voltado ao desenvolvimento e sugestão automatizada de blends de chás fitoterápicos com base em dados científicos. O sistema cruza propriedades medicinais, compatibilidade entre ervas e perfis de usuários para gerar combinações funcionais e seguras.

---

## 🔍 Objetivo

Criar uma plataforma interativa que auxilie usuários, profissionais de saúde e empreendedores na composição de chás personalizados, considerando:

- Ações terapêuticas das plantas
- Temperamento e contraindicações
- Interações entre fitoterápicos
- Afinidade energética e funcional

---

## 🛠️ Tecnologias utilizadas

- **Python** com `pandas`, `streamlit`, `openpyxl`
- **Interface Web** via [Streamlit](https://streamlit.io)
- **Excel** como banco de dados dinâmico
- Planejamento para expansão com **SQLite** e **API REST**

---

## 🧪 Funcionalidades principais

- 📂 Leitura e cruzamento de dados de plantas medicinais
- 🔀 Geração de combinações de até 3 ervas compatíveis
- ⚠️ Validação automática de contraindicações
- 🌿 Visualização simplificada das propriedades de cada blend
- 💡 Interface amigável com filtros por ação terapêutica, tipo de chá, público-alvo etc.

---

## 🚀 Como executar o projeto

1. Clone o repositório:

```bash
git clone https://github.com/GustavoBrock/odorata.git
cd odorata

Instale as dependências (se aplicável):

bash
Copiar
Editar
pip install -r requirements.txt
Execute a interface com Streamlit:

bash
Copiar
Editar
streamlit run app.py
📁 Estrutura do projeto
bash
Copiar
Editar
odorata/
├── data/                # Planilhas com as propriedades das plantas
├── src/                 # Código principal do sistema
│   ├── combinador.py
│   ├── extrator.py
│   └── validador.py
├── app.py               # Interface principal com Streamlit
├── README.md
└── requirements.txt     # Dependências Python
👨‍💻 Autor
Gustavo Felipe Brock
Químico, desenvolvedor e entusiasta de inovação e tecnologia aplicada à saúde natural.

💼 LinkedIn

📧 gustavobrock08@gmail.com

🧠 Certified Tech Developer - Rocketseat Brasil
