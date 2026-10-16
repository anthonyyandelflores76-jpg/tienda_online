from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'clave_secreta_taller_tci'

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def init_db():
    conexion = sqlite3.connect('tienda.db')
    cursor = conexion.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            categoria TEXT NOT NULL,
            precio_normal REAL NOT NULL,
            precio_oferta REAL,
            descuento INTEGER,
            descripcion TEXT,
            imagen TEXT
        )
    ''')
    
    cursor.execute("SELECT COUNT(*) FROM productos")
    count = cursor.fetchone()[0]
    
    if count == 0:
        productos_iniciales = [
            # Sublimación
            ("TAZA BRILLO", "Sublimacion", 15.00, 10.00, 33, "Taza de cerámica con acabado brillante para sublimación.", "uploads/tasas brillo.jpg"),
            ("TAZA MÁGICA", "Sublimacion", 22.00, 15.00, 32, "Taza termosensible que revela el diseño al verter agua caliente.", "uploads/magica.jpg"),
            ("TAZA DORADA", "Sublimacion", 25.00, 20.00, 20, "Taza decorativa con interior y detalles dorados exclusivos.", "uploads/tazas1.jpg"),
            ("TAZA TORNASOLADA", "Sublimacion", 25.00, 20.00, 20, "Taza con efecto tornasol brillante de alta gama.", "uploads/tasas 1.jpg"),
            ("Tomatodo 600ml", "Sublimacion", 25.00, 20.00, 20, "Tomatodo de aluminio de 600 ml con boquilla deportiva.", "uploads/tomatodos.jpg"),
            ("Tomatodo 400", "Sublimacion", 22.00, 18.00, 18, "Tomatodo compacto de 400 ml para uso escolar.", "uploads/tomatodos1.jpg"),
            ("Posavasos", "Sublimacion", 6.00, 4.00, 33, "Posavasos protectores de mesa personalizados.", "uploads/posa vasos.jpg"),
            ("Gorras", "Sublimacion", 25.00, 20.00, 20, "Gorras deportivas con diseño frontal sublimado o bordado.", "uploads/gorros1.jpg"),
            ("Thermo digital", "Sublimacion", 48.00, 40.00, 16, "Termo inteligente de acero inoxidable con indicador LED.", "uploads/tomatodos digital.jpg"),

            # Merchandising
            ("LLAVEROS ESPEJOS", "Merchandising", 4.00, 2.50, 37, "Llavero redondo con espejo posterior personalizado.", "uploads/espejo.jpg"),
            ("LLAVEROS de 44 y 56", "Merchandising", 3.00, 2.00, 33, "Llaveros metálicos y plásticos en medidas de 44mm y 56mm.", "uploads/llaveros.jpg"),
            ("PINES DE 44 Y 56mm", "Merchandising", 3.00, 2.00, 33, "Pines publicitarios y distintivos escolares de alta nitidez.", "uploads/pines.jpg"),
            ("IMANTADOS", "Merchandising", 4.00, 2.50, 37, "Imanes decorativos y publicitarios para refrigeradora.", "uploads/inmantados.jpg"),
            ("STICKER HOLOGRÁFICOS", "Merchandising", 3.00, 2.00, 33, "Stickers con efecto tornasol holográfico resistente al agua.", "uploads/78.jpg"),
            ("STCKER SIMPLES", "Merchandising", 2.00, 1.00, 50, "Stickers de vinil troquelados para diversos usos.", "uploads/stikers.jpg"),
            ("BOLSA DE TELA", "Merchandising", 18.00, 15.00, 16, "Bolsa ecológica de tela personalizada con diseño institucional.", "uploads/bolsas1.jpg"),
            ("POLOS", "Merchandising", 30.00, 25.00, 16, "Polo 100% algodón ideal para merchandising y estampado.", "uploads/POLOS.jpg"),
            ("DISTINTIVO", "Merchandising", 12.00, 10.00, 16, "Distintivos escolares y corporativos.", "uploads/distintivos.jpg"),
            ("Padmouse", "Merchandising", 15.00, 12.00, 20, "Pad mouse ergonómico antideslizante con base de goma.", "uploads/padmouse1.jpg"),
            ("Monederos", "Merchandising", 10.00, 8.00, 20, "Monederos personalizados con cierre.", "uploads/monederos.jpg"),
            ("Lapiceros", "Merchandising", 3.50, 2.00, 42, "Lapiceros corporativos grabados y personalizados.", "uploads/lapiceros.jpg"),
            ("MOCHILAS ESCOLARES BORDADAS", "Merchandising", 45.00, 38.00, 15, "Mochila escolar de lona con detalles bordados a color y bolsillo frontal.", "uploads/mochilas.jpg"),

            # Papelería
            ("AFICHES", "Papeleria", 4.00, 2.50, 37, "Afiches impresos a full color en alta resolución.", "uploads/afiche.jpg"),
            ("AGENDITAS", "Papeleria", 5.00, 3.50, 30, "Mini agendas personalizadas para apuntes diarios.", "uploads/agendas.jpg"),
            ("BLOCK ESCOLAR", "Papeleria", 12.00, 10.00, 16, "Block de apuntes y dibujo con portada personalizada.", "uploads/block.jpg"),
            ("Agenda holográfica", "Papeleria", 18.00, 15.00, 16, "Agenda ejecutiva con portada holográfica brillante.", "uploads/holografica.jpg"),
            ("Agenda Normal", "Papeleria", 15.00, 12.00, 20, "Agenda clásica argollada con diseño personalizado.", "uploads/agendas.jpg"),
            ("Agenda cartón grueso", "Papeleria", 25.00, 20.00, 20, "Agenda de pasta dura en cartón grueso ecológico.", "uploads/7.jpg"),
            ("Folder turísticos", "Papeleria", 5.00, 3.00, 40, "Folders corporativos y turísticos en couché pesado.", "uploads/folder.jpg"),
            ("ROMPECABEZAS EDUCATIVO", "Papeleria", 25.00, 20.00, 20, "Rompecabezas didáctico de 50 piezas con abecedario, números y figuras geométricas.", "uploads/rompecabezas.jpg"),

            # Cristalería
            ("FRASCO GRANDE DE VIDRIO", "Cristaleria", 18.00, 15.00, 16, "Frasco grande de vidrio grabado con diseños personalizados.", "uploads/frasco grande.jpg"),
            ("FRASCO MEDIANO DE VIDRIO", "Cristaleria", 12.00, 10.00, 16, "Frasco mediano de vidrio decorativo para conservas o regalos.", "uploads/frasco pequeño.jpg"),
            ("JARRA DE VIDRIO 2 LITROS", "Cristaleria", 24.00, 20.00, 16, "Jarra de vidrio de 2 litros con asa y diseño grabado.", "uploads/jaras de 2 litros.jpg"),
            ("VASO DE VIDRIO 1", "Cristaleria", 10.00, 8.00, 20, "Vaso de vidrio institucional estándar de alta resistencia.", "uploads/vaso.jpg"),
            ("VASO DE VIDRIO 2 DELGADO", "Cristaleria", 9.00, 7.00, 22, "Vaso de vidrio delgado y estilizado para bebidas frías.", "uploads/vaso2.webp"),
            ("VASO CHOP", "Cristaleria", 11.00, 8.50, 22, "Vaso chop cervecero de vidrio pesado con grabado personalizado.", "uploads/chop.jpg")
        ]
        
        cursor.executemany('''
            INSERT INTO productos (nombre, categoria, precio_normal, precio_oferta, descuento, descripcion, imagen)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', productos_iniciales)
        conexion.commit()
        
    conexion.close()

