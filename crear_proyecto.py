import os

# Crear estructura de carpetas automáticamente
os.makedirs("static/uploads", exist_ok=True)
os.makedirs("static/css", exist_ok=True)
os.makedirs("templates", exist_ok=True)

# 1. requirements.txt
with open("requirements.txt", "w", encoding="utf-8") as f:
  f.write("Flask\nFlask-SQLAlchemy\nPillow\n")

# 2. app.py
app_code = """import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tienda.db'
app.config['SECRET_KEY'] = 'clave_secreta_admin'
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQLAlchemy(app)

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    precio_normal = db.Column(db.Float, nullable=False)
    precio_oferta = db.Column(db.Float, nullable=True)
    descuento = db.Column(db.Integer, nullable=True)
    descripcion = db.Column(db.Text, nullable=True)
    imagen = db.Column(db.String(200), nullable=True)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    categoria_filtro = request.args.get('categoria')
    if categoria_filtro:
        productos = Producto.query.filter_by(categoria=categoria_filtro).all()
    else:
        productos = Producto.query.all()
    return render_template('index.html', productos=productos, categoria_activa=categoria_filtro)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    password_ingresada = request.form.get('password', '')
    autenticado = (password_ingresada == 'admin123')
    
    if request.method == 'POST' and autenticado:
        accion = request.form.get('accion')
        if accion == 'agregar':
            nombre = request.form.get('nombre')
            categoria = request.form.get('categoria')
            precio_normal = float(request.form.get('precio_normal'))
            precio_oferta_str = request.form.get('precio_oferta')
            precio_oferta = float(precio_oferta_str) if precio_oferta_str else None
            descuento_str = request.form.get('descuento')
            descuento = int(descuento_str) if descuento_str else None
            descripcion = request.form.get('descripcion')
            
            imagen_file = request.files.get('imagen')
            imagen_nombre = ''
            if imagen_file and imagen_file.filename != '':
                imagen_nombre = imagen_file.filename
                imagen_file.save(os.path.join(app.config['UPLOAD_FOLDER'], imagen_nombre))
                imagen_nombre = 'uploads/' + imagen_nombre
            
            nuevo_prod = Producto(
                nombre=nombre, categoria=categoria, precio_normal=precio_normal,
                precio_oferta=precio_oferta, descuento=descuento,
                descripcion=descripcion, imagen=imagen_nombre
            )
            db.session.add(nuevo_prod)
            db.session.commit()
            flash('¡Producto agregado con éxito!', 'success')
            
        elif accion == 'eliminar':
            prod_id = request.form.get('id')
            prod = Producto.query.get(prod_id)
            if prod:
                db.session.delete(prod)
                db.session.commit()
                flash('Producto eliminado.', 'warning')
                
    productos = Producto.query.all()
    return render_template('admin.html', productos=productos, autenticado=autenticado)

if __name__ == '__main__':
    app.run(debug=True)
"""
with open("app.py", "w", encoding="utf-8") as f:
  f.write(app_code)

# 3. Estilos CSS Estilo Tienda Comercial
css_code = """
body { background-color: #f8f9fa; font-family: 'Poppins', 'Segoe UI', Tahoma, sans-serif; }
.navbar-tienda { background-color: #111111; border-bottom: 3px solid #00a650; }
.navbar-brand { font-size: 1.8rem; letter-spacing: 1px; color: #ffffff !important; }
.card-producto { transition: all 0.3s ease; border: 1px solid #e0e0e0; border-radius: 12px; background: #fff; }
.card-producto:hover { transform: translateY(-6px); box-shadow: 0 12px 25px rgba(0,0,0,0.15); border-color: #00a650; }
.badge-descuento { background-color: #d32f2f; color: white; font-weight: bold; border-radius: 6px; padding: 6px 10px; }
.precio-tachado { text-decoration: line-through; color: #9e9e9e; font-size: 0.9rem; }
.precio-oferta { color: #d32f2f; font-weight: bold; font-size: 1.3rem; }
.carousel-item { height: 380px; background-color: #212121; border-radius: 15px; overflow: hidden; }
.carousel-item img { height: 100%; object-fit: cover; opacity: 0.8; }
.btn-verde { background-color: #00a650; color: white; font-weight: 600; }
.btn-verde:hover { background-color: #008f43; color: white; }
"""
with open("static/css/estilos.css", "w", encoding="utf-8") as f:
  f.write(css_code)

