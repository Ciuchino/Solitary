#                                    ++++++++++++++++++++++++++++++ GIOCO DEL TRIS VERSIONE vs PC ONLINE +++++++++++++++++++++++++++++++

from socket import *
from time import sleep
from threading import Thread

# funzione per convertire il dizionario in una lista per facilitare la stampa
def conversione(board):
    lista_convertita = []# Lista che contiene [indice usato per stampare, informazione su chi ha fatto la mossa(utente o pc?)
    lista_conversione = [[1, 1], [2, 3], [3, 5], [5, 9], [7, 11], [11, 13], [13, 17], [17, 19], [19, 21]] #lista che contiene[ chiave del dizionario, indice usato per stampare]
    for x in board.keys():
        for y in lista_conversione:
            if y[0] == x:
                lista_convertita.append([y[1], board[x]])
                break
    return lista_convertita

#   funzione per stampare la board. crea una lista con la struttura del gioco, gli indici dei caratteri vuoti sono salvati su una lista usata per la conversione, cosi mi basat dire che in quell'indiece devvo mettere x o o e poi stampo tutto
def print_gameboard(game_b, connectionS):
    lista_cov = conversione(game_b)
    visual_board = ['\n      |', ' ', '|', ' ', '|', ' ', '|', '\n','      |', ' ', '|', ' ', '|', ' ', '|', '\n', '      |', ' ', '|', ' ', '|', ' ', '|' ]
    for x in lista_cov:
        if x[1] == 'utente1':
            visual_board[x[0]] = 'x'
        else: visual_board[x[0]] = 'o'
    complete_board = ''.join(visual_board)
    connectionS.send(complete_board.encode('utf-8'))
    print(''.join(visual_board))
    print('---------------------')


# Sorteggio iniziale per decidere chi inizia, restituisce:
#--True se inizia l'utente
#--False se inizia il pc
import random
def sorteggio_inizio():
    if utente_che_inizia == 1:
        return True
    else: return False



# Questa funzione prende in input la scelta dell'utente, controlla sia corretta, la converte in un numro usato per le chiavi e aggiorna il dizionario con gli  elementi
def mossa_utente(board, utente, connectionS):
    trovato = False #Serve semplicemente per essere sicuri l'utente inserisca l'input giusto
    while (trovato == False):
        print('Fai la tua scelta (guardando lo schema qui sopra): ')
        Scelta = (connectionS.recv(1024)).decode('utf-8')
        Lista_conversione = [['1A', 1], ['1B', 2], ['1C', 3], ['2A', 5], ['2B', 7], ['2C', 11], ['3A', 13], ['3B', 17], ['3C', 19]]# lista per convertire l'inpute dell'utente nella giusta chiave, per semplificare il calcolo del risultato al pc
        for x in Lista_conversione:
            if Scelta == x[0]:
                Scelta = x[1]
                trovato = True
        while Scelta in board.keys(): #controllo l'input inserito non sia gia` presente
            trovato = False
            connectionS.send('Gia presente'.encode('utf-8'))
            print('Scegli meglio, che cazzo! l\'input inserito e` gia` stato scelto prima!')
            Scelta = (connectionS.recv(1024)).decode('utf-8')
            Lista_conversione = [['1A', 1], ['1B', 2], ['1C', 3], ['2A', 5], ['2B', 7], ['2C', 11], ['3A', 13], ['3B', 17], ['3C', 19]]
            for x in Lista_conversione:
                if Scelta == x[0]:
                    Scelta = x[1]
                    trovato = True
        if trovato == False:
            connectionS.send('Sbagliato'.encode('utf-8'))
            print('Scegli meglio, che cazzo! l\'input inserito non e` presente sullo schema')
    connectionS.send('Corretto'.encode('utf-8'))
    board[Scelta] = utente


