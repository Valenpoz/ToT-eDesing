# Proyecto Final Patrones - Tienda de Totebags Personalizadas (ToT-e Desing)

Esta plataforma es una aplicación web de comercio electrónico que permite la venta y personalización de Totebags con estampas diseñadas por diferentes artistas. El sistema cuenta con tres roles principales: **Cliente**, **Artista** y **Administrador**.

El proyecto está estructurado con un **Backend** en Python (Flask), un **Frontend** dinámico en HTML, CSS y JavaScript (con Tailwind CSS), y una base de datos **MySQL**.

---

## 🛠️ Requisitos Previos

Antes de comenzar, asegúrate de tener instalado lo siguiente en tu sistema:

1. **Python 3.x** (probado con Python 3.11)
2. **MySQL Server** (instalado de forma local, por defecto en el puerto `3306`) o bien **Docker Desktop** (si prefieres usar contenedores)
3. **Navegador Web** moderno (Chrome, Edge, Firefox, etc.)
4. **VS Code** (opcional, pero recomendado con la extensión *Live Server*)

---

## 📂 Estructura del Proyecto

```text
Proyecto-Final-FIS/
│
├── Code/
│   ├── Backend/                 # Lógica del Servidor (Python + Flask)
│   │   ├── CRUD/                # Operaciones de base de datos
│   │   ├── services/            # Servicios y lógica de negocio
│   │   ├── app.py               # Punto de entrada de la API Flask
│   │   ├── db.py                # Configuración de conexión MySQL
│   │   ├── querydb.txt          # Definición SQL del esquema de la Base de Datos
│   │   ├── init_db.py           # Script para inicializar tablas automáticamente
│   │   ├── requirements.txt     # Dependencias de Python
│   │   └── docker-compose.yml   # Despliegue opcional de MySQL con Docker
│   │
│   └── Front/                   # Interfaz de Usuario (HTML, CSS, JS)
│       ├── js/                  # Lógica del cliente (login, carrito, estampas, etc.)
│       ├── images/              # Recursos visuales (camisas, estampas, carrito)
│       ├── index.html           # Página de inicio / catálogo de camisetas
│       ├── estampas.html        # Catálogo de estampas del artista
│       ├── carrito.html         # Carrito de compras y proceso de pedido
│       ├── login.html           # Inicio de sesión
│       ├── register.html        # Creación de cuentas
│       └── style.css            # Estilos personalizados
│
└── README.md                    # Este archivo de documentación
```

---

## 🚀 Guía de Instalación y Ejecución Paso a Paso

Sigue estos pasos detallados para configurar y levantar todo el sistema en tu máquina local:

### 1. Configuración de la Base de Datos (MySQL)

Tienes dos maneras de correr tu base de datos MySQL. Elige la que prefieras:

#### Opción A: Usando tu MySQL local (Recomendado)
1. Asegúrate de que tu servicio local de MySQL esté corriendo en el puerto estándar `3306`.
2. Revisa las credenciales de acceso de tu MySQL local. En el archivo `Code/Backend/db.py` debes configurar tu usuario y contraseña:
   ```python
   connection = mysql.connector.connect(
       host='localhost',
       port=3306,
       database='tienda_camisetas',
       user='TU_USUARIO',       # Ej: 'root'
       password='TU_CONTRASEÑA'  # Ej: 'password1'
   )
   ```

#### Opción B: Usando Docker (Alternativa aislada)
Si prefieres no instalar MySQL local, puedes usar Docker Desktop:
1. Abre **Docker Desktop**.
2. Abre una terminal en `Code/Backend/` y ejecuta:
   ```bash
   docker compose up -d
   ```
3. Esto levantará un contenedor de MySQL escuchando en el puerto `3307` (evitando conflictos con tu MySQL local). Recuerda que si usas esta opción, debes cambiar el puerto a `3307` en `Code/Backend/db.py`.

---

### 2. Configuración y Ejecución del Backend (Flask)

1. Abre tu terminal de comandos en la carpeta del backend:
   ```bash
   cd Code/Backend
   ```

2. **Crea un entorno virtual de Python** (altamente recomendado para no mezclar librerías globales):
   ```bash
   # En Windows:
   python -m venv venv
   ```

