import random
import csv
import argparse

# Lista culorilor posibile ale bomboanelor, 0 va fi folosit pentru celule goale
COLORS = [1, 2, 3, 4]  # coduri numerice pentru culori

# Dicționar care asociază tipul formațiunii cu scorul obținut
SCORES = {
    "LINE3": 5,        # linie de 3
    "LINE4": 10,       # linie de 4
    "LINE5": 50,       # linie de 5 sau mai mare
    "L": 20,           # formațiune în L
    "T": 30            # formațiune în T
}


# functti pt tabla
def random_board(rows, cols):
    # Creează o tablă rows x cols cu valori aleatoare din COLORS
    board = []               # inițializează tabla goală
    for r in range(rows):         # parcurge fiecare rând
        row = []           # creează un rând nou
        for c in range(cols):          # parcurge fiecare coloană
            row.append(random.choice(COLORS))  # adaugă o bomboană aleatoare
        board.append(row)        # adaugă rândul la tablă
    return board      # returnează tabla completă


def inside(r, c, rows, cols):

    #Verifică dacă poziția (r, c) este în interiorul tablei

    return 0 <= r < rows and 0 <= c < cols  # verifică limitele rândurilor și coloanelor

# DETECTARE LINII (3,4,5)
def detect_lines(board):

    #Detectează liniile orizontale și verticale de lungime >= 3
    rows = len(board)           # numărul de rânduri
    cols = len(board[0])        # numărul de coloane
    formations = []        # listă pentru formațiuni detectate

    # Linii orizontale
    for r in range(rows):      # parcurge fiecare rând
        c = 0        # începe de la prima coloană
        while c < cols:      # parcurge rândul
            if board[r][c] == 0:       # dacă celula este goală
                c += 1          # sari peste ea
                continue

            start = c        # marchează începutul secvenței
            value = board[r][c]        # valoarea culorii curente

            while c < cols and board[r][c] == value:  # continuă cât timp culoarea e aceeași
                c += 1

            length = c - start         # lungimea secvenței

            if length >= 3:            # dacă este o linie validă
                score = SCORES[f"LINE{min(length, 5)}"]  # scorul corespunzător
                cells = set()          # set cu celulele formațiunii
                for cc in range(start, c):
                    cells.add((r, cc)) # adaugă coordonatele
                formations.append((score, cells))  # salvează formațiunea

    # Linii verticale
    for c in range(cols):        # parcurge fiecare coloană
        r = 0                          # începe de sus
        while r < rows:
            if board[r][c] == 0:       # dacă celula este goală
                r += 1
                continue

            start = r         # începutul secvenței
            value = board[r][c]      # culoarea curentă

            while r < rows and board[r][c] == value:  # coboară cât timp culoarea e aceeași
                r += 1

            length = r - start     # lungimea secvenței

            if length >= 3:         # verifică dacă e linie validă
                score = SCORES[f"LINE{min(length, 5)}"]
                cells = set()
                for rr in range(start, r):
                    cells.add((rr, c))
                formations.append((score, cells))

    return formations       # returnează toate liniile găsite



# DETECTARE FORMAȚIUNI L ȘI T
def detect_L_T(board):
    #Detectează formațiunile de tip L și T (toate rotațiile)

    rows = len(board)        # numărul de rânduri
    cols = len(board[0])        # numărul de coloane
    formations = []         # listă de formațiuni

    for r in range(rows):        # parcurge tabla
        for c in range(cols):
            value = board[r][c]        # valoarea curentă
            if value == 0:       # ignoră celulele goale
                continue

            # Modele posibile pentru L
            L_patterns = [
                [(0,0),(1,0),(2,0),(0,1),(0,2)],
                [(0,0),(-1,0),(-2,0),(0,1),(0,2)],
                [(0,0),(1,0),(2,0),(0,-1),(0,-2)],
                [(0,0),(-1,0),(-2,0),(0,-1),(0,-2)]
            ]

            for pattern in L_patterns: # testează fiecare model L
                cells = set()
                ok = True
                for dr, dc in pattern:
                    rr = r + dr
                    cc = c + dc
                    if not inside(rr, cc, rows, cols) or board[rr][cc] != value:
                        ok = False
                        break
                    cells.add((rr, cc))
                if ok:
                    formations.append((SCORES["L"], cells))

            # Modele posibile pentru T
            T_patterns = [
                [(0,0),(0,-1),(0,1),(1,0),(2,0)],
                [(0,0),(0,-1),(0,1),(-1,0),(-2,0)],
                [(0,0),(-1,0),(1,0),(0,1),(0,2)],
                [(0,0),(-1,0),(1,0),(0,-1),(0,-2)]
            ]

            for pattern in T_patterns: # testează fiecare model T
                cells = set()
                ok = True
                for dr, dc in pattern:
                    rr = r + dr
                    cc = c + dc
                    if not inside(rr, cc, rows, cols) or board[rr][cc] != value:
                        ok = False
                        break
                    cells.add((rr, cc))
                if ok:
                    formations.append((SCORES["T"], cells))

    return formations      # returnează toate L și T detectate


def detect_all_formations(board):

    #Reunește toate formațiunile posibile
    return detect_lines(board) + detect_L_T(board)  # combină toate detecțiile


# REGULA ANTI-DUBLARE
def select_formations(formations):

    #Selectează formațiunile fără suprapuneri, prioritizând scorul mai mare

    formations.sort(key=lambda x: x[0], reverse=True)  # sortează descrescător după scor

    used_cells = set()      # celule deja folosite
    selected = []          # formațiuni selectate

    for score, cells in formations:
        if cells.isdisjoint(used_cells):  # verifică suprapunerea
            selected.append((score, cells))
            used_cells |= cells      # marchează celulele ca folosite

    return selected        # returnează formațiunile valide



