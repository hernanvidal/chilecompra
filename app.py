import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta

# Título
st.title("Buscador de Licitaciones - Mercado Público")

# Inputs del usuario
api_key = st.text_input("🔑 API Key de Mercado Público", type="password")
keywords = st.text_input("🔍 Palabras clave (separadas por coma)", "servidores,switches,firewall")
fecha_desde = st.date_input("📅 Fecha desde", datetime.today() - timedelta(days=30))
fecha_hasta = st.date_input("📅 Fecha hasta", datetime.today())

# Botón de búsqueda
if st.button("Buscar Licitaciones"):
    palabras = [k.strip() for k in keywords.split(",")]
    resultados = []

    for palabra in palabras:
        with st.spinner(f"Buscando licitaciones para '{palabra}'..."):
            params = {
                "nombre": palabra,
                "fecha": fecha_desde.strftime("%d-%m-%Y"),
                "fechaHasta": fecha_hasta.strftime("%d-%m-%Y"),
                "ticket": api_key
            }
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
                st.error(f"❌ Error al consultar '{palabra}': Código {response.status_code}")

    # Mostrar resultados
    if resultados:
        df = pd.DataFrame(resultados)
        st.success(f"✅ Se encontraron {len(df)} resultados.")
        st.dataframe(df)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Descargar CSV", data=csv, file_name="licitaciones.csv", mime="text/csv")
    else:
        st.warning("⚠️ No se encontraron licitaciones con esos criterios.")
