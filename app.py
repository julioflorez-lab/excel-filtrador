import streamlit as st
import pandas as pd
from io import BytesIO

st.title("Filtro de Excel Pago=VERDADERO y ArchivoPlano=FALSO")

# Subir archivo
archivo = st.file_uploader("Sube el archivo Excel", type=["xlsx"])

if archivo is not None:
    # Leer Excel
    df = pd.read_excel(archivo)

    # Filtrar
    df_filtrado = df[
        (df['Pago'] == True) &
        (df['ArchivoPlano'] == False)
    ]

    # Crear nuevo DataFrame
    df_nuevo = pd.DataFrame()
    df_nuevo['CodigoEntidad'] = df_filtrado['Codigo entidad']
    df_nuevo['Cedula'] = df_filtrado['Identificación']
    df_nuevo['Concepto'] = df_filtrado['Concepto']
    df_nuevo['N° Factura'] = df_filtrado['No factura']
    df_nuevo['Fecha de pago'] = df_filtrado['Fecha de pago']
    df_nuevo['Fecha de factura'] = df_filtrado['Fecha de factura']
    df_nuevo['Valor total'] = df_filtrado['Valor total']
    df_nuevo['Valor 0'] = 0
    df_nuevo['Centro de Costo'] = 17395
    df_nuevo['Abreviatura'] = "US"
    df_nuevo['Observacion'] = df_filtrado['Observacion']

    # Descargar archivo
    output = BytesIO()
    df_nuevo.to_excel(output, index=False)
    output.seek(0)

    st.success("Archivo procesado con éxito.")
    st.download_button(
        label="Descargar archivo filtrado",
        data=output,
        file_name="archivo_nuevo.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    )
