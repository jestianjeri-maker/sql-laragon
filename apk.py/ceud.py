
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# =====================================
# KONEKSI DATABASE
# =====================================
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="siakad"
    )


# =====================================
# CLASS APLIKASI SIAKAD
# =====================================
class SIAKADApp:

    def __init__(self, root):
        self.root = root
        self.selected_nip = None

        self.root.title("SIAKAD - Data Dosen")
        self.root.geometry("1150x700")
        self.root.minsize(950, 600)
        self.root.configure(bg="#F1F5F9")

        self.entries = {}

        self.setup_style()
        self.create_header()
        self.create_form()
        self.create_table()
        self.create_status()

        self.load_data()

    # =====================================
    # STYLE
    # =====================================
    def setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Treeview",
            background="white",
            foreground="#334155",
            rowheight=35,
            fieldbackground="white",
            font=("Arial", 10)
        )

        style.configure(
            "Treeview.Heading",
            background="#1E3A8A",
            foreground="white",
            font=("Arial", 10, "bold"),
            padding=10
        )

        style.map(
            "Treeview",
            background=[("selected", "#BFDBFE")],
            foreground=[("selected", "#1E3A8A")]
        )

    # =====================================
    # HEADER
    # =====================================
    def create_header(self):
        header = tk.Frame(
            self.root,
            bg="#172554",
            height=100
        )
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="SIAKAD",
            font=("Arial", 23, "bold"),
            fg="white",
            bg="#172554"
        ).pack(anchor="w", padx=30, pady=(18, 0))

        tk.Label(
            header,
            text="Sistem Informasi Akademik | Manajemen Data Dosen",
            font=("Arial", 10),
            fg="#BFDBFE",
            bg="#172554"
        ).pack(anchor="w", padx=32)

    # =====================================
    # FORM DATA DOSEN
    # =====================================
    def create_form(self):
        form = tk.Frame(
            self.root,
            bg="white",
            highlightbackground="#E2E8F0",
            highlightthickness=1
        )
        form.pack(fill="x", padx=25, pady=20)

        tk.Label(
            form,
            text="FORMULIR DATA DOSEN",
            font=("Arial", 14, "bold"),
            fg="#1E3A8A",
            bg="white"
        ).grid(row=0, column=0, columnspan=4,
               sticky="w", padx=20, pady=15)

        fields = [
            ("nip", "NIP"),
            ("nama", "Nama Dosen"),
            ("jk", "Jenis Kelamin"),
            ("email", "Email"),
            ("tlp", "No. Telepon"),
            ("pendidikan", "Pendidikan Terakhir"),
            ("bidang", "Bidang Keahlian")
        ]

        for i, (key, label) in enumerate(fields):
            row = (i // 2) + 1
            col = (i % 2) * 2

            tk.Label(
                form,
                text=label,
                font=("Arial", 10, "bold"),
                bg="white",
                fg="#475569"
            ).grid(
                row=row, column=col,
                sticky="w", padx=(20, 8), pady=9
            )

            if key == "jk":
                widget = ttk.Combobox(
                    form,
                    values=["Laki-laki", "Perempuan"],
                    state="readonly",
                    font=("Arial", 10),
                    width=27
                )
            else:
                widget = tk.Entry(
                    form,
                    font=("Arial", 10),
                    bg="#F8FAFC",
                    fg="#334155",
                    relief="flat",
                    highlightthickness=1,
                    highlightbackground="#CBD5E1",
                    highlightcolor="#3B82F6"
                )

            widget.grid(
                row=row, column=col + 1,
                sticky="ew", padx=(0, 20), pady=9,
                ipady=7
            )

            self.entries[key] = widget

        form.grid_columnconfigure(1, weight=1)
        form.grid_columnconfigure(3, weight=1)

        # Tombol aksi
        button_frame = tk.Frame(form, bg="white")
        button_frame.grid(
            row=5, column=0, columnspan=4,
            sticky="w", padx=20, pady=18
        )

        self.create_button(
            button_frame, "＋ TAMBAH",
            "#2563EB", self.tambah_data
        )

        self.create_button(
            button_frame, "✎ EDIT",
            "#D97706", self.update_data
        )

        self.create_button(
            button_frame, "✕ HAPUS",
            "#DC2626", self.hapus_data
        )

        self.create_button(
            button_frame, "↻ RESET",
            "#64748B", self.clear_fields
        )

    # =====================================
    # MEMBUAT TOMBOL
    # =====================================
    def create_button(self, parent, text, color, command):
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            bg=color,
            fg="white",
            activebackground=color,
            activeforeground="white",
            font=("Arial", 9, "bold"),
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=10
        )

        btn.pack(side="left", padx=(0, 10))

        btn.bind(
            "<Enter>",
            lambda e: btn.config(bg="#334155")
        )

        btn.bind(
            "<Leave>",
            lambda e: btn.config(bg=color)
        )

        return btn

    # =====================================
    # TABEL DATA DOSEN
    # =====================================
    def create_table(self):
        container = tk.Frame(
            self.root,
            bg="white",
            highlightbackground="#E2E8F0",
            highlightthickness=1
        )
        container.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(0, 15)
        )

        tk.Label(
            container,
            text="DAFTAR DATA DOSEN",
            font=("Arial", 14, "bold"),
            fg="#1E3A8A",
            bg="white"
        ).pack(anchor="w", padx=20, pady=15)

        columns = (
            "nip", "nama", "jk", "email",
            "tlp", "pendidikan", "bidang"
        )

        table_frame = tk.Frame(container, bg="white")
        table_frame.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        headings = {
            "nip": "NIP",
            "nama": "NAMA DOSEN",
            "jk": "JENIS KELAMIN",
            "email": "EMAIL",
            "tlp": "NO. TELEPON",
            "pendidikan": "PENDIDIKAN",
            "bidang": "BIDANG KEAHLIAN"
        }

        widths = {
            "nip": 110,
            "nama": 150,
            "jk": 110,
            "email": 170,
            "tlp": 120,
            "pendidikan": 120,
            "bidang": 150
        }

        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(
                col,
                width=widths[col],
                minwidth=90,
                anchor="center"
            )

        scrollbar_y = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )

        scrollbar_x = ttk.Scrollbar(
            table_frame,
            orient="horizontal",
            command=self.tree.xview
        )

        self.tree.configure(
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set
        )

        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        scrollbar_x.grid(row=1, column=0, sticky="ew")

        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        self.tree.bind(
            "<<TreeviewSelect>>",
            self.select_item
        )

    # =====================================
    # STATUS
    # =====================================
    def create_status(self):
        self.status_var = tk.StringVar(
            value="Formulir siap digunakan"
        )

        status = tk.Label(
            self.root,
            textvariable=self.status_var,
            bg="#172554",
            fg="white",
            font=("Arial", 9),
            anchor="w",
            padx=20,
            pady=10
        )
        status.pack(fill="x")

    # =====================================
    # MENGAMBIL NILAI FORM
    # =====================================
    def get_form_values(self):
        return (
            self.entries["nip"].get().strip(),
            self.entries["nama"].get().strip(),
            self.entries["jk"].get().strip(),
            self.entries["email"].get().strip(),
            self.entries["tlp"].get().strip(),
            self.entries["pendidikan"].get().strip(),
            self.entries["bidang"].get().strip()
        )

    # =====================================
    # MENAMPILKAN DATA
    # =====================================
    def load_data(self):
        db = None
        cursor = None

        try:
            db = connect_db()
            cursor = db.cursor()

            cursor.execute("""
                SELECT nip, nama_dosen, jenis_kelamin,
                email, no_telepon, pendidikan_terakhir,
                bidang_keahlian
                FROM dosen
            """)

            records = cursor.fetchall()

            for item in self.tree.get_children():
                self.tree.delete(item)

            for row in records:
                self.tree.insert("", "end", values=row)

            self.status_var.set(
                f"Jumlah data dosen: {len(records)}"
            )

        except mysql.connector.Error as err:
            messagebox.showerror(
                "Kesalahan Database", str(err)
            )

        finally:
            if cursor:
                cursor.close()
            if db and db.is_connected():
                db.close()

    # =====================================
    # TAMBAH DATA
    # =====================================
    def tambah_data(self):
        data = self.get_form_values()

        if not data[0] or not data[1]:
            messagebox.showwarning(
                "Data Belum Lengkap",
                "NIP dan Nama Dosen wajib diisi."
            )
            return

        db = None
        cursor = None

        try:
            db = connect_db()
            cursor = db.cursor()

            sql = """
                INSERT INTO dosen
                (nip, nama_dosen, jenis_kelamin, email,
                no_telepon, pendidikan_terakhir,
                bidang_keahlian)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """

            cursor.execute(sql, data)
            db.commit()

            messagebox.showinfo(
                "Berhasil",
                "Data dosen berhasil ditambahkan."
            )

            self.clear_fields()
            self.load_data()

        except mysql.connector.Error as err:
            if db and db.is_connected():
                db.rollback()

            messagebox.showerror("Gagal Menambah Data", str(err))

        finally:
            if cursor:
                cursor.close()
            if db and db.is_connected():
                db.close()

    # =====================================
    # UPDATE DATA
    # =====================================
    def update_data(self):
        if not self.selected_nip:
            messagebox.showwarning(
                "Pilih Data",
                "Silakan pilih data dosen yang ingin diperbarui."
            )
            return

        data = self.get_form_values()

        if not data[0] or not data[1]:
            messagebox.showwarning(
                "Data Belum Lengkap",
                "NIP dan Nama Dosen wajib diisi."
            )
            return

        db = None
        cursor = None

        try:
            db = connect_db()
            cursor = db.cursor()

            sql = """
                UPDATE dosen SET
                nip=%s, nama_dosen=%s, jenis_kelamin=%s,
                email=%s, no_telepon=%s,
                pendidikan_terakhir=%s, bidang_keahlian=%s
                WHERE nip=%s
            """

            cursor.execute(
                sql,
                data + (self.selected_nip,)
            )

            db.commit()

            messagebox.showinfo(
                "Berhasil",
                "Data dosen berhasil diperbarui."
            )

            self.clear_fields()
            self.load_data()

        except mysql.connector.Error as err:
            if db and db.is_connected():
                db.rollback()

            messagebox.showerror(
                "Gagal Memperbarui Data", str(err)
            )

        finally:
            if cursor:
                cursor.close()
            if db and db.is_connected():
                db.close()

    # =====================================
    # HAPUS DATA
    # =====================================
    def hapus_data(self):
        if not self.selected_nip:
            messagebox.showwarning(
                "Pilih Data",
                "Pilih data dosen yang ingin dihapus."
            )
            return

        konfirmasi = messagebox.askyesno(
            "Konfirmasi Hapus",
            f"Yakin ingin menghapus data NIP "
            f"{self.selected_nip}?"
        )

        if not konfirmasi:
            return

        db = None
        cursor = None

        try:
            db = connect_db()
            cursor = db.cursor()

            cursor.execute(
                "DELETE FROM dosen WHERE nip=%s",
                (self.selected_nip,)
            )

            db.commit()

            if cursor.rowcount > 0:
                messagebox.showinfo(
                    "Berhasil",
                    "Data dosen berhasil dihapus."
                )

            self.clear_fields()
            self.load_data()

        except mysql.connector.Error as err:
            if db and db.is_connected():
                db.rollback()

            messagebox.showerror(
                "Gagal Menghapus Data", str(err)
            )

        finally:
            if cursor:
                cursor.close()
            if db and db.is_connected():
                db.close()

    # =====================================
    # PILIH DATA
    # =====================================
    def select_item(self, event=None):
        selected = self.tree.selection()

        if not selected:
            return

        values = self.tree.item(
            selected[0], "values"
        )

        self.clear_fields()

        self.entries["nip"].insert(0, values[0])
        self.entries["nama"].insert(0, values[1])
        self.entries["jk"].set(values[2])
        self.entries["email"].insert(0, values[3])
        self.entries["tlp"].insert(0, values[4])
        self.entries["pendidikan"].insert(0, values[5])
        self.entries["bidang"].insert(0, values[6])

        self.selected_nip = values[0]

        self.status_var.set(
            f"Data dipilih: {values[1]} | NIP: {values[0]}"
        )

    # =====================================
    # RESET FORM
    # =====================================
    def clear_fields(self):
        for key, widget in self.entries.items():
            if key == "jk":
                widget.set("")
            else:
                widget.delete(0, tk.END)

        self.selected_nip = None

        for item in self.tree.selection():
            self.tree.selection_remove(item)

        self.status_var.set(
            "Formulir siap digunakan"
        )


# =====================================
# MENJALANKAN APLIKASI
# =====================================
if __name__ == "__main__":
    root = tk.Tk()
    app = SIAKADApp(root)
    root.mainloop()
