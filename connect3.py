'''
Created on Aug 26, 2014

@author: justin
'''

from com.ib.client import EClientSocket
from com.ib.client import Contract, TagValue, Order, ExecutionFilter

from wrapper2 import Wrapper

import time
import sockLib
import Queue
import threading
import select

class ClientManager:
    """
    object that connects to the TWS gateway --> use an external program to drive this component
    """
    
    def __init__(self, host="localhost", port=7496, id=1):
        self.host=host
        self.port=port
        self.id=id
        self.subscriptions = {}
        self.tickerMap = {}
        self.funcMap = self._defineFuncMap()
        self.subscriptionCounter = 1
        
        self.wrapper = Wrapper()
        self.client=EClientSocket(self.wrapper)
        self.client.eConnect(host, port, id)
        
        time.sleep(5)
    
    def _defineFuncMap(self):
        
        funcMap = {
                    "reqMktData": self.reqMktData,
                    "cancelHistoricalData": self.cancelHistoricalData,
                    "cancelRealTimeBars": self.cancelRealTimeBars,
                    "reqHistoricalData": self.reqHistoricalData,
                    "reqRealTimeBars": self.reqRealTimeBars,
                    "reqContractDetails": self.reqContractDetails,
                    "reqMktDepth": self.reqMktDepth,
                    "cancelMktData": self.cancelMktData,
                    "cancelMktDepth": self.cancelMktDepth,
                    "exerciseOptions": self.exerciseOptions,
                    "placeOrder": self.placeOrder,
                    "reqAccountUpdates": self.reqAccountUpdates,
                    "reqExecutions": self.reqExecutions,
                    "cancelOrder": self.cancelOrder,
                    "reqOpenOrders": self.reqOpenOrders,
                    "reqIds": self.reqIds,
                    "reqNewsBulletins": self.reqNewsBulletins,
                    "cancelNewsBulletins": self.cancelNewsBulletins,
                    "setServerLogLevel": self.setServerLogLevel,
                    "reqAutoOpenOrders": self.reqAutoOpenOrders,
                    "reqAllOpenOrders": self.reqAllOpenOrders,
                    "reqManagedAccts": self.reqManagedAccts,
                    "requestFA": self.requestFA,
                    "replaceFA": self.replaceFA,
                    "reqFundamentalData": self.reqFundamentalData,
                    "cancelFundamentalData": self.cancelFundamentalData,
                    "calculateImpliedVolatility": self.calculateImpliedVolatility,
                    "cancelCalculateImpliedVolatility": self.cancelCalculateImpliedVolatility,
                    "calculateOptionPrice": self.calculateOptionPrice,
                    "cancelCalculateOptionPrice": self.cancelCalculateOptionPrice,
                    "reqGlobalCancel": self.reqGlobalCancel,
                    "reqMarketDataType": self.reqMarketDataType,
                    "reqPositions": self.reqPositions,
                    "cancelPositions": self.cancelPositions,
                    "reqAccountSummary": self.reqAccountSummary,
                    "cancelAccountSummary": self.cancelAccountSummary,
                    "queryDisplayGroups": self.queryDisplayGroups,
                    "subscribeToGroupEvents": self.subscribeToGroupEvents,
                    "updateDisplayGroup": self.updateDisplayGroup,
                    "unsubscribeFromGroupEvents": self.unsubscribeFromGroupEvents,
                    }
        
        return funcMap
    
    def runCommand(self, **kwargs):
        """
        takes in the commands from the run command function and then calls the appropriate command
        """
        
        cmd = kwargs["cmd"]
        self.funcMap[cmd](**kwargs)
        
        
    def subscribeStock(self, **kwargs):
        
        symbol = kwargs["symbol"]
        contract = Contract()
        contract.m_symbol = symbol
        contract.m_exchange = "SMART"
        contract.m_currency = "USD"
        contract.m_secType = "STK"

        self.subscriptions[symbol] = self.subscriptionCounter
        self.tickerMap[self.subscriptionCounter] = symbol
        self.client.reqMktData(self.subscriptionCounter, contract, "", False, [])
        self.subscriptionCounter+=1

    def subscribeFX(self, **kwargs):
        """
        base = base of the currency pair
        priceCur = currency for pricing
        
        ex. USD, JPY means buy/sell USD with price of JPY
        """
        
        base = kwargs["base"]
        priceCur = kwargs["priceCur"]
        
        contract = Contract()
        contract.m_symbol = base
        contract.m_exchange = "IDEALPRO"
        contract.m_currency = priceCur
        contract.m_secType = "CASH"
        
        symbol = ".".join([base, priceCur])

        self.subscriptions[symbol] = self.subscriptionCounter
        self.tickerMap[self.subscriptionCounter] = symbol
        self.client.reqMktData(self.subscriptionCounter, contract, "", False, [])
        self.subscriptionCounter+=1        
    
    def unsubscribeStock(self, **kwargs):
        
        symbol = kwargs["symbol"]
        
        if symbol in self.subscription:
            self.client.cancelMktData(self.subscriptions[symbol])
            self.tickerMap.pop(self.subscriptions.pop(symbol))
        
    def unsubscribeFX(self, **kwargs):
        
        base = kwargs["base"]
        priceCur = kwargs["priceCur"]
        symbol = ".".join([base, priceCur])
        
        if symbol in self.subscription:
            self.client.cancelMktData(self.subscriptions[symbol])
            self.tickerMap.pop(self.subscriptions.pop(symbol))
        
        
        
    ###Helper functions
    def _createContract(self, **kwargs):
        
        contract = Contract()
        if "contract_conId" in kwargs: contract.m_conId = kwargs["contract_conId"]
        if "contract_symbol" in kwargs: contract.m_symbol = kwargs["contract_symbol"]
        if "contract_secType" in kwargs: contract.m_secType = kwargs["contract_secType"]
        if "contract_expiry" in kwargs: contract.m_expiry = kwargs["contract_expiry"]
        if "contract_strike" in kwargs: contract.m_strike = kwargs["contract_strike"]
        if "contract_right" in kwargs: contract.m_right = kwargs["contract_right"]
        if "contract_multiplier" in kwargs: contract.m_multiplier = kwargs["contract_multiplier"]
        if "contract_exchange" in kwargs: contract.m_exchange = kwargs["contract_exchange"]

        if "contract_currency" in kwargs: contract.m_currency = kwargs["contract_currency"]
        if "contract_localSymbol" in kwargs: contract.m_localSymbol = kwargs["contract_localSymbol"]
        if "contract_tradingClass" in kwargs: contract.m_tradingClass = kwargs["contract_tradingClass"]
        if "contract_primaryExch" in kwargs: contract.m_primaryExch = kwargs["contract_primaryExch"]      # pick a non-aggregate (ie not the SMART exchange) exchange that the contract trades on.  DO NOT SET TO SMART.
        if "contract_includeExpired" in kwargs: contract.m_includeExpired = kwargs["contract_includeExpired"]  # can not be set to true for contracts.

        if "contract_secIdType" in kwargs: contract.m_secIdType = kwargs["contract_secIdType"]        # CUSIP;SEDOL;ISIN;RIC
        if "contract_secId" in kwargs: contract.m_secId = kwargs["contract_secId"]
        
        return contract
    
    def _createOrder(self, **kwargs):
        
        order = Order()
        
        # main order fields
        if "order_orderId" in kwargs: order.m_orderId = kwargs["order_orderId"]
        order.m_clientId = self.id
        if "order_permId" in kwargs: order.m_permId = kwargs["order_permId"]
        if "order_action" in kwargs: order.m_action = kwargs["order_action"] #values are BUY, SELL, SSHORT
        if "order_totalQuantity" in kwargs: order.m_totalQuantity = kwargs["order_totalQuantity"]
        if "order_orderType" in kwargs: order.m_orderType = kwargs["order_orderType"]
        if "order_lmtPrice" in kwargs: order.m_lmtPrice = kwargs["order_lmtPrice"]
        if "order_auxPrice" in kwargs: order.m_auxPrice = kwargs["order_auxPrice"]

        # extended order fields
        if "order_tif" in kwargs: order.m_tif = kwargs["order_tif"]  # "Time in Force" - DAY, GTC, etc.
        if "order_activeStartTime" in kwargs: order.m_activeStartTime = kwargs["order_activeStartTime"] # GTC orders
        if "order_activeStopTime" in kwargs: order.m_activeStopTime = kwargs["order_activeStopTime"] # GTC orders YYYYMMDD hh:mm:ss (optional time zone)
        if "order_ocaGroup" in kwargs: order.m_ocaGroup = kwargs["order_ocaGroup"] # one cancels all group name
        if "order_ocaType" in kwargs: order.m_ocaType = kwargs["order_ocaType"]  # 1 = CANCEL_WITH_BLOCK, 2 = REDUCE_WITH_BLOCK, 3 = REDUCE_NON_BLOCK
        if "order_orderRef" in kwargs: order.m_orderRef = kwargs["order_orderRef"]
        if "order_transmit" in kwargs: order.m_transmit = kwargs["order_transmit"]    # if false, order will be created but not transmited
        if "order_parentId" in kwargs: order.m_parentId = kwargs["order_parentId"]    # Parent order Id, to associate Auto STP or TRAIL orders with the original order.
        if "order_blockOrder" in kwargs: order.m_blockOrder = kwargs["order_blockOrder"]
        if "order_sweepToFill" in kwargs: order.m_sweepToFill = kwargs["order_sweepToFill"]
        if "order_displaySize" in kwargs: order.m_displaySize = kwargs["order_displaySize"]
        if "order_triggerMethod" in kwargs: order.m_triggerMethod = kwargs["order_triggerMethod"] # 0=Default, 1=Double_Bid_Ask, 2=Last, 3=Double_Last, 4=Bid_Ask, 7=Last_or_Bid_Ask, 8=Mid-point
        if "order_outsideRth" in kwargs: order.m_outsideRth = kwargs["order_outsideRth"]
        if "order_hidden" in kwargs: order.m_hidden = kwargs["order_hidden"]
        if "order_goodAfterTime" in kwargs: order.m_goodAfterTime = kwargs["order_goodAfterTime"] # FORMAT: 20060505 08:00:00 {time zone}
        if "order_goodTillDate" in kwargs: order.m_goodTillDate = kwargs["order_goodTillDate"]  # FORMAT: 20060505 08:00:00 {time zone} order must be GTD
        if "order_overridePercentageConstraints" in kwargs: order.m_overridePercentageConstraints = kwargs["order_overridePercentageConstraints"]
        if "order_rule80A" in kwargs: order.m_rule80A = kwargs["order_rule80A"]  # Individual = 'I', Agency = 'A', AgentOtherMember = 'W', IndividualPTIA = 'J', AgencyPTIA = 'U', AgentOtherMemberPTIA = 'M', IndividualPT = 'K', AgencyPT = 'Y', AgentOtherMemberPT = 'N'
        if "order_allOrNone" in kwargs: order.m_allOrNone = kwargs["order_allOrNone"]
        if "order_minQty" in kwargs: order.m_minQty = kwargs["order_minQty"]
        if "order_percentOffset" in kwargs: order.m_percentOffset = kwargs["order_percentOffset"]    # REL orders only specify the decimal, e.g. .04 not 4
        if "order_trailStopPrice" in kwargs: order.m_trailStopPrice = kwargs["order_trailStopPrice"]   # for TRAILLIMIT orders only
        if "order_trailingPercent" in kwargs: order.m_trailingPercent = kwargs["order_trailingPercent"]  # specify the percentage, e.g. 3, not .03

        # Financial advisors only
        if "order_faGroup" in kwargs: order.m_faGroup = kwargs["order_faGroup"]
        if "order_faProfile" in kwargs: order.m_faProfile = kwargs["order_faProfile"]
        if "order_faMethod" in kwargs: order.m_faMethod = kwargs["order_faMethod"]
        if "order_faPercentage" in kwargs: order.m_faPercentage = kwargs["order_faPercentage"]

        # Institutional orders only
        if "order_openClose" in kwargs: order.m_openClose = kwargs["order_openClose"]          # O=Open, C=Close
        if "order_origin" in kwargs: order.m_origin = kwargs["order_origin"]             # 0=Customer, 1=Firm
        if "order_shortSaleSlot" in kwargs: order.m_shortSaleSlot = kwargs["order_shortSaleSlot"]      # 1 if you hold the shares, 2 if they will be delivered from elsewhere.  Only for Action="SSHORT
        if "order_designatedLocation" in kwargs: order.m_designatedLocation = kwargs["order_designatedLocation"] # set when slot=2 only.
        if "order_exemptCode" in kwargs: order.m_exemptCode = kwargs["order_exemptCode"]

        # SMART routing only
        if "order_discretionaryAmt" in kwargs: order.m_discretionaryAmt = kwargs["order_discretionaryAmt"]
        if "order_eTradeOnly" in kwargs: order.m_eTradeOnly = kwargs["order_eTradeOnly"]
        if "order_firmQuoteOnly" in kwargs: order.m_firmQuoteOnly = kwargs["order_firmQuoteOnly"]
        if "order_nbboPriceCap" in kwargs: order.m_nbboPriceCap = kwargs["order_nbboPriceCap"]
        if "order_optOutSmartRouting" in kwargs: order.m_optOutSmartRouting = kwargs["order_optOutSmartRouting"]

        # BOX or VOL ORDERS ONLY
        if "order_auctionStrategy" in kwargs: order.m_auctionStrategy = kwargs["order_auctionStrategy"] # 1=AUCTION_MATCH, 2=AUCTION_IMPROVEMENT, 3=AUCTION_TRANSPARENT

        # BOX ORDERS ONLY
        if "order_startingPrice" in kwargs: order.m_startingPrice = kwargs["order_startingPrice"]
        if "order_stockRefPrice" in kwargs: order.m_stockRefPrice = kwargs["order_stockRefPrice"]
        if "order_delta" in kwargs: order.m_delta = kwargs["order_delta"]

        # pegged to stock or VOL orders
        if "order_stockRangeLower" in kwargs: order.m_stockRangeLower = kwargs["order_stockRangeLower"]
        if "order_stockRangeUpper" in kwargs: order.m_stockRangeUpper = kwargs["order_stockRangeUpper"]

        # VOLATILITY ORDERS ONLY
        if "order_volatility" in kwargs: order.m_volatility = kwargs["order_volatility"]  # enter percentage not decimal, e.g. 2 not .02
        if "order_volatilityType" in kwargs: order.m_volatilityType = kwargs["order_volatilityType"]     # 1=daily, 2=annual
        if "order_continuousUpdate" in kwargs: order.m_continuousUpdate = kwargs["order_continuousUpdate"]
        if "order_referencePriceType" in kwargs: order.m_referencePriceType = kwargs["order_referencePriceType"] # 1=Bid/Ask midpoint, 2 = BidOrAsk
        if "order_deltaNeutralOrderType" in kwargs: order.m_deltaNeutralOrderType = kwargs["order_deltaNeutralOrderType"]
        if "order_deltaNeutralAuxPrice" in kwargs: order.m_deltaNeutralAuxPrice = kwargs["order_deltaNeutralAuxPrice"]
        if "order_deltaNeutralConId" in kwargs: order.m_deltaNeutralConId = kwargs["order_deltaNeutralConId"]
        if "order_deltaNeutralSettlingFirm" in kwargs: order.m_deltaNeutralSettlingFirm = kwargs["order_deltaNeutralSettlingFirm"]
        if "order_deltaNeutralClearingAccount" in kwargs: order.m_deltaNeutralClearingAccount = kwargs["order_deltaNeutralClearingAccount"]
        if "order_deltaNeutralClearingIntent" in kwargs: order.m_deltaNeutralClearingIntent = kwargs["order_deltaNeutralClearingIntent"]
        if "order_deltaNeutralOpenClose" in kwargs: order.m_deltaNeutralOpenClose = kwargs["order_deltaNeutralOpenClose"]
        if "order_deltaNeutralShortSale" in kwargs: order.m_deltaNeutralShortSale = kwargs["order_deltaNeutralShortSale"]
        if "order_deltaNeutralShortSaleSlot" in kwargs: order.m_deltaNeutralShortSaleSlot = kwargs["order_deltaNeutralShortSaleSlot"]
        if "order_deltaNeutralDesignatedLocation" in kwargs: order.m_deltaNeutralDesignatedLocation = kwargs["order_deltaNeutralDesignatedLocation"]

        # COMBO ORDERS ONLY
        if "order_basisPoints" in kwargs: order.m_basisPoints = kwargs["order_basisPoints"]      # EFP orders only, download only
        if "order_basisPointsType" in kwargs: order.m_basisPointsType = kwargs["order_basisPointsType"]  # EFP orders only, download only

        # SCALE ORDERS ONLY
        if "order_scaleInitLevelSize" in kwargs: order.m_scaleInitLevelSize = kwargs["order_scaleInitLevelSize"]
        if "order_scaleSubsLevelSize" in kwargs: order.m_scaleSubsLevelSize = kwargs["order_scaleSubsLevelSize"]
        if "order_scalePriceIncrement" in kwargs: order.m_scalePriceIncrement = kwargs["order_scalePriceIncrement"]
        if "order_scalePriceAdjustValue" in kwargs: order.m_scalePriceAdjustValue = kwargs["order_scalePriceAdjustValue"]
        if "order_scalePriceAdjustInterval" in kwargs: order.m_scalePriceAdjustInterval = kwargs["order_scalePriceAdjustInterval"]
        if "order_scaleProfitOffset" in kwargs: order.m_scaleProfitOffset = kwargs["order_scaleProfitOffset"]
        if "order_scaleAutoReset" in kwargs: order.m_scaleAutoReset = kwargs["order_scaleAutoReset"]
        if "order_scaleInitPosition" in kwargs: order.m_scaleInitPosition = kwargs["order_scaleInitPosition"]
        if "order_scaleInitFillQty" in kwargs: order.m_scaleInitFillQty = kwargs["order_scaleInitFillQty"]
        if "order_scaleRandomPercent" in kwargs: order.m_scaleRandomPercent = kwargs["order_scaleRandomPercent"]
        if "order_scaleTable" in kwargs: order.m_scaleTable = kwargs["order_scaleTable"]

        # HEDGE ORDERS ONLY
        if "order_hedgeType" in kwargs: order.m_hedgeType = kwargs["order_hedgeType"] # 'D' - delta, 'B' - beta, 'F' - FX, 'P' - pair
        if "order_hedgeParam" in kwargs: order.m_hedgeParam = kwargs["order_hedgeParam"] # beta value for beta hedge (in range 0-1), ratio for pair hedge

        # Clearing info
        if "order_account" in kwargs: order.m_account = kwargs["order_account"] # IB account
        if "order_settlingFirm" in kwargs: order.m_settlingFirm = kwargs["order_settlingFirm"]
        if "order_clearingAccount" in kwargs: order.m_clearingAccount = kwargs["order_clearingAccount"] # True beneficiary of the order
        if "order_clearingIntent" in kwargs: order.m_clearingIntent = kwargs["order_clearingIntent"] # "" (Default), "IB", "Away", "PTA" (PostTrade)

        # ALGO ORDERS ONLY
        if "order_algoStrategy" in kwargs: order.m_algoStrategy = kwargs["order_algoStrategy"]
        if "order_algoParams" in kwargs: order.m_algoParams = kwargs["order_algoParams"]

        # What-if
        if "order_whatIf" in kwargs: order.m_whatIf = kwargs["order_whatIf"]

        # Not Held
        if "order_notHeld" in kwargs: order.m_notHeld = kwargs["order_notHeld"]

        # Smart combo routing params
        if "order_smartComboRoutingParams" in kwargs: order.m_smartComboRoutingParams = kwargs["order_smartComboRoutingParams"]

        # order combo legs
        #if "order_orderComboLegs" in kwargs: order.m_orderComboLegs = kwargs["order_orderComboLegs"] = new Vector<OrderComboLeg>()

        # order misc options
        if "order_orderMiscOptions" in kwargs: order.m_orderMiscOptions = kwargs["order_orderMiscOptions"]

        return order

    def connected(self, **kwargs):
        return self.client.connected

    def reqCurrentTime(self, **kwargs):
        return self.client.reqCurrentTime()    
   
    def faMsgTypeName(self, **kwargs):
        return self.client.faMsgTypeName(int)

    def serverVersion(self, **kwargs):
        return self.client.serverVersion()

    def TwsConnectionTime(self, **kwargs):
        return self.client.TwsConnectionTime()

    def wrapper(self, **kwargs):
        return self.client.wrapper()

    def reader(self, **kwargs):
        return self.client.reader()

    def isConnected(self, **kwargs):
        return self.client.isConnected()
            
    def eConnect(self, **kwargs):
        
        host = kwargs["host"]
        port = kwargs["port"]
        id = kwargs["id"]
        self.client.eConnect(host, port, id)
                            
    
