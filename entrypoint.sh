#!/bin/bash

# Detener el script si hay errores
set -e

echo "🛠️ Configurando DVC..."

# Si estamos en un entorno que tiene las variables de entorno de AWS
if [ -n "$AWS_ACCESS_KEY_ID" ]; then
    # Configuramos las credenciales de DVC dinámicamente
    dvc remote modify --local s3-remote access_key_id "$AWS_ACCESS_KEY_ID"
    dvc remote modify --local s3-remote secret_access_key "$AWS_SECRET_ACCESS_KEY"
    dvc remote modify --local s3-remote region "$AWS_REGION"
    
    echo "📥 Descargando modelos y datos desde S3..."
    dvc pull
else
    echo "⚠️ No se detectaron credenciales AWS. Asumiendo que los datos ya existen o fallará."
fi

echo "🚀 Iniciando Streamlit..."
# Ejecutamos el comando que se pase al docker (o el default)
exec "$@"