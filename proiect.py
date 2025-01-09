import tkinter as tk
from tkinter import ttk
import random
import time
import threading

# Variabile globale pentru lista și dreptunghiurile
lista = []
rects = []

# Variabila globală de control pentru oprirea sortării
stop_sorting = False

# Funcție pentru a opri sortarea
def stop_sortare():
    global stop_sorting
    stop_sorting = True

# Funcție pentru a relua sortarea
def relua_sortare(canvas, speed, sort_function):
    global stop_sorting
    stop_sorting = False  # Resetează variabila de oprire
    sort_function(canvas, lista, rects, speed)  # Reluăm sortarea

def animatie_sortare(canvas, lista, rects, speed, sort_function):
    sort_function(canvas, lista, rects, speed)
    for rect in rects:
        canvas.itemconfig(rect, fill="pink")  # Finalizare, toate barele devin roz
    canvas.update()

# Implementare Bubble Sort cu animație
def bubble_sort(canvas, lista, rects, speed):
    n = len(lista)
    for i in range(n):
        if stop_sorting:
            break
        for j in range(n - i - 1):
            if stop_sorting:
                break
            # Evidențiază elementele comparate
            canvas.itemconfig(rects[j], fill="purple")
            canvas.itemconfig(rects[j + 1], fill="purple")
            canvas.update()
            time.sleep(speed)

            if lista[j] > lista[j + 1]:
                # Schimbă valorile
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
                # Schimbă pozițiile vizuale ale barelor
                canvas.coords(rects[j], j * 10, 300 - lista[j], (j + 1) * 10, 300)
                canvas.coords(rects[j + 1], (j + 1) * 10, 300 - lista[j + 1], (j + 2) * 10, 300)

            # Revine la culoarea implicită
            canvas.itemconfig(rects[j], fill="blue")
            canvas.itemconfig(rects[j + 1], fill="blue")
            canvas.update()
            time.sleep(speed)

# Implementare Insertion Sort cu animație
def insertion_sort(canvas, lista, rects, speed):
    n = len(lista)
    for i in range(1, n):
        if stop_sorting:
            break
        key = lista[i]
        j = i - 1

        # Evidențiază elementul curent
        canvas.itemconfig(rects[i], fill="red")
        canvas.update()
        time.sleep(speed)

        while j >= 0 and key < lista[j]:
            if stop_sorting:
                break
            lista[j + 1] = lista[j]

            # Mută barele în pozițiile corespunzătoare vizual
            canvas.coords(rects[j + 1], (j + 1) * 10, 300 - lista[j + 1], (j + 2) * 10, 300)
            canvas.itemconfig(rects[j + 1], fill="yellow")

            j -= 1
            canvas.update()
            time.sleep(speed)

        lista[j + 1] = key

        # Mută elementul curent în poziția sa corectă
        canvas.coords(rects[j + 1], (j + 1) * 10, 300 - lista[j + 1], (j + 2) * 10, 300)
        canvas.itemconfig(rects[j + 1], fill="green")
        canvas.update()
        time.sleep(speed)

def selection_sort(canvas, lista, rects, speed):
    n = len(lista)
    for i in range(n):
        if stop_sorting:
            break
        min_idx = i
        for j in range(i + 1, n):
            if stop_sorting:
                break
            # Evidențiază elementele comparate
            canvas.itemconfig(rects[j], fill="purple")
            canvas.itemconfig(rects[min_idx], fill="red")
            canvas.update()
            time.sleep(speed)

            if lista[j] < lista[min_idx]:
                min_idx = j

            # Revine la culoarea implicită
            canvas.itemconfig(rects[j], fill="blue")

        # Schimbă valorile
        lista[i], lista[min_idx] = lista[min_idx], lista[i]
        canvas.coords(rects[i], i * 10, 300 - lista[i], (i + 1) * 10, 300)
        canvas.coords(rects[min_idx], min_idx * 10, 300 - lista[min_idx], (min_idx + 1) * 10, 300)
        canvas.itemconfig(rects[i], fill="green")
        canvas.update()
        time.sleep(speed)

# Generarea unei liste și desenarea inițială a barelor
def deseneaza_lista(canvas, num_elements):
    global lista, rects
    canvas.delete("all")
    lista = [random.randint(20, 300) for _ in range(num_elements)]
    rects = []
    width = canvas.winfo_width() // num_elements
    for i, val in enumerate(lista):
        height = val
        x1 = i * width
        y1 = canvas.winfo_height() - height
        x2 = (i + 1) * width
        y2 = canvas.winfo_height()
        rect = canvas.create_rectangle(x1, y1, x2, y2, fill="green")
        rects.append(rect)
    return lista, rects