#     def EClientSocket(self, **kwargs):
#         self.client.EClientSocket(AnyWrapper)
#   
# 
#     def eConnect(self, **kwargs):
#         self.client.eConnect(String, int, int, boolean)
# 
#     def createReader(self, **kwargs):
#         self.client.createReader(EClientSocket, DataInputStream)
# 
#     def eConnect(self, **kwargs):
#         self.client.eConnect(Socket, int)
# 
#     def eConnect(self, **kwargs):
#         self.client.eConnect(Socket)
# 
    def eDisconnect(self, **kwargs):
        self.client.eDisconnect()

###client functions for call backs

#Not using scanners at the moment
#     def cancelScannerSubscription(self, **kwargs):
#         subscriptionId = kwargs["id"]
#         self.client.cancelScannerSubscription(int)
# 
#     def reqScannerParameters(self, **kwargs):
#         self.client.reqScannerParameters()
# 
#     def reqScannerSubscription(self, **kwargs):
#         self.client.reqScannerSubscription(int, ScannerSubscription, Vector<TagValue>)

    def reqMktData(self, **kwargs):
        """
        function to request market data
        """
        #contract information:
        
        requestId = kwargs["tickerId"]
        contract = self._createContract(**kwargs)
         
        tickList = kwargs.get("tickList", "")
        snapshot = kwargs.get("snapshot", False)
        
        self.client.reqMktData(requestId, contract, tickList, snapshot, [])

    def cancelHistoricalData(self, **kwargs):
        requestId = kwargs["tickerId"]
        self.client.cancelHistoricalData(requestId)

    def cancelRealTimeBars(self, **kwargs):
        requestId = kwargs["tickerId"]
        self.client.cancelRealTimeBars(requestId)

    def reqHistoricalData(self, **kwargs):
        requestId = kwargs["tickerId"]
        contract = self._createContratct()
        endDateTime = kwargs["endDateTime"] #format of yyyymmdd HH:mm:ss ttt
        durationStr = kwargs["durationStr"] #can look like 1000 S (int [S D W])
        barSizeSetting = kwargs["barSizeSetting"] #valid values are: 1 sec|5 secs|15 secs|30 secs|1 min|2 mins|3 mins|5 mins|15 mins|30 mins|1 hour|1 day
        whatToShow = kwargs["whatToShow"] #valid values are: TRADES|MIDPOINT|BID|ASK|BID_ASK|HISTORICAL_VOLATILITY|OPTION_IMPLIED_VOLATILITY
        useRTH = bool(kwargs["useRTH"]) #0 for all data, 1 for market hours only
        formatDate = kwargs["formatDate"] #1 for yyyymmdd{space}{space}hh:mm:dd, 2 for timestamp value
        self.client.reqHistoricalData(requestId, contract, endDateTime, durationStr, barSizeSetting, whatToShow, useRTH, formatDate, [])

    def reqRealTimeBars(self, **kwargs):
        requestId = kwargs["tickerId"]
        contract = self._createContratct()
        barSize = 5 
        whatToShow = kwargs["whatToShow"] #valid values are: TRADES|MIDPOINT|BID|ASK|BID_ASK|HISTORICAL_VOLATILITY|OPTION_IMPLIED_VOLATILITY
        useRTH = bool(kwargs["useRTH"]) #0 for all data, 1 for market hours only
        self.client.reqRealTimeBars(requestId, contract, barSize, whatToShow, useRTH, [])

    def reqContractDetails(self, **kwargs):
        
        requestId = kwargs["reqId"]
        contract = self._createContract(**kwargs)
        
        self.client.reqContractDetails(requestId, contract)

    def reqMktDepth(self, **kwargs):
        
        requestId = kwargs["tickerId"]
        contract = self._createContract(**kwargs)
        
        depthRows = kwargs.get("depthRows", 1)
        
        self.client.reqMktDepth(requestId, contract, depthRows, [])

    def cancelMktData(self, **kwargs):
        """
        cancels the market data request
        """
        
        requestId = kwargs["tickerId"]
        self.client.cancelMktData(requestId)

    def cancelMktDepth(self, **kwargs):
        requestId = kwargs["tickerId"]
        self.client.cancelMktDepth(requestId)

    def exerciseOptions(self, **kwargs):
        
        requestId = kwargs["tickerId"]
        contract = self._createContract(**kwargs)
        exerciseAction = kwargs["exercise_action"]
        exerciseQty = kwargs["exercise_qty"]
        account = ""
        override = 0
        #wonder what exchange this should be though
        if contract.m_exchange == "SMART":
            raise("Exchange cannot be smart")
        self.client.exerciseOptions(requestId, contract, exerciseAction, exerciseQty, account, override)

    def placeOrder(self, **kwargs):
        requestId = kwargs["id"]
        contract = self._createContract(**kwargs)
        order = self._createOrder(**kwargs)
        
        self.client.placeOrder(requestId, contract, order)

    def reqAccountUpdates(self, **kwargs):
        
        subscribe = bool(kwargs["subscribe"])
        acctCode = kwargs["acctCode"]
        self.client.reqAccountUpdates(subscribe, acctCode)

    def reqExecutions(self, **kwargs):
        
        requestId = kwargs["reqId"]
        executionFilter = ExecutionFilter()
        self.client.reqExecutions(requestId, executionFilter)

    def cancelOrder(self, **kwargs):
        requestId = kwargs["reqId"] 
        self.client.cancelOrder(requestId)

    def reqOpenOrders(self, **kwargs):
        self.client.reqOpenOrders()

    def reqIds(self, **kwargs):
        numIds = kwargs["numIds"]
        self.client.reqIds(numIds)

    def reqNewsBulletins(self, **kwargs):
        news = kwargs["news"]
        self.client.reqNewsBulletins(news)

    def cancelNewsBulletins(self, **kwargs):
        self.client.cancelNewsBulletins()

    def setServerLogLevel(self, **kwargs):
