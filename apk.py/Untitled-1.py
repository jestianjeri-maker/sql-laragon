
import mysql.connector
import tkinter as tk
from tkinter import ttk, messagebox


class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("SIAKAD | Login")
        self.root.geometry("520x570")
        self.root.resizable(False, False)
        self.root.configure(bg="#F1F5F9")

        # Konfigurasi database
        self.db_config = {
            "host": "localhost",
            "user": "root",
            "password": "",
            "database": "siakad"
        }

        # Warna tema
        self.navy = "#142B4A"
        self.blue = "#2563EB"
        self.light_blue = "#EFF6FF"
        self.background = "#F1F5F9"
        self.text_color = "#1E293B"
        self.muted = "#64748B"

        # Style komponen
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Modern.TEntry",
            padding=10,
            font=("Segoe UI", 11),
            fieldbackground="white"
        )

        # Header
        header = tk.Frame(
            root,
            bg=self.navy,
            height=175
        )
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="SIAKAD",
            font=("Segoe UI", 27, "bold"),
            fg="white",
            bg=self.navy
        ).pack(pady=(28, 3))

        tk.Label(
            header,
            text="SISTEM INFORMASI AKADEMIK",
            font=("Segoe UI", 10, "bold"),
            fg="#93C5FD",
            bg=self.navy
        ).pack()

        tk.Label(
            header,
            text="Silakan masuk ke akun Anda",
            font=("Segoe UI", 10),
            fg="#E2E8F0",
            bg=self.navy
        ).pack(pady=8)

        # Kartu login
        card = tk.Frame(
            root,
            bg="white",
            highlightbackground="#E2E8F0",
            highlightthickness=1
        )
        card.place(x=45, y=140, width=430, height=365)

        tk.Label(
            card,
            text="Selamat Datang!",
            font=("Segoe UI", 20, "bold"),
            fg=self.text_color,
            bg="white"
        ).pack(anchor="w", padx=32, pady=(28, 3))

        tk.Label(
            card,
            text="Masukkan data akun untuk melanjutkan.",
            font=("Segoe UI", 9),
            fg=self.muted,
            bg="white"
        ).pack(anchor="w", padx=32, pady=(0, 22))

        # Input NIP
        tk.Label(
            card,
            text="Username / NIP",
            font=("Segoe UI", 10, "bold"),
            fg=self.text_color,
            bg="white"
        ).pack(anchor="w", padx=32, pady=(0, 7))

        self.entry_nip = ttk.Entry(
            card,
            style="Modern.TEntry",
            width=35
        )
        self.entry_nip.pack(fill="x", padx=32, ipady=2)

        # Input password
        tk.Label(
            card,
            text="Password",
            font=("Segoe UI", 10, "bold"),
            fg=self.text_color,
            bg="white"
        ).pack(anchor="w", padx=32, pady=(16, 7))

        password_frame = tk.Frame(
            card,
            bg="white"
        )
        password_frame.pack(fill="x", padx=32)

        self.entry_email = ttk.Entry(
            password_frame,
            style="Modern.TEntry",
            show="*"
        )
        self.entry_email.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=2
        )

        self.show_password = False

        self.btn_show = tk.Button(
            password_frame,
            text="Lihat",
            font=("Segoe UI", 9, "bold"),
            fg=self.blue,
            bg="white",
            activebackground="white",
            activeforeground=self.navy,
            relief="flat",
            cursor="hand2",
            command=self.toggle_password
        )
        self.btn_show.pack(side="left", padx=(7, 0))

        # Tombol login
        self.btn_login = tk.Button(
            card,
            text="MASUK KE AKUN",
            font=("Segoe UI", 11, "bold"),
            bg=self.blue,
            fg="white",
            activebackground="#1D4ED8",
            activeforeground="white",
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.proses_login
        )
        self.btn_login.pack(
            fill="x",
            padx=32,
            pady=(25, 0),
            ipady=10
        )

        # Efek hover tombol
        self.btn_login.bind(
            "<Enter>",
            lambda event: self.btn_login.config(bg="#1D4ED8")
        )
        self.btn_login.bind(
            "<Leave>",
            lambda event: self.btn_login.config(bg=self.blue)
        )

        # Footer
        tk.Label(
            root,
            text="SIAKAD  •  Sistem Informasi Akademik",
            font=("Segoe UI", 9),
            fg=self.muted,
            bg=self.background
        ).pack(side="bottom", pady=17)

        self.entry_nip.focus_set()
        self.root.bind("<Return>", lambda event: self.proses_login())

    def toggle_password(self):
        self.show_password = not self.show_password

        if self.show_password:
            self.entry_email.config(show="")
            self.btn_show.config(text="Sembunyi")
        else:
            self.entry_email.config(show="*")
            self.btn_show.config(text="Lihat")

    def proses_login(self):
        nip = self.entry_nip.get().strip()
        email = self.entry_email.get().strip()

        if not nip or not email:
            messagebox.showwarning(
                "Peringatan",
                "Username dan password wajib diisi!"
            )
            return

        conn = None
        cursor = None

        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor(dictionary=True)

            query = """
                SELECT nip, nama_dosen, email
                FROM dosen
                WHERE nip = %s AND email = %s
            """

            cursor.execute(query, (nip, email))
            user = cursor.fetchone()

            if user:
                messagebox.showinfo(
                    "Login Berhasil",
                    f"Selamat datang, {user['nama_dosen']}!"
                )
                self.buka_dashboard(user)
            else:
                messagebox.showerror(
                    "Login Gagal",
                    "Username atau password salah."
                )

        except mysql.connector.Error as err:
            messagebox.showerror(
                "Database Error",
                f"Koneksi database bermasalah:\n{err}"
            )

        finally:
            if cursor:
                cursor.close()

            if conn and conn.is_connected():
                conn.close()

    def buka_dashboard(self, user):
        # Tutup halaman login setelah berhasil masuk
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()
