from flask import Flask, render_template, request, jsonify
import pandas as pd
from bisect import bisect_left

# Inicializa a aplicação Flask
app = Flask(__name__, template_folder='../templates')

# Carrega e prepara os dados do CSV
try:
    # CORREÇÃO APLICADA AQUI:
    df = pd.read_csv("../motoparts.csv") 
    df = df.dropna(subset=["sku"])
    df["sku"] = df["sku"].astype(int)

    # Ordena os dados pelo SKU para a busca binária
    order = df["sku"].to_numpy().argsort()
    skus_sorted = df["sku"].to_numpy()[order]
except FileNotFoundError:
    print("Erro: O arquivo motoparts.csv não foi encontrado.")
    df = pd.DataFrame() # Cria um DataFrame vazio para evitar erros
    skus_sorted = []
    order = []


# --- Funções de Busca ---
def find_by_sku(target):
    """
    Encontra um item pelo SKU usando busca binária.
    """
    i = bisect_left(skus_sorted, target)
    if i < len(skus_sorted) and skus_sorted[i] == target:
        return df.iloc[order[i]].to_dict()
    return None

# --- Rotas da Aplicação ---
@app.route('/')
def index():
    """
    Renderiza a página inicial.
    """
    return render_template('index.html')

@app.route('/buscar', methods=['POST'])
def buscar():
    """
    Recebe um SKU do formulário e retorna o resultado da busca.
    """
    try:
        sku_buscado = int(request.form['sku'])
        resultado = find_by_sku(sku_buscado)
        if resultado:
            return render_template('index.html', peca=resultado, sku_buscado=sku_buscado)
        else:
            return render_template('index.html', erro="Peça não encontrada.", sku_buscado=sku_buscado)
    except (ValueError, KeyError):
        return render_template('index.html', erro="SKU inválido.")

if __name__ == '__main__':
    app.run(debug=True)