#     1 = SYSTEM
#     2 = ERROR
#     3 = WARNING
#     4 = INFORMATION
#     5 = DETAIL

        logLevel = kwargs["logLevel"]
        self.client.setServerLogLevel(logLevel)

    def reqAutoOpenOrders(self, **kwargs):
        #If set to TRUE, newly created TWS orders will be implicitly associated with the client. If set to FALSE, no association will be made.
        bAutoBind = kwargs["bAutoBind"]
        self.client.reqAutoOpenOrders(bAutoBind)

    def reqAllOpenOrders(self, **kwargs):
        self.client.reqAllOpenOrders()

    def reqManagedAccts(self, **kwargs):
        self.client.reqManagedAccts()

    def requestFA(self, **kwargs):
        
#     1 = GROUPS
#     2 = PROFILE
#     3 = ACCOUNT ALIASES
        faDataType = kwargs["faDataType"]
        self.client.requestFA(faDataType)

    def replaceFA(self, **kwargs):
        #Call this function to modify FA configuration information from the API. Note that this can also be done manually in TWS itself.
        faDataType = kwargs["faDataType"]
        cxml = kwargs["cxml"]
        self.client.replaceFA(faDataType, cxml)

    def reqFundamentalData(self, **kwargs):


#    report types
#     ReportSnapshot (company overview)
#     ReportsFinSummary (financial summary)
#     ReportRatios (financial ratios)
#     ReportsFinStatements (financial statements)
#     RESC (analyst estimates)
#     CalendarReport (company calendar)

        requestId = kwargs["reqId"]
        contract = self._createContract(**kwargs)
        reportType =kwargs["reportType"]  
        self.client.reqFundamentalData(requestId, contract, reportType)

    def cancelFundamentalData(self, **kwargs):
        requestId = kwargs["reqId"]
        self.client.cancelFundamentalData(requestId)

    def calculateImpliedVolatility(self, **kwargs):
        requestId = kwargs["reqId"]
        contract = self._createContract(**kwargs)
        optionPrice = kwargs["optionPrice"]
        underPrice = kwargs["underPrice"]
        
        self.client.calculateImpliedVolatility(requestId, contract, optionPrice, underPrice)

    def cancelCalculateImpliedVolatility(self, **kwargs):
        requestId = kwargs["reqId"]
        self.client.cancelCalculateImpliedVolatility(requestId)

    def calculateOptionPrice(self, **kwargs):
        requestId = kwargs["requestId"]
        contract = self._createContract(**kwargs)
        volatility = kwargs["volatility"]
        underPrice = kwargs["underPrice"]
        
        self.client.calculateOptionPrice(requestId, contract, volatility, underPrice)

    def cancelCalculateOptionPrice(self, **kwargs):
        requestId = kwargs["reqId"]
        self.client.cancelCalculateOptionPrice(requestId)

    def reqGlobalCancel(self, **kwargs):
        self.client.reqGlobalCancel()

    def reqMarketDataType(self, **kwargs):
        #1 for real-time streaming market data or 2 for frozen market data.
        marketDataType = kwargs["marketDataType"]
        self.client.reqMarketDataType(marketDataType)

    def reqPositions(self, **kwargs):
        self.client.reqPositions()

    def cancelPositions(self, **kwargs):
        self.client.cancelPositions()

    def reqAccountSummary(self, **kwargs):
        #This request can only be made when connected to a Financial Advisor (FA) account.
        requestId = kwargs["reqId"]
        group = kwargs["group"]
        tags = kwargs["tags"]
        self.client.reqAccountSummary(requestId, group, tags)

    def cancelAccountSummary(self, **kwargs):
        requestId = kwargs["reqId"]
        self.client.cancelAccountSummary(requestId)

