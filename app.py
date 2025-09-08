from flask import Flask, render_template, request
import pandas as pd

# A importação agora é direta e funcionará sem erros
from algoritmos import busca_binaria, busca_hash

# O Flask encontrará 'static' e 'templates' automaticamente
app = Flask(__name__)

# --- CARREGAMENTO E PREPARAÇÃO DOS DADOS ---
try:
    # O caminho para o CSV agora é direto
    df_principal = pd.read_csv('motoparts.csv')
    df_principal.dropna(subset=['SKU'], inplace=True)
    df_principal = df_principal.reset_index()

    # Prepara os dados para cada algoritmo
    busca_binaria.preparar_dados_para_busca_binaria(df_principal)
    busca_hash.preparar_indices_hash(df_principal)

except FileNotFoundError:
    print("ERRO CRÍTICO: 'motoparts.csv' não encontrado. Verifique se o arquivo está na mesma pasta que app.py.")
    df_principal = pd.DataFrame()


# --- Rotas da Aplicação ---

@app.route('/')
def index():
    return render_template('index.html', form_values={})

@app.route('/buscar_sku', methods=['POST'])
def buscar_sku():
    sku_prefixo = request.form.get('sku_prefix', '').strip().upper()
    resultados = busca_binaria.buscar_por_prefixo_sku(sku_prefixo)
    return render_template('index.html', pecas_por_sku=resultados, sku_buscado=sku_prefixo, form_values={})

@app.route('/filtrar', methods=['POST'])
def filtrar_pecas():
    filtros = {
        "Marca": request.form.get('marca'),
        "Modelo": request.form.get('modelo'),
        "Ano": request.form.get('ano'),
        "Categoria_Peca": request.form.get('categoria_peca')
    }
    pecas_filtradas = busca_hash.buscar_por_filtros_hash(filtros)
    return render_template('index.html', pecas_filtradas=pecas_filtradas, form_values=request.form)

if __name__ == '__main__':
    app.run(debug=True)