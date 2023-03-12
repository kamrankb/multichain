import multichain
from collections import OrderedDict

#Server Connection
serverUser = "multichainrpc"
serverPassword = "3JnoAvDN2CdwRpPTCWReqQRGw22gT96tbLc8siSsdZ4v"
serverHost = "127.0.0.1"
serverPort = "4794"
chainname = "kamran"
serverChain = multichain.MultiChainClient(serverHost, serverPort, serverUser, serverPassword)
serverAddress = serverChain.getaddresses()
print("Server Address: ", serverAddress)

#Client Side Connection
clientUser = "multichainrpc"
clientPassword = "4Xzt1g5AzwBBMcejoDBQsX7u2qYzKHPNc43GDQnDTfyN"
clientHost = "127.0.0.1"
clientPort = "4795"
chainname = "kamran"
clientChain = multichain.MultiChainClient(clientHost, clientPort, clientUser, clientPassword)
clientAddress = clientChain.getaddresses()
print("Client Address: ", clientAddress)

############################ Wallet Configuration #################################


serverAddress = serverChain.getaddresses(True)
serverPub = serverAddress[0]['pubkey']

clientAddress = clientChain.getaddresses(True)
clientPub=clientAddress[0]['pubkey']


###########################Create Walletinformation Create on ServerSide###########################


serverMultiSignAddress = serverChain.addmultisigaddress(2, [serverPub, clientPub])
clientMultiSignAddress = clientChain.addmultisigaddress(2, [serverPub, clientPub])

serverChain.grant(serverMultiSignAddress, 'send,receive') # global permission
clientChain.grant(clientMultiSignAddress, 'send,receive') # global permission

transactionWallet = serverChain.issue(serverMultiSignAddress, {'name' : 'TransactionWallet'}, 1000, 0.01)
transactionWalletBalance = serverChain.getaddressbalances(serverMultiSignAddress, 0)
print("Balance: ", transactionWalletBalance)


########################### This particular address send and recevieammount on Serverside ###

serverChain.grant(serverAddress[4]['address'], 'send,receive') # global permission
print("Address Two ",serverAddress[4]['address'])
print(serverAddress)
print(serverAddress[4]['address'])
sendRawFrom = serverChain.createrawsendfrom(serverMultiSignAddress, {serverAddress[4]['address']:{"MUltichainwallet":5}}, [], 'sign')
initialSign = sendRawFrom['hex']


signRawTransaction = serverChain.signrawtransaction(initialSign)
print(signRawTransaction)
txid = serverChain.sendrawtransaction(signRawTransaction['hex'])
print(txid)

transactionWalletBalance = serverChain.getaddressbalances(serverMultiSignAddress, 0)
print("TransactionWallet Balance: ",transactionWalletBalance)

