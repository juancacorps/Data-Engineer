from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import os
CREDENCIALS = 'credentials_module.json'

# Iniciar Sesion
def login():
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile(CREDENCIALS)
    if gauth.access_token_expired:
        gauth.Refresh()
        gauth.SaveCredentialsFile(CREDENCIALS)
    else:
        gauth.Authorize()
    return GoogleDrive(gauth)
# Subir Documento
def upload_file(path, id_folder):
    credencials = login()
    archivo = credencials.CreateFile({'parents': [{"kind": "drive#fileLink",\
                                        "id": id_folder}]})
    archivo['title'] = path.split('/')[-1]
    archivo.SetContentFile(path)
    return archivo.Upload()


