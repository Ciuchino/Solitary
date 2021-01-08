from socket import *

serverName = '192.168.1.195'
serverPort = 50000
nomeUtente = 'Utente1'
nomeAvversario = 'Utente2'
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

print('Server connesso!')
#   Prima fase di sorteggio
sorteggio = input('Ora decidiamo chi inizia :)\ntesta o croce? ')
ris_sorteggio = (clientSocket.recv(1024)).decode('utf-8')
if ris_sorteggio == 'True':  # Stampiamo chi inizia prima, se l'utente(utente = True) o il Pc, in base al risultato inviato dal server
    print('Bene, hai vinto il sorteggio!\nPuoi iniziare tu')
    Your_turn = True
else:
    print('Mi spiace, questa volta incomincia il tuo avversario, coglione.')
    Your_turn = False
while 1:
    print('|1A|1B|1C|\n|2A|2B|2C|\n|3A|3B|3C|\n')
    if Your_turn == False:
        Your_turn = True # La prossima mossa e` dell'utente
        while 1:
            via = clientSocket.recv(1024).decode('utf-8')
            if via == 'via':
                break
    else:
        Your_turn = False #La prossima mossa sara` del PC
        while 1:
            Scelta = input('Fai la tua scelta (guardando lo schema qui sopra): ')
            clientSocket.send(Scelta.encode('utf-8'))
            ris_scelta = (clientSocket.recv(1024)).decode('utf-8')
            if ris_scelta == 'Sbagliato':
                print('Scegli meglio, che cazzo! l\'input inserito non e` presente sullo schema')
            elif ris_scelta == 'Gia presente':
                print('Scegli meglio, che cazzo! l\'input inserito non e` presente sullo schema')
            elif ris_scelta == 'Corretto':
                break
    via = clientSocket.recv(1024).decode('utf-8')
    via = 'stop'
    # Ora stampiamo la board:
    board = (clientSocket.recv(1024)).decode('utf-8')
    print(board)
    print('------------------------')
    risultato = (clientSocket.recv(1024)).decode('utf-8')
    if risultato == nomeUtente:
        print('\nCongratulazioni! hai vinto! :)')
        break
    elif risultato == nomeAvversario:
        print('\nAh ah, ha vinto il tuo avversario, piccola testa di cazzo :)')
        break
if risultato == 'Nessuno':
    print('La partita e` finita in pareggio')
clientSocket.close()