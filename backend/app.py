from flask import Flask, render_template, request
import pandas as pd
from bisect import bisect_left
import math

app = Flask(__name__, template_folder='../templates')

# --- Carregamento e Preparação dos Dados ---
try:
    df = pd.read_csv("../motoparts.csv")
    df = df.dropna(subset=["sku"])
    df["sku"] = df["sku"].astype(int)
    
    order = df["sku"].to_numpy().argsort()
    skus_sorted = df["sku"].to_numpy()[order]
except FileNotFoundError:
    print("Erro: O arquivo motoparts.csv não foi encontrado.")
    df = pd.DataFrame()
    skus_sorted = []
    order = []

# --- Funções Auxiliares e de Busca ---

def find_by_sku(target):
    """Encontra um item pelo SKU usando busca binária."""
    i = bisect_left(skus_sorted, target)
    if i < len(skus_sorted) and skus_sorted[i] == target:
        peca_dict = df.iloc[order[i]].to_dict()
        return {k: ('' if isinstance(v, float) and math.isnan(v) else v) for k, v in peca_dict.items()}
    return None

def is_year_compatible(compatibility_range, target_year):
    """Verifica se um ano está dentro do intervalo de compatibilidade."""
    if not isinstance(compatibility_range, str):
        return False
    try:
        start_year, end_year = map(int, compatibility_range.split('-'))
        return start_year <= target_year <= end_year
    except (ValueError, TypeError):
        return False

# --- Rotas da Aplicação ---

@app.route('/')
def index():
    """Renderiza a página inicial."""
    # CORREÇÃO APLICADA AQUI:
    return render_template('index.html', form_values={})

@app.route('/buscar_sku', methods=['POST'])
def buscar_sku():
    """Recebe um SKU e retorna o resultado da busca."""
    try:
        sku_buscado = int(request.form['sku'])
        resultado = find_by_sku(sku_buscado)
        if resultado:
            return render_template('index.html', peca_sku=resultado, sku_buscado=sku_buscado, form_values=request.form)
        else:
            return render_template('index.html', erro_sku="Peça não encontrada.", sku_buscado=sku_buscado, form_values=request.form)
    except (ValueError, KeyError):
        return render_template('index.html', erro_sku="SKU inválido.", form_values=request.form)

@app.route('/filtrar', methods=['POST'])
def filtrar_pecas():
    """Filtra peças por marca, modelo e ano."""
    marca = request.form.get('marca')
    modelo = request.form.get('modelo')
    ano_str = request.form.get('ano')

    resultados = df[df['estoque'] > 0].copy()

    if marca:
        resultados = resultados[resultados['marca'].str.contains(marca, case=False, na=False)]
    
    if modelo:
        resultados = resultados[resultados['modelo'].str.contains(modelo, case=False, na=False)]

    if ano_str:
        try:
            ano = int(ano_str)
            resultados = resultados[resultados['compatibilidade_anos'].apply(lambda x: is_year_compatible(x, ano))]
        except ValueError:
            pass

    pecas_filtradas = resultados.to_dict('records')
    
    return render_template('index.html', pecas_filtradas=pecas_filtradas, form_values=request.form)

if __name__ == '__main__':
    app.run(debug=True)