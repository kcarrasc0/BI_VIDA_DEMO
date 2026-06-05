# 📊 BI da Minha Vida

> Um Dashboard de Business Intelligence pessoal desenvolvido para unificar e analisar dados da minha vida financeira e de projetos, atuando como um "sistema operacional" pessoal.

## 🚀 Sobre o Projeto

O **BI da Minha Vida** nasceu da necessidade de ter controle total sobre meus gastos e tarefas sem depender de aplicativos engessados de terceiros ou assinaturas. O grande diferencial deste projeto é a sua arquitetura de banco de dados "Serverless e Custo Zero": ele utiliza o **Google Sheets** como backend.

### 🔄 A Evolução da Arquitetura (V1 ➡️ V2)

Este repositório documenta a evolução da engenharia do projeto:

* **Versão 1.0 (Python/Streamlit):** O protótipo inicial (MVP) foi construído rapidamente utilizando Python e Streamlit. Ele validou a lógica de negócios, a leitura de dados via Pandas e a conexão com o Google Sheets.
* **Versão 2.0 (Next.js/React) - *Em Desenvolvimento*:** Para resolver limitações de renderização de página (page reloads) e aprimorar a experiência do usuário (UX/UI), o projeto está sendo reescrito em **Next.js**. Esta transição traz uma interface mais fluida, controle de estado avançado e a robustez de uma aplicação web moderna.

---

## ⚙️ Arquitetura e Banco de Dados (Google Sheets)

O projeto não utiliza bancos de dados tradicionais (SQL/NoSQL). A persistência de dados é feita 100% através do ecossistema Google, da seguinte forma:

1.  **Escrita de Dados (POST):** O frontend envia requisições HTTP para um **Google Apps Script** personalizado, que insere as novas linhas de gastos ou tarefas diretamente nas abas da planilha.
2.  **Leitura de Dados (GET):** O painel consome os dados atualizados lendo a planilha publicada na web no formato `.csv`, utilizando técnicas de *Cache Busting* para garantir que os dados exibidos sejam sempre processados em tempo real.

---

## 📈 Eixos e Funcionalidades

O sistema é dividido em grandes eixos de gestão:

### 💰 Eixo 1: Gestão Financeira
* **Registro de Movimentações:** Cadastro de entradas e saídas com categorias, valores, e datas.
* **Balanço Mensal:** Cálculo automático do saldo (Entradas vs Saídas).
* **Análise Visual:** Gráficos interativos mostrando os maiores focos de gastos e insights de consumo.

### 🚀 Eixo 2: Gestão de Projetos e Tarefas
* **Visão de Águia:** Tabela de status de todos os projetos em andamento.
* **Alertas Críticos:** Sistema de inteligência que identifica tarefas perto do prazo de vencimento (ex: 5 dias restantes) ou marcadas com alta prioridade.

---

## 🛠️ Tecnologias Utilizadas

**Stack Atual (V2):**
* **Frontend:** Next.js (App Router), React, Tailwind CSS
* **Visualização de Dados:** Recharts / Chart.js *(A definir)*
* **Leitura de Dados:** Fetch API / PapaParse (CSV)

**Stack Legado (V1 - Protótipo):**
* **Linguagem:** Python
* **Framework:** Streamlit
* **Manipulação de Dados:** Pandas
* **Gráficos:** Plotly Express

**Backend / Banco de Dados (Constante):**
* Google Sheets
* Google Apps Script (Javascript)

---

## 💻 Como rodar o projeto localmente

*(Instruções para a versão Next.js serão adicionadas aqui em breve)*

```bash
# 1. Clone este repositório
git clone [https://github.com/SEU_USUARIO/bi-da-minha-vida.git](https://github.com/SEU_USUARIO/bi-da-minha-vida.git)

# 2. Instale as dependências
npm install

# 3. Configure as variáveis de ambiente (.env)
# Crie um arquivo .env na raiz e adicione as URLs do Google Sheets e Apps Script

# 4. Rode o servidor de desenvolvimento
npm run dev
