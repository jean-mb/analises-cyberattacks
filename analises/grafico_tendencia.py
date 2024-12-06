import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import kagglehub

# DATASET: https://www.kaggle.com/datasets/fireballbyedimyrnmom/cyber-incidents-up-to-2020
caminho_dados = kagglehub.dataset_download(
    "fireballbyedimyrnmom/cyber-incidents-up-to-2020", path='cyber-operations-incidents.csv')
dados = pd.read_csv(caminho_dados)

dados['Data'] = pd.to_datetime(dados['Date'], errors='coerce')
dados = dados.dropna(subset=['Data'])  # invalidas
dados['Ano'] = dados['Data'].dt.year

ataques_por_ano = dados['Ano'].value_counts().sort_index()

ataques_por_ano_df = ataques_por_ano.reset_index()
ataques_por_ano_df.columns = ['Ano', 'Quantidade_Ataques']

sns.set(style="whitegrid")
plt.figure(figsize=(10, 6))
sns.lineplot(data=ataques_por_ano_df, x='Ano',
             y='Quantidade_Ataques', marker='o')

# março de 2018, guerra comercial eua x china
posicao_linha_guerra = 2017 + (3 / 12)
plt.axvline(x=posicao_linha_guerra, color='grey', linestyle='--', linewidth=2)

plt.text(posicao_linha_guerra - 0.25, max(ataques_por_ano_df['Quantidade_Ataques']) * 0.6,
         'Início da Guerra Comercial EUA x CHINA', color='#8f8d8d', fontsize=10,
         ha='right', va='bottom', fontweight='bold', rotation=0,
         bbox=dict(facecolor='white', edgecolor='white'))

plt.title('Tendências de ataques cibernéticos de espionagem apoiados por Estados: Evolução de 2005 a 2020 (Fonte: Council of Foreign Relations)', fontsize=16)
plt.xlabel('Anos', fontsize=14)
plt.ylabel('Número de Ataques Cibernéticos', fontsize=14)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
