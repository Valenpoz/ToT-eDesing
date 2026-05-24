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

const estampas = [
    { id: 0, titulo: "America", descripcion: "Logo del equipo de futbol America de Cali", img: "images/estampas/estampaAmerica.png", estado: "aprobada" },
    { id: 1, titulo: "Cali", descripcion: "Logo del equipo de futbol Deportivo Cali", img: "images/estampas/estampaCali.png", estado: "pendiente" },
    { id: 2, titulo: "Millonarios", descripcion: "Logo del equipo del equipo de futbol Millonarios", img: "images/estampas/estampaMillonarios.png", estado: "pendiente" },
    { id: 3, titulo: "Nacional", descripcion: "Logo del equipo de futbol de Nacional", img: "images/estampas/estampaNacional.png", estado: "aprobada" },
    { id: 4, titulo: "Naruto", descripcion: "Logo de la serie animada Naruto", img: "images/estampas/estampaNaruto.png", estado: "pendiente" },
    { id: 5, titulo: "RealMadrid", descripcion: "Logo del equipo de futbol RealMadrid", img: "images/estampas/estampaRM.png", estado: "aprobada" },
    { id: 6, titulo: "Stitch", descripcion: "Stitch de lilo y Stitch", img: "images/estampas/estampaDibujo1.png", estado: "aprobada" },
    { id: 7, titulo: "Piolin", descripcion: "Estampa de piolin", img: "images/estampas/estampaDibujo2.png", estado: "aprobada" },
    { id: 8, titulo: "Tralalero", descripcion: "Estampa de Tralalero Tralala", img: "images/estampas/estampaDibujo3.png", estado: "pendiente" },
    { id: 9, titulo: "Gato SM", descripcion: "Gato de la serie Sailor Moon", img: "images/estampas/estampaDibujo4.png", estado: "aprobada" },
    { id: 10, titulo: "Black Sabbath", descripcion: "Logo banda Black Sabbath", img: "images/estampas/estampaBanda1.png", estado: "pendiente" },
    { id: 11, titulo: "AC DC", descripcion: "Logo banda AC DC", img: "images/estampas/estampaBanda2.png", estado: "aprobada" },
    { id: 12, titulo: "Nirvana", descripcion: "Logo banda Nirvana", img: "images/estampas/estampaBanda3.png", estado: "pendiente" },
    { id: 13, titulo: "Linkin Park", descripcion: "Logo banda Linkin Park", img: "images/estampas/estampaBanda4.png", estado: "pendiente" },
    { id: 14, titulo: "Green Day", descripcion: "Logo banda GreenDay", img: "images/estampas/estampaBanda5.png", estado: "aprobada" },
    


];






