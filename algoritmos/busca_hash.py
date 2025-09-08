from collections import defaultdict
import pandas as pd

df_completo = pd.DataFrame()
indices_hash = {
    "Marca": defaultdict(list),
    "Modelo": defaultdict(list),
    "Ano": defaultdict(list),
    "Categoria_Peca": defaultdict(list)
}

def preparar_indices_hash(df_original):
    """
    Cria e armazena os índices de hash a partir do DataFrame.
    Esta função deve ser chamada uma vez na inicialização da aplicação.
    """
    global df_completo
    df_completo = df_original
    
    print("Criando índices de Hash...")
    for index, peca in df_completo.iterrows():
        indices_hash["Marca"][str(peca["Marca"]).lower()].append(index)
        indices_hash["Modelo"][str(peca["Modelo"]).lower()].append(index)
        indices_hash["Ano"][str(peca["Ano"])].append(index)
        indices_hash["Categoria_Peca"][str(peca["Categoria_Peca"]).lower()].append(index)
    print("Índices de Hash prontos.")

def buscar_por_filtros_hash(filtros):
    """
    Executa a BUSCA POR HASHING usando múltiplos filtros (VERSÃO CORRIGIDA).
    """
    # Cria uma lista apenas com os filtros que o usuário realmente preencheu
    filtros_ativos = {chave: valor for chave, valor in filtros.items() if valor}

    # Se nenhum filtro foi usado, não há o que buscar
    if not filtros_ativos:
        return []

    # Pega o primeiro filtro para iniciar o nosso conjunto de resultados
    primeira_chave, primeiro_valor = next(iter(filtros_ativos.items()))
    
    lookup_value = str(primeiro_valor).lower() if primeira_chave != 'Ano' else str(primeiro_valor)
    
    # Se o primeiro filtro já não encontrar nada, o resultado final é zero
    if lookup_value not in indices_hash[primeira_chave]:
        return []
    
    # Inicia o conjunto de resultados com os índices do primeiro filtro
    indices_finais = set(indices_hash[primeira_chave][lookup_value])
    
    # Remove o primeiro filtro da lista para não o processarmos duas vezes
    filtros_ativos.pop(primeira_chave)

    # Agora, itera sobre os filtros RESTANTES
    for chave, valor in filtros_ativos.items():
        lookup_value = str(valor).lower() if chave != 'Ano' else str(valor)

        # Se um dos filtros não encontrar nada, o resultado final tem que ser zero
        if lookup_value not in indices_hash[chave]:
            return []

        # Pega os índices do filtro atual
        indices_candidatos = set(indices_hash[chave][lookup_value])
        
        # ATUALIZA o conjunto de resultados, mantendo apenas os itens
        # que também existem no novo conjunto (operação de INTERSEÇÃO).
        indices_finais.intersection_update(indices_candidatos)

        # Otimização: Se em algum momento a interseção zerar, já podemos parar
        if not indices_finais:
            return []
            
    if not indices_finais:
        return []

    resultados_df = df_completo.iloc[list(indices_finais)]
    return resultados_df[resultados_df['Estoque'] > 0].to_dict('records')