import ins as ins
import requests
from web3 import Web3
import sqlite3
import json


w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/00e46f3ce2d8433daecdd8006aaf1c95'))

def getTokenMaticTransactions(blockNumber):
    url = "https://api.etherscan.io/api?module=account" \
          "&action=txlist" \
          "&address=0x7D1AfA7B718fb893dB30A3aBc0Cfc608AaCfeBB0" \
          "&startblock=" + str(blockNumber)+ \
          "&endblock=99999999" \
          "&page=1" \
          "&offset=10000" \
          "&sort=asc" \
          "&apikey=5EATU9EBIGV772GYY8U3YNBQC56R62C72C"
    reponse = requests.get(url)
    return reponse.json()['result']

def InsertBdd(T):
    connection = sqlite3.connect('WhalesEth.db')
    cursor = connection.cursor()
    requete = f"insert into MaticTransactions (blockNumber,timeStamp,hash,nonce,blockHash,transactionIndex,adresseFrom,adresseTo,value,gas,gasPrice,isError,txreceipt_status,input,contractAddress,cumulativeGasUsed,gasUsed,confirmations) " \
              f"values ({T['blockNumber']},{T['timeStamp']},'{T['hash']}',{T['nonce']},'{T['blockHash']}',{T['transactionIndex']},'{T['from']}','{T['to']}',{T['value']},{T['gas']},{T['gasPrice']},{T['isError']},{T['txreceipt_status']},'{T['input']}','{T['contractAddress']}',{T['cumulativeGasUsed']},{T['gasUsed']},{T['confirmations']} )"
    cursor.execute(requete)
    connection.commit()
    connection.close()

def InsertBddManualy(blockNumber,nbTxAlreadyBdd):
    result = getTokenMaticTransactions(blockNumber)
    result = result[nbTxAlreadyBdd:]
    result= [x for x in result if x['blockNumber']==blockNumber]
    for i in result:
        print(i)
        InsertBdd(i)
    print(len(result))

def MainExtractTx(dernierBlockbdd):
    dernierBlock=dernierBlockbdd
    for i in range(300):
        print(f"-------------boucle---------------- numéro : {i}" )
        dixMilleTransacs = getTokenMaticTransactions(dernierBlock)
        #print(f"this is dixMilleTransacs : {dixMilleTransacs}")
        lastTx = dixMilleTransacs[-1]
        #print(f"this is lastTx : {lastTx}")
        #print(f"this is lastTx['blockNumber'] : {lastTx['blockNumber']}")
        dernierBlock = lastTx['blockNumber']+1
        #print(f"this is dernierBlock : {dernierBlock}")
        for j in dixMilleTransacs:
            InsertBdd(j)

def buildDictTx(TxBrut):
    Tx = {
        "id": TxBrut[0],
        "blockNumber": TxBrut[1],
        "timeStamp": TxBrut[2],
        "hash": TxBrut[3],
        "nonce": TxBrut[4],
        "blockHash": TxBrut[5],
        "transactionIndex": TxBrut[6],
        "adresseFrom": TxBrut[7],
        "adresseTo": TxBrut[8],
        "value": TxBrut[9],
        "gas": TxBrut[10],
        "gasPrice": TxBrut[11],
        "isError": TxBrut[12],
        "txreceipt_status": TxBrut[13],
        "input": TxBrut[14],
        "contractAddress": TxBrut[15],
        "cumulativeGasUsed": TxBrut[16],
        "gasUsed": TxBrut[17],
        "confirmations": TxBrut[18]
    }

    return Tx

def getTxByID(Id):
    connection = sqlite3.connect('WhalesEth.db')
    cursor = connection.cursor()
    requete = "select * " \
              "from MaticTransactions where id = "+ str(Id)
    cursor.execute(requete)
    TxBrut = cursor.fetchone()
    connection.commit()
    connection.close()
    return buildDictTx(TxBrut)

def getAllTx():
    connection = sqlite3.connect('WhalesEth.db')
    cursor = connection.cursor()
    requeteLastLigne = "SELECT * " \
                       "FROM MaticTransactions " \
                       "order by id desc " \
