from playwright.sync_api import sync_playwright
import hashlib
import datetime

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        url = "https://www.csj.gov.py/verificarDocumento/Default.aspx?c=ccga00f&o=0"
        page.goto(url)

        # Cambia el selector según corresponda
        page.click("#btnMostrar")

        # Esperar que el contenido aparezca
        page.wait_for_selector("#contenidoEscrito")

        contenido = page.inner_html("#contenidoEscrito")

        fecha = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"escrito_csj_{fecha}.html"
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            f.write(contenido)

        hash_sha256 = hashlib.sha256(contenido.encode('utf-8')).hexdigest()
        print(f"Archivo guardado: {nombre_archivo}")
        print(f"Hash SHA256: {hash_sha256}")

        browser.close()

if __name__ == "__main__":
    main()
