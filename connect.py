'''
Created on Aug 26, 2014

@author: justin
'''

from com.ib.client import EClientSocket
from com.ib.client import Contract, TagValue

from wrapper import Wrapper

import time
import sockLib
import Queue
import threading
import select

class ClientManager:
    
    def __init__(self, host="localhost", port=7496, id=1):
        self.host=host
        self.port=port
        self.id=id
        self.subscriptions = {}
        self.subscriptionCounter = 1
        
        wrapper = Wrapper()
        self.client=EClientSocket(wrapper)
        self.client.eConnect(host, port, id)
        
        time.sleep(5)
        
    def subscribeStock(self, symbol):
        contract = Contract()
        contract.m_symbol = symbol
        contract.m_exchange = "SMART"
        contract.m_currency = "USD"
        contract.m_secType = "STK"

        self.subscriptions[symbol] = self.subscriptionCounter
        self.client.reqMktData(self.subscriptionCounter, contract, "", False, [])
        self.subscriptionCounter+=1

    def subscribeFX(self, base, priceCur):
        """
        base = base of the currency pair
        priceCur = currency for pricing
        
        ex. USD, JPY means buy/sell USD with price of JPY
        """
        contract = Contract()
        contract.m_symbol = base
        contract.m_exchange = "IDEALPRO"
        contract.m_currency = priceCur
        contract.m_secType = "CASH"
        
        symbol = ".".join([base, priceCur])

        self.subscriptions[symbol] = self.subscriptionCounter
        self.client.reqMktData(self.subscriptionCounter, contract, "", False, [])
        self.subscriptionCounter+=1        
        
    def unsubscribeStock(self, symbol):
        
        if symbol in self.subscription:
            self.client.cancelMktData(self.subscriptions[symbol])
            self.subscriptions.pop(symbol)
        
    def unsubscribeFX(self, base, priceCur):
        
        symbol = ".".join([base, priceCur])
        
        if symbol in self.subscription:
            self.client.cancelMktData(self.subscriptions[symbol])
            self.subscriptions.pop(symbol)
    def reqCurrentTime(self):
        
        print self.client.reqCurrentTime()
        
    def connected(self):
        
        return self.client.connected
    
class Server:
    
    def __init__(self, port  = 12000):
    
        self.activeClients = []
        self.acceptQueue = Queue.Queue()
        self.serverSocket = sockLib.serverSocket(port)
        
        self.acceptThread = threading.Thread(target = self.acceptConnection)
        
    def acceptConnection(self):
        
        while True:
            sock, address = self.serverSocket.accept()
            self.acceptQueue.put(sock)
    
    
        
        

if __name__ == "__main__":
    
    clientManager = ClientManager()
#     clientManager.subscribeStock("AAPL")
#     clientManager.subscribeStock("AMZN")
#     clientManager.subscribeStock("YHOO")
#     clientManager.subscribeStock("GOOG")
#     clientManager.subscribeStock("SNE")
    clientManager.subscribeFX("USD", "JPY")
    
    
# contract = Contract()
# contract.m_symbol = "AAPL"
# contract.m_exchange = "SMART"
# contract.m_currency = "USD"
# contract.m_secType = "STK"
# 
# wrapper = Wrapper()
# 
# client = EClientSocket(wrapper)
# client.eConnect("localhost", 7496, 1)
# print client.connected
# 
# time.sleep(5)
# client.reqMktData(1, contract, "", False, [])
# for x in range(10):
#     print client.connected
#     client.reqCurrentTime()
#     time.sleep(1)
    