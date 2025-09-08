from bisect import bisect_left
import pandas as pd

df_sorted_sku = pd.DataFrame()
skus_sorted_list = []

def preparar_dados_para_busca_binaria(df_completo):
    """
    Prepara e armazena os dados ordenados necessários para a busca binária.
    Esta função deve ser chamada uma vez na inicialização da aplicação.
    """
    global df_sorted_sku, skus_sorted_list
    print("Preparando dados para a Busca Binária...")
    df_sorted_sku = df_completo.sort_values(by='SKU').reset_index(drop=True)
    skus_sorted_list = df_sorted_sku['SKU'].tolist()
    print("Dados para Busca Binária prontos.")

def buscar_por_prefixo_sku(prefixo):
    """
    Executa a BUSCA BINÁRIA para encontrar SKUs por prefixo.
    """
    if df_sorted_sku.empty: return []

    start_index = bisect_left(skus_sorted_list, prefixo)
    resultados = []
    for i in range(start_index, len(skus_sorted_list)):
        if skus_sorted_list[i].startswith(prefixo):
            resultados.append(df_sorted_sku.iloc[i].to_dict())
        else:
            break
    return resultados