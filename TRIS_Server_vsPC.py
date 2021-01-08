#                                    ++++++++++++++++++++++++++++++ GIOCO DEL TRIS VERSIONE vs PC ONLINE +++++++++++++++++++++++++++++++

from socket import *
from time import sleep
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
def print_gameboard(game_b):
    lista_cov = conversione(game_b)
    visual_board = ['\n      |', ' ', '|', ' ', '|', ' ', '|', '\n','      |', ' ', '|', ' ', '|', ' ', '|', '\n', '      |', ' ', '|', ' ', '|', ' ', '|' ]
    for x in lista_cov:
        if x[1] == 'utente':
            visual_board[x[0]] = 'x'
        else: visual_board[x[0]] = 'o'
    complete_board = ''.join(visual_board)
    connectionSocket.send(complete_board.encode('utf-8'))
    print(''.join(visual_board))
    print('---------------------')


# Sorteggio iniziale per decidere chi inizia, restituisce:
#--True se inizia l'utente
#--False se inizia il pc
import random
def sorteggio_inizio():
    print('Ora decidiamo chi inizia :)\ntesta o croce? ')
    sorteggio = (connectionSocket.recv(1024)).decode('utf-8')
    if sorteggio == 'testa':
        sorteggio = 0
    else: sorteggio = 1
    if sorteggio == random.randint(0,1):
        return True  # Il sorteggio e` stato vinto dall'utente
    else: return False # Il sorteggio e` stato vinto dal pc

def mossa_pc(board):
    chiave = random.choice([1,2, 3, 5, 7, 11, 13, 17, 19])
    while (chiave in board.keys()): # se la chiave scelta casualmente e` gia presente nel dizionario continuo a generare una nuova chiave finche` non becco una che non sta nel dizionario
        chiave = random.choice([1,2, 3, 5, 7, 11, 13, 17, 19])
    board[chiave] = 'pc'


# Questa funzione prende in input la scelta dell'utente, controlla sia corretta, la converte in un numro usato per le chiavi e aggiorna il dizionario con gli  elementi
def mossa_utente(board):
    trovato = False #Serve semplicemente per essere sicuri l'utente inserisca l'input giusto
    while (trovato == False):
        print('Fai la tua scelta (guardando lo schema qui sopra): ')
        Scelta = (connectionSocket.recv(1024)).decode('utf-8')
        Lista_conversione = [['1A', 1], ['1B', 2], ['1C', 3], ['2A', 5], ['2B', 7], ['2C', 11], ['3A', 13], ['3B', 17], ['3C', 19]]# lista per convertire l'inpute dell'utente nella giusta chiave, per semplificare il calcolo del risultato al pc
        for x in Lista_conversione:
            if Scelta == x[0]:
                Scelta = x[1]
                trovato = True
        while Scelta in board.keys(): #controllo l'input inserito non sia gia` presente
            trovato = False
            connectionSocket.send('Gia presente'.encode('utf-8'))
            print('Scegli meglio, che cazzo! l\'input inserito e` gia` stato scelto prima!')
            Scelta = (connectionSocket.recv(1024)).decode('utf-8')
            Lista_conversione = [['1A', 1], ['1B', 2], ['1C', 3], ['2A', 5], ['2B', 7], ['2C', 11], ['3A', 13], ['3B', 17], ['3C', 19]]
            for x in Lista_conversione:
                if Scelta == x[0]:
                    Scelta = x[1]
                    trovato = True
        if trovato == False:
            connectionSocket.send('Sbagliato'.encode('utf-8'))
            print('Scegli meglio, che cazzo! l\'input inserito non e` presente sullo schema')
    connectionSocket.send('Corretto'.encode('utf-8'))
    board[Scelta] = 'utente'


#   Questa funzione riceve in ingresso il dizionario con gli elemnti inseriti e le rispettivi chiavi e la lista cn il pordotto di chiavi vincenti.
#   Restituisce:
#       --True se ha vinto qualcuno, stampandoil relativo messaggio
#       --False se non ha vinto nessuno, e la partita puo` continuare o, eventualmente, finire in pareggio
def risultato(board, ris_vinc):
    if len(board.keys()) < 3:#se ci sono meno di tre elementi e` impossibile qualcuno abbia vinto, esco dalla funzione
        return False
    ris_utente = []
    ris_pc = []
    for x in board.items(): #salvo su due liste diversi gli le chiavi degli elemnti messi dall'utente e le chiavi degli elemnti messi dal pc
        if x[1] == 'utente':
            ris_utente.append(x[0])
        elif x[1] == 'pc':
            ris_pc.append(x[0])
    for x in ris_utente[:-2]:# Moltiplico tuttle le chiavi degli elemnti dell'utente a tre a tre tra diloro e, se un dei prodotti ottenuti e` presente nella lista con i prodotti vincenti, allora l'utente ha vinto
        for y in ris_utente[ris_utente.index(x)+1:-1]:
            for z in ris_utente[ris_utente.index(y)+1:]:
                ris = x * y * z
                if ris in ris_vinc:
                    connectionSocket.send('Utente'.encode('utf-8'))
                    print('\nCongratulazioni! hai vinto! :)')
                    return True
    for x in ris_pc[:-2]:# faccio la stessa cosa di prima ma questa volta con le chiavi degli elemnti del pc
        for y in ris_pc[ris_pc.index(x)+1:-1]:
            for z in ris_pc[ris_pc.index(y)+1:]:
                ris = x * y * z
                if ris in ris_vinc:
                    connectionSocket.send('PC'.encode('utf-8'))
                    print('\nAh ah, ho vinto io, piccola testa di cazzo :)')
                    return True
    #print(ris_utente)
    #print(ris_pc)
    return False #se nessuno ha vinto restituisco false


#Prima configuro il server.....
serverPort = 50000
serverName = '192.168.1.195'
welcomeSocket = socket(AF_INET, SOCK_STREAM)
welcomeSocket.bind((serverName, serverPort))
welcomeSocket.listen(1)

while 1:
    print('Server pronto!')
    connectionSocket, clientAddress = welcomeSocket.accept()
    print('In comunicazione con: ', clientAddress)
    while 1:
        game_board = {}
        ris_vincenti = [6, 385, 4199, 65, 238, 627, 133, 273]
        vinto = False
        if sorteggio_inizio() == True:# Decidiamo se inizia priam l'utente(utente = True) o il Pc
            connectionSocket.send('True'.encode('utf-8'))
            utente = True
            print('Bene, hai vinto il sorteggio!\nPuoi iniziare tu')
        else:
            connectionSocket.send('False'.encode('utf-8'))
            utente = False
            print('Mi spiace, questa volta ho vinto io il sorteggio.\nInizio io, coglione')
        print('|1A|1B|1C|\n|2A|2B|2C|\n|3A|3B|3C|\n')
        while len(game_board.keys()) < 9: #la piattaforma ha 9 caselle, se vengono riempite tutte esce dal ciclo while
            if (utente == True):
                mossa_utente(game_board) #funzione che implemeta la mossa dell'utente
                utente = False
            else:
                mossa_pc(game_board) #funzione che implementa la mossa del pc
                utente = True
            print_gameboard(game_board)
            sleep(2)
            if risultato(game_board, ris_vincenti) == True:#Se qualcuni tra l'utente e il pc ha vinto
                vinto = True
                break #esco dal ciclo perche il gioco e` finito
            else:
                connectionSocket.send('Nessuno'.encode('utf-8'))
        if vinto == False:
            if risultato(game_board, ris_vincenti) == False:
                print('La partita e` finita in pareggio')
        break
    connectionSocket.close()