'''
Created on Dec 28, 2014

@author: justin

a helper library to flatten the java structs to allow data to be passed through
'''


def flattenContract(contract, msg):
    
    msg["contract_conId"] = contract.m_conId
    msg["contract_symbol"] = contract.m_symbol
    msg["contract_secType"] = contract.m_secType
    msg["contract_expiry"] = contract.m_expiry
    msg["contract_strike"] = contract.m_strike
    msg["contract_right"] = contract.m_right
    msg["contract_multiplier"] = contract.m_multiplier
    msg["contract_exchange"] = contract.m_exchange

    msg["contract_currency"] = contract.m_currency
    msg["contract_localSymbol"] = contract.m_localSymbol
    msg["contract_tradingClass"] = contract.m_tradingClass
    msg["contract_primaryExch"] = contract.m_primaryExch      # pick a non-aggregate (ie not the SMART exchange) exchange that the contract trades on.  DO NOT SET TO SMART.
    msg["contract_includeExpired"] = contract.m_includeExpired  # can not be set to true for orders.

    msg["contract_secIdType"] = contract.m_secIdType        # CUSIP;SEDOL;ISIN;RIC
    msg["contract_secId"] = contract.m_secId

    # COMBOS
    msg["contract_comboLegsDescrip"] = contract.m_comboLegsDescrip # received in open order version 14 and up for all combos
    #public Vector<ComboLeg> m_comboLegs = new Vector<ComboLeg>();

    # delta neutral
    msg["contract_underComp"] = contract.m_underComp
    
    return msg

