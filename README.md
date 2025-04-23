# Bot de Leitura MQTT para Produção Industrial

Projeto desenvolvido para escutar tópicos MQTT com dados de linhas de produção, tratar as informações recebidas
e armazená-las em um banco de dados PostgreSQL para posterior análise via Grafana.

---

## ⚙️ Tecnologias Utilizadas

- Python 3
- Paho MQTT (cliente MQTT)
- Psycopg2 (PostgreSQL)
- python-dotenv (.env para variáveis de ambiente)
- PostgreSQL
- Grafana (visualização de dados)
- Render/Railway (deploy)

---

## 📁 Estrutura do Projeto

bot_Leitura_MQTT/                         ← pasta principal do projeto
├── bots/                                 ← subpasta onde ficarão os bots individuais
│   └── __init__.py                       ← arquivo vazio para reconhecer 'bots' como módulo Python
├── config.py                             ← script que carrega variáveis do .env (banco, MQTT, etc.)
├── env.txt                               ← modelo de preenchimento do arquivo .env (sem dados sensíveis)
├── main.py                               ← bot pai, que orquestra os bots
├── README.md                             ← documentação do projeto
├── .env                                  ← arquivo com senhas e configs (Está apenas no PC local)
├── .gitignore                            ← define o que deve ser ignorado pelo Git
└── requirements.txt                      ← lista de bibliotecas usadas no projet


---

## ⚙️ Funcionamento

Cada bot se conecta a um broker MQTT e escuta tópicos específicos (a serem definidos).  
Sinais recebidos (como HIGH e LOW) indicam eventos de produção, defeitos, consumo, entre outros.

Esses dados são tratados localmente e gravados no banco de dados PostgreSQL.  
Posteriormente, são utilizados para geração de dashboards e análises no Grafana.

---

## 🚀 Como Executar Localmente

1. Crie o ambiente virtual:
    python -m venv .venv
2. Ative o ambiente (Windows):
    .venv\Scripts\activate
3. Instale as dependências:
    pip install -r requirements.txt
4. Execute o bot pai:
    python main.py

---

## 📡 Status Atual

- ✅ Ambiente virtual e dependências prontos  
- ✅ Estrutura de arquivos organizada  
- 🔄 Aguardando definição dos tópicos MQTT
- ⏳ Bots em desenvolvimento (um por variável/função)  
- ☁️ Deploy na nuvem programado (Render ou Railway) 
- ⏳ mudança drastica no funcionamento do projeto, lembrar de modificar com os novos tópicos e dados os bots

---

## 👤 Desenvolvedor

**Felipe Manzan**  
Engenharia Mecatrônica & Automação Industrial  
GitHub: [@ManzanFinalBoss](https://github.com/ManzanFinalBoss)

