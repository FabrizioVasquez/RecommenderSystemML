#!/bin/bash

# Detener el script si cualquier comando falla
set -e

echo "INICIO: Configurando entorno..."

# --- 1. Configuración de DVC (Solo si hay credenciales) ---
if [ -n "$AWS_ACCESS_KEY_ID" ]; then
    echo " Credenciales AWS detectadas. Configurando DVC..."
    
    # Configuramos DVC localmente para no ensuciar el repo global
    dvc remote modify --local s3-remote access_key_id "$AWS_ACCESS_KEY_ID"
    dvc remote modify --local s3-remote secret_access_key "$AWS_SECRET_ACCESS_KEY"
    dvc remote modify --local s3-remote region "$AWS_REGION"
    
    echo "Descargando datos y modelos desde S3..."
    dvc pull
    
    echo " Datos descargados correctamente."
else
    echo " ADVERTENCIA: No se detectaron credenciales AWS. Si los modelos no están en la imagen, la app fallará."
fi

# --- 2. Ejecutar el comando principal (Streamlit) ---
echo " Arrancando aplicación..."
# exec "$@" reemplaza este script con el proceso de Streamlit.
# Sin esto, Streamlit no recibiría las señales de apagado de Render.
exec "$@"