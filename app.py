from flask import Flask, render_template, request
import pandas as pd

# A importação agora é direta e funcionará sem erros
from algoritmos import busca_binaria, busca_hash, busca_preco

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
    busca_preco.preparar_dados_para_busca_preco(df_principal)

except FileNotFoundError:
    print("ERRO CRÍTICO: 'motoparts.csv' não encontrado. Verifique se o arquivo está na mesma pasta que app.py.")
    df_principal = pd.DataFrame()


# --- Rotas da Aplicação ---

@app.route('/')
def index():
    # Obter opções únicas para os filtros
    marcas = sorted(df_principal['Marca'].unique().tolist()) if not df_principal.empty else []
    modelos = sorted(df_principal['Modelo'].unique().tolist()) if not df_principal.empty else []
    categorias = sorted(df_principal['Categoria_Peca'].unique().tolist()) if not df_principal.empty else []
    anos = sorted(df_principal['Ano'].unique().tolist(), reverse=True) if not df_principal.empty else []
    
    return render_template('index.html', 
                         form_values={}, 
                         marcas=marcas, 
                         modelos=modelos, 
                         categorias=categorias, 
                         anos=anos)

@app.route('/buscar_sku', methods=['POST'])
def buscar_sku():
    sku_prefixo = request.form.get('sku_prefix', '').strip().upper()
    resultados = busca_binaria.buscar_por_prefixo_sku(sku_prefixo)
    
    # Obter opções únicas para os filtros
    marcas = sorted(df_principal['Marca'].unique().tolist()) if not df_principal.empty else []
    modelos = sorted(df_principal['Modelo'].unique().tolist()) if not df_principal.empty else []
    categorias = sorted(df_principal['Categoria_Peca'].unique().tolist()) if not df_principal.empty else []
    anos = sorted(df_principal['Ano'].unique().tolist(), reverse=True) if not df_principal.empty else []
    
    return render_template('index.html', 
                         pecas_por_sku=resultados, 
                         sku_buscado=sku_prefixo, 
                         form_values={},
                         marcas=marcas, 
                         modelos=modelos, 
                         categorias=categorias, 
                         anos=anos)

@app.route('/filtrar', methods=['POST'])
def filtrar_pecas():
    filtros = {
        "Marca": request.form.get('marca'),
        "Modelo": request.form.get('modelo'),
        "Ano": request.form.get('ano'),
        "Categoria_Peca": request.form.get('categoria_peca')
    }
    pecas_filtradas = busca_hash.buscar_por_filtros_hash(filtros)
    
    # Obter opções únicas para os filtros
    marcas = sorted(df_principal['Marca'].unique().tolist()) if not df_principal.empty else []
    modelos = sorted(df_principal['Modelo'].unique().tolist()) if not df_principal.empty else []
    categorias = sorted(df_principal['Categoria_Peca'].unique().tolist()) if not df_principal.empty else []
    anos = sorted(df_principal['Ano'].unique().tolist(), reverse=True) if not df_principal.empty else []
    
    return render_template('index.html', 
                         pecas_filtradas=pecas_filtradas, 
                         form_values=request.form,
                         marcas=marcas, 
                         modelos=modelos, 
                         categorias=categorias, 
                         anos=anos)

@app.route('/buscar_preco', methods=['POST'])
def buscar_preco():
    preco_min = request.form.get('preco_min')
    preco_max = request.form.get('preco_max')
    
    # Obter filtros de peça também
    filtros_peca = {
        "Marca": request.form.get('marca'),
        "Modelo": request.form.get('modelo'),
        "Ano": request.form.get('ano'),
        "Categoria_Peca": request.form.get('categoria_peca')
    }
    
    # Validar se pelo menos um preço foi informado
    if not preco_min and not preco_max:
        # Obter opções únicas para os filtros
        marcas = sorted(df_principal['Marca'].unique().tolist()) if not df_principal.empty else []
        modelos = sorted(df_principal['Modelo'].unique().tolist()) if not df_principal.empty else []
        categorias = sorted(df_principal['Categoria_Peca'].unique().tolist()) if not df_principal.empty else []
        anos = sorted(df_principal['Ano'].unique().tolist(), reverse=True) if not df_principal.empty else []
        
        return render_template('index.html', 
                             form_values=request.form,
                             marcas=marcas, 
                             modelos=modelos, 
                             categorias=categorias, 
                             anos=anos,
                             error_message="Informe pelo menos um preço (mínimo ou máximo)")
    
    # Buscar por preço E filtros de peça
    pecas_por_preco = busca_preco.buscar_por_faixa_preco_com_filtros(preco_min, preco_max, filtros_peca)
    
    # Obter opções únicas para os filtros
    marcas = sorted(df_principal['Marca'].unique().tolist()) if not df_principal.empty else []
    modelos = sorted(df_principal['Modelo'].unique().tolist()) if not df_principal.empty else []
    categorias = sorted(df_principal['Categoria_Peca'].unique().tolist()) if not df_principal.empty else []
    anos = sorted(df_principal['Ano'].unique().tolist(), reverse=True) if not df_principal.empty else []
    
    return render_template('index.html', 
                         pecas_por_preco=pecas_por_preco, 
                         form_values=request.form,
                         marcas=marcas, 
                         modelos=modelos, 
                         categorias=categorias, 
                         anos=anos)

if __name__ == '__main__':
    app.run(debug=True)