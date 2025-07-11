from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import hashlib
import datetime

def main():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=options)
    try:
        url = "https://www.csj.gov.py/verificarDocumento/Default.aspx?c=ccga00f&o=0"
        driver.get(url)

        # Cambia el selector del botón según corresponda
        boton = driver.find_element(By.ID, "btnMostrar")  # Ejemplo, cambia si es otro
        boton.click()

        driver.implicitly_wait(5)

        # Cambia el selector del contenido según corresponda
        contenido = driver.find_element(By.ID, "contenidoEscrito").get_attribute('innerHTML')

        fecha = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"escrito_csj_{fecha}.html"
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            f.write(contenido)

        hash_sha256 = hashlib.sha256(contenido.encode('utf-8')).hexdigest()
        print(f"Archivo guardado: {nombre_archivo}")
        print(f"Hash SHA256: {hash_sha256}")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
