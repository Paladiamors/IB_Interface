'''
Created on Aug 26, 2014

@author: justin
'''

from com.ib.client import EClientSocket
from com.ib.client import EWrapper
from com.ib.client import Contract, TagValue

import time

contract = Contract()
contract.m_symbol = "AAPL"
contract.m_exchange = "SMART"
contract.m_currency = "USD"
contract.m_secType = "STK"

class Wrapper(EWrapper):
    
    def __init__(self):
        self.handle = open("data.txt", "w")
    
       
    def tickPrice(self,  tickerId,  field,  price,  canAutoExecute):
        print "tickPrice", tickerId, field, price, canAutoExecute
    def tickSize(self,  tickerId,  field,  size):
        print "tickSize", tickerId,  field,  size
    def tickOptionComputation(self,  tickerId,  field,  impliedVol,
             delta,  optPrice,  pvDividend,
             gamma,  vega,  theta,  undPrice):
        pass
    def tickGeneric(self, tickerId,  tickType,  value):
        print "tickGeneric", tickerId,  tickType,  value 
    def tick(self, tickerId,  tickType,  value):
        print "tick", tickerId,  tickType,  value
    def tickEFP(self, tickerId,  tickType,  basisPos,
             formattedBasisPos,  impliedFuture,  holdDays,
             futureExpiry,  dividendImpact,  dividendsToExpiry):
        pass
    def orderStatus(self,  orderId,  status,  filled,  remaining,
             avgFillPrice,  permId,  parentId,  lastFillPrice,
             clientId,  whyHeld):
        pass
    def openOrder(self,  orderId,  contract,  order,  orderState):
        pass
    def openOrderEnd(self,):
        pass
    def updateAccountValue(self, key,  value,  currency,  accountName):
        pass
    def updatePortfolio(self, contract,  position,  marketPrice,  marketValue,
             averageCost,  unrealizedPNL,  realizedPNL,  accountName):
        pass
    def updateAccountTime(self, timeStamp):
        pass
    def accountDownloadEnd(self, accountName):
        pass
    def nextValidId(self,  orderId):
        pass
    def contractDetails(self, reqId,  contractDetails):
        pass
    def bond(self, reqId,  contractDetails):
        pass
    def contractDetailsEnd(self, reqId):
        pass
    def execDetails(self,  reqId,  contract,  execution):
        pass
    def execDetailsEnd(self,  reqId):
        pass
    def updateMktDepth(self,  tickerId,  position,  operation,  side,  price,  size):
        pass
    def updateMktDepthL2(self,  tickerId,  position,  marketMaker,  operation,
             side,  price,  size):
        pass
    def updateNewsBulletin(self,  msgId,  msgType,  message,  origExchange):
        pass
    def managedAccounts(self,  accountsList):
        pass
    def receiveFA(self, faDataType,  xml):
        pass
    def historicalData(self, reqId,  date,  open,  high,  low,
                       close,  volume,  count,  WAP, hasGaps):
        pass
    def scannerParameters(self, xml):
        pass
    def scannerData(self, reqId,  rank,  contractDetails,  distance,
             benchmark,  projection,  legsStr):
        pass
    def scannerDataEnd(self, reqId):
        pass
    def realtimeBar(self, reqId,  time,  open,  high,  low,  close,  volume,  wap,  count):
        pass
    def currentTime(self, time):
        pass
    def fundamentalData(self, reqId,  data):
        pass
    def deltaNeutralValidation(self, reqId,  underComp):
        pass
    def tickSnapshotEnd(self, reqId):
        pass
    def marketDataType(self, reqId,  marketDataType):
        pass
    def commissionReport(self, commissionReport):
        pass
    def position(self, account,  contract,  pos,  avgCost):
        pass
    def positionEnd(self,):
        pass
    def accountSummary(self, reqId,  account,  tag,  value,  currency):
        pass
    def accountSummaryEnd(self, reqId):
        pass
    def verifyMessageAPI(self,  apiData):
        pass
    def verifyCompleted(self, isSuccessful,  errorText):
        pass
    def displayGroupList(self,  reqId,  groups):
        pass
    def displayGroupUpdated(self,  reqId,  contractInfo):
        pass

    def error(self, *args):
        print "error", args
    
    def connectionClosed(self):
        print "connection closed"
wrapper = Wrapper()

client = EClientSocket(wrapper)
client.eConnect("localhost", 7496, 1)
print client.connected

time.sleep(5)
client.reqMktData(1, contract, "", False, [])
for x in range(10):
    print client.connected
    client.reqCurrentTime()
    time.sleep(1)
    