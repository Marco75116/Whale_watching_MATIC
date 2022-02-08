import sqlite3

import bal as bal
from web3 import Web3
from attributedict.collections import AttributeDict
import copy

print("AttributeDict TEST---------------")
data = AttributeDict({'foo': {'bar': [1, 2, 3]}})
print(data.foo)
print(type(data.foo))
print(data.keys())


print("---------------------------------")

print ("WEB------------------------------")
w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/00e46f3ce2d8433daecdd8006aaf1c95'))

data2 = AttributeDict(copy.deepcopy(w3.eth.getTransactionByBlock(13421133,0)))
print(data2.keys)
print("-------------")
print("dir----------")
print(dir(w3.eth.getTransactionByBlock(13421133,0)))
print("-------------")
print("getTransaction")
print(w3.eth.getTransaction("0x1944dbfd3aa560a9f5390c94291591988112f5efe4bcbf5ed0a82c32a4eca11e"))
print("-------------")
print("getBlock")
print(w3.eth.getBlock(13421133))
print("-------------")
print("getTransactionByBlock")
print(w3.eth.getTransactionByBlock(13421133,0))
print("-------------WHAT IS ACCESSLIST ?")
print("-------------")
print("getTransactionByBlock---KEYS")
print(w3.eth.getTransactionByBlock(13421133,0).keys())
print("-------------")
print("getBlockTransactionCount")
print(w3.eth.getBlockTransactionCount(13421133))
print("-------------")

print(w3.eth.getBalance('0x580150ce0052C40B09d20fFF61E5a71Ba4cfBf4f')/1000000000000000000)


print("-------------REAL CODE -----------------")
print("-------------")
print("Combien de blocs voulez vous analyser ? ")
print("écrivez un nombre dans la console")
nombreBlocs= int(input())
numberlatestblock = w3.eth.getBlock('latest').number-1

for i in range(nombreBlocs):
    counterCoupleAdresse = 1
    currentnumberblock = numberlatestblock-i
    if(i!=0 ):
        print("-------------------------")
        print("---Changement de block---")
    print("Bloc numéro : "+str(currentnumberblock))
    for i in range(w3.eth.getBlockTransactionCount(currentnumberblock)):
        if (w3.eth.getTransactionByBlock(currentnumberblock, i).value / 1000000000000000000 > 100):
            print("-------------------------")
            print(w3.eth.getTransactionByBlock(currentnumberblock, i))
            print("Couple D'adresses : " + str(counterCoupleAdresse))
            print("value : " + str(w3.eth.getTransactionByBlock(currentnumberblock, i).value / 1000000000000000000))
            print("from : " + w3.eth.getTransactionByBlock(currentnumberblock, i)['from'])
            if(w3.eth.getBalance(w3.eth.getTransactionByBlock(currentnumberblock, i)['from'])/1000000000000000000>100 and w3.eth.getBalance(w3.eth.getTransactionByBlock(currentnumberblock, i)['from'])/1000000000000000000<10000):
                print("Balance :" + str(w3.eth.getBalance(w3.eth.getTransactionByBlock(currentnumberblock, i)['from'])/1000000000000000000))
            print("to : " + w3.eth.getTransactionByBlock(currentnumberblock, i)['to'])
            if(w3.eth.getBalance(w3.eth.getTransactionByBlock(currentnumberblock, i)['to'])/1000000000000000000>100 and w3.eth.getBalance(w3.eth.getTransactionByBlock(currentnumberblock, i)['to'])/1000000000000000000<10000):
                print("Balance : " + str(w3.eth.getBalance(w3.eth.getTransactionByBlock(currentnumberblock, i)['to'])/1000000000000000000))
            counterCoupleAdresse += 1
        if(i==w3.eth.getBlockTransactionCount(currentnumberblock)):
            counterCoupleAdresse=1
print("-------END------")
