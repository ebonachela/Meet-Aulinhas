import pickle, time, os, json, datetime, ctypes
from infi.systray import SysTrayIcon
from selenium import webdriver

# Quantidade minima de pessoas para sair da sala
minQtdPessoas = 20

def abrir_aula(link):
    driver = webdriver.Firefox()
    driver.get(link)

    cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)

    time.sleep(2) 
    driver.refresh()

    time.sleep(2)

    driver.find_element_by_css_selector('.dP0OSd > div:nth-child(1) > div:nth-child(1)').click()
    driver.find_element_by_css_selector('.HNeRed').click()

    time.sleep(2)

    driver.find_element_by_css_selector('#yDmH0d > c-wiz > div > div > div:nth-child(9) > div.crqnQb > div > div > div.vgJExf > div > div > div.d7iDfe.NONs6c > div > div.Sla0Yd > div > div.XCoPyb > div.uArJ5e.UQuaGc.Y5sE8d.uyXBBb.xKiqt').click()

    time.sleep(2)
    
    deveVerificar = False

    while True:
        qtdPessoas = int(driver.find_element_by_css_selector('.uGOf1d').text)
        
        if qtdPessoas > minQtdPessoas:
            deveVerificar = True

        if qtdPessoas <= minQtdPessoas and deveVerificar:
            driver.find_element_by_css_selector('.jh0Tpd').click()
            win32gui.ShowWindow(hide, win32con.SW_SHOW)
            break
            
        time.sleep(2)
        
    driver.close()

os.system('cls')
print('-------- Gerenciador de Aulas --------\n')

if not os.path.isfile('cookies.pkl'):
    print('Você precisa se logar em sua conta USP para continuar. Clique em login e insira suas informações na aba que se abrirá em instantes.')
    
    driver = webdriver.Firefox()
    driver.get('https://meet.google.com/')
    
    input("Aperte 'Enter' quando finalizar... (não feche manualmente a aba nova que se abriu)")
    
    pickle.dump(driver.get_cookies() , open("cookies.pkl", "wb")) 
    
    if os.path.isfile('cookies.pkl'):
        print('\nInformações de login salvas com sucesso! O programa iniciará em 5 segundos...\n')
        driver.close()
        time.sleep(5)
    else:
        print('\nErro ao salvar informações de login. Tente novamente!')
        driver.close()
        os._exit(0)

#hide = win32gui.GetForegroundWindow()

hover_text = "Gerenciador de Aulas"

def mostrar(sysTrayIcon):
    #win32gui.ShowWindow(hide, win32con.SW_SHOW)
    ctypes.windll.user32.ShowWindow( ctypes.windll.kernel32.GetConsoleWindow(), 1 )

def esconder(sysTrayIcon):
    #win32gui.ShowWindow(hide, win32con.SW_HIDE)
    ctypes.windll.user32.ShowWindow( ctypes.windll.kernel32.GetConsoleWindow(), 0 )
    
def sair(sysTrayIcon):
    os._exit(0)
  
menu_options = (
                ('Mostrar', None, mostrar),
                ('Esconder', None, esconder),
               )

sysTrayIcon = SysTrayIcon(None, hover_text, menu_options, on_quit=sair)
sysTrayIcon.start()

print('Utilize o icone no systray para esconder ou mostrar o console.\n')

aulas = json.load(open('aulas.json'))
diasDaSemana = ['segunda', 'terça', 'quarta', 'quinta', 'sexta', 'sabado', 'domingo']

if len(aulas[diasDaSemana[datetime.datetime.today().weekday()]]) == 0:
    print('Não temos aula hoje ;)')
    os._exit(0)

print('Aulas de hoje:')

index = 1

for aula in aulas[diasDaSemana[datetime.datetime.today().weekday()]]:
    print(index, aula[0], aula[1])
    index += 1

print('\nAguardando aulas...\n')

while True:
    diaDaSemana = diasDaSemana[datetime.datetime.today().weekday()]
    hora = datetime.datetime.now().strftime("%H:%M")
    
    for aula in aulas[diaDaSemana]:
        if aula[1] == hora:
            print(aula[0], 'começando...')
            abrir_aula(aula[2])
            aulas[diaDaSemana].remove(aula)

    time.sleep(2)