import random
import re #pt a extrage cuvinte formate doar din litere
import csv
import time

# Incarcam dictionarul dintr-un fisier txt
def incarca_dictionar(fisier_txt):
    cuvinte = []
    with open(fisier_txt, encoding='utf-8') as f: #codoare UTF-8 pentru diacritice
        for linie in f: #parcurge fiecare linie
            linie = linie.strip().upper() #elimina spatile si transforma in majuscule
            for cuv in re.findall(r"[A-ZĂÂÎȘȚ]+", linie): #gaseste toate cuvintele scrise cu majuscule
                if len(cuv) > 1: #cauta cuvintele ce sunt mai lungi de un singur caracter
                    if cuv not in cuvinte:
                        cuvinte.append(cuv) # adauga cuvantul in lista daca acesta nu ii deka acolo

    return cuvinte


# incarcare din fisierul cuvinte_de_verificat.csv
def incarca_cuvinte_de_test(fisier):
    lista = []
    with open(fisier, encoding='utf-8') as f: #deschide fisierul csv
        for linie in f:
            parti = linie.strip().split(';')#curata spatiile si imparte dupa saparatorul ;
            if len(parti) == 3: #se verifica ca linia are 3 elemente
                nr = parti[0].strip()
                forma = parti[1].strip()
                cuv = parti[2].strip().upper()
                lista.append((nr, forma, cuv))

    return lista


# verifica daca exista cuvinte ce se potrivesc cu modelul cuvantului de verificat
def filtreaza_cuvinte(model, dictionar):
    model = model.upper()
    potriviri = [] #creeaza o lista unde se vor pune cuvintele ce se potrives cu modelil
    for cuvant in dictionar: #ia fiecare cuvant potrivit pe rand
        if len(cuvant) != len(model): #daca lungimea modelului cu cuvantul nu se potriveste sare peste el
            continue
        ok = True
        for i in range(len(model)):
            if model[i] != '*' and model[i] != cuvant[i]:
                ok = False
                break #daca are o litera care modelul nu o are ca * atunci opreste bucla si trece la urmatorul
        if ok:
            potriviri.append(cuvant) # daca se potriveste se adauga in lista
    return potriviri


def joaca_automat(model, cuv_corect, dictionar):
    stare = list(model.upper()) #transforma modelul in lista de caractere
    litere_incercate = [] # se salveaza fiecare litera incercata
    incercari = 0


    while "*" in stare:
        candidati = filtreaza_cuvinte("".join(stare), dictionar) #foloseste filtreaza cuvinte ca sa gaseasca potrivirile din dictionar
        if not candidati:
            break

        # frecventa literelor in candidati
        frecvente = {}
        for cuv in candidati:
            for litera in cuv:
                if litera not in litere_incercate:
                    if litera not in frecvente:
                        frecvente[litera] = 1
                    else:
                        frecvente[litera] += 1 #adauga literele in frecvente daca nu o fost incercata, daca o fost ii mareste frecventa

        if not frecvente:
            break

        litera = max(frecvente, key=frecvente.get)

        litere_incercate.append(litera)
        incercari += 1 #adauga litera aleasa in litere incercate si creste contorul

        # daca litera este in cuvant, o completam
        if litera in cuv_corect:
            for i in range(len(cuv_corect)):
                if cuv_corect[i] == litera:
                    stare[i] = litera #dca litera se potriveste se inlocuieste in toate pozitiile in care apare

        # afișează toate literele încercate și numărul încercării
        print(f"Încercarea {incercari}: {' '.join(litere_incercate)}")

        # verificare finala
        if "".join(stare) == cuv_corect: #daca s-o gasit cuvantul se opreste bucla
            break

    # mesaj final
    if "".join(stare) == cuv_corect:
        print(f"Cuvântul '{cuv_corect}' a fost ghicit în {incercari} încercări!\n")
    else:
        print(f"Nu s-a reușit ghicirea cuvântului '{cuv_corect}'. Litere încercate: {' '.join(litere_incercate)}\n")

    return "".join(stare), incercari


if __name__ == "__main__":
    start_time = time.time()  # pornim cronometrarea
#incarcam dictionarul si lista de cuvinte
    dict_rom = incarca_dictionar("loc-dif-flexiuni-5.0-6.0.txt")
    teste = incarca_cuvinte_de_test("cuvinte_de_verificat.csv")

    rezultate = []
    total = 0
    corecte = 0

    for _ in range(100):
        print("--------------------------------------------------------")
        nr, forma, cuv = random.choice(teste)
        rezultat, inc = joaca_automat(forma, cuv, dict_rom)

        if rezultat == cuv:
            corecte += 1
        total += inc

        rezultate.append({
            "Nr": nr,
            "Forma": forma,
            "Cuvant_corect": cuv,
            "Rezultat": rezultat,
            "Corect": "DA" if rezultat == cuv else "NU",
            "Incercari": inc
        })

        print(f"{nr}) {forma} -> {rezultat} ({'OK' if rezultat == cuv else 'gresit'}) in {inc} incercari")

    # salvare rezultate in fisier csv
    with open("rezultate/rezultate_test.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Nr", "Forma", "Cuvant_corect", "Rezultat", "Corect", "Incercari"])
        writer.writeheader()
        writer.writerows(rezultate)

    # oprim cronometrarea
    end_time = time.time()
    durata_secunde = end_time - start_time

    print("\nREZUMAT:")
    print("Cuvinte corecte:", corecte)
    print("Total incercari:", total)
    print("Media per cuvant:", total / 100)
    print(f"Timp total de rulare: {durata_secunde:.2f} secunde")