from pydantic import BaseModel
from enum import Enum
from typing import Optional, List


from app.schema.common_schema import QclGenericData


class QclDeinstallDetails(BaseModel):
    qcl_cc_deinstall_id: str
    qcl_cc_removal_date: Optional[str]


class QclItemDetails(BaseModel):
    qcl_inventory_item_id: str
    qcl_inventory_item_name: str
    qcl_cc_deinstall_details: QclDeinstallDetails
    original_item_details: Optional[List]


class SourceSpecificFields(BaseModel):
    qcl_ia_id: str
    qcl_item_details: List[QclItemDetails]


class QclTransactionData(BaseModel):
    generic_fields: Optional[dict]
    source_fields: SourceSpecificFields
    destination_fields: Optional[dict]


class QclDeinstallDataObject(BaseModel):
    qcl_generic_data: QclGenericData
    qcl_transaction_data: QclTransactionData
