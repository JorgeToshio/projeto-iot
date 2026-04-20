import pandas as pd
from sqlalchemy import create_engine, text

# Conexão com o banco
engine = create_engine('postgresql://admin:admin@localhost:5432/iot_db')

def iniciar_banco():
    print("🚀 Iniciando processamento de dados...")
    
    try:
        # 1. Ler o CSV
        df = pd.read_csv('data/iot_data.csv')
        
        # 2. Corrigir as colunas (Evitando duplicidade)
        # Vamos usar 'room_id/id' como o nosso 'device_id' oficial
        # E 'temp' como 'temperature'
        mapeamento = {
            'room_id/id': 'device_id',
            'temp': 'temperature'
        }
        df.rename(columns=mapeamento, inplace=True)
        
        # 3. Converter a coluna de data para o formato real de data (importante!)
        df['noted_date'] = pd.to_datetime(df['noted_date'], dayfirst=True)

        # 4. Enviar para o banco
        # if_exists='replace' vai apagar a tabela antiga e criar essa nova certinha
        df.to_sql('temperature_readings', engine, if_exists='replace', index=False)
        print("✅ Tabela 'temperature_readings' criada com sucesso!")

        # 5. Criar as Views SQL
        with engine.connect() as conexao:
            # View 1: Média por dispositivo
            conexao.execute(text("""
                CREATE OR REPLACE VIEW avg_temp_por_dispositivo AS
                SELECT device_id, AVG(temperature) as avg_temp 
                FROM temperature_readings 
                GROUP BY device_id;
            """))
            
            # View 2: Leituras por hora
            conexao.execute(text("""
                CREATE OR REPLACE VIEW leituras_por_hora AS
                SELECT date_trunc('hour', noted_date) as hora, COUNT(*) as contagem
                FROM temperature_readings
                GROUP BY hora;
            """))

            # View 3: Máximas e mínimas por dia
            conexao.execute(text("""
                CREATE OR REPLACE VIEW temp_max_min_por_dia AS
                SELECT noted_date::date as data, MAX(temperature) as temp_max, MIN(temperature) as temp_min
                FROM temperature_readings
                GROUP BY data;
            """))
            
            conexao.commit()
            
        print("✅ Todas as 3 Views SQL foram criadas!")
        print("✨ Agora rode o Dashboard.")

    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    iniciar_banco()