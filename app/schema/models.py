from pydantic import BaseModel
from typing import Optional


class QCLDataObject(BaseModel):
    qcl_generic_data: dict
    qcl_transaction_data: dict

class OrderDetails(BaseModel):
    lattice_transaction_id: str
    qcl_inventory_item_id : str
    qcl_order_status : Optional[str] = None
    qcl_asset_id : Optional[str] = None
    qcl_destination_id : Optional[str] = None
    qcl_order_id : str
