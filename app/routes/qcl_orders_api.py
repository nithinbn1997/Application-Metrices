from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder

from app import logger
from app.schema.models import QCLDataObject
from app.actions import orders_actions

log = logger.get_logger()

router = APIRouter(
    prefix="/api/v1/accounting/orders",
    tags=["QCL Orders APIs"],
)


@router.post("/qcl_order_details")
def get_order_details(request: QCLDataObject):
    """
    API to get order details from data center

    Args:
        request (QCLDataObject): _description_

    Returns:
        _type_: _description_
    """
    log.info("Get order details API called")
    qcl_data_obj = jsonable_encoder(request)
    log.debug(f"get order details data -> {qcl_data_obj}")
    data = {
        "qcl_destination_id": qcl_data_obj.get("qcl_generic_data").get(
            "qcl_destination_id"
        ),
        "qcl_order_id": (
            qcl_data_obj.get("qcl_transaction_data")
            .get("source_fields")
            .get("qcl_order_id")
        ),
    }
    return orders_actions.get_order_details(data)


@router.post("/qcl_order_list")
def get_order_list(request: QCLDataObject):
    """
    API to get list of orders from data center

    Args:
        request (QCLDataObject): _description_

    Returns:
        _type_: _description_
    """
    log.info("Get order list API called")
    qcl_data_obj = jsonable_encoder(request)
    log.debug(f"get order list data -> {qcl_data_obj}")
    data = {
        "qcl_destination_id": qcl_data_obj.get("qcl_generic_data").get(
            "qcl_destination_id"
        )
    }
    return orders_actions.get_order_list(data)
