import gspread
from oauth2client.service_account import ServiceAccountCredentials
from common.constants import GOOGLE_DRIVE_SCOPE, GOOGLE_SPREADSHEET_SCOPE, GOOGLE_JSON_CREDENTIALS, DOWNLOAD_PATH
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os

def get_gspread_client():
    scope = [GOOGLE_DRIVE_SCOPE, GOOGLE_SPREADSHEET_SCOPE]
    creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_JSON_CREDENTIALS, scope) # load json credentials
    client = gspread.authorize(creds) # authenticate Google Drive and Sheets client
    
    return client

def get_drive_service():
    """Autentica y devuelve un servicio para Google Drive."""
    scope = [GOOGLE_DRIVE_SCOPE]
    creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_JSON_CREDENTIALS, scope)  # Cargar credenciales
    drive_service = build('drive', 'v3', credentials=creds)  # Autenticar el cliente de Google Drive
    return drive_service

def upload_pdf_to_drive(file_path, folder_id):
    """Sube un archivo PDF a Google Drive."""
    drive_service = get_drive_service()
    file_metadata = {
        'name': os.path.basename(file_path),  # Nombre del archivo que se subirá
        'parents': [folder_id]  # ID de la carpeta en Google Drive
    }

    # Preparar el archivo para la subida
    media = MediaFileUpload(file_path, mimetype='application/pdf')

    # Subir el archivo a Google Drive
    file = drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()

    print(f'Archivo subido con ID: {file.get("id")}')