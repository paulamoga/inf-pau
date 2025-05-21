import json
import os
import random


json_path = "date_casa_marcat.json"

if not os.path.exists(json_path):
    date = {
        "bancnote": [
            { "valoare": 50, "stoc": 20 },
            { "valoare": 20, "stoc": 30 },
            { "valoare": 10, "stoc": 40 },
            { "valoare": 5, "stoc": 50 },
            { "valoare": 1, "stoc": 100 }
        ],
        "produse": [
            { "nume": "Lapte", "pret": 7 },
            { "nume": "Paine", "pret": 3 },
            { "nume": "Ciocolata", "pret": 5 },
            { "nume": "Apa", "pret": 2 },
            { "nume": "Cafea", "pret": 9 }
        ]
    }

    with open(json_path, "w") as f:
        json.dump(date, f, indent=2)
    print("Fișierul JSON a fost generat.\n")


with open(json_path, "r") as f:
    data = json.load(f)

bancnote = sorted(data["bancnote"], key=lambda x: -x["valoare"])
produse = data["produse"]

stoc_bancnote = {b["valoare"]: b["stoc"] for b in bancnote}
valori_bancnote = [b["valoare"] for b in bancnote]


def calculeaza_rest(rest, stoc):
    dp = [None] * (rest + 1)
    dp[0] = {}

    for valoare in valori_bancnote:
        for suma in range(rest, -1, -1):
            if dp[suma] is not None:
                for k in range(1, stoc[valoare] + 1):
                    noua_suma = suma + valoare * k
                    if noua_suma > rest:
                        break
                    if dp[noua_suma] is None or sum(dp[noua_suma].values()) > sum(dp[suma].get(v, 0) for v in dp[suma]) + k:
                        dp[noua_suma] = dp[suma].copy()
                        dp[noua_suma][valoare] = dp[noua_suma].get(valoare, 0) + k

    return dp[rest]

# 4. Simularea
client = 1

while True:
    produs = random.choice(produse)
    pret = produs["pret"]
    suma_platita = random.randint(pret + 1, pret + 20)
    rest = suma_platita - pret

    print(f"\nClient {client}:")
    print(f"Produs cumpărat: {produs['nume']}")
    print(f"Preț: {pret} RON")
    print(f"Suma plătită: {suma_platita} RON")
    print(f"Rest de oferit: {rest} RON")

    combinatia = calculeaza_rest(rest, stoc_bancnote)

    if combinatia is None:
        print("\n⚠ Nu se poate oferi restul cu stocul disponibil.")
        print(" Simularea s-a oprit.")
        break

    print("Rest oferit cu bancnote:")
    for val, nr in sorted(combinatia.items(), reverse=True):
        print(f"  {nr} x {val} RON")
        stoc_bancnote[val] -= nr

    client += 1

# 5. Afișare stoc rămas
print("\n Stoc de bancnote rămas în sertar:")
for valoare in sorted(stoc_bancnote.keys(), reverse=True):
    print(f"  {valoare} RON: {stoc_bancnote[valoare]} bucăți")