#     def verifyRequest(self, **kwargs):
#         self.client.verifyRequest(String, String)
# 
#     def verifyMessage(self, **kwargs):
#         self.client.verifyMessage(String)

    def queryDisplayGroups(self, **kwargs):
        requestId = kwargs["reqId"]
        self.client.queryDisplayGroups(requestId)

    def subscribeToGroupEvents(self, **kwargs):
        #groupId =      The ID of the group, currently it is a number from 1 to 7. This is the display group subscription request sent by the API to TWS. 
        requestId = kwargs["reqId"]
        groupId = kwargs["groupId"]
        self.client.subscribeToGroupEvents(requestId, groupId)

    def updateDisplayGroup(self, **kwargs):
#     contractInfo:
#     none = empty selection
#     contractID@exchange – any non-combination contract. Examples: 8314@SMART for IBM SMART; 8314@ARCA for IBM @ARCA.
#     combo = if any combo is selected.
        requestId = kwargs["reqId"]
        contractInfo = kwargs["contractInfo"]
        self.client.updateDisplayGroup(requestId, contractInfo)

    def unsubscribeFromGroupEvents(self, **kwargs):
        requestId = kwargs["reqId"]
        self.client.unsubscribeFromGroupEvents(requestId)    
    
    def getData(self):
        """
        called to get information out of the queue in the wrapper for information passing
        """
        data = self.wrapper.queue.get()
        
        #this is specialized code to deal with mapping of ids to symbol information
        #work to create something more natural that is layer or at a different level?
        data["tickerId"] = self.tickerMap[data["tickerId"]]
        return data
        
