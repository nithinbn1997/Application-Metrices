import os
from dotenv import load_dotenv

load_dotenv()

##############################
# Micro services BASE URLs
##############################

MS1_HOST = os.getenv("MS1_HOST")
MS2_HOST = os.getenv("MS2_HOST")
MS4_HOST = os.getenv("MS4_HOST")
MS5_HOST = os.getenv("MS5_HOST")

##############################
# MS2 APIs
##############################

# ONS
MS2_ONS_UPDATE_PO_STATUS = f"{MS2_HOST}/internal/ms2/ons/update_po_message"
MS2_ONS_UPDATE_IA_STATUS = f"{MS2_HOST}/internal/ms2/ons/update_ia_message"
MS2_ONS_MARK_ONS_PO_COMPLETE = f"{MS2_HOST}/internal/ms2/ons/mark_po_complete"
MS2_ONS_MARK_ITEM_RECEIVED = f"{MS2_HOST}/internal/ms2/ons/mark_item_received"
MS2_ONS_MARK_ITEM_INACTIVE = f"{MS2_HOST}/internal/ms2/ons/mark_item_inactive"

# ZOHO
MS2_ZOHO_UPDATE_PO_STATUS = f"{MS2_HOST}/internal/ms2/zoho/update_po_message"
MS2_ZOHO_UPDATE_IA_STATUS = f"{MS2_HOST}/internal/ms2/zoho/update_ia_message"
MS2_ZOHO_MARK_ITEM_RECEIVED = f"{MS2_HOST}/internal/ms2/zoho/mark_item_received"
MS2_ZOHO_MARK_ITEM_INACTIVE = f"{MS2_HOST}/internal/ms2/zoho/mark_item_inactive"

##############################
# MS4 APIs
##############################

# EQX - CrossConnect
MS4_EQX_ORDER_CC = f"{MS4_HOST}/internal/qcl_to_south/equinix/order/cc"
MS4_EQX_DEINSTALL_CC = f"{MS4_HOST}/internal/qcl_to_south/equinix/deinstall/cc"
MS4_EQX_CANCEL_CC = f"{MS4_HOST}/internal/qcl_to_south/equinix/cancel/cc"
MS4_EQX_CC_LIST = f"{MS4_HOST}/internal/qcl_to_south/equinix/crossconnect/list"
MS4_EQX_CC_DETAILS = f"{MS4_HOST}/internal/qcl_to_south/equinix/crossconnect/details"
# EQX - Orders
MS4_EQX_ORDER_LIST = f"{MS4_HOST}/internal/qcl_to_south/equinix/order/list"
MS4_EQX_ORDER_DETAILS = f"{MS4_HOST}/internal/qcl_to_south/equinix/order/details"

# CYX - CrossConnect
MS4_CYX_ORDER_CC = f"{MS4_HOST}/internal/qcl_to_south/cyxtera/order/cc"
MS4_CYX_UPLOAD_LOA = f"{MS4_HOST}/internal/qcl_to_south/upload/loa/file"
MS4_CYX_DEINSTALL_CC = f"{MS4_HOST}/internal/qcl_to_south/cyxtera/deinstall/cc"
MS4_CYX_MOVE_CC = f"{MS4_HOST}/internal/qcl_to_south/cyxtera/move/cc"
MS4_CYX_CC_LIST = f"{MS4_HOST}/internal/qcl_to_south/cyxtera/crossconnect/list"
MS4_CYX_CC_DETAILS = f"{MS4_HOST}/internal/qcl_to_south/cyxtera/crossconnect/details"
# CYX - Orders
MS4_CYX_ORDER_LIST = f"{MS4_HOST}/internal/qcl_to_south/cyxtera/order/list"
MS4_CYX_ORDER_DETAILS = f"{MS4_HOST}/internal/qcl_to_south/cyxtera/order/details"

##############################
# MS5 APIs
##############################
MS5_ADD_CC_ORDER = f"{MS5_HOST}/internal/south_to_qcl/add_poll_order"
MS5_ADD_DEINSTALL_CC_ORDER = f"{MS5_HOST}/internal/south_to_qcl/de_install_poll_order"
