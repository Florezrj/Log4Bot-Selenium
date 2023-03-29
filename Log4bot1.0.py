# importando bibliotecas variaveis
from time import sleep
from datetime import date


from selenium import webdriver  # Importa do selenium o webdriver
from webdriver_manager.chrome import ChromeDriverManager # Importa a biblioteca q vai baixar o ChromeDriver
from selenium.webdriver.chrome.service import Service # Importa o serviço do chrome
from selenium.webdriver.chrome.options import Options # Importando options
from selenium.webdriver.common.by import By # Importa o By para selecionar o XPATHm por qual chave vai buscar o elemento
# Importa a função de esperar carregar do selenium
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# Importa a função de exessão para o try
from selenium.common.exceptions import TimeoutException
# Importa funções do sistema
import sys
# Importa o pandas, nosso manipulador de tabelas
import pandas as pd


# Variaveis de filtro.
print('ESCOLHA O FILTRO QUE SERÁ FEITO')
print('''[1] - Inicio Pré-Pago
[2] - Inicio Controle
[3] - Inicio Combo Pré
[4] - Inicio Flex ''')

escolhafiltro = input('Escolha uma opção: ')
filtro = ''
if escolhafiltro == '1':
    filtro = '//*[@id="popup-window-content-CRM_DEAL_LIST_V12_C_0_search_container"]/div/div/div[1]/div[2]/div[3]/span[2]/span[1]'
elif escolhafiltro == '2':
    filtro = '//*[@id="popup-window-content-CRM_DEAL_LIST_V12_C_0_search_container"]/div/div/div[1]/div[2]/div[5]/span[2]/span[1]'
elif escolhafiltro == '3':
    filtro = '//*[@id="popup-window-content-CRM_DEAL_LIST_V12_C_0_search_container"]/div/div/div[1]/div[2]/div[4]/span[2]/span[1]'
elif escolhafiltro == '4':
    filtro = '//*[@id="popup-window-content-CRM_DEAL_LIST_V12_C_0_search_container"]/div/div/div[1]/div[2]/div[6]/span[2]/span[1]'
else:
    print('ESCOLHA INVALIDA')
    sys.exit()

# Variaveis de login
email = 'bernardowelsing90@gmail.com'
senha = 'Esqueci123W'

print(f'Logando como [{email}]')

# Gerando data atual
print('ESCOLHA A DATA DESEJADA.')
escolhadata = input('Digite 0 para data de hoje ou digite a data desejada: ')
if escolhadata == '0':
    data = ''
    dia = date.today().day
    mes = date.today().month
    ano = date.today().year
    if mes < 10:
        data = f"{dia}/0{mes}/{ano}"
    elif mes > 10:
        data = f"{dia}/{mes}/{ano}"
else:
    data = escolhadata  

print('Trataremos os envios para {}'.format(data))

# Importando opções de não fechar navegador
# Criando a variavel noquit pra não fechar navegador
noquit = Options()
noquit.add_experimental_option('detach', True)

# Instalando e abrindo navegador
installChrome = Service(ChromeDriverManager().install())  # Serviço de instalação
browser = webdriver.Chrome(service=installChrome, options=noquit)  # Abrir navegador
browser.maximize_window()

# Iniciando a automação
# Abrindo bitrix
browser.get('https://vertexdigital.bitrix24.com.br/crm/deal/category/0/')

# Preenchendo email
element = WebDriverWait(browser, 30).until(EC.presence_of_element_located(
    (By.XPATH, '//*[@id="login"]'))).send_keys(email)
sleep(1)

# Clicando no botão pra avançar
browser.find_element(
    By.XPATH, '//*[@id="authorize-layout"]/div/div[3]/div/form/div/div[5]/button[1]').click()
sleep(1)

# Preenchendo senha

element = WebDriverWait(browser, 30).until(EC.presence_of_element_located(
    (By.XPATH, '//*[@id="password"]'))).send_keys(senha)
sleep(1)

# Clicando no botão de logar
element = WebDriverWait(browser, 30).until(EC.presence_of_element_located(
    (By.XPATH, '//*[@id="authorize-layout"]/div/div[3]/div/form/div/div[3]/button[1]'))).click()
sleep(1)


# Clicando para filtrar
element = WebDriverWait(browser, 30).until(EC.presence_of_element_located(
    (By.XPATH, '//*[@id="CRM_DEAL_LIST_V12_C_0_search"]'))).click()
sleep(1)

# Fazendo filtro INICIO PRE
element = WebDriverWait(browser, 30).until(EC.presence_of_element_located(
    (By.XPATH, f'{filtro}'))).click()
sleep(5)


# Verificador de Mostrar Mais
tot = WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, "(//span[@class='main-grid-counter-displayed'])[1]")))
total = tot.text
if total == 100:
    try:
        more = WebDriverWait(browser, 10).until(EC.visibility_of_element_located(
            (By.XPATH, "(//span[@class='main-grid-more-text'])")))
        tem = more.text

        if more.text == 'Mostrar mais':
            print('Devemos {}'.format(tem))
            browser.find_element(By.XPATH, '//*[@id="CRM_DEAL_LIST_V12_C_0_nav_more"]/a/span[1]').click()
        
    except TimeoutException:
        print('Não precisamos Mostrar Mais')
else:
    print('Não precisamos Mostrar Mais.')



# Rolar para o topo da tela
browser.execute_script("window.scrollTo(0, -document.body.scrollHeight);")
sleep(2)

# Selecionando tudo 
element = WebDriverWait(browser, 30).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="CRM_DEAL_LIST_V12_C_0_check_all"]'))).click()
sleep(1)


# Pegando quantidade de clientes TOTAL
casospegar = WebDriverWait(browser, 30).until(EC.presence_of_element_located(
    (By.XPATH, "(//span[@class='main-grid-counter-selected'])[1]")))
casos = casospegar.text
casos = int(casos)
print('Temos {} Clientes para tratar.'.format(casos))
sleep(1)

# Clicando em editar
element = WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="grid_edit_button_control"]'))).click()
sleep(1)

# Rolar para o topo da tela
browser.execute_script("window.scrollTo(0, -document.body.scrollHeight);")

# PEDIR PARA COLOCAR OS ICCID
while True:
    print(f'COLOQUE {casos} ICCIDs NO BANCO DE DADOS')
    print('COLOU OS ICCID E SALVOU?')
    resposta = input('DIGITE S/N: ').upper()
    if resposta == 'S':
        print('Obrigado, colando ICCIDS!')
        break
    elif resposta == 'N':
        print('Não colocou? Tente novamente!')
    else:
        print('RESPOSTA INVALIDA, FECHANDO PROGRAMA')
        sys.exit()


# Ler tabelas de ICCIDS
tabela = pd.read_excel('C:\\Userszberna\\Documents\\dbiccid.xlsx')

# Preenchendo DATA e ICCID
for c in range(1, casos+1):
    iccids = tabela.loc[c-1, 'ICCID']
    element = WebDriverWait(browser, 30).until(EC.presence_of_element_located(
    (By.XPATH, f"(//input[@id='UF_CRM_1549387846_control'])[{c}]"))).send_keys(iccids)
    element = WebDriverWait(browser, 30).until(EC.presence_of_element_located(
    (By.XPATH, f"(//input[@name='UF_CRM_1543599852'])[{c}]"))).send_keys(data)


print('ACABOU!')