def flattenOrder(order, msg):
    # main order fields
    msg["order_orderId"] = order.m_orderId
    msg["order_clientId"] = order.m_clientId
    msg["order_permId"] = order.m_permId
    msg["order_action"] = order.m_action
    msg["order_totalQuantity"] = order.m_totalQuantity
    msg["order_orderType"] = order.m_orderType
    msg["order_lmtPrice"] = order.m_lmtPrice
    msg["order_auxPrice"] = order.m_auxPrice

    # extended order fields
    msg["order_tif"] = order.m_tif  # "Time in Force" - DAY, GTC, etc.
    msg["order_activeStartTime"] = order.m_activeStartTime # GTC orders
    msg["order_activeStopTime"] = order.m_activeStopTime # GTC orders
    msg["order_ocaGroup"] = order.m_ocaGroup # one cancels all group name
    msg["order_ocaType"] = order.m_ocaType  # 1 = CANCEL_WITH_BLOCK, 2 = REDUCE_WITH_BLOCK, 3 = REDUCE_NON_BLOCK
    msg["order_orderRef"] = order.m_orderRef
    msg["order_transmit"] = order.m_transmit    # if false, order will be created but not transmited
    msg["order_parentId"] = order.m_parentId    # Parent order Id, to associate Auto STP or TRAIL orders with the original order.
    msg["order_blockOrder"] = order.m_blockOrder
    msg["order_sweepToFill"] = order.m_sweepToFill
    msg["order_displaySize"] = order.m_displaySize
    msg["order_triggerMethod"] = order.m_triggerMethod # 0=Default, 1=Double_Bid_Ask, 2=Last, 3=Double_Last, 4=Bid_Ask, 7=Last_or_Bid_Ask, 8=Mid-point
    msg["order_outsideRth"] = order.m_outsideRth
    msg["order_hidden"] = order.m_hidden
    msg["order_goodAfterTime"] = order.m_goodAfterTime # FORMAT: 20060505 08:00:00 {time zone}
    msg["order_goodTillDate"] = order.m_goodTillDate  # FORMAT: 20060505 08:00:00 {time zone}
    msg["order_overridePercentageConstraints"] = order.m_overridePercentageConstraints
    msg["order_rule80A"] = order.m_rule80A  # Individual = 'I', Agency = 'A', AgentOtherMember = 'W', IndividualPTIA = 'J', AgencyPTIA = 'U', AgentOtherMemberPTIA = 'M', IndividualPT = 'K', AgencyPT = 'Y', AgentOtherMemberPT = 'N'
    msg["order_allOrNone"] = order.m_allOrNone
    msg["order_minQty"] = order.m_minQty
    msg["order_percentOffset"] = order.m_percentOffset    # REL orders only; specify the decimal, e.g. .04 not 4
    msg["order_trailStopPrice"] = order.m_trailStopPrice   # for TRAILLIMIT orders only
    msg["order_trailingPercent"] = order.m_trailingPercent  # specify the percentage, e.g. 3, not .03

    # Financial advisors only
    msg["order_faGroup"] = order.m_faGroup
    msg["order_faProfile"] = order.m_faProfile
    msg["order_faMethod"] = order.m_faMethod
    msg["order_faPercentage"] = order.m_faPercentage

    # Institutional orders only
    msg["order_openClose"] = order.m_openClose          # O=Open, C=Close
    msg["order_origin"] = order.m_origin             # 0=Customer, 1=Firm
    msg["order_shortSaleSlot"] = order.m_shortSaleSlot      # 1 if you hold the shares, 2 if they will be delivered from elsewhere.  Only for Action="SSHORT
    msg["order_designatedLocation"] = order.m_designatedLocation # set when slot=2 only.
    msg["order_exemptCode"] = order.m_exemptCode

    # SMART routing only
    msg["order_discretionaryAmt"] = order.m_discretionaryAmt
    msg["order_eTradeOnly"] = order.m_eTradeOnly
    msg["order_firmQuoteOnly"] = order.m_firmQuoteOnly
    msg["order_nbboPriceCap"] = order.m_nbboPriceCap
    msg["order_optOutSmartRouting"] = order.m_optOutSmartRouting

    # BOX or VOL ORDERS ONLY
    msg["order_auctionStrategy"] = order.m_auctionStrategy # 1=AUCTION_MATCH, 2=AUCTION_IMPROVEMENT, 3=AUCTION_TRANSPARENT

    # BOX ORDERS ONLY
    msg["order_startingPrice"] = order.m_startingPrice
    msg["order_stockRefPrice"] = order.m_stockRefPrice
    msg["order_delta"] = order.m_delta

    # pegged to stock or VOL orders
    msg["order_stockRangeLower"] = order.m_stockRangeLower
    msg["order_stockRangeUpper"] = order.m_stockRangeUpper

    # VOLATILITY ORDERS ONLY
    msg["order_volatility"] = order.m_volatility  # enter percentage not decimal, e.g. 2 not .02
    msg["order_volatilityType"] = order.m_volatilityType     # 1=daily, 2=annual
    msg["order_continuousUpdate"] = order.m_continuousUpdate
    msg["order_referencePriceType"] = order.m_referencePriceType # 1=Bid/Ask midpoint, 2 = BidOrAsk
    msg["order_deltaNeutralOrderType"] = order.m_deltaNeutralOrderType
    msg["order_deltaNeutralAuxPrice"] = order.m_deltaNeutralAuxPrice
    msg["order_deltaNeutralConId"] = order.m_deltaNeutralConId
    msg["order_deltaNeutralSettlingFirm"] = order.m_deltaNeutralSettlingFirm
    msg["order_deltaNeutralClearingAccount"] = order.m_deltaNeutralClearingAccount
    msg["order_deltaNeutralClearingIntent"] = order.m_deltaNeutralClearingIntent
    msg["order_deltaNeutralOpenClose"] = order.m_deltaNeutralOpenClose
    msg["order_deltaNeutralShortSale"] = order.m_deltaNeutralShortSale
    msg["order_deltaNeutralShortSaleSlot"] = order.m_deltaNeutralShortSaleSlot
    msg["order_deltaNeutralDesignatedLocation"] = order.m_deltaNeutralDesignatedLocation

    # COMBO ORDERS ONLY
    msg["order_basisPoints"] = order.m_basisPoints      # EFP orders only, download only
    msg["order_basisPointsType"] = order.m_basisPointsType  # EFP orders only, download only

    # SCALE ORDERS ONLY
    msg["order_scaleInitLevelSize"] = order.m_scaleInitLevelSize
    msg["order_scaleSubsLevelSize"] = order.m_scaleSubsLevelSize
    msg["order_scalePriceIncrement"] = order.m_scalePriceIncrement
    msg["order_scalePriceAdjustValue"] = order.m_scalePriceAdjustValue
    msg["order_scalePriceAdjustInterval"] = order.m_scalePriceAdjustInterval
    msg["order_scaleProfitOffset"] = order.m_scaleProfitOffset
    msg["order_scaleAutoReset"] = order.m_scaleAutoReset
    msg["order_scaleInitPosition"] = order.m_scaleInitPosition
    msg["order_scaleInitFillQty"] = order.m_scaleInitFillQty
    msg["order_scaleRandomPercent"] = order.m_scaleRandomPercent
    msg["order_scaleTable"] = order.m_scaleTable

    # HEDGE ORDERS ONLY
    msg["order_hedgeType"] = order.m_hedgeType # 'D' - delta, 'B' - beta, 'F' - FX, 'P' - pair
    msg["order_hedgeParam"] = order.m_hedgeParam # beta value for beta hedge (in range 0-1), ratio for pair hedge

    # Clearing info
    msg["order_account"] = order.m_account # IB account
    msg["order_settlingFirm"] = order.m_settlingFirm
    msg["order_clearingAccount"] = order.m_clearingAccount # True beneficiary of the order
    msg["order_clearingIntent"] = order.m_clearingIntent # "" (Default), "IB", "Away", "PTA" (PostTrade)

    # ALGO ORDERS ONLY
    msg["order_algoStrategy"] = order.m_algoStrategy
    msg["order_algoParams"] = order.m_algoParams

    # What-if
    msg["order_whatIf"] = order.m_whatIf

    # Not Held
    msg["order_notHeld"] = order.m_notHeld

    # Smart combo routing params
    msg["order_smartComboRoutingParams"] = order.m_smartComboRoutingParams

    # order combo legs
    #public Vector<OrderComboLeg> m_orderComboLegs = new Vector<OrderComboLeg>();

    # order misc options
    msg["order_orderMiscOptions"] = order.m_orderMiscOptions
    
    return msg