# ELIMINARE, GRAVITAȚIE, REUMPLERE
def apply_elimination(board, selected):

    #Elimină celulele selectate și calculează scorul

    gained = 0         # scorul obținut în această eliminare
    for score, cells in selected:    # parcurge fiecare formațiune selectată
        gained += score     # adaugă scorul formațiunii
        for r, c in cells:      # parcurge fiecare celulă din formațiune
            board[r][c] = 0     # marchează celula ca fiind goală
    return gained           # returnează scorul total obținut


def apply_gravity(board):

    #Aplică gravitația pe fiecare coloană

    rows = len(board)          # numărul de rânduri
    cols = len(board[0])         # numărul de coloane

    for c in range(cols):      # parcurge fiecare coloană
        stack = []        # stivă temporară pentru bomboane
        for r in range(rows):    # parcurge coloana de sus în jos
            if board[r][c] != 0:     # dacă celula nu este goală
                stack.append(board[r][c])  # adaugă bomboana în stivă

        for r in range(rows - 1, -1, -1):  # reumple coloana de jos în sus
            if stack:               # dacă mai există bomboane
                board[r][c] = stack.pop()  # pune ultima bomboană
            else:
                board[r][c] = 0     # restul devin goale


def refill(board):

    #Umple celulele goale cu valori aleatoare

    for r in range(len(board)):      # parcurge toate rândurile
        for c in range(len(board[0])):  # parcurge toate coloanele
            if board[r][c] == 0:     # dacă celula este goală
                board[r][c] = random.choice(COLORS)  # pune o bomboană nouă



# CASCADĂ
def resolve_cascade(board):

    #Rezolvă toate cascările până la stabilizare

    total_score = 0     # scor total obținut
    cascades = 0       # numărul de cascade produse

    while True:               # rulează până nu mai apar formațiuni
        formations = detect_all_formations(board)  # detectează formațiuni
        selected = select_formations(formations)   # selectează formațiuni valide

        if not selected:       # dacă nu mai sunt formațiuni
            break        # oprește cascada

        total_score += apply_elimination(board, selected)  # elimină și adună scor
        apply_gravity(board)    # aplică gravitația
        refill(board)         # reumple celulele goale
        cascades += 1        # crește numărul de cascade

    return total_score, cascades     # returnează scorul și cascadele



# SWAP
def try_swap(board, r1, c1, r2, c2):

    #Încearcă un swap și verifică dacă produce formațiuni

    board[r1][c1], board[r2][c2] = board[r2][c2], board[r1][c1]  # face swap-ul

    valid = bool(detect_all_formations(board))  # verifică dacă apar formațiuni

    if not valid:   # dacă swap-ul nu e valid
        board[r1][c1], board[r2][c2] = board[r2][c2], board[r1][c1]  # revine

    return valid     # returnează dacă swap-ul e valid


def find_swap(board):

    #Caută primul swap valid (strategie simplă)

    rows = len(board)      # număr de rânduri
    cols = len(board[0])     # număr de coloane

    for r in range(rows):    # parcurge tabla
        for c in range(cols):
            for dr, dc in [(1, 0), (0, 1)]:  # verifică jos și dreapta
                rr = r + dr
                cc = c + dc
                if inside(rr, cc, rows, cols):  # dacă poziția e validă
                    if try_swap(board, r, c, rr, cc):  # încearcă swap
                        return True   # a găsit un swap valid
    return False      # nu există mutări valide



# JOC COMPLET
def play_game(game_id, target):
    board = random_board(11, 11)     # creează o tablă 11x11

    points = 0        # scorul curent
    swaps = 0       # numărul de mutări
    cascades = 0        # numărul total de cascade
    moves_to_target = ""    # mutări până la atingerea targetului

    p, c = resolve_cascade(board)    # rezolvă cascadele inițiale
    points += p
    cascades += c

    while points < target:      # rulează până se atinge scorul țintă
        if not find_swap(board):     # dacă nu mai există mutări
            return {    # jocul se termină
                "game_id": game_id,
                "points": points,
                "swaps": swaps,
                "cascades": cascades,
                "reached_target": False,
                "stopping_reason": "NO_MOVES",
                "moves_to_10000": ""
            }

        swaps += 1     # contorizează mutarea
        p, c = resolve_cascade(board)  # rezolvă cascada produsă
        points += p
        cascades += c

        if points >= target and moves_to_target == "":
            moves_to_target = swaps  # salvează mutarea la care s-a atins targetul

    return {      # joc finalizat cu succes
        "game_id": game_id,
        "points": points,
        "swaps": swaps,
        "cascades": cascades,
        "reached_target": True,
        "stopping_reason": "REACHED_TARGET",
        "moves_to_10000": moves_to_target
    }


def main():
    parser = argparse.ArgumentParser()     # creează parser de argumente
    parser.add_argument("--games", type=int, default=100)  # număr de jocuri
    parser.add_argument("--target", type=int, default=10000)  # scor țintă
    parser.add_argument("--out", default="results/summary.csv")  # fișier output
    args = parser.parse_args()             # parsează argumentele

    results = []       # listă cu rezultate
    for i in range(args.games):     # rulează jocurile
        results.append(play_game(i, args.target))

    with open(args.out, "w", newline="") as f:  # deschide fișierul CSV
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()      # scrie header-ul
        writer.writerows(results)      # scrie toate rezultatele


if __name__ == "__main__":
    main()                                 # pornește programul
