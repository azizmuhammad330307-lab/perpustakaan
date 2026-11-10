# app.py
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from db import get_db, init_db

app = Flask(__name__)

# Pastikan database terinisiasi saat pertama kali jalan
init_db()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/katalog')
def katalog():
    db = get_db()
    buku_list = db.execute('SELECT * FROM buku').fetchall()

    # Ambil riwayat peminjaman beserta judul bukunya
    riwayat_list = db.execute('''
                              SELECT peminjaman.*, buku.judul
                              FROM peminjaman
                                       JOIN buku ON peminjaman.buku_id = buku.id
                              WHERE status = 'Dipinjam'
                              ''').fetchall()
    db.close()

    return render_template('katalog.html', buku_list=buku_list, riwayat_list=riwayat_list)


@app.route('/pinjam/<int:buku_id>', methods=['POST'])
def pinjam(buku_id):
    peminjam = request.form.get('peminjam')
    tanggal_pinjam = datetime.now().strftime('%Y-%m-%d %H:%M')

    if peminjam:
        db = get_db()
        # Cek stok buku
        buku = db.execute('SELECT stok FROM buku WHERE id = ?', (buku_id,)).fetchone()
        if buku and buku['stok'] > 0:
            # Kurangi stok
            db.execute('UPDATE buku SET stok = stok - 1 WHERE id = ?', (buku_id,))
            # Catat peminjaman
            db.execute('INSERT INTO peminjaman (buku_id, peminjam, tanggal_pinjam) VALUES (?, ?, ?)',
                       (buku_id, peminjam, tanggal_pinjam))
            db.commit()
        db.close()

    return redirect(url_for('katalog'))


@app.route('/pustakawan')
def pustakawan():
    db = get_db()
    buku_list = db.execute('SELECT * FROM buku').fetchall()
    db.close()
    return render_template('pustakawan.html', buku_list=buku_list)


@app.route('/tambah_buku', methods=['POST'])
def tambah_buku():
    judul = request.form.get('judul')
    penulis = request.form.get('penulis')
    stok = request.form.get('stok')

    if judul and penulis and stok:
        db = get_db()
        db.execute('INSERT INTO buku (judul, penulis, stok) VALUES (?, ?, ?)',
                   (judul, penulis, int(stok)))
        db.commit()
        db.close()

    return redirect(url_for('pustakawan'))


@app.route('/hapus_buku/<int:buku_id>')
def hapus_buku(buku_id):
    db = get_db()
    db.execute('DELETE FROM buku WHERE id = ?', (buku_id,))
    db.commit()
    db.close()
    return redirect(url_for('pustakawan'))


if __name__ == '__main__':
    app.run(debug=True)