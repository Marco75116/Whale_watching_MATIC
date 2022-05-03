from web3 import Web3
import json
import requests
import math

urlprovider = "https://speedy-nodes-nyc.moralis.io/1882d3dd929705d95a7c9918/eth/mainnet"
w3 = Web3(Web3.HTTPProvider(urlprovider))
def correctBalance(retour):
    retour['balance'] = str(int(retour['balance']) / 10 ** int(retour['decimals']))
    retour['logo'] = str(retour['logo'])
    retour['thumbnail'] = str(retour['thumbnail'])
    return retour

def allToken(adress):
    if w3.isConnected()==True:
        try:
            url = 'https://deep-index.moralis.io/api/v2/' + adress + '/erc20'
            headers = {"x-api-key": "9GxIIHz1XZaypZLqgVb91zl5yCYMJ06d6eKlS1jDt17SEUe6FzeYF0IxoS1IbyaC"}
            response = requests.request("GET", url, headers=headers)
            retour = response.json()
            for token in retour:
                correctBalance(token)
        except:
            print("Wrong adress. man")
    else:
        print("Connexion failed.")
    return retour

def getPriceToken(adressToken):
        try:
            url = 'https://deep-index.moralis.io/api/v2/erc20/' + adressToken + '/price'
            headers = {"x-api-key": "9GxIIHz1XZaypZLqgVb91zl5yCYMJ06d6eKlS1jDt17SEUe6FzeYF0IxoS1IbyaC"}
            response = requests.request("GET", url, headers=headers)
            retour = response.json()['usdPrice']
        except:
            print(response.json())
            print("Wrong adress buddy.")
            retour = 0
        return retour

def proportion():
    listTokens = allToken('0x7abE0cE388281d2aCF297Cb089caef3819b13448')
    retour=[]
    totalvalue=0
    for t in listTokens:
        retour.append(
            {
            'token_address': t['token_address'],
            'symbol': t['symbol'],
            'balance': t['balance'],
            'priceToken': getPriceToken(t['token_address']),
            'valueBalance': getPriceToken(t['token_address'])*float(t['balance'])
            })
        totalvalue+=getPriceToken(t['token_address'])*float(t['balance'])
    for t in retour:
        t['pourcentage'] = t['valueBalance']*100/totalvalue
    print(retour[0])
    print(retour[10])
    print(retour[20])
    print(retour[50])

def pieChart():
    listTokens = allToken('0x4e65175f05b4140a0747c29cce997cd4bb7190d4')
    pieChartTypeData = []
    for token in listTokens:
        priceToken = getPriceToken(token['token_address'])
        if(priceToken != 0):
            totalvalue = priceToken* float(token['balance'])
            pieChartTypeData.append(
                {
                    "name": token['symbol'],
                    "y": totalvalue,
                    #'pricetoken':priceToken,
                    #'balance': token['balance']
                }
            )
    return pieChartTypeData



#print(getPriceToken('0x812d1431a02dd3198d47a5ed51f49137c8308271'))
# for i in allToken('0x7abE0cE388281d2aCF297Cb089caef3819b13448'):
#     print(i['token_address'])
#     print(getPriceToken(i['token_address'])['usdPrice'])

#print(getPriceToken('0xf16007dbf9d4d566cbc9fd00e850d824e236d464'))
#proportion()