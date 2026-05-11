import pytest
import pytest_html
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

SCREENSHOTS_DIR = "reports/screenshots"

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Captura de pantalla automática en caso de fallo"""
    outcome = yield
    report = outcome.get_result()
    extras = getattr(report, "extra", [])

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            # Embeber en reporte HTML
            screenshot = driver.get_screenshot_as_base64()
            html = f'<div><img src="data:image/png;base64,{screenshot}" alt="screenshot" style="width:304px;height:228px;" onclick="window.open(this.src)" align="right"/></div>'
            extras.append(pytest_html.extras.html(html))

            # Guardar también como PNG
            os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
            driver.save_screenshot(f"{SCREENSHOTS_DIR}/FAIL_{item.name}.png")

    report.extra = extras

@pytest.fixture
def driver():
    """Fixture del navegador"""
    options = Options()

    # Headless solo en GitHub Actions (CI=true lo define GitHub automáticamente)
    if os.environ.get("CI"):
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    yield driver
    driver.quit()