#   Questa funzione riceve in ingresso il dizionario con gli elemnti inseriti e le rispettivi chiavi e la lista cn il pordotto di chiavi vincenti.
#   Restituisce:
#       --True se ha vinto qualcuno, stampandoil relativo messaggio
#       --False se non ha vinto nessuno, e la partita puo` continuare o, eventualmente, finire in pareggio
def risultato(board, ris_vinc, connectionS):
    if len(board.keys()) < 3:#se ci sono meno di tre elementi e` impossibile qualcuno abbia vinto, esco dalla funzione
        return False
    ris_utente1 = []
    ris_utente2 = []
    for x in board.items(): #salvo su due liste diversi gli le chiavi degli elemnti messi dall'utente e le chiavi degli elemnti messi dal pc
        if x[1] == 'utente1':
            ris_utente1.append(x[0])
        elif x[1] == 'utente2':
            ris_utente2.append(x[0])
    for x in ris_utente1[:-2]:# Moltiplico tuttle le chiavi degli elemnti dell'utente a tre a tre tra diloro e, se un dei prodotti ottenuti e` presente nella lista con i prodotti vincenti, allora l'utente ha vinto
        for y in ris_utente1[ris_utente1.index(x)+1:-1]:
            for z in ris_utente1[ris_utente1.index(y)+1:]:
                ris = x * y * z
                if ris in ris_vinc:
                    connectionS.send('Utente1'.encode('utf-8'))
                    print('\nCongratulazioni! hai vinto! :)')
                    return True
    for x in ris_utente2[:-2]:# faccio la stessa cosa di prima ma questa volta con le chiavi degli elemnti del pc
        for y in ris_utente2[ris_utente2.index(x)+1:-1]:
            for z in ris_utente2[ris_utente2.index(y)+1:]:
                ris = x * y * z
                if ris in ris_vinc:
                    connectionS.send('Utente2'.encode('utf-8'))
                    print('\nAh ah, ho vinto io, piccola testa di cazzo :)')
                    return True
    #print(ris_utente)
    #print(ris_pc)
    return False #se nessuno ha vinto restituisco false

def handler(connectionSocket):
    while 1:
        game_board = {}
        ris_vincenti = [6, 385, 4199, 65, 238, 627, 133, 273]
        vinto = False
        if sorteggio_inizio() == True:# Decidiamo se inizia priam l'utente(utente = True) o il Pc
            connectionSocket.send('True'.encode('utf-8'))
            utente1 = True
            print('Sorteggio vinto dall\'utente 1')
        else:
            connectionSocket.send('False'.encode('utf-8'))
            utente1 = False
            print('Sorteggio vinto dall\'utente 2')
        print('|1A|1B|1C|\n|2A|2B|2C|\n|3A|3B|3C|\n')
        while len(game_board.keys()) < 9: #la piattaforma ha 9 caselle, se vengono riempite tutte esce dal ciclo while
            if (utente1 == True):
                mossa_utente(game_board, 'utente1', connectionSocket) #funzione che implemeta la mossa dell'utente
                utente1 = False
            else:
                mossa_utente(game_board, 'utente2', connectionSocket) #funzione che implementa la mossa del pc
                utente1 = True
            sleep(5)
            connectionSocket.send('via'.encode('utf-8'))
            print_gameboard(game_board, connectionSocket)
            sleep(2)
            if risultato(game_board, ris_vincenti, connectionSocket) == True:#Se qualcuni tra l'utente e il pc ha vinto
                vinto = True
                break #esco dal ciclo perche il gioco e` finito
            else:
                connectionSocket.send('Nessuno'.encode('utf-8'))
        if vinto == False:
            if risultato(game_board, ris_vincenti) == False:
                print('La partita e` finita in pareggio')
        break
    connectionSocket.close()

#Prima configuro il server.....
serverPort = 50000
serverName = '192.168.1.18'
welcomeSocket = socket(AF_INET, SOCK_STREAM)
welcomeSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
welcomeSocket.bind((serverName, serverPort))
welcomeSocket.listen(1)

while 1:
    print('Server pronto!')
    print('Ora decidiamo chi inizia :)\ntesta o croce? ')
    utente_che_inizia = random.randint(1,2)
    newSocket, clientAddress = welcomeSocket.accept()
    print('In comunicazione con: ', clientAddress)
    thread = Thread(target=handler, args=(newSocket,))
    thread.start()