# 4. index.html con Carrusel Dinámico y mejor diseño
index_html = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>TCI Store - Tienda Oficial</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/estilos.css') }}">
</head>
<body>
    <!-- Barra de Navegación -->
    <nav class="navbar navbar-expand-lg navbar-dark navbar-tienda px-4 py-3 shadow-sm">
        <div class="container-fluid">
            <a class="navbar-brand fw-bold" href="/">TCI<span style="color: #00a650;">.STORE</span> 🛍️</a>
            <div class="d-flex">
                <a href="/admin" class="btn btn-outline-light btn-sm px-4 rounded-pill">⚙️ Panel Admin</a>
            </div>
        </div>
    </nav>

    <!-- Barra de Categorías -->
    <div class="container my-3">
        <div class="d-flex gap-2 overflow-auto pb-2">
            <a href="/" class="btn btn-dark btn-sm rounded-pill px-4 shadow-sm">🔥 Todos</a>
            <a href="/?categoria=Tecnologia" class="btn btn-outline-dark btn-sm rounded-pill px-4">💻 Tecnología</a>
            <a href="/?categoria=Moda" class="btn btn-outline-dark btn-sm rounded-pill px-4">👕 Moda</a>
            <a href="/?categoria=Hogar" class="btn btn-outline-dark btn-sm rounded-pill px-4">🏠 Hogar</a>
        </div>
    </div>

    <!-- Carrusel de Ofertas Principal -->
    <div class="container mb-5">
        <div id="bannerCarousel" class="carousel slide shadow rounded-4 overflow-hidden" data-bs-ride="carousel">
            <div class="carousel-indicators">
                <button type="button" data-bs-target="#bannerCarousel" data-bs-slide-to="0" class="active"></button>
                <button type="button" data-bs-target="#bannerCarousel" data-bs-slide-to="1"></button>
                <button type="button" data-bs-target="#bannerCarousel" data-bs-slide-to="2"></button>
            </div>
            <div class="carousel-inner">
                <div class="carousel-item active">
                    <img src="https://images.unsplash.com/photo-1607082348824-0a96f2a4b9da?auto=format&fit=crop&w=1200&q=80" class="d-block w-100" alt="Cyber Days">
                    <div class="carousel-caption d-none d-md-block bg-dark bg-opacity-50 rounded p-3">
                        <h2 class="fw-bold text-white">¡Mega Ofertas Cyber TCI!</h2>
                        <p class="fs-5">Descuentos imperdibles en toda la tecnología de última generación.</p>
                    </div>
                </div>
                <div class="carousel-item">
                    <img src="https://images.unsplash.com/photo-1483985988355-763728e1935b?auto=format&fit=crop&w=1200&q=80" class="d-block w-100" alt="Moda">
                    <div class="carousel-caption d-none d-md-block bg-dark bg-opacity-50 rounded p-3">
                        <h2 class="fw-bold text-white">Nueva Colección Moda</h2>
                        <p class="fs-5">Renueva tu guardarropa con las mejores tendencias y precios.</p>
                    </div>
                </div>
                <div class="carousel-item">
                    <img src="https://images.unsplash.com/photo-1556911220-e15b29be8c8f?auto=format&fit=crop&w=1200&q=80" class="d-block w-100" alt="Hogar">
                    <div class="carousel-caption d-none d-md-block bg-dark bg-opacity-50 rounded p-3">
                        <h2 class="fw-bold text-white">Especial Hogar y Confort</h2>
                        <p class="fs-5">Todo lo que necesitas para tu casa con ofertas exclusivas.</p>
                    </div>
                </div>
            </div>
            <button class="carousel-control-prev" type="button" data-bs-target="#bannerCarousel" data-bs-slide="prev">
                <span class="carousel-control-prev-icon"></span>
            </button>
            <button class="carousel-control-next" type="button" data-bs-target="#bannerCarousel" data-bs-slide="next">
                <span class="carousel-control-next-icon"></span>
            </button>
        </div>
    </div>

    <!-- Grilla de Productos -->
    <div class="container mb-5">
        <h3 class="mb-4 fw-bold text-dark">📦 Productos Destacados</h3>
        {% if not productos %}
            <div class="alert alert-warning text-center p-4 rounded-4 shadow-sm">
                <h5>Aún no hay productos en el catálogo.</h5>
                <p class="mb-2">Entra al panel de administración para agregar el primero.</p>
                <a href="/admin" class="btn btn-verde px-4 rounded-pill">Ir al Panel Admin</a>
            </div>
        {% else %}
            <div class="row row-cols-1 row-cols-md-3 row-cols-lg-4 g-4">
                {% for p in productos %}
                <div class="col">
                    <div class="card card-producto h-100 p-2 position-relative">
                        {% if p.descuento %}
                        <span class="badge badge-descuento position-absolute top-0 start-0 m-3 shadow-sm">-{{ p.descuento }}%</span>
                        {% endif %}
                        
                        {% if p.imagen %}
                        <img src="{{ url_for('static', filename=p.imagen) }}" class="card-img-top object-fit-cover rounded" style="height: 220px;" alt="{{ p.nombre }}">
                        {% else %}
                        <img src="https://via.placeholder.com/300x220?text=Sin+Imagen" class="card-img-top rounded" style="height: 220px;" alt="Sin imagen">
                        {% endif %}

                        <div class="card-body d-flex flex-column">
                            <span class="text-muted small text-uppercase fw-semibold">{{ p.categoria }}</span>
                            <h5 class="card-title fw-bold text-dark mt-1">{{ p.nombre }}</h5>
                            <p class="card-text text-muted small flex-grow-1">{{ p.descripcion[:60] }}...</p>
                            
                            <div class="mt-auto pt-2 border-top">
                                {% if p.precio_oferta %}
                                    <div class="precio-tachado">S/. {{ "%.2f"|format(p.precio_normal) }}</div>
                                    <div class="precio-oferta">S/. {{ "%.2f"|format(p.precio_oferta) }}</div>
                                {% else %}
                                    <div class="fw-bold fs-5 text-dark">S/. {{ "%.2f"|format(p.precio_normal) }}</div>
                                {% endif %}
                            </div>
                        </div>
                    </div>
                </div>
                {% endfor %}
            </div>
        {% endif %}
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""
with open("templates/index.html", "w", encoding="utf-8") as f:
  f.write(index_html)

