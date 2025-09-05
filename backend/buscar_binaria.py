import pandas as pd
from bisect import bisect_left

df = pd.read_csv("motoparts.csv")
df = df.dropna(subset=["sku"])
df["sku"] = df["sku"].astype(int)

order = df["sku"].to_numpy().argsort()
skus_sorted = df["sku"].to_numpy()[order]

def find_by_sku(target):
    i = bisect_left(skus_sorted, target)
    if i < len(skus_sorted) and skus_sorted[i] == target:
        return df.iloc[order[i]].to_dict()
    return None

if __name__ == "__main__":
    target = int(input("Digite o SKU da peça que deseja buscar: "))
    result = find_by_sku(target)
    if result:
        print("Peça encontrada:")
        for k, v in result.items():
            print(f"{k}: {v}")
    else:
        print("SKU não encontrado.")
