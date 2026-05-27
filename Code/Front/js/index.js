
// Código para el menú desplegable del perfil
const menuButton = document.getElementById('menu-button');
const dropdown = document.getElementById('profile-dropdown');

menuButton.addEventListener('click', (e) => {
    e.stopPropagation();
    dropdown.classList.toggle('hidden');
});

window.addEventListener('click', (e) => {
    if (!menuButton.contains(e.target) && !dropdown.contains(e.target)) {
        dropdown.classList.add('hidden');
    }
});



//Verificar si el usuario está logeado
// y mostrar su nombre en el perfil
const user = JSON.parse(sessionStorage.getItem("user"));
const profile = document.getElementById('perfil');

if (user) {
    console.log("Nombre del usuario:", user.nombre);
    const nombreUsuario = user.nombre || "Usuario Anónimo";

    if (profile) {
        profile.innerText = nombreUsuario;
    }

} else {
    console.warn("Usuario no logeado");

    if (profile) {
        profile.innerText = "Invitado";  // O déjalo vacío si prefieres
    }

    // window.location.href = "/Front/login.html";
}

// Datos de los productos
// nombre, precio, imagen, talla, stock
const EXPIRATION_MINUTES = 30;

// Al cargar la página
const lastCartTime = localStorage.getItem("cartTimestamp");
if (lastCartTime) {
    const now = new Date().getTime();
    const diffMinutes = (now - parseInt(lastCartTime)) / 60000;

    if (diffMinutes > EXPIRATION_MINUTES) {
        localStorage.removeItem("cart");
        localStorage.removeItem("cartTimestamp");
        console.log("Carrito expirado");
    }
}


