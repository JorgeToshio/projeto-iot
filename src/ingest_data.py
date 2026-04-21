import pandas as pd
from sqlalchemy import create_engine, text

# Conexão com o banco
engine = create_engine('postgresql://admin:admin@localhost:5432/iot_db')

def iniciar_banco():
    print("🚀 Iniciando processamento de dados...")
    
    try:
        # 1. FORÇAR A REMOÇÃO DA TABELA E DE TUDO QUE DEPENDE DELA (Views)
        with engine.connect() as conexao:
            print("🧹 Limpando banco de dados (Removendo tabela e views)...")
            # O CASCADE deleta a tabela e já limpa as views de uma vez só
            conexao.execute(text("DROP TABLE IF EXISTS temperature_readings CASCADE;"))
            conexao.commit()
        
        # 2. Ler o CSV
        df = pd.read_csv('data/iot_data.csv')
        
        # 3. Corrigir as colunas
        mapeamento = {
            'room_id/id': 'device_id',
            'temp': 'temperature'
        }
        df.rename(columns=mapeamento, inplace=True)
        
        # Converter a coluna de data
        df['noted_date'] = pd.to_datetime(df['noted_date'], dayfirst=True)

        # 4. Enviar para o banco
        # Como já deletamos a tabela manualmente acima, o replace vai funcionar sem erros
        df.to_sql('temperature_readings', engine, if_exists='replace', index=False)
        print("✅ Tabela 'temperature_readings' criada do zero!")

        # 5. Criar as Views SQL novamente
        with engine.connect() as conexao:
            print("📊 Criando Views SQL...")
            
            # View 1: Média por dispositivo
            conexao.execute(text("""
                CREATE VIEW avg_temp_por_dispositivo AS
                SELECT device_id, AVG(temperature) as avg_temp 
                FROM temperature_readings 
                GROUP BY device_id;
            """))
            
            # View 2: Leituras por hora
            conexao.execute(text("""
                CREATE VIEW leituras_por_hora AS
                SELECT date_trunc('hour', noted_date) as hora, COUNT(*) as contagem
                FROM temperature_readings
                GROUP BY hora;
            """))

            # View 3: Máximas e mínimas por dia
            conexao.execute(text("""
                CREATE VIEW temp_max_min_por_dia AS
                SELECT noted_date::date as data, MAX(temperature) as temp_max, MIN(temperature) as temp_min
                FROM temperature_readings
                GROUP BY data;
            """))
            
            conexao.commit()
            
        print("✅ Todas as 3 Views SQL foram recriadas!")
        print("✨ Sucesso total. Pode rodar o Dashboard.")

    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    iniciar_banco()