meniu = ['papanasi'] * 10 + ['ceafa'] * 3 + ["guias"] * 6
preturi = [["papanasi", 7], ["ceafa", 10], ["guias", 5]]
studenti = ["Liviu", "Ion", "George", "Ana", "Florica"]  # coada FIFO
comenzi = ["guias", "ceafa", "ceafa", "papanasi", "ceafa"]  # coada FIFO
tavi = ["tava"] * 7  # stiva LIFO
istoric_comenzi = []
portii =[]

for i in range(len(studenti)) :
    student = studenti.pop(0)
    comanda=comenzi.pop(0)
    print(f"Studentul {student} a comandat {comanda}")
    tavi.pop()
    istoric_comenzi.append([student, comanda])
    portii.append(comanda)

print(istoric_comenzi)

papanasi_comenzi = portii.count('papanasi')
ceafa_coemenzi = portii.count("ceafa")
guias_comenzi = portii.count("guias")
print(f"S-au comandat {papanasi_comenzi} papanasi, {ceafa_coemenzi} ceafa, {guias_comenzi} guias.")

numar_papanasi = meniu.count("papanasi") - papanasi_comenzi
if numar_papanasi>0:
    print("Mai sunt papanasi: True")
else:
    print("Mai sunt papansi: False")

numar_ceafa = meniu.count("ceafa") - ceafa_coemenzi
if numar_ceafa>0:
    print("Mai este ceafa: True")
else:
    print("Mai este ceafa: False")

numar_guias = meniu.count("guias") - guias_comenzi
if numar_guias>0:
    print("Mai sunt guias: True")
else:
    print("Mai sunt guias: False")

produse_papansi = []
produse_ceafa = []
produse_guias = []

preturi_papanasi = preturi[0]
preturi_papanasi = preturi_papanasi[1]

pret_mare = 7
if pret_mare <= preturi_papanasi:
    produse_papanasi = preturi[0]

bani_finali = papanasi_comenzi *  preturi_papanasi

preturi_ceafa = preturi[1]
preturi_ceafa = preturi_ceafa[1]

pret_mare = 7
if pret_mare >= preturi_ceafa:
    produse_ceafa = preturi[1]

bani_finali = bani_finali + ceafa_coemenzi * preturi_ceafa

preturi_guias = preturi[2]
preturi_guias = preturi_guias[1]

pret_mare = 7
if pret_mare >= preturi_guias:
    produse_guias = preturi[2]

bani_finali = bani_finali + guias_comenzi * preturi_guias
print(f"Cantina a încasat: {bani_finali} lei")

sub_7 =[]
sub_7 = produse_guias + produse_papanasi + produse_ceafa
print(f"Produse care costă cel mult 7 lei: {sub_7}")
