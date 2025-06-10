from flask import Flask, request, jsonify
import requests
import os
from flask_cors import CORS
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()
API_KEY = os.getenv("API_KEY")
SOURCE_ID = "src_nNE4vEZ0EeEHNTUOdIT6S"  # cha_BgUii5mzrVWD9941P6Qnw

# Crear la app Flask
app = Flask(__name__)
CORS(app)  # Permitir peticiones desde el frontend

print("🧪 API_KEY (desde .env):", API_KEY)
print("📎 SOURCE_ID inicial:", SOURCE_ID)

@app.route("/")
def home():
    return "✅ API de ChatPDF funcionando correctamente."

@app.route("/upload", methods=["POST"])
def upload_pdf():
    global SOURCE_ID

    if "file" not in request.files:
        return jsonify({"error": "No se encontró archivo 'file' en la petición"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No se ha seleccionado ningún archivo"}), 400

    print(f"📤 Subiendo archivo: {file.filename}")

    files = [
        ("file", (file.filename, file.stream, "application/octet-stream"))
    ]

    headers = {
        "x-api-key": API_KEY,
    }

    try:
        response = requests.post(
            "https://api.chatpdf.com/v1/sources/add-file",
            headers=headers,
            files=files
        )

        print("✅ Código de respuesta:", response.status_code)
        print("📨 Respuesta completa:", response.text)

        if response.status_code == 200:
            json_resp = response.json()
            SOURCE_ID = json_resp.get("sourceId")
            print(f"🎉 Archivo subido correctamente. SOURCE_ID actualizado a: {SOURCE_ID}")
            return jsonify({"message": "Archivo subido correctamente", "sourceId": SOURCE_ID})
        else:
            return jsonify({
                "error": "Error subiendo archivo a ChatPDF",
                "status": response.status_code,
                "details": response.text
            }), 500

    except Exception as e:
        print("🔥 Excepción lanzada al subir archivo:", str(e))
        return jsonify({"error": str(e)}), 500

@app.route("/ask", methods=["POST"])
def ask_pdf():
    global SOURCE_ID

    print("\n📩 Se recibió una petición POST en /ask")

    user_input = request.json.get("message")
    print("🧠 Mensaje recibido:", user_input)

    if not user_input:
        print("❌ Error: No se recibió mensaje")
        return jsonify({"error": "Falta mensaje"}), 400

    if not API_KEY:
        print("❌ Error: API_KEY no configurada")
        return jsonify({"error": "API_KEY no configurada"}), 500

    if not SOURCE_ID:
        print("❌ Error: No se ha subido ningún PDF aún")
        return jsonify({"error": "No se ha subido ningún PDF aún. Usa /upload primero."}), 400

    # Aquí modificamos el prompt para añadir la instrucción extra
    enhanced_prompt = (
        f"""La pregunta del usuario es: {user_input}\n\n,. Responde a la pregunta del usuario basándote exclusivamente en el contenido del PDF subido.\n
        Complementa, si corresponde, pero sin alterar lo que aporte el documento subido, información relacionada con la normativa de instrucciones de 8 de marzo de 2017, de la Dirección General de Participación y Equidad, por las que se actualiza el protocolo de detección, identificación del alumnado con necesidades específicas de apoyo educativo y organización de la respuesta educativa., 
        Si existen mecasnismos de seneca ponlos basandote en el documento subido.\n
        Pon un teléfono, responsable si hubiere, de la estructura ETPOEP asociada al tema y la url del blog del etpoep más afín de los siguientes datos:
    ETPOEP CÓRDOBA
ESTRUCTURA ORGANIZATIVA

Coordinadora ETPOEP
Francisca Cerezo
957001219
Área de Necesidades Educativas Especiales
Cristina Ruiz
957001175
Área de Orientación Vocacional y Profesional
Raúl Roldán
957001506
Área de Recursos Técnicos
Carlos Serrano
957001504
Área de Compensación Educativa
Francisco López
957001245
Comisión Provincial de Absentismo
Alfredo Montero
957736324
Profesorado
ATAL, AED, CIMI, A. HOSPITALARIAS, USMIJ, PIACM
957001245
Área de Acción Tutorial y Convivencia
Antonio Páez
957001503
Gabinete de Convivencia e Igualdad
Presentación López
957001494
Gloria Torres
957002189
Bienestar Emocional
Olga García-Arévalo
Adela Vizcaíno
José Campillo
957002191


Zona Recursos Técnicos:
- Normativa y procedimientos de recursos técnicos: https://blogsaverroes.juntadeandalucia.es/etpoepcordoba/normativaprocedimiento-rrmmee/


Zona de Absentismos Escolar:
[Guía de absentismo escolar](https://drive.google.com/file/d/13Q8_o1xmz7VAnxOiKRRVm-mZFv0AqbVp/view?usp=sharing)
[Dossier de absentismo](https://drive.google.com/file/d/1cTOu5IYbpzwB5r7wsKGefAdEevl6vO5b/view?usp=sharing)

Zona de Compensación Educativa:
[Atención educativa domiciliaria](https://drive.google.com/open?id=1wOhWcoAaoE4oHvaEWPUzv7flGX1eyyRU)

**Aulas Hospitalarias:**
[Aulas Hospitalarias](https://blogsaverroes.juntadeandalucia.es/etpoepcordoba/ce-educacion-compensatoria-a-quien/)

Interculturalidad:  
[ATAL Normativa](http://www.adideandalucia.es/normas/ordenes/Orden%2015-1-2007%20Inmigrantes%20ATAL.pdf)  
[Dossier Atal](https://drive.google.com/open?id=189X4ghqOrmSktOCX7T5_I3s-anoCUn9Y)

[Instrucciones PROA](https://drive.google.com/open?id=17BzrQSqw6x8Bcv2RkfuPqNfXhLxfKz-G)
[Programa PROMOCIONA](https://blogsaverroes.juntadeandalucia.es/etpoepcordoba/subvenciones/)
[Subvenciones BOJA](https://juntadeandalucia.es/boja/2011/95/d1.pdf)


Zona de Acción Tutorial:
https://blogsaverroes.juntadeandalucia.es/etpoepcordoba/noticias-del-area-de-apoyo-a-la-funcion-tutorial-del-profesorado/

Normativa Altas Capacidades:  
https://blogsaverroes.juntadeandalucia.es/etpoepcordoba/normativa-altas-capacidades/

Zona de Gabinete:
https://blogsaverroes.juntadeandalucia.es/etpoepcordoba/8915-2/

Red Andaluza: Escuela Espacio de Paz (RAEEP):  
https://blogsaverroes.juntadeandalucia.es/etpoepcordoba/red-andaluza-escuela-espacio-de-paz-raeep/

ZONA DE ORIENTACIÓN VOCACIONAL Y PROFESIONAL
https://blogsaverroes.juntadeandalucia.es/etpoepcordoba/2024/01/24/presentamos-el-blog-de-orientacion-vocacional-y-profesional-de-andalucia/

Oferta formativa de Bachillerato en Córdoba y provincia.
https://blogsaverroes.juntadeandalucia.es/etpoepcordoba/2024/01/18/oferta-formativa-de-bachillerato-en-cordoba-y-provincia/

Orientación Profesional
https://blogsaverroes.juntadeandalucia.es/etpoepcordoba/ovp-transito-al-mundo-laboral/

Cultura Emprendedora
https://blogsaverroes.juntadeandalucia.es/etpoepcordoba/ovp-cultura-emprendedora/

MANUAL CONSEJOS ORIENTADOR
https://drive.google.com/file/d/1mcR32MLiNdJlQL6oPaEMjxZDdGn8SmDP/view

GUIA ORIENTACION VOCACIONAL
https://drive.google.com/file/d/1cy-tsqVqKhxC0hu3ptKsdqjWxtGRUPg4/view?usp=sharing

Recursos Personales
https://blogsaverroes.juntadeandalucia.es/etpoepcordoba/recursos-personales/

CONVENIOS CON FEDERACIONES
https://blogsaverroes.juntadeandalucia.es/etpoepcordoba/gabinete-d-convivenciaigualdad/

Centros Específicos de Educación Especial
https://blogsaverroes.juntadeandalucia.es/etpoepcordoba/eoe-e/

ETPOEP: Directorio
https://blogsaverroes.juntadeandalucia.es/etpoepcordoba/directorio/

Guía breve del ETPOEP 2023-2024
https://blogsaverroes.juntadeandalucia.es/etpoepcordoba/2024/02/21/actualizacion-de-la-guia-breve-del-etpoep/

Generador de Actuaciones Realizadas y Desplazamientos
https://script.google.com/a/macros/g.educaand.es/s/AKfycbwU1C6ndJUL2v7TkrZ_XIiAjbgRdMvsdWiVOzPuDPSuH27ZFrsyKvsDQ7FTuApw_uwq/exec

ETPOEP: ORIENTACIONES EOE
https://blogsaverroes.juntadeandalucia.es/etpoepcordoba/planes-provinciales/

ETPOEP: IMPRESOS RELLENABLES
https://blogsaverroes.juntadeandalucia.es/etpoepcordoba/impresos-rellenables/

LÍNEAS DE INTERVENCIÓNDEL EQUIPO DE ORIENTACIÓN EDUCATIVA ESPECIALIZADO
https://blogsaverroes.juntadeandalucia.es/etpoepcordoba/lineas-de-intervencion-del-eoee/

MOTÓRICOS
https://blogsaverroes.juntadeandalucia.es/etpoepcordoba/motoricos/

ALTAS CAPACIDADES INTELECTUALES
https://blogsaverroes.juntadeandalucia.es/etpoepcordoba/altas-capacidades-intelectuales/

TRASTORNOS GRAVES DE CONDUCTA
https://blogsaverroes.juntadeandalucia.es/etpoepcordoba/trastornos-graves-de-conducta/

DISCAPACIDAD AUDITIVA
https://blogsaverroes.juntadeandalucia.es/etpoepcordoba/discapacidad-auditiva/

ATENCIÓN TEMPRANA
https://blogsaverroes.juntadeandalucia.es/etpoepcordoba/atencion-temprana/

DIFICULTADES DE APRENDIZAJE
https://blogsaverroes.juntadeandalucia.es/etpoepcordoba/dificultades-especificas-de-aprendizaje-de-la-lectura-y-escritura/

TRASTORNO GENERALIZADO DEL DESARROLLO
https://blogsaverroes.juntadeandalucia.es/etpoepcordoba/trastorno-generalizado-del-desarrollo/

si no encuentras nada pon la web del blog del etpoep más afín: https://blogsaverroes.juntadeandalucia.es/etpoepcordoba/"""

       
    )
    print(enhanced_prompt)

    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "sourceId": SOURCE_ID,
        "messages": [
            {
                "role": "user",
                "content": enhanced_prompt
            }
        ]
    }

    print("📤 Enviando solicitud a ChatPDF...")
    print("🧾 Payload:", payload)

    try:
        response = requests.post("https://api.chatpdf.com/v1/chats/message",
                                 headers=headers, json=payload)

        print("✅ Código de respuesta:", response.status_code)
        print("📨 Respuesta completa:", response.text)

        if response.status_code == 200:
            return jsonify(response.json())
        else:
            print("⚠️ Error desde ChatPDF:", response.status_code)
            return jsonify({
                "error": "Error desde ChatPDF",
                "status": response.status_code,
                "details": response.text
            }), 500

    except Exception as e:
        print("🔥 Excepción lanzada:", str(e))
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
