import sqlite3
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS productos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    descripcion TEXT,
                    precio REAL NOT NULL,
                    disponible INTEGER NOT NULL,
                    imagen TEXT
                )''')
    
    productos = [
        ("TECLADO INALAMBRICO TOUCHPAD T650 Recargable", "Teclado inalámbrico con touchpad recargable.", 679.03, 1, "/static/images/teclado.png"),
        ("Repetidor de wifi - Velop WHW AC1200 3 PK", "Repetidor de señal Wi-Fi para mejor cobertura.", 1199.01, 1, "/static/images/repetidor.png"),
        ("Adaptador AC580 Wireless", "Adaptador USB inalámbrico de alta velocidad.", 409.03, 1, "/static/images/adaptador.png")
    ]
    
    c.execute("SELECT COUNT(*) FROM productos")
    if c.fetchone()[0] == 0:
        c.executemany("INSERT INTO productos (nombre, descripcion, precio, disponible, imagen) VALUES (?, ?, ?, ?, ?)", productos)

    conn.commit()
    conn.close()
