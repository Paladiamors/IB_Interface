'''
Created on Oct 14, 2014

@author: justin
'''

from com.ib.client import EWrapper

import datetime
import Queue

class Wrapper(EWrapper):
    
    def __init__(self):
        self.handle = open("data.txt", "w")
        self.queue = Queue.Queue()
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
        msgType = "tickPrice"
        data = {"msgType":msgType, "time": datetime.datetime.now().isoformat(), "tickerId": tickerId, "field": self.tickDict[field], "price": price, "canAutoExecute": canAutoExecute}
        self.queue.put(data)
    
    def tickSize(self,  tickerId,  field,  size):
        msgType = "tickSize"
        data = {"msgType":msgType, "time": datetime.datetime.now().isoformat(), "tickerId": tickerId, "field": self.tickDict[field], "size": size}
        self.queue.put(data)
        
    def tickOptionComputation(self,  tickerId,  field,  impliedVol,
             delta,  optPrice,  pvDividend,
             gamma,  vega,  theta,  undPrice):
        
        msgType = "tickOptionComputation" 
        data = {"msgType":msgType, "tickerId":tickerId,  "field":field,  "impliedVol":impliedVol, "delta":delta,  "optPrice":optPrice,  "pvDividend":pvDividend, "gamma":gamma,  "vega":vega,  "theta":theta,  "undPrice":undPrice}
        self.queue.put(data)
        
    def tickGeneric(self, tickerId,  tickType,  value):
        msgType = "tickGeneric"
        data = {"msgType":msgType, "tickerId":tickerId,  "tickType":tickType,  "value":value} 
        self.queue.put(data)
        
    def tick(self, tickerId,  tickType,  value):
        msgType = "tick"
        data = {"msgType":msgType, "tickerId":tickerId,  "tickType":tickType,  "value":value}
        self.queue.put(data)
        
    def tickEFP(self, tickerId,  tickType,  basisPos,
             formattedBasisPos,  impliedFuture,  holdDays,
             futureExpiry,  dividendImpact,  dividendsToExpiry):
        
        msgType = "tickEFP"
        data = {"msgType":msgType, "tickerId":tickerId,  "tickType":tickType,  "basisPos":basisPos, "formattedBasisPos":formattedBasisPos,  "impliedFuture":impliedFuture,  "holdDays":holdDays, "futureExpiry":futureExpiry,  "dividendImpact":dividendImpact,  "dividendsToExpiry":dividendsToExpiry}
        self.queue.put(data)
        
    def orderStatus(self,  orderId,  status,  filled,  remaining,
             avgFillPrice,  permId,  parentId,  lastFillPrice,
             clientId,  whyHeld):
        
        msgType = "orderStatus" 
        data = {"msgType":msgType, "orderId":orderId,  "status":status,  "filled":filled,  "remaining":remaining, "avgFillPrice":avgFillPrice,  "permId":permId,  "parentId":parentId,  "lastFillPrice":lastFillPrice, "clientId":clientId,  "whyHeld":whyHeld}
        self.queue.put(data)
        
    def openOrder(self,  orderId,  contract,  order,  orderState):
        
        msgType = "openOrder"
        data = {"msgType":msgType, "orderId":orderId,  "contract":contract,  "order":order,  "orderState":orderState}
        self.queue.put(data)
   
    def openOrderEnd(self):
        pass
    
    def updateAccountValue(self, key,  value,  currency,  accountName):
        msgType = "updateAccountValue"
        data = {"msgType":msgType, "key":key,  "value":value,  "currency":currency,  "accountName":accountName}
        self.queue.put(data)
        
        
    def updatePortfolio(self, contract,  position,  marketPrice,  marketValue,
             averageCost,  unrealizedPNL,  realizedPNL,  accountName):
        msgType = "updatePortfolio"
        data = {"msgType":msgType, "contract":contract,  "position":position,  "marketPrice":marketPrice,  "marketValue":marketValue, "averageCost":averageCost,  "unrealizedPNL":unrealizedPNL,  "realizedPNL":realizedPNL,  "accountName":accountName}
        self.queue.put(data)
    
    def updateAccountTime(self, timeStamp):
        msgType = "updateAccountTime" 
        data = {"msgType":msgType, "timestamp" : timeStamp}
        self.queue.put(data)
        
    def accountDownloadEnd(self, accountName):
        msgType = "accountDownloadEnd"
        data = {"msgType":msgType, "accountName": accountName}
        self.queue.put(data)
    
    def nextValidId(self,  orderId):
        msgType = "nextValidId"
        data = {"msgType":msgType, "orderId": orderId}
        self.queue.put(data)
    
    def contractDetails(self, reqId,  contractDetails):
        msgType = "contractDetails"
        data = {"msgType":msgType, "reqId":reqId,  "contractDetails":contractDetails}
        self.queue.put(data)
    
    def bond(self, reqId,  contractDetails):
        msgType = "bond"
        data = {"msgType":msgType, "reqId":reqId,  "contractDetails":contractDetails}
        self.queue.put(data)
    
    def contractDetailsEnd(self, reqId):
        msgType = "contractDetailsEnd"
        data = {"msgType":msgType, "reqId": reqId}
        self.queue.put(data)
        
    def execDetails(self,  reqId,  contract,  execution):
        msgType = "execDetails"
        data = {"msgType":msgType, "reqId":reqId,  "contract":contract,  "execution":execution}
        self.queue.put(data)
    
    def execDetailsEnd(self,  reqId):
        msgType = "execDetailsEnd"
        data = {"msgType":msgType, "reqId": reqId}
        self.queue.put(data)
    
    def updateMktDepth(self,  tickerId,  position,  operation,  side,  price,  size):
        msgType = "updateMktDepth"
        data = {"msgType":msgType, "tickerId":tickerId,  "position":position,  "operation":operation,  "side":side,  "price":price,  "size":size}
        self.queue.put(data)
        
    def updateMktDepthL2(self,  tickerId,  position,  marketMaker,  operation,
             side,  price,  size):
        msgType = "updateMktDepthL2"
        data = {"msgType":msgType, "tickerId":tickerId,  "position":position,  "marketMaker":marketMaker,  "operation":operation, "side":side,  "price":price,  "size":size}
        self.queue.put(data)
    
    def updateNewsBulletin(self,  msgId,  msgType,  message,  origExchange):
        msgType = "updateNewsBulletin"
        data = {"msgType":msgType, "msgId":msgId,  "msgType":msgType,  "message":message,  "origExchange":origExchange}
        self.queue.put(data)
    
    def managedAccounts(self,  accountsList):
        msgType = "managedAccounts"
        data = {"msgType":msgType, "accountsList": accountsList}
        self.queue.put(data)
    
    def receiveFA(self, faDataType,  xml):
        msgType = "receiveFA"
        data = {"msgType":msgType, "faDataType":faDataType,  "xml":xml}
        self.queue.put(data)
    
    def historicalData(self, reqId,  date,  open,  high,  low,
                       close,  volume,  count,  WAP, hasGaps):
        msgType = "historicalData"
        data = {"msgType":msgType, "reqId":reqId,  "date":date,  "open":open,  "high":high,  "low":low, "close":close,  "volume":volume,  "count":count,  "WAP":WAP, "hasGaps":hasGaps}
        self.queue.put(data) 
    
    def scannerParameters(self, xml):
        msgType = "scannerParameters"
        data = {"msgType":msgType, "xml": xml}
        self.queue.put(data)
    
    def scannerData(self, reqId,  rank,  contractDetails,  distance,
             benchmark,  projection,  legsStr):
        
        msgType = "scannerData"
        data = {"msgType":msgType, "reqId":reqId,  "rank":rank,  "contractDetails":contractDetails,  "distance":distance, "benchmark":benchmark,  "projection":projection,  "legsStr":legsStr}
        self.queue.put(data)
    
    def scannerDataEnd(self, reqId):
        msgType = "scannerDataEnd"
        data = {"msgType":msgType, "reqId": reqId}
        self.queue.put(data)
        
    def realtimeBar(self, reqId,  time,  open,  high,  low,  close,  volume,  wap,  count):
        msgType = "realtimeBar"
        data = {"msgType":msgType, "reqId":reqId,  "time":time,  "open":open,  "high":high,  "low":low,  "close":close,  "volume":volume,  "wap":wap,  "count":count}
        self.queue.put(data)
    
    def currentTime(self, time):
        msgType = "currentTime"
        data = {"msgType":msgType, "time": time}
        self.queue.put(data)
        
    def fundamentalData(self, reqId,  data):
        msgType = "fundamentalData"
        data = {"msgType":msgType, "reqId":reqId,  "data":data}
        self.queue.put(data)
   
    def deltaNeutralValidation(self, reqId,  underComp):
        msgType = "deltaNeutralValidation"
        data = {"msgType":msgType, "reqId":reqId,  "underComp":underComp}
        self.queue.put(data)
        
    def tickSnapshotEnd(self, reqId):
        msgType = "tickSnapshotEnd"
        data = {"msgType":msgType, "reqId": reqId}
        self.queue.put(data)
    
    def marketDataType(self, reqId,  marketDataType):
        msgType = "marketDataType"
        data = {"msgType":msgType, "reqId":reqId,  "marketDataType":marketDataType}
        self.queue.put(data)
    
    def commissionReport(self, commissionReport):
        msgType = "commissionReport"
        data = {"msgType":msgType, "commissionReport": commissionReport}
        self.queue.put(data)
    
    def position(self, account,  contract,  pos,  avgCost):
        msgType = "position"
        data = {"msgType":msgType, "account":account,  "contract":contract,  "pos":pos,  "avgCost": avgCost}
        self.queue.put(data)    
    
    def positionEnd(self):
        msgType = "positionEnd"
        data = {"msgType":msgType}
        self.queue.put(data)
             
    def accountSummary(self, reqId,  account,  tag,  value,  currency):
        msgType = "accountSummary" 
        data = {"msgType":msgType, "reqId":reqId,  "account":account,  "tag":tag,  "value":value,  "currency":currency}
        self.queue.put(data)
        
    def accountSummaryEnd(self, reqId):
        msgType = "accountSummaryEnd"
        data = {"msgType":msgType, "reqId": reqId}
        self.queue.put(data)
    
    def verifyMessageAPI(self,  apiData):
        msgType = "verifyMessageAPI"
        data = {"msgType":msgType, "apiData": apiData}
        self.queue.put(data)
        
    def verifyCompleted(self, isSuccessful,  errorText):
        msgType = "verifyCompleted"
        data = {"msgType":msgType, "isSuccessful":isSuccessful,  "errorText":errorText}
        self.queue.put(data)
        
    def displayGroupList(self,  reqId,  groups):
        msgType = "displayGroupList"
        data = {"msgType":msgType, "reqId":reqId,  "groups":groups}
        self.queue.put(data)
        
    def displayGroupUpdated(self,  reqId,  contractInfo):
        msgType = "displayGroupUpdated"
        data = {"msgType":msgType, "reqId":reqId,  "contractInfo":contractInfo}
        self.queue.put(data)

    def error(self, *args):
        print "error", args
    
    def connectionClosed(self):
        print "connection closed"