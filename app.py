import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# Título
st.title("🔍 Buscador de Licitaciones - Mercado Público (API Oficial)")

# Inputs
st.write("Usando la API de pruebas de Mercado Público.")
keywords = st.text_input("Palabras clave (separadas por coma)", "servidores,switches,firewall")
fecha = st.date_input("Fecha a consultar", datetime.today())
estado = st.selectbox("Estado de la licitación", ["", "publicada", "cerrada", "desierta", "adjudicada", "revocada", "suspendida", "activas", "todos"])

# Ticket de pruebas (oficialmente publicado)
api_key = "F8537A18-6766-4DEF-9E59-426B4FEE2844"

# Acción
if st.button("Buscar"):
    resultados = []
    fecha_str = fecha.strftime("%d%m%Y")
    palabras = [k.strip() for k in keywords.split(",")]

    for palabra in palabras:
        with st.spinner(f"Buscando '{palabra}'..."):
            params = {
                "fecha": fecha_str,
                "ticket": api_key
            }
            if estado:
                params["estado"] = estado
            if palabra:
                params["nombre"] = palabra

            url = "https://api.mercadopublico.cl/servicios/v1/publico/licitaciones.json"
            response = requests.get(url, params=params)

            if response.status_code == 200:
                data = response.json()
                for lic in data.get("Listado", []):
                    resultados.append({
                        "Código": lic.get("CodigoExterno"),
                        "Nombre": lic.get("Nombre"),
                        "Estado": lic.get("Estado"),
                        "Fecha Publicación": lic.get("FechaPublicacion"),
                        "Fecha Cierre": lic.get("FechaCierre"),
                        "Comprador": lic.get("NombreOrganismo"),
                        "Link": lic.get("UrlLicitacion")
                    })
            else:
                st.error(f"Error: {response.status_code} - {response.text}")

    # Mostrar resultados
    if resultados:
        df = pd.DataFrame(resultados)
        st.success(f"Se encontraron {len(df)} resultados.")
        st.dataframe(df)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Descargar CSV", data=csv, file_name="licitaciones.csv", mime="text/csv")
    else:
        st.warning("No se encontraron resultados.")