# Inicializar la base de datos al arrancar la app en cualquier entorno (incluyendo Gunicorn/Render)
init_db()

@app.route('/')
def index():
    conexion = sqlite3.connect('tienda.db')
    conexion.row_factory = sqlite3.Row
    cursor = conexion.cursor()
    
    categoria = request.args.get('categoria')
    busqueda = request.args.get('q')
    
    if busqueda:
        cursor.execute("SELECT * FROM productos WHERE nombre LIKE ? OR descripcion LIKE ?", ('%' + busqueda + '%', '%' + busqueda + '%'))
    elif categoria:
        cursor.execute("SELECT * FROM productos WHERE categoria = ?", (categoria,))
    else:
        cursor.execute("SELECT * FROM productos")
        
    productos = cursor.fetchall()
    conexion.close()
    
    return render_template('index.html', productos=productos, categoria_activa=categoria)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == 'motita2024abc':
            session['admin_logged'] = True
            return redirect(url_for('panel'))
        else:
            return render_template('login.html', error='Contraseña incorrecta')
            
    return render_template('login.html')

@app.route('/admin/panel', methods=['GET', 'POST'])
def panel():
    if not session.get('admin_logged'):
        return redirect(url_for('admin'))
        
    conexion = sqlite3.connect('tienda.db')
    conexion.row_factory = sqlite3.Row
    cursor = conexion.cursor()
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        categoria = request.form['categoria']
        precio_normal = float(request.form['precio_normal'])
        precio_oferta = request.form.get('precio_oferta')
        precio_oferta = float(precio_oferta) if precio_oferta else None
        descuento = request.form.get('descuento')
        descuento = int(descuento) if descuento else None
        descripcion = request.form['descripcion']
        
        imagen = request.files['imagen']
        imagen_nombre = ''
        if imagen and imagen.filename != '':
            imagen_nombre = imagen.filename
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            imagen.save(os.path.join(app.config['UPLOAD_FOLDER'], imagen_nombre))
            imagen_nombre = 'uploads/' + imagen_nombre

        cursor.execute('''
            INSERT INTO productos (nombre, categoria, precio_normal, precio_oferta, descuento, descripcion, imagen)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (nombre, categoria, precio_normal, precio_oferta, descuento, descripcion, imagen_nombre))
        conexion.commit()
        conexion.close()
        return redirect(url_for('panel'))

    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    conexion.close()
    return render_template('admin.html', productos=productos)

@app.route('/admin/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    if not session.get('admin_logged'):
        return redirect(url_for('admin'))
        
    conexion = sqlite3.connect('tienda.db')
    conexion.row_factory = sqlite3.Row
    cursor = conexion.cursor()
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        categoria = request.form['categoria']
        precio_normal = float(request.form['precio_normal'])
        precio_oferta = request.form.get('precio_oferta')
        precio_oferta = float(precio_oferta) if precio_oferta else None
        descuento = request.form.get('descuento')
        descuento = int(descuento) if descuento else None
        descripcion = request.form['descripcion']
        
        eliminar_imagen = request.form.get('eliminar_imagen')
        
        if eliminar_imagen == 'si':
            cursor.execute('UPDATE productos SET imagen = "" WHERE id = ?', (id,))
        else:
            imagen = request.files['imagen']
            if imagen and imagen.filename != '':
                imagen_nombre = imagen.filename
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                imagen.save(os.path.join(app.config['UPLOAD_FOLDER'], imagen_nombre))
                imagen_path = 'uploads/' + imagen_nombre
                cursor.execute('''
                    UPDATE productos SET imagen = ? WHERE id = ?
                ''', (imagen_path, id))
                
        cursor.execute('''
            UPDATE productos SET nombre=?, categoria=?, precio_normal=?, precio_oferta=?, descuento=?, descripcion=?
            WHERE id=?
        ''', (nombre, categoria, precio_normal, precio_oferta, descuento, descripcion, id))
            
        conexion.commit()
        conexion.close()
        return redirect(url_for('panel'))

    cursor.execute("SELECT * FROM productos WHERE id = ?", (id,))
    producto = cursor.fetchone()
    conexion.close()
    return render_template('editar.html', producto=producto)

@app.route('/admin/eliminar/<int:id>')
def eliminar(id):
    if not session.get('admin_logged'):
        return redirect(url_for('admin'))
        
    conexion = sqlite3.connect('tienda.db')
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM productos WHERE id = ?", (id,))
    conexion.commit()
    conexion.close()
    return redirect(url_for('panel'))

@app.route('/logout')
def logout():
    session.pop('admin_logged', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port5000, debug=True)
