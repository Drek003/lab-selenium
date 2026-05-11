"""
login_page.py — Page Object del formulario de login de SauceDemo.
Encapsula locators y acciones de la página de inicio de sesión.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    """Page Object para https://www.saucedemo.com/"""

    # ── URL ──────────────────────────────────────────────────────────────
    URL = "https://www.saucedemo.com/"

    # ── Locators (constantes de clase) ───────────────────────────────────
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    # ── Acciones ─────────────────────────────────────────────────────────
    def abrir(self):
        """Navega a la página de login."""
        self.driver.get(self.URL)
        self.wait.until(EC.visibility_of_element_located(self.LOGIN_BUTTON))

    def ingresar_usuario(self, usuario: str):
        """Escribe el nombre de usuario en el campo correspondiente."""
        campo = self.wait.until(EC.visibility_of_element_located(self.USERNAME_INPUT))
        campo.clear()
        campo.send_keys(usuario)

    def ingresar_password(self, password: str):
        """Escribe la contraseña en el campo correspondiente."""
        campo = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_INPUT))
        campo.clear()
        campo.send_keys(password)

    def hacer_click_login(self):
        """Hace clic en el botón de login."""
        boton = self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON))
        boton.click()

    def login(self, usuario: str, password: str):
        """Flujo completo: abre la página, ingresa credenciales y hace clic en Login."""
        self.abrir()
        self.ingresar_usuario(usuario)
        self.ingresar_password(password)
        self.hacer_click_login()

    def obtener_mensaje_error(self) -> str:
        """Retorna el texto del mensaje de error mostrado tras un login fallido."""
        elemento = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
        return elemento.text
