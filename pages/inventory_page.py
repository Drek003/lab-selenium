"""
inventory_page.py — Page Object de la página de inventario/carrito de SauceDemo.
Encapsula locators y acciones de la página de productos.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class InventoryPage:
    """Page Object para https://www.saucedemo.com/inventory.html"""

    # ── Locators (constantes de clase) ───────────────────────────────────
    ADD_BACKPACK_BUTTON = (By.ID, "add-to-cart-sauce-labs-backpack")
    CART_BADGE = (By.CSS_SELECTOR, ".shopping_cart_badge")
    INVENTORY_CONTAINER = (By.ID, "inventory_container")

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    # ── Acciones ─────────────────────────────────────────────────────────
    def esperar_carga(self):
        """Espera a que el contenedor de inventario sea visible."""
        self.wait.until(EC.visibility_of_element_located(self.INVENTORY_CONTAINER))

    def agregar_backpack_al_carrito(self):
        """Hace clic en el botón 'Add to cart' del producto Sauce Labs Backpack."""
        boton = self.wait.until(EC.element_to_be_clickable(self.ADD_BACKPACK_BUTTON))
        boton.click()

    def obtener_cantidad_carrito(self) -> str:
        """Retorna el texto del badge del carrito (cantidad de productos)."""
        badge = self.wait.until(EC.visibility_of_element_located(self.CART_BADGE))
        return badge.text
