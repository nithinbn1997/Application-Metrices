from pydantic import BaseModel
from enum import Enum


class DestinationId(str, Enum):
    cyx = "CYX"
    eqx = "EQX"
    # dlr = "DLR"


class SourceId(str, Enum):
    ons = "ONS"
    zoh = "ZOH"
    slf = "SLF"

class Category(str, Enum):
    accounting = "accounting"
    # fault = "fault"
    # configuration = "configuration"
    # performance = "performance"
    # security = "security"
    # mef = "mef"
    

class AccountingSubCategory(str, Enum):
    crossconnect = "crossconnect"
    order = "order"


class TransactionTypeName(str, Enum):
    cc_order = "QCL_CC_ORDER"
    cc_deinstall = "QCL_CC_DEINSTALL"
    cc_move = "QCL_CC_MOVE"
    cc_cancel = "QCL_CC_CANCEL"
    cc_list = "QCL_CC_LIST"
    cc_details = "QCL_CC_DETAILS"
    order_list = "QCL_ORDER_LIST"
    order_details = "QCL_ORDER_LIST"
    

class TransactionTypeNumber(str, Enum):
    cc_order = "003010001012"
    cc_deinstall = "003010003612"
    cc_move = "003010005012"
    cc_cancel = "003010001032"
    cc_list = "003010006011"
    cc_details = "003010005011"
    order_list = "003020002011"
    order_details = "003020001011"
    
    
# class QclTransactionData(BaseModel):
#     qcl_transaction_type_number: str
#     qcl_transaction_type_name: str


class QclGenericData(BaseModel):
    qcl_source_id: SourceId
    qcl_destination_id: DestinationId
