import sqlite3
import requests
import web3
from web3 import Web3


w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/00e46f3ce2d8433daecdd8006aaf1c95'))

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
def buildDictTxExploitables(TxBrut):
    Tx = {
        "hash": TxBrut[0],
        "timeStamp": TxBrut[1],
        "adresseFromE": TxBrut[2],
        "adresseToE": TxBrut[3],
        "valueE": TxBrut[4],
    }
    return Tx


def getAllTx():
    connection = sqlite3.connect('WhalesEth.db')
    cursor = connection.cursor()
    requeteLastLigne = "SELECT * " \
                       "FROM MaticTransactions " \
                       "order by id desc " \

    cursor.execute(requeteLastLigne)
    cursor.execute
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


# # #
# connection = sqlite3.connect('WhalesEth.db')
# cursor = connection.cursor()
# requeteLastLigne = "SELECT distinct hash " \
#                    "FROM MaticTransactions " \
#                     \
#
# #
# cursor.execute(requeteLastLigne)
# # cursor.execute
# # # # adressTo = ('0x7d1afa7b718fb893db30a3abc0cfc608aacfebb0',)
# # # # requeteTxDernierBlock = "SELECT count(*)  " \
# # # #                         "FROM MaticTransactions" \
# # # #                         "WHERE adresseTo = ?"
# # # # cursor.execute("SELECT count(*) FROM MaticTransactions WHERE adresseTo= ?",adressTo)
# lastTx = cursor.fetchall()
# connection.commit()
# connection.close()
#
contract = w3.eth.contract(address="0x7D1AfA7B718fb893dB30A3aBc0Cfc608AaCfeBB0", abi=getAbiForContract())


def InsertBddExploitable(T,retourDecode):
    connection = sqlite3.connect('WhalesEth.db')
    cursor = connection.cursor()
    requete = f"insert into TxExploitables (hash,timeStamp,adresseFromE,adresseToE,valueE) " \
              f"values ('{T['hash']}',{T['timeStamp']},'{retourDecode[0]}','{retourDecode[1]}',{retourDecode[2]})"
    cursor.execute(requete)
    connection.commit()
    connection.close()

def getALlTxfromAdressToE(adress):
    connection = sqlite3.connect('WhalesEth.db')
    cursor = connection.cursor()
    inputReverted = (adress,)
    cursor.execute("SELECT * FROM TxExploitables WHERE adresseToE=? ", inputReverted)
    allTxBrut = cursor.fetchall()
    connection.commit()
    connection.close()
    print(allTxBrut)
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


listTx =getALlTxAdressFromE('0xeC504bfcC11021045598bb24C9DAd5818033bbD4')

def historicalBalanceValue(listTx):
    Indicateur = []
    for tx in listTx:
        Indicateur.append({
            'timestamp': tx['timeStamp'],
            'valueModified': tx['valueE']
        })
    return Indicateur