def flattenContractDetails(contractDetails, msg):
    
    #msg["contractDetails_summary"] = contractDetails.m_summary #try without this for now
    msg["contractDetails_marketName"] = contractDetails.m_marketName
    msg["contractDetails_minTick"] = contractDetails.m_minTick
    msg["contractDetails_priceMagnifier"] = contractDetails.m_priceMagnifier
    msg["contractDetails_orderTypes"] = contractDetails.m_orderTypes
    msg["contractDetails_validExchanges"] = contractDetails.m_validExchanges
    msg["contractDetails_underConId"] = contractDetails.m_underConId
    msg["contractDetails_longName"] = contractDetails.m_longName
    msg["contractDetails_contractMonth"] = contractDetails.m_contractMonth
    msg["contractDetails_industry"] = contractDetails.m_industry
    msg["contractDetails_category"] = contractDetails.m_category
    msg["contractDetails_subcategory"] = contractDetails.m_subcategory
    msg["contractDetails_timeZoneId"] = contractDetails.m_timeZoneId
    msg["contractDetails_tradingHours"] = contractDetails.m_tradingHours
    msg["contractDetails_liquidHours"] = contractDetails.m_liquidHours
    msg["contractDetails_evRule"] = contractDetails.m_evRule
    msg["contractDetails_evMultiplier"] = contractDetails.m_evMultiplier

    msg["contractDetails_secIdList"] = contractDetails.m_secIdList # CUSIP/ISIN/etc.

    # BOND values
    msg["contractDetails_cusip"] = contractDetails.m_cusip
    msg["contractDetails_ratings"] = contractDetails.m_ratings
    msg["contractDetails_descAppend"] = contractDetails.m_descAppend
    msg["contractDetails_bondType"] = contractDetails.m_bondType
    msg["contractDetails_couponType"] = contractDetails.m_couponType
    msg["contractDetails_callable"] = contractDetails.m_callable
    msg["contractDetails_putable"] = contractDetails.m_putable
    msg["contractDetails_coupon"] = contractDetails.m_coupon
    msg["contractDetails_convertible"] = contractDetails.m_convertible
    msg["contractDetails_maturity"] = contractDetails.m_maturity
    msg["contractDetails_issueDate"] = contractDetails.m_issueDate
    msg["contractDetails_nextOptionDate"] = contractDetails.m_nextOptionDate
    msg["contractDetails_nextOptionType"] = contractDetails.m_nextOptionType
    msg["contractDetails_nextOptionPartial"] = contractDetails.m_nextOptionPartial
    msg["contractDetails_notes"] = contractDetails.m_notes
    
    return msg

def flattenOrderState(orderState, msg):
    
    msg["orderState_status"] = orderState.m_status

    msg["orderState_initMargin"] = orderState.m_initMargin
    msg["orderState_maintMargin"] = orderState.m_maintMargin
    msg["orderState_equityWithLoan"] = orderState.m_equityWithLoan

    msg["orderState_commission"] = orderState.m_commission
    msg["orderState_minCommission"] = orderState.m_minCommission
    msg["orderState_maxCommission"] = orderState.m_maxCommission
    msg["orderState_commissionCurrency"] = orderState.m_commissionCurrency

    msg["orderState_warningText"] = orderState.m_warningText

    return msg

def flattenExecution(execution, msg):
    
    msg["execution_orderId"] = execution.m_orderId
    msg["execution_clientId"] = execution.m_clientId
    msg["execution_execId"] = execution.m_execId
    msg["execution_time"] = execution.m_time
    msg["execution_acctNumber"] = execution.m_acctNumber
    msg["execution_exchange"] = execution.m_exchange
    msg["execution_side"] = execution.m_side
    msg["execution_shares"] = execution.m_shares
    msg["execution_price"] = execution.m_price
    msg["execution_permId"] = execution.m_permId
    msg["execution_liquidation"] = execution.m_liquidation
    msg["execution_cumQty"] = execution.m_cumQty
    msg["execution_avgPrice"] = execution.m_avgPrice
    msg["execution_orderRef"] = execution.m_orderRef
    msg["execution_evRule"] = execution.m_evRule
    msg["execution_evMultiplier"] = execution.m_evMultiplier
    
    return msg

def flattenUnderComp(underComp, msg):
    
    msg["underComp_conId"] = underComp.m_conId
    msg["underComp_delta"] = underComp.m_delta
    msg["underComp_price"] = underComp.m_price
    
    return msg

def flattenExecutionReport(executionReport, msg):
    
    msg["executionReport_execId"] = executionReport.m_execId
    msg["executionReport_commission"] = executionReport.m_commission
    msg["executionReport_currency"] = executionReport.m_currency
    msg["executionReport_realizedPNL"] = executionReport.m_realizedPNL
    msg["executionReport_yield"] = executionReport.m_yield
    msg["executionReport_yieldRedemptionDate"] = executionReport.m_yieldRedemptionDate # YYYYMMDD format
    
    return msg