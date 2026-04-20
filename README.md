# Pipeline de Dados IoT com Docker e Python 🌡️

Este projeto foi desenvolvido como parte da disciplina **Disruptive Architectures: IoT, Big Data e IA** da UNIFECAF. O objetivo é criar um pipeline completo de dados que processa leituras de temperatura de dispositivos IoT, armazena-os em um banco de dados PostgreSQL via Docker e os visualiza através de um dashboard interativo.

## 🛠️ Tecnologias Utilizadas
*   **Python 3.x**: Linguagem principal para ingestão e processamento.
*   **Docker**: Conteinerização do banco de dados PostgreSQL.
*   **PostgreSQL**: Banco de dados relacional para armazenamento das leituras.
*   **Pandas**: Manipulação e limpeza de dados.
*   **SQLAlchemy**: Conexão entre Python e o Banco de Dados.
*   **Streamlit**: Criação do Dashboard web.
*   **Plotly**: Gráficos interativos.

## 📂 Estrutura do Projeto
```text
projeto_iot/
├── data/               # Arquivo CSV original (Kaggle)
├── docs/               # Documentação e capturas de tela
├── sql/                # Scripts das Views SQL
├── src/
│   ├── ingest_data.py  # Script de processamento e carga
│   └── dashboard.py    # Aplicação do Dashboard Streamlit
├── requirements.txt    # Bibliotecas necessárias
└── README.md           # Instruções do projeto

Como Executar o Projeto
1. Preparação do Ambiente
Certifique-se de ter o Python e o Docker Desktop instalados.
code
Bash
# Clone o repositório
git clone https://github.com/JorgeToshio/projeto-iot.git

# Crie e ative o ambiente virtual
python -m venv venv
# No Windows:
venv\Scripts\activate
# No Mac/Linux:
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt
2. Subir o Banco de Dados (Docker)
Execute o comando abaixo para subir o container do PostgreSQL:
code
Bash
docker run --name postgres-iot -e POSTGRES_PASSWORD=admin -e POSTGRES_USER=admin -e POSTGRES_DB=iot_db -p 5432:5432 -d postgres
3. Ingestão de Dados
Coloque o arquivo iot_data.csv (baixado do Kaggle) dentro da pasta data/ e execute:
code
Bash
python src/ingest_data.py
Este comando irá criar a tabela, renomear as colunas e gerar as Views SQL automaticamente.
4. Executar o Dashboard
Para visualizar os gráficos interativos, execute:
code
Bash
streamlit run src/dashboard.py
📊 Views SQL Criadas
O projeto utiliza 3 Views SQL para organizar os insights:
avg_temp_por_dispositivo: Calcula a temperatura média registrada por cada ID de dispositivo. Útil para identificar quais sensores estão em ambientes mais quentes.
leituras_por_hora: Agrupa a quantidade de registros por hora do dia, permitindo identificar picos de tráfego de dados no pipeline.
temp_max_min_por_dia: Extrai a temperatura máxima e mínima de cada dia, ideal para monitorar oscilações térmicas bruscas.
📈 Insights Obtidos
O gráfico de Oscilação Diária permite identificar o comportamento térmico ao longo dos meses, mostrando quedas ou aumentos graduais.
A Média por Dispositivo ajuda a validar se algum sensor está apresentando valores fora do padrão (outliers).
📝 Comandos Git Utilizados
code
Bash
git init
git add .
git commit -m "Projeto inicial: Pipeline de Dados IoT"
git remote add origin <URL_DO_REPOSITORIO>
git push -u origin main
Desenvolvido por: Jorge Toshio