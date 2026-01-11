import random          # pentru generarea aleatoare a bomboanelor
import csv             # pentru scrierea rezultatelor în fișier CSV
import argparse        # pentru parametri din linia de comandă

# Culorile posibile ale bomboanelor
# 0 este rezervat pentru celule goale
COLORS = [1, 2, 3, 4]

# Dicționar cu scorurile pentru fiecare tip de formațiune
SCORES = {
    "LINE3": 5,
    "LINE4": 10,
    "LINE5": 50,
    "L": 20,
    "T": 30
}

# --------------------------------------------------
# FUNCȚII UTILITARE PENTRU TABLĂ
# --------------------------------------------------

def random_board(rows, cols):
    """
    Creează o tablă rows x cols cu valori aleatoare din {1,2,3,4}
    """
    board = []
    for r in range(rows):
        row = []
        for c in range(cols):
            row.append(random.choice(COLORS))
        board.append(row)
    return board


def inside(r, c, rows, cols):
    """
    Verifică dacă o poziție (r,c) este în interiorul tablei
    """
    return 0 <= r < rows and 0 <= c < cols


# --------------------------------------------------
# DETECTARE LINII (3,4,5)
# --------------------------------------------------

def detect_lines(board):
    """
    Detectează liniile orizontale și verticale de lungime >= 3
    """
    rows = len(board)
    cols = len(board[0])
    formations = []

    # Linii orizontale
    for r in range(rows):
        c = 0
        while c < cols:
            if board[r][c] == 0:
                c += 1
                continue

            start = c
            value = board[r][c]

            # mergem spre dreapta cât timp culoarea este aceeași
            while c < cols and board[r][c] == value:
                c += 1

            length = c - start

            if length >= 3:
                score = SCORES[f"LINE{min(length, 5)}"]
                cells = set()
                for cc in range(start, c):
                    cells.add((r, cc))
                formations.append((score, cells))

    # Linii verticale
    for c in range(cols):
        r = 0
        while r < rows:
            if board[r][c] == 0:
                r += 1
                continue

            start = r
            value = board[r][c]

            # mergem în jos cât timp culoarea este aceeași
            while r < rows and board[r][c] == value:
                r += 1

            length = r - start

            if length >= 3:
                score = SCORES[f"LINE{min(length, 5)}"]
                cells = set()
                for rr in range(start, r):
                    cells.add((rr, c))
                formations.append((score, cells))

    return formations


# --------------------------------------------------
# DETECTARE FORMAȚIUNI L ȘI T
# --------------------------------------------------

def detect_L_T(board):
    """
    Detectează formațiunile de tip L și T (toate rotațiile)
    """
    rows = len(board)
    cols = len(board[0])
    formations = []

    for r in range(rows):
        for c in range(cols):
            value = board[r][c]
            if value == 0:
                continue

            # Modele pentru L
            L_patterns = [
                [(0,0),(1,0),(2,0),(0,1),(0,2)],
                [(0,0),(-1,0),(-2,0),(0,1),(0,2)],
                [(0,0),(1,0),(2,0),(0,-1),(0,-2)],
                [(0,0),(-1,0),(-2,0),(0,-1),(0,-2)]
            ]

            for pattern in L_patterns:
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

            # Modele pentru T
            T_patterns = [
                [(0,0),(0,-1),(0,1),(1,0),(2,0)],
                [(0,0),(0,-1),(0,1),(-1,0),(-2,0)],
                [(0,0),(-1,0),(1,0),(0,1),(0,2)],
                [(0,0),(-1,0),(1,0),(0,-1),(0,-2)]
            ]

            for pattern in T_patterns:
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

    return formations


def detect_all_formations(board):
    """
    Reunește toate formațiunile posibile
    """
    return detect_lines(board) + detect_L_T(board)


# --------------------------------------------------
# REGULA ANTI-DUBLARE
# --------------------------------------------------