class Server:
    
    def __init__(self, port  = 12000):
    
        self.activeClients = {}
        self.acceptQueue = Queue.Queue()
        self.serverSocket = sockLib.serverSocket(port)
        
        print "starting client manager"
        self.clientManager = ClientManager()
        
        print "creating connection"
        self.acceptThread = threading.Thread(target = self.acceptConnection)
        self.acceptThread.start()
        
        print "subscribing"
        self.clientManager.subscribeFX("USD", "JPY")
        
        self.transmitData()

    def acceptConnection(self):
        
        while True:
            sock, address = self.serverSocket.accept()
            print "adding connection"
            self.activeClients[sock] = sockLib.JsonProtocol(sock)
    
    def transmitData(self):
        
        while True:
            print "getting data"
            data = self.clientManager.getData()
            badSocks = []
            for sock, protocol in self.activeClients.items():
                try:
                    protocol.sendData(data)
                except:
                    badSocks.append(sock)

                    
            while badSocks: #remove bad sockets
                self.activeClients.pop(badSocks.pop())


if __name__ == "__main__":
    
    #clientManager = ClientManager()
#     clientManager.subscribeStock("AAPL")
#     clientManager.subscribeStock("AMZN")
#     clientManager.subscribeStock("YHOO")
#     clientManager.subscribeStock("GOOG")
#     clientManager.subscribeStock("SNE")
    #clientManager.subscribeFX("USD", "JPY")
    
    server = Server()
    
    
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
    