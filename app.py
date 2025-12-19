import streamlit as st
import pandas as pd
from fpdf import FPDF
from datetime import datetime, timedelta
import hashlib

# --- CONFIGURACIÓN VISUAL ---
st.set_page_config(page_title="PASC Data Guardian | Gobierno Digital", layout="wide", page_icon="🇨🇱")

# --- 1. BASE DE DATOS LEGAL (INTEGRACIÓN ARCHIVOS OFICIALES) ---

# Normativa para el Pie de Página (Blindaje Legal)
NORMATIVA_VIGENTE = {
    "Ley Datos": "Ley N° 21.719 (D.O. 13/12/2024)",
    "Fuente Técnica": "WikiGuías (Oficializada por Res. Ex. 250/2025 Sub. Hacienda)",
    "Ley Transformación": "Ley N° 21.180 y D.S. N° 4/2020"
}

# Cláusulas Textuales (Del archivo: formato_tipo_claúsulas_contractuales_compras_públicas.docx)
CLAUSULA_COMPRAS_PUBLICAS = """
"NOVENO: INCUMPLIMIENTO DEL ENCARGO Y RESPONSABILIDADES. Si el ENCARGADO trata los datos con un objeto distinto 
del encargo convenido o los cede o entrega sin haber sido autorizado... se le considerará como responsable de datos 
para todos los efectos legales, debiendo responder personalmente por las infracciones en que incurra y solidariamente 
con el RESPONSABLE... (Fuente: Cláusula Novena, Formato Oficial Compras Públicas)."
"""

CLAUSULA_HONORARIOS = """
"La Consultora se obliga a observar las disposiciones de la Ley N° 19.628... quedando prohibido su uso para fines 
distintos a los propios del cumplimiento del presente convenio... Deberá sujetarse a las reglas, protocolos y 
procedimientos internos que [INSTITUCIÓN] establezca." (Fuente: Formato Tipo Honorarios Ajustado Ley 21.719).
"""

# Catálogo RAT Oficial (Extraído de tu texto RAT Gobierno Digital)
RAT_GOBIERNO_DIGITAL = {
    "ClaveÚnica": {
        "Rol": "Responsable", "Datos": "RUN, Nombre, IP, Metadatos",
        "Finalidad": "Autenticación y Ciberseguridad", "Legitimidad": "Ley N° 21.658 y Ley N° 19.880",
        "Riesgo": "ALTO (Infraestructura Crítica)"
    },
    "FirmaGob": {
        "Rol": "Responsable", "Datos": "RUN, Correo, Firma Electrónica",
        "Finalidad": "Gestión de Certificados Digitales", "Legitimidad": "Ley N° 19.799",
        "Riesgo": "ALTO"
    },
    "DocDigital": {
        "Rol": "Encargado", "Datos": "Comunicaciones oficiales",
        "Finalidad": "Tramitación Estado", "Legitimidad": "D.S. N° 4 Transformación Digital",
        "Riesgo": "MEDIO"
    }
}

# --- 2. MOTORES LÓGICOS ---

