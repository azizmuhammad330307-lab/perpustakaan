# db.py
import sqlite3

DATABASE = 'library.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    db = get_db()
    # Tabel Buku
    db.execute('''
        CREATE TABLE IF NOT EXISTS buku (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            judul TEXT NOT NULL,
            penulis TEXT NOT NULL,
            stok INTEGER NOT NULL
        )
    ''')
    # Tabel Peminjaman
    db.execute('''
        CREATE TABLE IF NOT EXISTS peminjaman (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            buku_id INTEGER,
            peminjam TEXT NOT NULL,
            tanggal_pinjam TEXT NOT NULL,
            status TEXT DEFAULT 'Dipinjam',
            FOREIGN KEY (buku_id) REFERENCES buku (id)
        )
    ''')
    db.commit()
    db.close()

if __name__ == '__main__':
    init_db()
    print("Database SQLite berhasil diinisialisasi!")