#                       "limit 100000 "
    cursor.execute(requeteLastLigne)
    allTxBrut = cursor.fetchall()
    connection.commit()
    connection.close()
    listAllTx = []
    for tx in allTxBrut:
        listAllTx.append(buildDictTx(tx))
    return listAllTx

def getAbiForContract():
    url = " https://api.etherscan.io/api" \
          "?module=contract" \
          "&action=getabi" \
          "&address=0x7D1AfA7B718fb893dB30A3aBc0Cfc608AaCfeBB0" \
          "&apikey=5EATU9EBIGV772GYY8U3YNBQC56R62C72C "
    reponse = requests.get(url)
    return reponse.json()['result']

def getAllTxReverted():
    connection = sqlite3.connect('WhalesEth.db')
    cursor = connection.cursor()
    inputReverted = ('0x',)
    cursor.execute("SELECT * FROM MaticTransactions WHERE input = ?" , inputReverted)
    allTxBrut = cursor.fetchall()
    connection.commit()
    connection.close()
    listAllTx = []
    for tx in allTxBrut:
        listAllTx.append(buildDictTx(tx))
    return listAllTx


def deleteRowByHash(hash,connection):
#    connection = sqlite3.connect('WhalesEth.db')
    cursor = connection.cursor()
    hashnet=(hash,)
    requete = "delete " \
              "from MaticTransactions " \
              "where hash= ?"
    cursor.execute("delete from MaticTransactions where hash=?",hashnet)
    connection.commit()
#   connection.close()

def deleteTxReverted():
    allTxReverted = getAllTxReverted()
    for txR in allTxReverted:
        deleteRowByHash(txR['hash'])

contract = w3.eth.contract(address="0x7D1AfA7B718fb893dB30A3aBc0Cfc608AaCfeBB0", abi=getAbiForContract())

def decodeInput(tx):
    try:
        func_obj, func_params = contract.decode_function_input(tx["input"])
        if str(func_obj) == '<Function transfer(address,uint256)>' :
             #print(func_params['to'])
             #print(func_params['value'] / 10 ** 18)
             return tx['adresseFrom'],func_params['to'],func_params['value']/10 ** 18
        elif str(func_obj) == '<Function transferFrom(address,address,uint256)>' :
             #print(tx['hash'])
             #print(func_obj)
             #print(func_params)
             return func_params['from'],func_params['to'],func_params['value']/10 ** 18
        elif str(func_obj) != '<Function approve(address,uint256)>':
            print(tx['hash'])
            print(func_obj)

    except:
        print('--------strange tx -------')
        print(tx['hash'])


def getHistoricalPrice(Timestamp):
    url = "https://min-api.cryptocompare.com/data/v2/histohour" \
          "?fsym=MATIC" \
          "&tsym=USD" \
          "&limit=1" \
          "&toTs=" + Timestamp
    reponse = requests.get(url)
    print(reponse.json())
    prices = reponse.json()['Data']['Data']
    price =  ( prices[0]['high'] + prices[0]['low'] + prices[1]['high'] + prices[1]['low'] ) / 4
    return round(price,5)

def insertBddExploitable(T,retourDecode):
    connection = sqlite3.connect('WhalesEth.db')
    cursor = connection.cursor()
    requete = f"insert into TxExploitables (hash,timeStamp,adresseFromE,adresseToE,valueE) " \
              f"values ('{T['hash']}','{T['timeStamp']}','{retourDecode[0]}','{retourDecode[1]}',{retourDecode[2]})"
    cursor.execute(requete)
    connection.commit()
    connection.close()

def insertBddTxExceptions(hash):
    connection = sqlite3.connect('WhalesEth.db')
    cursor = connection.cursor()
    requete = f"insert into TxException (hash) " \
              f"values (   '{hash}')"
    cursor.execute(requete)
    connection.commit()
    connection.close()

def getDoublonsBdd():
    connection = sqlite3.connect('WhalesEth.db')
    cursor = connection.cursor()
    requete = f"select hash,input " \
              f"from MaticTransactions "\
              f"group by hash,input " \
              f"having count(*)>1 "
    cursor.execute(requete)
    retour = cursor.fetchall()
    connection.commit()
    connection.close()
    return retour

