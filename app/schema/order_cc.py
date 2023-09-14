from pydantic import BaseModel
from typing import Optional, List

from app.schema.common_schema import QclGenericData


class QclCcASideDetails(BaseModel):
    qcl_cc_account_id: Optional[str]
    qcl_cc_pod_id: Optional[str]
    qcl_cc_model_id: Optional[str]
    qcl_cc_port_id: Optional[str] 
    qcl_cc_a_side_patch_panel_id: Optional[str] 
    qcl_cc_connection_service: Optional[str] 
    qcl_cc_media_type: Optional[str]
    qcl_cc_protocol_type: Optional[str] 
    qcl_cc_connector_type: Optional[str] 
    qcl_cc_patch_panel_port_a: Optional[str] 
    qcl_cc_patch_panel_port_b: Optional[str]


class QclCcZSideDetails(BaseModel):
    qcl_cc_z_side_patch_panel_id: Optional[str]
    qcl_cc_connector_type: Optional[str] 
    qcl_cc_patch_panel_port_a: Optional[str] 
    qcl_cc_patch_panel_port_b: Optional[str] 
    qcl_cc_z_side_provider_name: Optional[str] 
    qcl_cc_loa_attachment_id: Optional[str] 


class QcLCrossConnectDetails(BaseModel):
    qcl_cc_a_side_details: QclCcASideDetails
    qcl_cc_z_side_details: QclCcZSideDetails
    qcl_cc_request_date: Optional[str] 


class QclItemDetails(BaseModel):
    qcl_inventory_item_id: str
    qcl_inventory_item_name: str
    qcl_crossconnect_details: QcLCrossConnectDetails
    original_item_details: Optional[List] 


class SourceSpecificFields(BaseModel):
    qcl_po_id: str
    qcl_item_details: List[QclItemDetails]


class QclTransactionData(BaseModel):
    generic_fields: Optional[dict]
    source_fields: SourceSpecificFields
    destination_fields: Optional[dict]


class QclOrderDataObject(BaseModel):
    qcl_generic_data: QclGenericData
    qcl_transaction_data: QclTransactionData