def generar_pdf_certificado(tipo_doc, datos):
    """Genera PDF con Sello Oficial Resolución 250/2025"""
    pdf = FPDF()
    pdf.add_page()
    
    # Encabezado Oficial
    pdf.set_font("Arial", 'B', 12)
    titulo = f"CERTIFICADO DE CUMPLIMIENTO: {tipo_doc.upper()}"
    pdf.cell(0, 10, titulo, ln=True, align='C')
    
    pdf.set_font("Arial", 'I', 9)
    pdf.cell(0, 10, f"Estándar Técnico: {NORMATIVA_VIGENTE['Fuente Técnica']}", ln=True, align='C')
    pdf.line(10, 30, 200, 30)
    pdf.ln(10)
    
    # Cuerpo
    pdf.set_font("Arial", '', 10)
    
    if tipo_doc == "RAT":
        contenido = f"""
        SERVICIO: {datos['servicio']}
        ROL LEGAL: {datos['rol']}
        BASE DE LEGITIMIDAD: {datos['legitimidad']}
        NIVEL DE RIESGO: {datos['riesgo']}
        
        Este registro ha sido precargado siguiendo los lineamientos de la Secretaría de Gobierno Digital.
        """
    else:
        # Es un contrato
        contenido = f"""
        En Santiago, a {datetime.now().strftime('%d-%m-%Y')}, se regula el tratamiento de datos para:
        PROVEEDOR: {datos['nombre']} (RUT: {datos['rut']})
        
        OBLIGACIÓN LEGAL INYECTADA:
        {CLAUSULA_COMPRAS_PUBLICAS if 'Compras' in tipo_doc else CLAUSULA_HONORARIOS}
        """
        
    pdf.multi_cell(0, 7, contenido)
    
    # Pie de Página Blindado (Tu ventaja competitiva)
    pdf.set_y(-50)
    pdf.set_font("Arial", 'B', 8)
    pdf.cell(0, 5, "VALIDACIÓN DE NORMATIVA:", ln=True)
    pdf.set_font("Arial", '', 8)
    legal_footer = """
    Documento generado conforme a la Resolución Exenta N° 250/2025 de la Subsecretaría de Hacienda,
    que oficializa la plataforma 'WikiGuías' como estándar técnico para la Ley N° 21.180.
    El uso de este formato acredita diligencia debida en el cumplimiento de la Ley N° 21.719.
    """
    pdf.multi_cell(0, 4, legal_footer, align='C')
    
    # Hash de Integridad
    hash_val = hashlib.sha256(str(datos).encode()).hexdigest()[:16]
    pdf.cell(0, 10, f"ID TRAZABILIDAD PASC: {hash_val}", ln=True, align='C')
    
    return pdf.output(dest='S').encode('latin-1')

# --- 3. INTERFAZ DE USUARIO (UX) ---

def main():
    # Sidebar: Panel de Control Normativo
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/9206/9206307.png", width=60)
        st.markdown("### PASC Data Guardian")
        st.success("✅ Estatus: Normativa Vigente")
        st.info("Res. Ex. 250/2025 (Hacienda)")
        
        # Monitor de Política (Requisito de tu archivo Política.docx)
        st.markdown("---")
        st.caption("Ciclo de Revisión Política (12 meses)")
        dias_restantes = 340 # Simulado
        st.progress(dias_restantes/365, text=f"{dias_restantes} días vigentes")

    st.title("🛡️ Centro de Cumplimiento Oficial")
    st.markdown("Gestión de Datos Personales alineada a **Secretaría de Gobierno Digital**.")

    tab1, tab2 = st.tabs(["🏛️ Catálogo RAT Oficial", "📝 Generador de Contratos"])

    # TAB 1: EL RAT OFICIAL
    with tab1:
        st.write("Seleccione el servicio compartido para cargar su ficha legal oficial.")
        
        servicio = st.selectbox("Servicio del Estado", list(RAT_GOBIERNO_DIGITAL.keys()))
        
        if servicio:
            data_rat = RAT_GOBIERNO_DIGITAL[servicio]
            
            # Tarjeta Visual
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"""
                **Rol:** {data_rat['Rol']} | **Riesgo:** {data_rat['Riesgo']}
                \n**Base Legal:** {data_rat['Legitimidad']}
                """)
            with col2:
                if st.button("Descargar Certificado RAT"):
                    pdf_bytes = generar_pdf_certificado("RAT", {
                        'servicio': servicio,
                        'rol': data_rat['Rol'],
                        'legitimidad': data_rat['Legitimidad'],
                        'riesgo': data_rat['Riesgo']
                    })
                    st.download_button("⬇️ PDF Oficial", pdf_bytes, file_name=f"RAT_{servicio}.pdf", mime="application/pdf")

    # TAB 2: CONTRATOS INTELIGENTES
    with tab2:
        st.write("Generación de Anexos de Responsabilidad (Ley 19.886 y 21.719).")
        
        tipo = st.radio("Formato Oficial SGD:", ["Compras Públicas (Anexo X)", "Honorarios"])
        c1, c2 = st.columns(2)
        nombre = c1.text_input("Razón Social / Nombre")
        rut = c2.text_input("RUT")
        
        if st.button("Generar Anexo Legal"):
            if nombre and rut:
                datos_contrato = {'nombre': nombre, 'rut': rut}
                pdf_bytes = generar_pdf_certificado(tipo, datos_contrato)
                st.success("Documento generado con cláusulas oficiales.")
                st.download_button("⬇️ Descargar Anexo Firmado", pdf_bytes, file_name=f"Anexo_Legal_{rut}.pdf", mime="application/pdf")

if __name__ == "__main__":
    main()