# Fereastra pentru un algoritm de sortare specific
def deschide_fereastra(optiune):
    fereastra = tk.Toplevel()
    fereastra.title(f"Sortare: {optiune}")

    # Canvas pentru animație
    canvas = tk.Canvas(fereastra, width=800, height=300, bg="skyblue")
    canvas.pack(padx=10, pady=10)

    # Slider pentru numărul de elemente
    tk.Label(fereastra, text="Numărul de elemente:").pack(pady=5)
    num_slider = ttk.Scale(fereastra, from_=5, to=100, orient="horizontal")
    num_slider.set(20)
    num_slider.pack()
    num_value_label = tk.Label(fereastra, text=f"{int(num_slider.get())}")
    num_value_label.pack(pady=5)

    def update_num_label(event):
        num_value_label.config(text=f"{num_slider.get()}")

    num_slider.bind("<Motion>", update_num_label)

    # Slider pentru viteza animației
    tk.Label(fereastra, text="Viteza animației (s):").pack(pady=5)
    speed_slider = ttk.Scale(fereastra, from_=0.001, to=1, orient="horizontal")
    speed_slider.set(0.1)
    speed_slider.pack()
    speed_value_label = tk.Label(fereastra, text=f"{speed_slider.get():.2f}s")
    speed_value_label.pack(pady=5)

    def update_speed_label(event):
        speed_value_label.config(text=f"{speed_slider.get():.2f}s")

    speed_slider.bind("<Motion>", update_speed_label)

    # Funcție pentru a inițializa și începe sortarea
    def init_sortare():
        global stop_sorting
        stop_sorting = False  # Resetează variabila de oprire la fiecare sortare
        num_elements = int(num_slider.get())
        speed = speed_slider.get()
        deseneaza_lista(canvas, num_elements)

        if optiune == "Bubble Sort":
            animatie_sortare(canvas, lista, rects, speed, bubble_sort)
        elif optiune == "Insertion Sort":
            animatie_sortare(canvas, lista, rects, speed, insertion_sort)
        else:
            animatie_sortare(canvas, lista, rects, speed, selection_sort)

    # Buton pentru a începe sortarea
    ttk.Button(fereastra, text="Începe sortarea", command=init_sortare).pack(pady=10)

    # Buton pentru a opri sortarea
    ttk.Button(fereastra, text="Oprește sortarea", command=stop_sortare).pack(pady=10)

    # Buton pentru a relua sortarea
    ttk.Button(fereastra, text="Relua sortarea", command=lambda: relua_sortare(canvas, speed_slider.get(), bubble_sort if optiune == "Bubble Sort" else insertion_sort if optiune == "Insertion Sort" else selection_sort)).pack(pady=10)

    # Buton pentru a închide fereastra
    ttk.Button(fereastra, text="Închide", command=fereastra.destroy).pack(pady=10)

# Crearea ferestrei principale
def creeaza_interfata():
    optiuni_sortare = ["Bubble Sort", "Insertion Sort", "Selection Sort"]
    valori = [20, 30, 40]

    root = tk.Tk()
    root.title("Opțiuni de sortare")
    root.geometry("800x400")
    root.config(bg="purple")

    canvas = tk.Canvas(root, bg="pink")
    canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    buton = ttk.Button(root, text="Afișează opțiunile",
                       command=lambda: deseneaza_coloane(canvas, optiuni_sortare, valori))
    buton.pack(pady=10)

    root.mainloop()

# Funcția pentru desenarea opțiunilor inițiale
def deseneaza_coloane(canvas, optiuni, valori):
    canvas.delete("all")
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    num_bars = len(optiuni)
    bar_width = width // num_bars
    max_value = max(valori)

    for i, (optiune, valoare) in enumerate(zip(optiuni, valori)):
        x1 = i * bar_width
        x2 = (i + 1) * bar_width
        y1 = height - (valoare / max_value) * (height - 20)  # Înălțimea proporțională
        y2 = height - 10

        buton = tk.Button(canvas, text=optiune, bg="pink", fg="purple", command=lambda o=optiune: deschide_fereastra(o))
        buton.place(x=x1, y=y1, width=x2 - x1, height=y2 - y1)

# Lansarea aplicației
creeaza_interfata()
