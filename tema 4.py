import random
cuvinte = ["python", "programare", "calculator", "date", "algoritm"]
cuvant_de_ghicit = random.choice(cuvinte)
progres = ["_" for _ in cuvant_de_ghicit]

incercari_ramase = 6
litere_incercate = []

de_afisat = " ".join(progres)
print(f"Cuvantul ii: {de_afisat}")

ghicit = False

while ghicit or incercari_ramase > 0:
   litera_introdusa = input("Introduceti o litera ")
   litere_incercate.append(litera_introdusa)
   if not litera_introdusa.isalpha():
       print("Nu este o litera, introdu o litera valida")
   else:
       if litera_introdusa in cuvant_de_ghicit:
         for i in range(len(cuvant_de_ghicit)):
          if  cuvant_de_ghicit[i] == litera_introdusa:
              progres[i] = litera_introdusa
       else:
           incercari_ramase = incercari_ramase - 1
           print(f"Au mai ramas {incercari_ramase} incercari")

   print(" ".join(progres))
   if cuvant_de_ghicit == "".join(progres):
       ghicit = True
       break


if ghicit:
    print("Felicitari! Ai ghicit cuvantul")
else:
    print(f"Nu mai ai ncercari, cuvantul era {cuvant_de_ghicit}")



