import tkinter as tk
from tkinter import messagebox
import sqlite3


# 1. Membuat dan menghubungkan database SQLite
koneksi = sqlite3.connect("nilai_siswa.db")
cursor = koneksi.cursor()

# 2. Membuat tabel nilai_siswa
cursor.execute("""
CREATE TABLE IF NOT EXISTS nilai_siswa (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama_siswa TEXT NOT NULL,
    biologi REAL NOT NULL,
    fisika REAL NOT NULL,
    inggris REAL NOT NULL,
    prediksi_fakultas TEXT NOT NULL
)
""")

koneksi.commit()


# 3. Fungsi untuk memprediksi fakultas
def prediksi_fakultas(biologi, fisika, inggris):
    nilai_tertinggi = max(biologi, fisika, inggris)

    mata_pelajaran_tertinggi = []

    if biologi == nilai_tertinggi:
        mata_pelajaran_tertinggi.append("Biologi")

    if fisika == nilai_tertinggi:
        mata_pelajaran_tertinggi.append("Fisika")

    if inggris == nilai_tertinggi:
        mata_pelajaran_tertinggi.append("Inggris")

    if len(mata_pelajaran_tertinggi) > 1:
        return None

    if biologi == nilai_tertinggi:
        return "Kedokteran"
    elif fisika == nilai_tertinggi:
        return "Teknik"
    else:
        return "Bahasa"


# 4. Fungsi untuk menyimpan nilai siswa
def submit_nilai():
    nama = entry_nama.get().strip()

    if not nama:
        messagebox.showwarning(
            "Peringatan", "Nama siswa harus diisi!"
        )
        return

    try:
        biologi = float(entry_biologi.get())
        fisika = float(entry_fisika.get())
        inggris = float(entry_inggris.get())

        if not all(
            0 <= nilai <= 100
            for nilai in [biologi, fisika, inggris]
        ):
            messagebox.showwarning(
                "Peringatan",
                "Nilai harus berada antara 0 sampai 100!"
            )
            return

    except ValueError:
        messagebox.showerror(
            "Kesalahan",
            "Masukkan nilai berupa angka yang valid!"
        )
        return

    fakultas = prediksi_fakultas(
        biologi, fisika, inggris
    )

    if fakultas is None:
        messagebox.showwarning(
            "Nilai Seri",
            "Nilai tertinggi sama. "
            "Silakan masukkan nilai yang berbeda."
        )
        return

    # 5. Menyimpan data ke tabel SQLite
    cursor.execute("""
        INSERT INTO nilai_siswa
        (nama_siswa, biologi, fisika, inggris,
         prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    """, (nama, biologi, fisika, inggris, fakultas))

    koneksi.commit()

    # 6. Menampilkan hasil prediksi
    messagebox.showinfo(
        "Hasil Prediksi",
        f"Nama Siswa: {nama}\n"
        f"Biologi: {biologi}\n"
        f"Fisika: {fisika}\n"
        f"Inggris: {inggris}\n"
        f"Prediksi Fakultas: {fakultas}\n\n"
        "Data berhasil disimpan ke database!"
    )

    # 7. Mengosongkan form setelah submit
    entry_nama.delete(0, tk.END)
    entry_biologi.delete(0, tk.END)
    entry_fisika.delete(0, tk.END)
    entry_inggris.delete(0, tk.END)


# 8. Membuat tampilan Tkinter
root = tk.Tk()
root.title("Prediksi Fakultas Siswa")
root.geometry("400x350")
root.resizable(False, False)

judul = tk.Label(
    root,
    text="FORM PREDIKSI FAKULTAS",
    font=("Arial", 14, "bold")
)
judul.pack(pady=15)

frame = tk.Frame(root)
frame.pack(pady=5)

tk.Label(frame, text="Nama Siswa").grid(
    row=0, column=0, sticky="w", padx=10, pady=5
)
entry_nama = tk.Entry(frame, width=25)
entry_nama.grid(row=0, column=1, pady=5)

tk.Label(frame, text="Nilai Biologi").grid(
    row=1, column=0, sticky="w", padx=10, pady=5
)
entry_biologi = tk.Entry(frame, width=25)
entry_biologi.grid(row=1, column=1, pady=5)

tk.Label(frame, text="Nilai Fisika").grid(
    row=2, column=0, sticky="w", padx=10, pady=5
)
entry_fisika = tk.Entry(frame, width=25)
entry_fisika.grid(row=2, column=1, pady=5)

tk.Label(frame, text="Nilai Inggris").grid(
    row=3, column=0, sticky="w", padx=10, pady=5
)
entry_inggris = tk.Entry(frame, width=25)
entry_inggris.grid(row=3, column=1, pady=5)

tombol_submit = tk.Button(
    root,
    text="Submit Nilai",
    command=submit_nilai,
    bg="green",
    fg="white",
    font=("Arial", 10, "bold"),
    width=20
)
tombol_submit.pack(pady=15)

root.mainloop()