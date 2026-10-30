
import tkinter as tk
from tkinter import ttk
import os

# Membuat jendela utama
root = tk.Tk()
root.title("Konverter Suhu")
root.geometry("430x500")
root.resizable(False, False)
root.configure(bg="#F1F5F9")

# Ikon aplikasi
base_dir = os.path.dirname(os.path.abspath(__file__))
icon_path = os.path.join(base_dir, "calc.ico")

if os.path.exists(icon_path):
    root.iconbitmap(icon_path)

# Warna tema
NAVY = "#172554"
BLUE = "#2563EB"
LIGHT_BLUE = "#DBEAFE"
WHITE = "#FFFFFF"
TEXT = "#1E293B"
GRAY = "#64748B"
GREEN = "#15803D"
RED = "#DC2626"

# Header aplikasi
header = tk.Frame(root, bg=NAVY, height=145)
header.pack(fill="x")
header.pack_propagate(False)

tk.Label(
    header,
    text="🌡 KONVERTER SUHU",
    font=("Segoe UI", 20, "bold"),
    bg=NAVY,
    fg=WHITE
).pack(pady=(28, 7))

tk.Label(
    header,
    text="Konversi Celsius ke Fahrenheit dengan mudah",
    font=("Segoe UI", 9),
    bg=NAVY,
    fg="#BFDBFE"
).pack()

# Panel utama
card = tk.Frame(
    root,
    bg=WHITE,
    highlightbackground="#E2E8F0",
    highlightthickness=1
)
card.pack(fill="both", expand=True, padx=25, pady=20)

tk.Label(
    card,
    text="Masukkan Suhu",
    font=("Segoe UI", 15, "bold"),
    bg=WHITE,
    fg=TEXT
).pack(pady=(22, 5))

tk.Label(
    card,
    text="Suhu dalam derajat Celsius (°C)",
    font=("Segoe UI", 10),
    bg=WHITE,
    fg=GRAY
).pack(pady=(0, 12))

# Input suhu
entry_celsius = tk.Entry(
    card,
    font=("Segoe UI", 16),
    justify="center",
    relief="solid",
    bd=1,
    bg="#F8FAFC",
    fg=TEXT,
    insertbackground=BLUE
)
entry_celsius.pack(fill="x", padx=35, ipady=9)

entry_celsius.focus_set()

# Label hasil
label_hasil = tk.Label(
    card,
    text="Hasil konversi akan muncul di sini",
    font=("Segoe UI", 11, "bold"),
    bg=LIGHT_BLUE,
    fg=NAVY,
    wraplength=300,
    padx=10,
    pady=15
)
label_hasil.pack(fill="x", padx=35, pady=18)

def konversi():
    try:
        celsius = float(entry_celsius.get().strip())
        fahrenheit = (celsius * 9 / 5) + 32

        label_hasil.config(
            text=f"{celsius:g} °C  =  {fahrenheit:.2f} °F",
            bg="#DCFCE7",
            fg=GREEN
        )

    except ValueError:
        label_hasil.config(
            text="Masukkan angka yang valid!",
            bg="#FEE2E2",
            fg=RED
        )

def reset():
    entry_celsius.delete(0, tk.END)
    label_hasil.config(
        text="Hasil konversi akan muncul di sini",
        bg=LIGHT_BLUE,
        fg=NAVY
    )
    entry_celsius.focus_set()

# Tombol konversi
btn_konversi = tk.Button(
    card,
    text="KONVERSI SUHU",
    command=konversi,
    font=("Segoe UI", 11, "bold"),
    bg=BLUE,
    fg=WHITE,
    activebackground="#1D4ED8",
    activeforeground=WHITE,
    relief="flat",
    cursor="hand2"
)
btn_konversi.pack(fill="x", padx=35, ipady=9)

btn_konversi.bind(
    "<Enter>",
    lambda event: btn_konversi.config(bg="#1D4ED8")
)
btn_konversi.bind(
    "<Leave>",
    lambda event: btn_konversi.config(bg=BLUE)
)

# Tombol reset
btn_reset = tk.Button(
    card,
    text="Reset",
    command=reset,
    font=("Segoe UI", 10),
    bg=WHITE,
    fg=GRAY,
    activebackground="#E2E8F0",
    relief="flat",
    cursor="hand2"
)
btn_reset.pack(pady=(7, 12))

# Tombol Enter untuk konversi
root.bind("<Return>", lambda event: konversi())

# Footer
tk.Label(
    root,
    text="Aplikasi Konverter Suhu | Python Tkinter",
    font=("Segoe UI", 8),
    bg="#F1F5F9",
    fg=GRAY
).pack(pady=(0, 10))

root.mainloop()