# 5. admin.html
admin_html = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Panel Admin - TCI Store</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
    <div class="container my-5">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h2>⚙️ Panel de Control - TCI Store</h2>
            <a href="/" class="btn btn-dark rounded-pill px-4">Ver Tienda</a>
        </div>

        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}

        {% if not autenticado %}
            <div class="card shadow p-4 mx-auto rounded-4" style="max-width: 400px;">
                <h4 class="mb-3 text-center fw-bold">Acceso Administrador</h4>
                <form method="POST">
                    <div class="mb-3">
                        <label class="form-label">Contraseña</label>
                        <input type="password" name="password" class="form-control" placeholder="Contraseña (admin123)" required>
                    </div>
                    <button type="submit" class="btn btn-dark w-100 rounded-pill">Ingresar</button>
                </form>
            </div>
        {% else %}
            <div class="row">
                <div class="col-md-5 mb-4">
                    <div class="card shadow p-4 rounded-4 border-0">
                        <h4 class="mb-3 fw-bold text-success">➕ Agregar Producto</h4>
                        <form method="POST" enctype="multipart/form-data">
                            <input type="hidden" name="password" value="admin123">
                            <input type="hidden" name="accion" value="agregar">
                            
                            <div class="mb-3">
                                <label class="form-label">Nombre del Producto</label>
                                <input type="text" name="nombre" class="form-control" required>
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Categoría</label>
                                <select name="categoria" class="form-select">
                                    <option value="Tecnologia">Tecnología</option>
                                    <option value="Moda">Moda</option>
                                    <option value="Hogar">Hogar</option>
                                </select>
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Precio Normal (S/.)</label>
                                <input type="number" step="0.01" name="precio_normal" class="form-control" required>
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Precio Oferta (Opcional - S/.)</label>
                                <input type="number" step="0.01" name="precio_oferta" class="form-control">
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Descuento % (Ej: 20 para -20%)</label>
                                <input type="number" name="descuento" class="form-control">
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Descripción</label>
                                <textarea name="descripcion" class="form-control" rows="3"></textarea>
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Imagen del Producto</label>
                                <input type="file" name="imagen" class="form-control">
                            </div>
                            <button type="submit" class="btn btn-success w-100 rounded-pill">Guardar Producto</button>
                        </form>
                    </div>
                </div>

                <div class="col-md-7">
                    <div class="card shadow p-4 rounded-4 border-0">
                        <h4 class="mb-3 fw-bold">📦 Productos Registrados</h4>
                        <div class="table-responsive">
                            <table class="table align-middle">
                                <thead>
                                    <tr>
                                        <th>Nombre</th>
                                        <th>Precio</th>
                                        <th>Acción</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {% for p in productos %}
                                    <tr>
                                        <td class="fw-semibold">{{ p.nombre }}</td>
                                        <td>S/. {{ "%.2f"|format(p.precio_oferta if p.precio_oferta else p.precio_normal) }}</td>
                                        <td>
                                            <form method="POST" style="display:inline;">
                                                <input type="hidden" name="password" value="admin123">
                                                <input type="hidden" name="accion" value="eliminar">
                                                <input type="hidden" name="id" value="{{ p.id }}">
                                                <button type="submit" class="btn btn-danger btn-sm rounded-pill px-3">Eliminar</button>
                                            </form>
                                        </td>
                                    </tr>
                                    {% endfor %}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        {% endif %}
    </div>
</body>
</html>
"""
with open("templates/admin.html", "w", encoding="utf-8") as f:
  f.write(admin_html)

print("¡TCI Store actualizado con carrusel y nuevo estilo comercial!")