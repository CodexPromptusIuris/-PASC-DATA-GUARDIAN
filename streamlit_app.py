import streamlit as st

st.set_page_config(page_title="PASC Data Guardian", layout="centered")

st.title("PASC Data Guardian")
st.write("Aplicación convertida a Streamlit — personaliza esta interfaz según tu lógica de negocio.")

# Ejemplo de entrada y salida simple
user_input = st.text_input("Introduce texto de prueba", "")
if st.button("Procesar"):
    # Aquí puedes integrar la lógica existente de app.py si es necesario
    st.success(f"Has introducido: {user_input}")
