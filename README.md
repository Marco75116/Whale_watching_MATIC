# Whale_watching_MATIC

what we used : Python,Sqlite,Angular,FastApi,HighCharts,web3,Etherscan,CryptoCompare,Infura,Postman,Moralis.

This project consists of analyzing the ethereum blockchain to identify whales and track their movements. We have chosen to focus on the matic token.
We extracted 2.8 M matic transactions on the mainet from etherscan to put them in our database.We have decoded the input of transactions.  We cleaned and filtered those transactions to keep only the events transfer,transferFrom and the amount of token transferred.

Now the goal is to obtain the history of the matic token balance of an address and to know if this address is performing well. This will be done using timestamps and the amount of token matic on the whale transactions as well as the historical price of the token. Once an interesting address has been identified we can look at the composition of its wallet.

Finally, to expose our work our format will be a dashboard. It will be an interactive app where the user can input addresses. We will use graphical charts to give a deep and easy understanding of our results to the user.

<img width=2100 src="https://github.com/Marco75116/Whale_watching_MATIC/blob/main/DASHBOARDangular.png">
Unfornately I have reached the limit of the Cryptocompare api that I use to get the historical price of the matic token for every tx. So I can't analyse relevant address with many tx.
<br>
<img width=2100 src="https://github.com/Marco75116/Whale_watching_MATIC/blob/main/image.png">
