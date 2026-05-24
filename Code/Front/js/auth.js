function verificarSesion(redirigir = true) {
    const user = JSON.parse(sessionStorage.getItem("user"));
    if (!user && redirigir) {
        window.location.href = "login.html";
    }
    return user;
}