// Datos de los productos
async function obtenerDatos() {
    try {
        const respuesta = await fetch('/productos', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        if (!respuesta.ok) throw new Error('Error en la respuesta del servidor');

        const datos = await respuesta.json();
        console.log('Datos obtenidos:', datos);

        return datos;
    } catch (error) {
        console.error('Error al obtener los datos:', error);
    }
}

const products = [
    { id: 0, name: "Totebag Grande Blanca", price: 80000, img: "images/totebag/toteGrandeBlanca.png", talla: "Grande", stock: 10 },
    { id: 1, name: "Totebag De Lona", price: 25000, img: "images/totebag/toteDeLona.png", talla: "Pequeña", stock: 5 },
    { id: 2, name: "Totebag Grande Lima", price: 70000, img: "images/totebag/toteGrandeLima.png", talla: "Grande", stock: 8 },
    { id: 3, name: "Totebag Grande RosaBlue", price: 90000, img: "images/totebag/toteGrandeRosaBlue.png", talla: "Grande", stock: 3 },
    { id: 4, name: "Totebag Grande Verde", price: 70000, img: "images/totebag/toteGrandeVerde.png", talla: "Media", stock: 12 },
    { id: 5, name: "Totebag Grande Roja", price: 50000, img: "images/totebag/toteGrandeRoja.png", talla: "Media", stock: 7 },
    { id: 6, name: "Totebag Pequeña Azul", price: 30000, img: "images/totebag/totepequeAzul.png", talla: "Pequeña", stock: 4 },
    { id: 7, name: "Totebag Pequeña Cian", price: 25000, img: "images/totebag/totePequeCian.png", talla: "Pequeña", stock: 20},
    { id: 8, name: "Totebag Pequeña Negra", price: 30000, img: "images/totebag/totepequeNegra.png", talla: "Media", stock: 25},
    { id: 9, name: "Totebag Pequeña Roja", price: 30000, img: "images/totebag/totePequeRoja.png", talla: "Pequeña", stock: 20},
    { id: 10, name: "Totebag Grande Negra", price: 500000, img: "images/totebag/toteNegraGrande.png", talla: "Grande", stock: 22},
    { id: 12, name: "Totebag Grande Blanca y Rojo", price: 50000, img: "images/totebag/toteGrandeBlancaRoja.png", talla: "Grande", stock: 20},
];


// <button onclick="window.modal.showModal()">Abrir Modal</button>

//         <dialog id="modal" class="bg-white p-6 rounded-lg shadow-lg">
//             <h2>Prueba</h2>
//             <p>Sirve¿</p>
//             <button onclick="window.modal.close()">
//                 Cerrar
//         </dialog>




// Función principal para ejecutar al cargar el DOM
function main() {
    try {

        // const products = await obtenerDatos();
        const container = document.getElementById("products-container");

        products.forEach(product => {
            // Crear un div para cada producto
            const div = document.createElement("div");
            div.className = "bg-white rounded-lg shadow-md overflow-hidden";
            div.innerHTML = `
            <div class="relative group">
                <img 
                    src="${product.img}"   
                    alt="${product.name}" 
                    class="w-full h-64 object-contain transition-all duration-300">

                <div class="absolute bottom-0 left-0 right-0 flex flex-col gap-2 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                    <button 
                        class="add-to-cart-btn bg-white hover:bg-gray-100 text-gray-800 px-3 py-1 text-sm font-medium shadow-md w-full"
                        data-product-id="${product.id}">Agregar al carrito
                    </button>
                    
                </div>

                
            </div>
            
            <div class="p-4">
                <div class="flex justify-between items-center">
                    <h3 class="text-left text-lg font-semibold text-gray-800 pr-2">${product.name}</h3>
                    <p class="text-xl font-bold text-blue-600">$${product.price}</p>
                </div>
                <p class="text-sm text-gray-600 mt-1">${product.talla}</p>
            </div>

        `;
            container.appendChild(div);
            
            // Add event listener to the button after it's been added to the DOM
            const addToCartBtn = div.querySelector('.add-to-cart-btn');
            addToCartBtn.addEventListener('click', () => {
                openModal(product.id);
            });
        });
    } catch (err) {
        console.error(err);
        document.getElementById('catalogo').innerText = 'No se pudo cargar el catálogo.';
    }
}

// Ejecutar apenas cargue el DOM
document.addEventListener('DOMContentLoaded', main);


function toggleDropdown(dropdownId) {
    const dropdown = document.getElementById(dropdownId);
    dropdown.classList.toggle('hidden');
}

// Agrega un producto al carrito
function addProduct(id) {
  const product = products.find(p => p.id === id);
  if (product) {
    let cart = JSON.parse(localStorage.getItem("cart")) || [];
    const existing = cart.find(item => item.id === product.id);

    if (existing) {
      existing.quantity += 1;
    } else {
      cart.push({ ...product, quantity: 1 });
    }

    localStorage.setItem("cart", JSON.stringify(cart));
    localStorage.setItem("cartTimestamp", new Date().getTime());
    alert(`${product.name} agregado al carrito`);
  } else {
    console.error("Producto no encontrado");
  }
}




// Abre el modal con la info del producto
function openModal(productId) {
  const product = products.find(p => p.id === productId);
  if (!product) return;

  document.getElementById("modal-img").src = product.img;
  document.getElementById("modal-title").textContent = product.name;
  document.getElementById("modal-quantity").value = 1;

  window.selectedProduct = product;

  const modal = document.getElementById("product-modal");
  modal.showModal();
  
  // Add event listeners for modal interactions
  setupModalEventListeners();
}

// Configura los event listeners del modal
function setupModalEventListeners() {
    const modal = document.getElementById("product-modal");
    const closeBtn = document.getElementById("close-modal-btn");
    const addToCartBtn = document.getElementById("add-to-cart-modal-btn");
    
    // Remove existing listeners to prevent duplicates
    const newCloseBtn = closeBtn.cloneNode(true);
    closeBtn.parentNode.replaceChild(newCloseBtn, closeBtn);
    
    const newAddToCartBtn = addToCartBtn.cloneNode(true);
    addToCartBtn.parentNode.replaceChild(newAddToCartBtn, addToCartBtn);
    
    // Add close button listener
    newCloseBtn.addEventListener('click', closeModal);
    
    // Add "Agregar al carrito" button listener
    newAddToCartBtn.addEventListener('click', goToNextStep);
    
    // Close modal when clicking outside
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            closeModal();
        }
    });
}


// Cierra el modal
function closeModal() {
    const modal = document.getElementById("product-modal");
    modal.close();
    
    // Clean up - remove click outside listener
    modal.removeEventListener('click', closeModal);
}

// Ir a la siguiente página y guardar info temporal
function goToNextStep() {
    const quantity = parseInt(document.getElementById("modal-quantity").value);

    if (quantity < 1) {
        alert("Cantidad inválida");
        return;
    }

    const product = window.selectedProduct;

    // Guardar temporalmente en localStorage para usar en la siguiente página
    const tempSelection = {
        id: product.id,
        name: product.name,
        img: product.img,
        price: product.price,  // Agregar el precio
        talla: product.talla,  // Agregar la talla
        stock: product.stock,  // Agregar el stock
        quantity: quantity
    };

    localStorage.setItem("selectedProduct", JSON.stringify(tempSelection));

    // Redirigir a la página que tú indiques
    window.location.href = "estampas.html";  // <-- cámbialo por tu ruta
}
