import streamlit as st
import pandas as pd
from io import BytesIO

st.title("Filtro ArchivoPlano Tiempo Libre")

# Subir archivo
archivo = st.file_uploader("Sube el archivo Excel", type=["xlsx"])

if archivo is not None:
    # Leer Excel
    df = pd.read_excel(archivo)

    # Convertir fechas (incluyendo la columna Fecha original)
    for col in ["Fecha de pago", "Fecha de factura", "Fecha"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    # Filtro por fecha "Desde" (columna Fecha)
    fecha_desde = None
    if "Fecha" in df.columns:
        fecha_min = df["Fecha"].min()
        fecha_max = df["Fecha"].max()

        fecha_desde = st.date_input(
            "Mostrar registros desde la fecha (columna Fecha):",
            value=None,  # por defecto no aplica filtro
            min_value=fecha_min,
            max_value=fecha_max
        )

    # Filtrar por Pago y ArchivoPlano
    df_filtrado = df[
        (df['Pago'] == True) &
        (df['ArchivoPlano'] == False)
    ]

    # Aplicar filtro de fecha si el usuario selecciona
    if fecha_desde:
        df_filtrado = df_filtrado[
            df_filtrado["Fecha"] >= pd.to_datetime(fecha_desde)
        ]

    # Crear nuevo DataFrame
    df_nuevo = pd.DataFrame()
    df_nuevo['CodigoEntidad'] = df_filtrado['Codigo entidad']
    df_nuevo['Cedula'] = df_filtrado['Identificación']
    df_nuevo['Concepto'] = df_filtrado['Concepto']
    df_nuevo['N° Factura'] = df_filtrado['No factura'].fillna("").astype(str)
    df_nuevo['Fecha'] = df_filtrado['Fecha'].dt.strftime("%d/%m/%Y")  # solo Fecha
    df_nuevo['Valor total'] = df_filtrado['Valor total']
    df_nuevo['Valor 0'] = 0
    df_nuevo['Centro de Costo'] = 17395
    df_nuevo['Abreviatura'] = "US"
    df_nuevo['Observacion'] = df_filtrado['Observacion']

    # Mostrar vista previa completa
    st.dataframe(df_nuevo)

    # Descargar archivo
    output = BytesIO()
    df_nuevo.to_excel(output, index=False, engine="openpyxl")
    output.seek(0)

    st.success("Archivo procesado con éxito.")
    st.download_button(
        label="Descargar archivo filtrado",
        data=output,
        file_name="archivo_nuevo.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
