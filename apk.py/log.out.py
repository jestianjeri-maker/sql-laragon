
import tkinter as tk
from tkinter import messagebox

# Fungsi Logout
def logout():
    konfirmasi = messagebox.askyesno(
        "Konfirmasi Logout",
        "Apakah Anda yakin ingin keluar dari aplikasi?"
    )

    if konfirmasi:
        halaman.destroy()


# Membuat jendela utama
halaman = tk.Tk()
halaman.title("Logout - Sistem Informasi Akademik")
halaman.geometry("500x400")
halaman.resizable(False, False)
halaman.configure(bg="#101B35")

# Mengatur posisi jendela di tengah layar
halaman.update_idletasks()
x = (halaman.winfo_screenwidth() // 2) - 250
y = (halaman.winfo_screenheight() // 2) - 200
halaman.geometry(f"500x400+{x}+{y}")


# Header aplikasi
header = tk.Frame(
    halaman,
    bg="#101B35"
)
header.pack(fill="x", pady=(25, 10))

tk.Label(
    header,
    text="SIAKAD",
    font=("Arial", 13, "bold"),
    fg="#60A5FA",
    bg="#101B35"
).pack()

tk.Label(
    header,
    text="Sistem Informasi Akademik",
    font=("Arial", 10),
    fg="#CBD5E1",
    bg="#101B35"
).pack(pady=5)


# Card utama
card = tk.Frame(
    halaman,
    bg="white",
    highlightbackground="#33466B",
    highlightthickness=1
)
card.pack(
    padx=65,
    pady=15,
    fill="both",
    expand=True
)


# Ikon Logout
tk.Label(
    card,
    text="↪",
    font=("Arial", 42, "bold"),
    fg="#2563EB",
    bg="white"
).pack(pady=(20, 5))


# Judul
tk.Label(
    card,
    text="Selamat Datang!",
    font=("Arial", 19, "bold"),
    fg="#172554",
    bg="white"
).pack(pady=5)


# Deskripsi
tk.Label(
    card,
    text="Anda telah berhasil masuk ke sistem.",
    font=("Arial", 9),
    fg="#64748B",
    bg="white"
).pack(pady=3)

tk.Label(
    card,
    text="Klik tombol di bawah untuk keluar dari akun.",
    font=("Arial", 9),
    fg="#64748B",
    bg="white"
).pack(pady=3)


# Tombol Logout
def hover_masuk(event):
    tombol_logout.config(bg="#1D4ED8")

def hover_keluar(event):
    tombol_logout.config(bg="#2563EB")


tombol_logout = tk.Button(
    card,
    text="↪   LOGOUT",
    command=logout,
    bg="#2563EB",
    fg="white",
    activebackground="#1D4ED8",
    activeforeground="white",
    font=("Arial", 11, "bold"),
    relief="flat",
    cursor="hand2",
    bd=0,
    width=25,
    pady=11
)
tombol_logout.pack(pady=22)

tombol_logout.bind("<Enter>", hover_masuk)
tombol_logout.bind("<Leave>", hover_keluar)


# Footer
tk.Label(
    card,
    text="© 2026 SIAKAD | All Rights Reserved",
    font=("Arial", 8),
    fg="#94A3B8",
    bg="white"
).pack(side="bottom", pady=12)


# Menjalankan aplikasi
halaman.mainloop()