// Función principal para ejecutar al cargar el DOM
function main() {
    try {
        // Verificar si hay una camisa seleccionada
        const selectedProduct = JSON.parse(localStorage.getItem("selectedProduct"));
        const container = document.getElementById("products-container");
        
        if (!selectedProduct) {
            // Si no hay camisa seleccionada, mostrar mensaje pero seguir mostrando estampas
            const messageContainer = document.createElement("div");
            messageContainer.className = "col-span-full mb-8";
            messageContainer.innerHTML = `
                <div class="bg-yellow-50 border border-yellow-200 rounded-lg p-6 text-center">
                    <p class="text-gray-700 text-lg mb-4">⚠️ Primero debes seleccionar una camisa</p>
                    <a href="index.html" class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded">
                        Ir a seleccionar camisa
                    </a>
                </div>
            `;
            container.appendChild(messageContainer);
        } else {
            // Mostrar información de la camisa seleccionada
            const infoContainer = document.createElement("div");
            infoContainer.className = "bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6";
            infoContainer.innerHTML = `
                <div class="flex items-center gap-4">
                    <img src="${selectedProduct.img}" alt="${selectedProduct.name}" class="w-16 h-16 object-contain">
                    <div>
                        <h3 class="font-semibold text-gray-800">${selectedProduct.name}</h3>
                        <p class="text-sm text-gray-600">Cantidad: ${selectedProduct.quantity}</p>
                        <p class="text-sm text-blue-600">Ahora selecciona una estampa para esta camisa</p>
                    </div>
                </div>
            `;
            
            container.parentNode.insertBefore(infoContainer, container);
        }

        // Siempre mostrar las estampas
        estampas.forEach(estampa => {
            // Crear un div para cada estampa
            const div = document.createElement("div");
            div.className = "bg-white rounded-lg shadow-md overflow-hidden";
            
            // Determinar si la estampa está disponible y si hay camisa seleccionada
            const isAvailable = estampa.estado === "aprobada" && selectedProduct;
            const isDisabled = !selectedProduct;
            
            div.innerHTML = `
            <div class="relative group">
                <img 
                    src="${estampa.img}"   
                    alt="${estampa.titulo}" 
                    class="w-full h-64 object-contain transition-all duration-300 ${!isAvailable || isDisabled ? 'grayscale opacity-50' : ''}">

                ${isAvailable && !isDisabled ? `
                <div class="absolute bottom-0 left-0 right-0 flex flex-col gap-2 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                    <button 
                        class="select-stamp-btn bg-white hover:bg-gray-100 text-gray-800 px-3 py-1 text-sm font-medium shadow-md w-full"
                        data-stamp-id="${estampa.id}">Seleccionar estampa
                    </button>
                </div>
                ` : `
                <div class="absolute bottom-0 left-0 right-0 bg-gray-800 bg-opacity-75 p-2">
                    <p class="text-white text-xs text-center">
                        ${isDisabled ? 'Selecciona una camisa primero' : 'No disponible'}
                    </p>
                </div>
                `}
            </div>
            
            <div class="p-4">
                <div class="flex justify-between items-center">
                    <h3 class="text-left text-lg font-semibold text-gray-800 pr-2">${estampa.titulo}</h3>
                    <p class="text-xs font-bold ${getStatusColor(estampa.estado)}">${estampa.estado}</p>
                </div>
                <p class="text-sm text-gray-600 mt-1">${estampa.descripcion}</p>
            </div>

        `;
            container.appendChild(div);
            
            // Solo agregar event listener si la estampa está disponible Y hay camisa seleccionada
            if (isAvailable && !isDisabled) {
                const selectStampBtn = div.querySelector('.select-stamp-btn');
                selectStampBtn.addEventListener('click', () => {
                    selectStampAndAddToCart(estampa.id);
                });
            }
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

// Función para seleccionar estampa y agregar al carrito
function selectStampAndAddToCart(stampId) {
    const selectedProduct = JSON.parse(localStorage.getItem("selectedProduct"));
    const selectedStamp = estampas.find(e => e.id === stampId);
    
    if (!selectedProduct || !selectedStamp) {
        alert("Error: No se pudo procesar la selección");
        return;
    }

    // Crear el producto completo con camisa y estampa
    const completedProduct = {
        id: `${selectedProduct.id}-${selectedStamp.id}`, // ID único combinado
        name: `${selectedProduct.name} con ${selectedStamp.titulo}`,
        price: selectedProduct.price, // Podrías agregar precio de estampa aquí
        img: selectedProduct.img,
        talla: selectedProduct.talla || 'N/A',
        quantity: selectedProduct.quantity,
        estampa: {
            id: selectedStamp.id,
            titulo: selectedStamp.titulo,
            descripcion: selectedStamp.descripcion,
            img: selectedStamp.img
        },
        camisa: {
            id: selectedProduct.id,
            name: selectedProduct.name,
            img: selectedProduct.img
        }
    };

    // Obtener carrito actual
    let cart = JSON.parse(localStorage.getItem("cart")) || [];
    
    // Verificar si ya existe este producto exacto (misma camisa + estampa)
    const existingIndex = cart.findIndex(item => item.id === completedProduct.id);
    
    if (existingIndex > -1) {
        // Si ya existe, aumentar cantidad
        cart[existingIndex].quantity += completedProduct.quantity;
    } else {
        // Si no existe, agregar nuevo
        cart.push(completedProduct);
    }

    // Guardar en localStorage
    localStorage.setItem("cart", JSON.stringify(cart));
    localStorage.setItem("cartTimestamp", new Date().getTime());
    
    // Limpiar selección temporal
    localStorage.removeItem("selectedProduct");
    
    // Mostrar mensaje de éxito
    showSuccessMessage(selectedProduct.name, selectedStamp.titulo);
    
    // Redirigir después de un delay más corto, pero dando opción al usuario
    setTimeout(() => {
        if (confirm("¿Deseas ir al carrito para ver tu producto?")) {
            window.location.href = "carrito.html";
        } else {
            window.location.href = "index.html";
        }
    }, 1200);
}

// Función para mostrar mensaje de éxito
function showSuccessMessage(camisaName, estampaName) {
    // Crear elemento de mensaje
    const successMessage = document.createElement("div");
    successMessage.className = "fixed top-4 right-4 bg-green-500 text-white px-6 py-4 rounded-lg shadow-lg z-50 transform translate-x-full transition-transform duration-300";
    successMessage.innerHTML = `
        <div class="flex items-center gap-3">
            <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
            </svg>
            <div>
                <p class="font-semibold">¡Producto agregado al carrito!</p>
                <p class="text-sm opacity-90">${camisaName} con ${estampaName}</p>
            </div>
        </div>
    `;
    
    document.body.appendChild(successMessage);
    
    // Animar entrada
    setTimeout(() => {
        successMessage.classList.remove("translate-x-full");
    }, 100);
    
    // Animar salida y remover
    setTimeout(() => {
        successMessage.classList.add("translate-x-full");
        setTimeout(() => {
            if (successMessage.parentNode) {
                successMessage.parentNode.removeChild(successMessage);
            }
        }, 300);
    }, 2500);
}

// Función para obtener el color según el estado de la estampa
function getStatusColor(estado) {
    switch(estado) {
        case "aprobada":
            return "text-green-500";
        case "pendiente":
            return "text-yellow-500";
        case "no disponible":
            return "text-red-500";
        default:
            return "text-gray-500";
    }
}

