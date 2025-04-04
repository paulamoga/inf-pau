import csv
import random
from collections import defaultdict
import time

# Dicționar cu județele și codurile lor corespunzătoare
judete_coduri = {
    '01': 'Alba', '02': 'Arad', '03': 'Argeș', '04': 'Bacău', '05': 'Bihor', '06': 'Bistrița-Năsăud',
    '07': 'Botoșani', '08': 'Brașov', '09': 'Brăila', '10': 'Buzău', '11': 'Caraș-Severin', '12': 'Călărași',
    '13': 'Cluj', '14': 'Constanța', '15': 'Covasna', '16': 'Dâmbovița', '17': 'Dolj', '18': 'Galați',
    '19': 'Giurgiu', '20': 'Gorj', '21': 'Harghita', '22': 'Hunedoara', '23': 'Ialomița', '24': 'Iași',
    '25': 'Ilfov', '26': 'Maramureș', '27': 'Mehedinți', '28': 'Mureș', '29': 'Neamț', '30': 'Olt',
    '31': 'Prahova', '32': 'Satu Mare', '33': 'Sălaj', '34': 'Sibiu', '35': 'Suceava', '36': 'Teleorman',
    '37': 'Timiș', '38': 'Tulcea', '39': 'Vaslui', '40': 'Vâlcea', '41': 'Vrancea', '42': 'Municipiul București',
    '43': 'Județul X', '44': 'Județul Y', '45': 'Județul Z', '50': 'Județul 50', '51': 'Judetul 51', '52': 'Judetul 52',
    '60': 'Județul 60', '61': 'Județul 61', '62': 'Judetul 62'
}

# Funcție pentru curățarea fișierului CSV și păstrarea doar a două coloane (CNP și Nume)
with open('cnp_data.csv', mode='r', newline='') as csv_file:
    reader = csv.reader(csv_file)
    cleaned_data = [(row[0].strip(), row[1].strip()) for row in reader if len(row) >= 2]

# Salvarea fișierului curățat
with open('cnp_data_cleaned.csv', mode='w', newline='') as clean_file:
    writer = csv.writer(clean_file)
    writer.writerows(cleaned_data)


# HashTable cu funcție de hash
class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(size)]

    def hash_function(self, cnp):
        hash_value = 0
        prime = 31
        for digit in cnp:
            hash_value = (hash_value * prime + int(digit)) % self.size
        return hash_value

    def insert(self, cnp, name):
        index = self.hash_function(cnp)
        self.table[index].append((cnp, name))

    def search(self, cnp):
        index = self.hash_function(cnp)
        for i, (stored_cnp, name) in enumerate(self.table[index]):
            if stored_cnp == cnp:
                return i + 1, name
        return -1, None


# Crearea tabelului hash
hash_table = HashTable(50000000)

# Citirea din fișierul curățat și inserarea în hash table
with open('cnp_data_cleaned.csv', mode='r', newline='') as csv_file:
    reader = csv.reader(csv_file)
    for cnp, name in reader:
        hash_table.insert(cnp, name)

# Selecția aleatorie a 1000 de CNP-uri pentru căutare
selected_cnp_list = random.sample(range(len(cleaned_data)), 1000)

# Dicționar pentru distribuția pe vârste și sexe
distribution = defaultdict(lambda: {'M': {"14-18": 0, "18-22": 0, "22+": 0}, 'F': {"14-18": 0, "18-22": 0, "22+": 0}})
county_distribution = defaultdict(int)

# Variabila pentru totalul iterațiilor
total_iterations = 0

# Măsurarea timpului de căutare
start_time = time.time()

# Căutarea CNP-urilor și calculul distribuției
with open('cnp_data_cleaned.csv', mode='r', newline='') as csv_file:
    reader = list(csv.reader(csv_file))
    for cnp_index in selected_cnp_list:
        if cnp_index >= len(reader):
            continue
        cnp, name = reader[cnp_index]

        # Verificarea județului din CNP
        county_code = cnp[:2]
        county_name = judete_coduri.get(county_code, "Necunoscut")

        # Dacă județul este necunoscut, afișăm un mesaj pentru depanare
        if county_name == "Necunoscut":
            print(f"Cod județ necunoscut: {county_code} pentru CNP: {cnp}")

        sex = 'M' if cnp[0] in ['1', '5'] else 'F'
        birth_year = int("19" + cnp[1:3]) if cnp[0] in ['1', '2'] else int("20" + cnp[1:3])
        age = 2025 - birth_year

        if 14 <= age <= 18:
            category = "14-18"
        elif 18 < age <= 22:
            category = "18-22"
        else:
            category = "22+"

        # Incrementăm distribuția pe județ
        county_distribution[county_name] += 1

        # Incrementăm distribuția pe sex și categorie de vârstă
        distribution[county_name][sex][category] += 1

        # Căutăm CNP-ul în hash table și numărăm iterațiile
        iterations, _ = hash_table.search(cnp)

        # Adăugăm iterațiile la total
        total_iterations += iterations

# Măsurarea timpului de căutare
end_time = time.time()

# Afișarea rezultatului
print("\nDistribuția populației selectate după județ, sex și categorie de vârstă:\n")
for county, data in distribution.items():
    print(f"Județ: {county} (Total persoane: {county_distribution[county]})")
    for sex, ages in data.items():
        print(f"  Sex: {sex}")
        for age_category, count in ages.items():
            print(f"    {age_category} ani: {count} persoane")
    print("-" * 50)

# Timpul total de căutare
search_time = end_time - start_time
print(f"Timpul total de căutare pentru 1000 de CNP-uri: {search_time:.4f} secunde")
print(f"Numărul total de iterații: {total_iterations}")
