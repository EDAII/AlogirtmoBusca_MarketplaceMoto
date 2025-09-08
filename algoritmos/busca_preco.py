import pandas as pd

df_completo = pd.DataFrame()

def preparar_dados_para_busca_preco(df_original):

    global df_completo
    df_completo = df_original
    print("Dados para busca por preço prontos.")

def buscar_por_faixa_preco(preco_min=None, preco_max=None):

    if df_completo.empty:
        return []
    
    if preco_min is not None and preco_min != '':
        try:
            preco_min = float(preco_min)
            df_filtrado = df_completo[df_completo['Preco_Recomendado'] >= preco_min]
        except (ValueError, TypeError):
            df_filtrado = df_completo
    else:
        df_filtrado = df_completo
    
    if preco_max is not None and preco_max != '':
        try:
            preco_max = float(preco_max)
            df_filtrado = df_filtrado[df_filtrado['Preco_Recomendado'] <= preco_max]
        except (ValueError, TypeError):
            pass
    
    df_filtrado = df_filtrado[df_filtrado['Estoque'] > 0]
    
    df_filtrado = df_filtrado.sort_values('Preco_Recomendado')
    
    return df_filtrado.to_dict('records')

def buscar_por_faixa_preco_com_filtros(preco_min=None, preco_max=None, filtros_peca=None):
    """
    Executa a busca por faixa de preço combinada com filtros de peça.
    
    Args:
        preco_min (float): Preço mínimo (opcional)
        preco_max (float): Preço máximo (opcional)
        filtros_peca (dict): Filtros de peça (marca, modelo, etc.)
    
    Returns:
        list: Lista de peças que atendem aos critérios de preço e filtros
    """
    if df_completo.empty:
        return []
    
    df_filtrado = df_completo.copy()
    
    # Aplicar filtros de peça primeiro
    if filtros_peca:
        for campo, valor in filtros_peca.items():
            if valor and valor != '':
                if campo == 'Ano':
                    df_filtrado = df_filtrado[df_filtrado[campo] == int(valor)]
                else:
                    df_filtrado = df_filtrado[df_filtrado[campo].str.lower() == str(valor).lower()]
    
    # Aplicar filtros de preço
    if preco_min is not None and preco_min != '':
        try:
            preco_min = float(preco_min)
            df_filtrado = df_filtrado[df_filtrado['Preco_Recomendado'] >= preco_min]
        except (ValueError, TypeError):
            pass
    
    if preco_max is not None and preco_max != '':
        try:
            preco_max = float(preco_max)
            df_filtrado = df_filtrado[df_filtrado['Preco_Recomendado'] <= preco_max]
        except (ValueError, TypeError):
            pass
    
    # Filtrar apenas peças com estoque > 0
    df_filtrado = df_filtrado[df_filtrado['Estoque'] > 0]
    
    # Ordenar por preço (menor para maior)
    df_filtrado = df_filtrado.sort_values('Preco_Recomendado')
    
    return df_filtrado.to_dict('records')

def obter_estatisticas_preco():
    if df_completo.empty:
        return {}
    
    precos = df_completo['Preco_Recomendado']
    
    return {
        'preco_min': float(precos.min()),
        'preco_max': float(precos.max()),
        'preco_medio': float(precos.mean()),
        'preco_mediano': float(precos.median()),
        'total_pecas': len(df_completo)
    }
