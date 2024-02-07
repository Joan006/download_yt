from pytube import YouTube
import pandas as pd
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive 

#cremos las variables de excel
file_path = '/Users/mac/Desktop/Escritorio/py/app_downloader_yt/enlaces_videos/enlances_yt.xlsx'
sheet_name = 'Hoja1'
column_name = 'videos'

#vriables de drive
directorio_credenciales = 'credentials_module.json'
id_folder_drive = '18P18J_OXREsKxe0HaG8e2wbMGbgHCf1n'

#funcion de login
def login():
    GoogleAuth.DEFAULT_SETTINGS['client_config_file'] = directorio_credenciales
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile(directorio_credenciales)
    
    if gauth.credentials is None:
        gauth.LocalWebserverAuth(port_numbers=[8092])
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()
        
    gauth.SaveCredentialsFile(directorio_credenciales)
    credenciales = GoogleDrive(gauth)
    return credenciales

# SUBIR UN ARCHIVO A DRIVE
def subir_archivo(ruta_archivo,id_folder_drive):
    credenciales = login()
    archivo = credenciales.CreateFile({'parents': [{"kind": "drive#fileLink",\
                                                    "id": id_folder_drive}]})
    archivo['title'] = ruta_archivo.split("/")[-1]
    archivo.SetContentFile(ruta_archivo)
    archivo.Upload()

def main ():
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    column_data = df[column_name]
    videos = column_data.values


    for link_video in videos:
        yt = YouTube(link_video)
        video = yt.streams.get_highest_resolution()
        video.download('./yt')

    #subir
        subir_archivo(f'YT/{video.title}.mp4',id_folder_drive)

if __name__ == "__main__":
    main()
