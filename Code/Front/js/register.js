console.log("Register script loaded");

const registerForm = document.getElementById('registerForm');

registerForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const nombre = document.querySelector('input[placeholder="Username"]').value;
    const correo = document.querySelector('input[placeholder="Email"]').value;
    const contrasena = document.querySelector('input[placeholder="Password"]').value;
    const rol_id = document.getElementById('role').value;

    console.log("Datos:", { nombre, correo, contrasena, rol_id });

    try {
        const response = await fetch("http://127.0.0.1:5000/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                nombre,
                correo,
                contrasena,
                rol_id
            })
        });

        if (response.ok) {
            const data = await response.json();
            alert('Registro exitoso: ' + data.message);

            // Redirigir al usuario a la página de inicio de sesión o a otra página
            window.location.href = "login.html"; 
        } else {
            const errorData = await response.json();
            alert('Error: ' + errorData.message);
        }

    } catch (error) {
        console.error('Error de conexión:', error);
        alert('No se pudo conectar con el servidor');
    }
});