def select_formations(formations):
    """
    Selectează formațiunile fără suprapuneri,
    prioritizând scorul mai mare
    """
    formations.sort(key=lambda x: x[0], reverse=True)

    used_cells = set()
    selected = []

    for score, cells in formations:
        if cells.isdisjoint(used_cells):
            selected.append((score, cells))
            used_cells |= cells

    return selected


# --------------------------------------------------
# ELIMINARE, GRAVITAȚIE, REUMPLERE
# --------------------------------------------------

def apply_elimination(board, selected):
    """
    Elimină celulele selectate și calculează scorul
    """
    gained = 0
    for score, cells in selected:
        gained += score
        for r, c in cells:
            board[r][c] = 0
    return gained


def apply_gravity(board):
    """
    Aplică gravitația pe fiecare coloană
    """
    rows = len(board)
    cols = len(board[0])

    for c in range(cols):
        stack = []
        for r in range(rows):
            if board[r][c] != 0:
                stack.append(board[r][c])

        for r in range(rows-1, -1, -1):
            if stack:
                board[r][c] = stack.pop()
            else:
                board[r][c] = 0


def refill(board):
    """
    Umple celulele goale cu valori aleatoare
    """
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == 0:
                board[r][c] = random.choice(COLORS)


# --------------------------------------------------
# CASCADĂ
# --------------------------------------------------

def resolve_cascade(board):
    """
    Rezolvă toate cascările până la stabilizare
    """
    total_score = 0
    cascades = 0

    while True:
        formations = detect_all_formations(board)
        selected = select_formations(formations)

        if not selected:
            break

        total_score += apply_elimination(board, selected)
        apply_gravity(board)
        refill(board)
        cascades += 1

    return total_score, cascades


# --------------------------------------------------
# SWAP
# --------------------------------------------------

def try_swap(board, r1, c1, r2, c2):
    """
    Încearcă un swap și verifică dacă produce formațiuni
    """
    board[r1][c1], board[r2][c2] = board[r2][c2], board[r1][c1]

    valid = bool(detect_all_formations(board))

    if not valid:
        board[r1][c1], board[r2][c2] = board[r2][c2], board[r1][c1]

    return valid


def find_swap(board):
    """
    Caută primul swap valid (strategie simplă)
    """
    rows = len(board)
    cols = len(board[0])

    for r in range(rows):
        for c in range(cols):
            for dr, dc in [(1,0),(0,1)]:
                rr = r + dr
                cc = c + dc
                if inside(rr, cc, rows, cols):
                    if try_swap(board, r, c, rr, cc):
                        return True
    return False


# --------------------------------------------------
# JOC COMPLET
# --------------------------------------------------

def play_game(game_id, target):
    board = random_board(11, 11)

    points = 0
    swaps = 0
    cascades = 0
    moves_to_target = ""

    p, c = resolve_cascade(board)
    points += p
    cascades += c

    while points < target:
        if not find_swap(board):
            return {
                "game_id": game_id,
                "points": points,
                "swaps": swaps,
                "cascades": cascades,
                "reached_target": False,
                "stopping_reason": "NO_MOVES",
                "moves_to_10000": ""
            }

        swaps += 1
        p, c = resolve_cascade(board)
        points += p
        cascades += c

        if points >= target and moves_to_target == "":
            moves_to_target = swaps

    return {
        "game_id": game_id,
        "points": points,
        "swaps": swaps,
        "cascades": cascades,
        "reached_target": True,
        "stopping_reason": "REACHED_TARGET",
        "moves_to_10000": moves_to_target
    }


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--games", type=int, default=100)
    parser.add_argument("--target", type=int, default=10000)
    parser.add_argument("--out", default="results/summary.csv")
    args = parser.parse_args()

    results = []
    for i in range(args.games):
        results.append(play_game(i, args.target))

    with open(args.out, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)


if __name__ == "__main__":
    main()
