# import requests
# from bs4 import BeautifulSoup

# url= "https://www.youtube.com/"
# query="results?search_query=lady+gaga"

# response = requests.get(url)
# html_content = response.text # Ottieni il contenuto della pagina
# soup = BeautifulSoup(html_content, 'html.parser')

# #print(soup.prettify())

# elements = soup.find_all('div', class_='ytd-video-renderer')

# print(elements)
# # Estrazione e stampa dei titoli
# for title in elements:
#     print(title.text.strip())
# #########################################
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# import time

# # Imposta il percorso del ChromeDriver
# driver_path = r'C:\Users\prora\Desktop\Music_library\server\chromedriver\chromedriver.exe'  # Modifica con il percorso corretto

# # Imposta il percorso del browser Brave
# brave_path = r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe'  # Modifica con il percorso corretto

# # Crea un oggetto Service
# service = Service(driver_path)

# # Imposta Chrome in modalità headless (opzionale)
# options = Options()
# options.add_argument('--headless')  # Rimuovi questa riga se vuoi vedere la finestra del browser
# options.binary_location = brave_path  # Imposta il percorso del browser Brave

# # Inizializza il driver con il servizio
# driver = webdriver.Chrome(service=service, options=options)

# # Vai a un URL
# driver.get("https://www.youtube.com/results?search_query=lady+gaga")

# # Attendi qualche secondo per far caricare la pagina
# time.sleep(5)

# # Esegui operazioni sul sito
# title = driver.title  # Titolo della pagina
# print(f"Titolo della pagina: {title}")

# # Chiudi il browser
# driver.quit()

from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Imposta il percorso di EdgeDriver
driver_path = r'C:\Users\prora\Desktop\Music_library\server\edgedriver\msedgedriver.exe'  # Modifica con il percorso corretto

# Crea un oggetto Service per Edge
service = Service(driver_path)

# Imposta Edge in modalità headless (opzionale)
options = Options()
#options.add_argument('--headless')  # Rimuovi questa riga se vuoi vedere la finestra del browser

# Inizializza il driver con il servizio
driver = webdriver.Edge(service=service, options=options)

# Vai a un URL
driver.get("https://www.youtube.com/results?search_query=lady+gaga")

# Attendi qualche secondo per far caricare la pagina
time.sleep(5)

# Esegui operazioni sul sito
title = driver.title  # Titolo della pagina
print(f"Titolo della pagina: {title}")

wait = WebDriverWait(driver, 20)
elements = driver.find_elements(By.CLASS_NAME, 'ytd-video-renderer')

for element in elements:
    try:
        # Titolo del video
        title = element.find_element(By.ID, 'video-title').text
        
        # Link del video
        video_url = element.find_element(By.ID, 'video-title').get_attribute('href')
        
        # Durata del video
        duration = element.find_element(By.CLASS_NAME, 'style-scope ytd-thumbnail-overlay-time-status-renderer').text
        
        # Numero di visualizzazioni
        views = element.find_element(By.CLASS_NAME, 'style-scope ytd-video-meta-block').text
        
        # Data di caricamento
        upload_date = element.find_element(By.CLASS_NAME, 'style-scope ytd-video-meta-block').text
        
        # Nome del canale
        channel_name = element.find_element(By.CLASS_NAME, 'style-scope ytd-channel-name').text
        
        # Thumbnail del video (URL dell'immagine)
        # thumbnail_url = element.find_element(By.CLASS_NAME, 'yt-core-image yt-core-image--fill-parent-height yt-core-image--fill-parent-width yt-core-image--content-mode-scale-aspect-fill yt-core-image--loaded').get_attribute('src')
        # thumbnail_url = element.find_element(By.TAG_NAME, 'img').get_attribute('src')

        # Stampa tutte le informazioni estratte
        print(f"Title: {title}")
        print(f"Video URL: {video_url}")
        print(f"Duration: {duration}")
        print(f"Views: {views}")
        print(f"Upload Date: {upload_date}")
        print(f"Channel Name: {channel_name}")
        print(f"Thumbnail URL: {thumbnail_url}")
        print("="*50)
        
    except Exception as e:
        pass
        # print(f"An error occurred: {e}")


# Chiudi il browser
driver.quit()