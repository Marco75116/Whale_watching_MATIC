import sqlite3
from web3 import Web3
from attributedict.collections import AttributeDict
import copy

#Connection sqlite3 BDD#
import sqlite3
connection = sqlite3.connect('WhalesEth.db')
#FIN#

#Creation Table#
#cursor = connection.cursor()
#requete = "create table Portefeuille(id integer primary key autoincrement, adresse text , balance float)"
#cursor.execute(requete)
#connection.commit()
#connection.close()
#Fin#

ad ="'0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2'"


bal=8216524.39875819

#Insert Table#
#cursor = connection.cursor()
#requete = "insert into Portefeuille (adresse,balance) values ( "+ad+", 8216524.39875819 )"
#cursor.execute(requete)
#connection.commit()
#connection.close()
#Fin#


print ("WEB------------------------------")
w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/00e46f3ce2d8433daecdd8006aaf1c95'))


print("-------------REAL CODE -----------------")
print("-------------")
print("Combien de blocs voulez vous analyser ? ")
print("écrivez un nombre dans la console")
nombreBlocs= int(input())
numberlatestblock = w3.eth.getBlock('latest').number-1
decimal = 1000000000000000000
for i in range(nombreBlocs):
    counterAdresse = 1
    currentnumberblock = numberlatestblock-i
    print(w3.eth.getBlockTransactionCount(currentnumberblock))
    if(i!=0 ):
        print("-------------------------")
        print("---Changement de block---")
    print("Bloc numéro : "+str(currentnumberblock))
    for i in range(w3.eth.getBlockTransactionCount(currentnumberblock)-1):
        if(w3.eth.getBalance(w3.eth.getTransactionByBlock(currentnumberblock, i)['from'])/decimal>1000):
            print("adresse no : " +str(counterAdresse))
            print("Adresse : " + w3.eth.getTransactionByBlock(currentnumberblock, i)['from'])
            print("Balance :" + str(w3.eth.getBalance(w3.eth.getTransactionByBlock(currentnumberblock, i)['from'])/decimal))
            ad=w3.eth.getTransactionByBlock(currentnumberblock, i)['from']
            bal= str(w3.eth.getBalance(w3.eth.getTransactionByBlock(currentnumberblock, i)['from'])/decimal)
            print("dedans---------")
            cursor = connection.cursor()
            requete = f"insert into Portefeuille (adresse,balance) values ( '{ad}' ,{bal})"
            cursor.execute(requete)
            connection.commit()

            counterAdresse += 1
        if(w3.eth.getBalance(w3.eth.getTransactionByBlock(currentnumberblock, i)['to'])/decimal>10000):
            print("adresse no : " + str(counterAdresse))
            print("Adresse : " + w3.eth.getTransactionByBlock(currentnumberblock, i)['to'])
            print("Balance : " + str(w3.eth.getBalance(w3.eth.getTransactionByBlock(currentnumberblock, i)['to'])/decimal))
            addeux = w3.eth.getTransactionByBlock(currentnumberblock, i)['to']
            baldeux = str(w3.eth.getBalance(w3.eth.getTransactionByBlock(currentnumberblock, i)['to']) / decimal)
            baldeux = str(w3.eth.getBalance(w3.eth.getTransactionByBlock(currentnumberblock, i)['to']) / decimal)



            counterAdresse += 1
        if(i==w3.eth.getBlockTransactionCount(currentnumberblock)):
            counterAdresse=1

connection.close()
print("-------END------")

