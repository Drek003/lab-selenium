"""
test_saucedemo.py — Casos de prueba funcionales para SauceDemo.
Utiliza el patrón Page Object Model (POM) y el fixture 'driver' de conftest.py.
"""

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


class TestSauceDemo:
    """Suite de pruebas funcionales sobre https://www.saucedemo.com/"""

    # ── Credenciales ─────────────────────────────────────────────────────
    USUARIO_VALIDO = "standard_user"
    PASSWORD_VALIDO = "secret_sauce"
    USUARIO_INVALIDO = "usuario_falso"
    PASSWORD_INVALIDO = "clave_incorrecta"

    # ── Test 1: Login exitoso ────────────────────────────────────────────
    def test_login_exitoso(self, driver):
        """
        Verifica que un login con credenciales válidas redirige
        a la página de inventario (la URL contiene 'inventory').
        """
        login_page = LoginPage(driver)
        login_page.login(self.USUARIO_VALIDO, self.PASSWORD_VALIDO)

        # Validar que la URL contiene "inventory"
        inventory_page = InventoryPage(driver)
        inventory_page.esperar_carga()
        assert "pagina_que_no_existe" in driver.current_url, (
            f"Se esperaba 'inventory' en la URL, pero se obtuvo: {driver.current_url}"
        )

    # ── Test 2: Login fallido ────────────────────────────────────────────
    def test_login_fallido(self, driver):
        """
        Verifica que un login con credenciales incorrectas muestra
        el mensaje de error esperado.
        """
        login_page = LoginPage(driver)
        login_page.login(self.USUARIO_INVALIDO, self.PASSWORD_INVALIDO)

        mensaje_error = login_page.obtener_mensaje_error()
        mensaje_esperado = (
            "Epic sadface: Username and password do not match "
            "any user in this service"
        )
        assert mensaje_error == mensaje_esperado, (
            f"Mensaje de error inesperado: '{mensaje_error}'"
        )

    # ── Test 3: Agregar producto al carrito ──────────────────────────────
    def test_agregar_producto_al_carrito(self, driver):
        """
        Verifica que al agregar el producto 'Sauce Labs Backpack' al carrito,
        el badge del carrito muestra '1'.
        """
        # Paso 1: Login exitoso
        login_page = LoginPage(driver)
        login_page.login(self.USUARIO_VALIDO, self.PASSWORD_VALIDO)

        # Paso 2: Agregar producto
        inventory_page = InventoryPage(driver)
        inventory_page.esperar_carga()
        inventory_page.agregar_backpack_al_carrito()

        # Paso 3: Validar badge del carrito
        cantidad = inventory_page.obtener_cantidad_carrito()
        assert cantidad == "1", (
            f"Se esperaba '1' en el badge del carrito, pero se obtuvo: '{cantidad}'"
        )