def deletedoublon():
    allTxDoublons = getDoublonsBdd()
    connection = sqlite3.connect('WhalesEth.db')
    for tx in allTxDoublons:
        deleteRowByHash(tx[0],connection)
    connection.close()

def buildBddExploitable():
    alltx = getAllTx()
    for tx in alltx:
        retourDecode = decodeInput(tx)
        if retourDecode:
            try:
                insertBddExploitable(tx, retourDecode)
            except:
                print("exception")
                print(tx['hash'])

def sortAdressbyNounce():
    connection = sqlite3.connect('WhalesEth.db')
    cursor = connection.cursor()
    requeteLastLigne = "SELECT distinct adresseFrom " \
                       "FROM MaticTransactions " \
                       "order by nonce DESC " \
                       "limit 5000"
    cursor.execute(requeteLastLigne)
    cursor.execute
    allTxBrut = cursor.fetchall()
    connection.commit()
    connection.close()
    listRetour = []
    for address in allTxBrut:
        listRetour.append(address[0])
    return listRetour

def InsertBddActiveAdress():
    listAddress = sortAdressbyNounce()
    connection = sqlite3.connect('WhalesEth.db')
    cursor = connection.cursor()
    for adress in listAddress:
        requete = f"insert into ActiveAdress (activeAddress) " \
                  f"values ('{adress}')"
        cursor.execute(requete)
    connection.commit()
    connection.close()

def buildDictTxExploitables(TxBrut):
    Tx = {
        "hash": TxBrut[0],
        "timeStamp": TxBrut[1],
        "adresseFromE": TxBrut[2],
        "adresseToE": TxBrut[3],
        "valueE": TxBrut[4],
    }
    return Tx

def getALlTxfromAdressToE(adress):
    connection = sqlite3.connect('WhalesEth.db')
    cursor = connection.cursor()
    inputReverted = (adress,)
    cursor.execute("SELECT * FROM TxExploitables WHERE adresseToE=? ", inputReverted)
    allTxBrut = cursor.fetchall()
    connection.commit()
    connection.close()
    listAllTx = []
    for tx in allTxBrut:
        listAllTx.append(buildDictTxExploitables(tx))
    return listAllTx

def getALlTxAdressFromE(adress):
    connection = sqlite3.connect('WhalesEth.db')
    cursor = connection.cursor()
    inputReverted = (adress,)
    cursor.execute("SELECT * FROM TxExploitables WHERE adresseFromE=? ", inputReverted)
    allTxBrut = cursor.fetchall()
    connection.commit()
    connection.close()
    listAllTx = []
    for tx in allTxBrut:
        listAllTx.append(buildDictTxExploitables(tx))
    return listAllTx


#listTxfrom =getALlTxAdressFromE('0xeC504bfcC11021045598bb24C9DAd5818033bbD4')
#listTxto= getALlTxfromAdressToE('0xeC504bfcC11021045598bb24C9DAd5818033bbD4')



def historicalBalanceValue(address):
    listTxfrom = getALlTxAdressFromE('0x0084dfd7202e5f5c0c8be83503a492837ca3e95e')
    listTxto = getALlTxfromAdressToE('0x0084dfd7202e5f5c0c8be83503a492837ca3e95e')
    Indicateur = []
    for tx in listTxfrom:
        Indicateur.append({
            'timestamp': tx['timeStamp'],
            'valueModified': -tx['valueE']*getHistoricalPrice(tx['timeStamp'])
        })
    for tx in listTxto:
        Indicateur.append({
            'timestamp': tx['timeStamp'],
            'valueModified': +tx['valueE'] * getHistoricalPrice(tx['timeStamp'])
        })
    Indicateur = sorted(Indicateur, key=lambda tx:tx['timestamp'])
    print(Indicateur)
    return Indicateur




def getBenefice(Indicateur):
    benef = 0
    for indic in Indicateur:
        benef += indic['valueModified']
    print(benef)

Indic = historicalBalanceValue("0xeC504bfcC11021045598bb24C9DAd5818033bbD4")

getBenefice(Indic)

