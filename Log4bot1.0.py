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
print('        \033[35;7mMENU DE ROTINAS\033[m')
print('''[1] - Inicio \033[31mPré-Pago\033[m
[2] - Inicio \033[31mCombo Pré\033[m
[3] - Inicio \033[31mFlex\033[m
[4] - Inicio \033[34mTIM\033[m
[5] - PréPostar \033[34mTIM\033[m ''')

menu_Inicial = input('Escolha uma opção: ')
if menu_Inicial in '123':
    link = 'https://vertexdigital.bitrix24.com.br/crm/deal/category/0/'
elif menu_Inicial in '45':
    link = 'https://vertextim.bitrix24.com.br/crm/deal/category/0/'
xpath_Filtro = ''
if menu_Inicial == '1':
    xpath_Filtro = "(//span[@class='main-ui-filter-sidebar-item-text'])[3]"
elif menu_Inicial == '2':
    xpath_Filtro = "(//span[@class='main-ui-filter-sidebar-item-text'])[4]"
elif menu_Inicial == '3':
    xpath_Filtro = "(//span[@class='main-ui-filter-sidebar-item-text'])[5]"
elif menu_Inicial == '4':
    xpath_Filtro = "(//span[@class='main-ui-filter-sidebar-item-text'])[3]"
elif menu_Inicial == '5':
    xpath_Filtro = "(//span[@class='main-ui-filter-sidebar-item-text'])[4]"
else:
    print('ESCOLHA INVALIDA')
    sys.exit()

# Variaveis de login
email = ''
senha = ''



print(f'Fazendo Login como \033[4;32m{email}\033[m')

# Gerando data atual
print('ESCOLHA A \033[34mDATA\033[m DESEJADA. | DIGITE \033[4;34m0\033[m PARA DATA ATUAL')
escolhadata = input('DIGITE A DATA: ')
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
browser.get(f'{link}')

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

# Fazendo FILTRO 
element = WebDriverWait(browser, 30).until(EC.presence_of_element_located(
    (By.XPATH, f'{xpath_Filtro}'))).click()
sleep(5) # To usando esse sleep aqui pois ele não espera carregar para pegar a variavel TOT pois ela aparece na tela anterior também.
# Verificador de Mostrar Mais
tot = WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, "(//span[@class='main-grid-counter-displayed'])[1]")))
total = tot.text
sleep(1)
if total == '100':
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


if menu_Inicial in '1234':
    # PEDIR PARA COLOCAR OS ICCID
    while True:
        print(f'COLOQUE {casos} ICCID NA DATABASE')
        print('COLOU OS ICCID E SALVOU?')
        resposta = input('DIGITE S/X: ').upper()
        if resposta == 'S':
            print('Obrigado, colando ICCIDS!')
            break
        elif resposta == 'X':
            print('FECHANDO O PROGRAMA')
            sys.exit()
        else:
            print('Não colocou? Tente novamente!')
            

    # Ler tabelas de ICCIDS
    db = pd.read_excel('database.xlsx')

    # Preenchendo DATA e ICCID
    for c in range(1, casos+1):
        iccids = db.loc[c-1, 'ICCID']
        element = WebDriverWait(browser, 30).until(EC.presence_of_element_located(
        (By.XPATH, f"(//input[@id='UF_CRM_1549387846_control'])[{c}]"))).send_keys(iccids)
        element = WebDriverWait(browser, 30).until(EC.presence_of_element_located(
        (By.XPATH, f"(//input[@name='UF_CRM_1543599852'])[{c}]"))).send_keys(data)
    print('ICCIDS COLADOS!')


# PEDIR PARA INSERIR CODIGOS DE RASTREIO
while True:
    print(f'COLOQUE {casos} CODIGOS NA DATABASE')
    print('Podemos colar o Cod. de Rastreio?')
    respostacod = input('Digite S/X: ').upper()
    if respostacod == 'S':
        print('Colocando codigos de rastreamento.')
        break
    elif respostacod == 'X':
        sys.exit()
    else:
        print('Okay, quando puder!')

# Ler tabela com codigos
db = pd.read_excel('database.xlsx')

# Preenchendo cod de rastreio e substatus

if menu_Inicial in '45': # Escolhe xpath para cada bitrix
    xpath_CodRastreio = "(//input[@id='UF_CRM_1543950066_control'])"
else:
    xpath_CodRastreio = "(//input[@id='UF_CRM_1543591399_control'])"

for cc in range(1, casos+1):
    codigos = db.loc[cc-1, 'RASTREIO']
    element = WebDriverWait(browser, 30).until(EC.presence_of_element_located(
    (By.XPATH, f"{xpath_CodRastreio}[{cc}]"))).send_keys(codigos)
    # Seleciona Substatus CASO for prepago, combo ou flex
    if menu_Inicial == '1' or menu_Inicial == '2' or menu_Inicial == '3':
        element = WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, f"(//div[@id='UF_CRM_1542637220_control'])[{cc}]"))).click()
        element = WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, "(//span[@class='main-dropdown-item'])[4]"))).click()

# Rolar para o topo da tela
sleep(1)
browser.execute_script("window.scrollTo(0, -document.body.scrollHeight);")

print('ACABOU!')


# xpath tim
# (//input[@id='UF_CRM_1543950066_control'])[{cc}]