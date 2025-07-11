import requests
from bs4 import BeautifulSoup
import datetime
import hashlib

def obtener_tokens(session, url):
    """Obtiene tokens necesarios para el POST desde la página inicial."""
    r = session.get(url)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    viewstate = soup.find(id="__VIEWSTATE")["value"]
    viewstategenerator = soup.find(id="__VIEWSTATEGENERATOR")["value"]
    eventvalidation = soup.find(id="__EVENTVALIDATION")["value"]
    return viewstate, viewstategenerator, eventvalidation

def descargar_pdf():
    url_base = "https://www.csj.gov.py/verificarDocumento/Default.aspx?c=ccga00f&o=0"
    url_pdf_base = "https://www.csj.gov.py"

    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://www.csj.gov.py",
        "Referer": url_base,
    }

    # Obtener tokens para el POST
    viewstate, viewstategenerator, eventvalidation = obtener_tokens(session, url_base)

    # Datos del formulario POST
    data = {
        "__EVENTTARGET": "ver",
        "__EVENTARGUMENT": '{"codDocumento":3371006,"codTipoActuacion":6,"codOrigenBaseDato":0}',
        "__VIEWSTATE": viewstate,
        "__VIEWSTATEGENERATOR": viewstategenerator,
        "__EVENTVALIDATION": eventvalidation,
    }

    # Hacer POST para generar el PDF
    r_post = session.post(url_base, data=data, headers=headers, allow_redirects=False)
    if r_post.status_code == 302 and "Location" in r_post.headers:
        url_pdf = url_pdf_base + r_post.headers["Location"]
        print(f"Redirigiendo a PDF: {url_pdf}")

        # Descargar PDF
        r_pdf = session.get(url_pdf, headers=headers)
        if r_pdf.status_code == 200 and r_pdf.headers.get("Content-Type") == "application/pdf":
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"escrito_csj_{timestamp}.pdf"
            with open(filename, "wb") as f:
                f.write(r_pdf.content)
            print(f"PDF guardado como {filename}")

            # Calcular hash SHA256
            hash_sha256 = hashlib.sha256(r_pdf.content).hexdigest()
            print(f"Hash SHA256: {hash_sha256}")
            return filename, hash_sha256
        else:
            print("Error: No se pudo descargar el PDF correctamente")
    else:
        print("Error: POST no redirigió al PDF como se esperaba")

if __name__ == "__main__":
    descargar_pdf()