3. **Activa el entorno virtual**:
   ```bash
   # En Windows (PowerShell):
   .\venv\Scripts\Activate.ps1

   # En Windows (CMD):
   .\venv\Scripts\activate.bat

   # En macOS / Linux:
   source venv/bin/activate
   ```

4. **Instala las dependencias necesarias**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Inicializa la base de datos automáticamente**:
   Para ahorrarte tener que copiar y pegar comandos SQL en un cliente externo, ejecuta nuestro script automatizado que creará la base de datos `tienda_camisetas`, todas sus tablas, llaves foráneas y roles por defecto:
   ```bash
   python init_db.py
   ```
   *(Nota: Asegúrate de que tu MySQL esté encendido antes de correr este comando).*

6. **Inicia el servidor Flask**:
   ```bash
   python app.py
   ```
   El backend se iniciará y quedará escuchando peticiones en: **`http://127.0.0.1:5000`**

---

### 3. Configuración y Ejecución del Frontend

Dado que el frontend utiliza JavaScript dinámico para consumir la API de Flask, abrir los archivos HTML haciendo doble clic directo (`file:///`) puede generar problemas de CORS y bloqueos de seguridad del navegador. Por ende, debes servirlo desde un servidor web local:

#### Opción A: Usando la extensión "Live Server" de VS Code (Recomendado)
1. Abre la carpeta del proyecto en **VS Code**.
2. Instala la extensión **"Live Server"** (de Ritwick Dey).
3. Abre el archivo `Code/Front/index.html` en el editor, haz clic derecho y selecciona **"Open with Live Server"** (o presiona el botón *Go Live* abajo a la derecha).
4. Tu navegador se abrirá automáticamente en: **`http://127.0.0.1:5500/index.html`** (o similar).

#### Opción B: Usando el servidor de Python en terminal
1. Abre una nueva terminal en la carpeta raíz `Code/` del proyecto.
2. Ejecuta el servidor HTTP de Python:
   ```bash
   python -m http.server 8000
   ```
3. Abre tu navegador e ingresa a: **`http://localhost:8000/Front/index.html`**

---

## 👥 Cuentas de Prueba Pre-configuradas

Para facilitar la evaluación y navegación rápida del proyecto sin necesidad de registrar nuevas cuentas manualmente, el script de inicialización ha configurado los siguientes accesos:

| Rol de Usuario | Correo electrónico | Contraseña | ¿Qué permite hacer? |
| :--- | :--- | :--- | :--- |
| **Cliente** | `cliente@test.com` | `password1` | Navegar por camisetas, personalizarlas con estampas y gestionar pedidos en el carrito. |
| **Artista** | `artista@test.com` | `password1` | Subir y proponer nuevos diseños de estampas al catálogo. |
| **Administrador** | `admin@test.com` | `password1` | Gestionar usuarios, aprobar o rechazar diseños de estampas propuestos por los artistas. |

*¡Por supuesto, también puedes registrar tus propios usuarios usando el formulario de **Sign Up** en la aplicación!*

---

## 💡 Funcionalidades del Sistema

* **Catálogo de Camisetas**: Visualiza todas las prendas con sus respectivos tallajes, precios y stock disponible.
* **Personalización**: Selecciona una camiseta y agrégale una estampa artística autorizada para crear un producto único.
* **Carrito de Compras**: Administra las cantidades, elimina prendas personalizadas y procesa la compra vinculando tu usuario.
* **Sistema de Roles**: El backend restringe accesos y gestiona los permisos de manera controlada según el tipo de usuario.

---

## ⚡ Solución de Problemas Comunes

* **Error de conexión con la base de datos (`ConnectionRefusedError`)**:
  Asegúrate de que tu servidor MySQL local o tu contenedor de Docker esté activo y corriendo en el mismo puerto configurado en `db.py`.
* **Error 404 al navegar entre páginas**:
  Este error ocurría debido a rutas inconsistentes de navegación. Se ha limpiado el código del frontend de modo que todos los enlaces son **100% relativos y limpios** (ej: `register.html` en lugar de `../Front/register.html`), por lo que ahora funciona tanto en Live Server como en servidores estáticos locales.
