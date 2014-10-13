'''
Created on Oct 14, 2014

@author: justin
'''

from com.ib.client import EWrapper

import datetime
class Wrapper(EWrapper):
    
    def __init__(self):
        self.handle = open("data.txt", "w")
    
        #tickDict used by the following commands
        #tickSize()
        #tickEFP()
        #tickGeneric()
        #tickOptionComputation()
        #tickPrice()
        #tickSize()
        #tickString()
        self.tickDict = {
                            0: "BID_SIZE",
                            1: "BID_PRICE",
                            2: "ASK_PRICE",
                            3: "ASK_SIZE",
                            4: "LAST_PRICE",
                            5: "LAST_SIZE",
                            6: "HIGH",
                            7: "LOW",
                            8: "VOLUME",
                            9: "CLOSE_PRICE",
                            10: "BID_OPTION_COMPUTATION",
                            11: "ASK_OPTION_COMPUTATION",
                            12: "LAST_OPTION_COMPUTATION",
                            13: "MODEL_OPTION_COMPUTATION",
                            14: "OPEN_TICK",
                            15: "LOW_13_WEEK",
                            16: "HIGH_13_WEEK",
                            17: "LOW_26_WEEK",
                            18: "HIGH_26_WEEK",
                            19: "LOW_52_WEEK",
                            20: "HIGH_52_WEEK",
                            21: "AVG_VOLUME",
                            22: "OPEN_INTEREST",
                            23: "OPTION_HISTORICAL_VOL",
                            24: "OPTION_IMPLIED_VOL",
                            27: "OPTION_CALL_OPEN_INTEREST",
                            28: "OPTION_PUT_OPEN_INTEREST",
                            29: "OPTION_CALL_VOLUME",
                            30: "OPTION_PUT_VOLUME",
                            31: "INDEX_FUTURE_PREMIUM",
                            32: "BID_EXCH",
                            33: "ASK_EXCH",
                            34: "AUCTION_VOLUME",
                            35: "AUCTION_PRICE",
                            36: "AUCTION_IMBALANCE",
                            37: "MARK_PRICE",
                            38: "BID_EFP_COMPUTATION",
                            39: "ASK_EFP_COMPUTATION",
                            40: "LAST_EFP_COMPUTATION",
                            41: "OPEN_EFP_COMPUTATION",
                            42: "HIGH_EFP_COMPUTATION",
                            43: "LOW_EFP_COMPUTATION",
                            44: "CLOSE_EFP_COMPUTATION",
                            45: "LAST_TIMESTAMP",
                            46: "SHORTABLE",
                            47: "FUNDAMENTAL_RATIOS",
                            48: "RT_VOLUME",
                            49: "HALTED",
                            50: "BIDYIELD",
                            51: "ASKYIELD",
                            52: "LASTYIELD",
                            53: "CUST_OPTION_COMPUTATION",
                            54: "TRADE_COUNT",
                            55: "TRADE_RATE",
                            56: "VOLUME_RATE"
                        }
    def tickPrice(self,  tickerId,  field,  price,  canAutoExecute):
        
        print  {"time": datetime.datetime.now(), "tickerId": tickerId, "field": self.tickDict[field], "price": price, "canAutoExecute": canAutoExecute}
    
    def tickSize(self,  tickerId,  field,  size):
        print {"time": datetime.datetime.now(), "tickerId": tickerId, "field": self.tickDict[field], "size": size}
    
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