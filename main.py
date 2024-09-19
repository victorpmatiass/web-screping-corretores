import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# Função para extrair os dados da página
def extract_data():
    rows = driver.find_elements(By.CSS_SELECTOR, "tbody tr")
    for row in rows:
        cols = row.find_elements(By.CSS_SELECTOR, "td")
        if cols and cols[2].text.strip()=="ATIVO":  # Verificar se há colunas na linha
            entry = {
                'Inscrição': cols[0].text.strip(),
                'Identificação': cols[1].text.strip(),
                'Situação': cols[2].text.strip(),
                'Contato': cols[4].text.strip(),
            }
            data.append(entry)

# Configura as opções do Chrome e inicia o ChromeDriver
chrome_options = Options()
chrome_options.add_experimental_option("prefs", {"safebrowsing.enabled": True})
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Navega até a página
url = 'https://www.crecice.conselho.net.br/form_pesquisa_cadastro_geral_site.php'
driver.get(url)

# Interagindo com o campo de busca
search_box_xpath = '//*[@id="input-24"]'
search_box = driver.find_element(By.XPATH, search_box_xpath)
search_box.click()
search_box.send_keys('Fortaleza')

# Clicar para seguir
continue_box_xpath = '//*[@id="app"]/div/main/div/div/div/div[3]/form/div[3]/button/span'
continue_box = driver.find_element(By.XPATH, continue_box_xpath)
driver.execute_script("arguments[0].scrollIntoView(true);", continue_box)
time.sleep(1)
continue_box.click()

# Esperar a página carregar
time.sleep(10)  

# Lista para armazenar os dados
data = []

# Executar o loop para extrair e navegar pelas páginas
for _ in range(923):  
    extract_data()
    next_button_xpath = '//*[@id="app"]/div[3]/div/div/div[2]/div[2]/div[4]/button/span/i'
    next_button = driver.find_element(By.XPATH, next_button_xpath)
    next_button.click()
    time.sleep(2)  # Menos que 2 não da tempo

# Fechar o driver
driver.quit()

# Criar DataFrame com os dados coletados
df = pd.DataFrame(data)
df = df.dropna(subset=["Contato"]).reset_index(drop=True)
df.to_csv('dados_crecice.csv', index=False)

# Log de sucesso 
print("Dados coletados e salvos com sucesso.")