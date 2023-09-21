import json
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from fastapi.requests import Request
from fastapi.encoders import jsonable_encoder
from fastapi import (
    APIRouter,
    BackgroundTasks,
    Response,
    FastAPI
)   

from app import logger
from app.managers.transaction_manager import transaction_manager
from app.schema.order_cc import QclOrderDataObject
from app.schema.common_schema import (
    Category,
    AccountingSubCategory,
    TransactionTypeName,
    TransactionTypeNumber
)
from app.schema.deinstall_cc import QclDeinstallDataObject
from app.schema.models import QCLDataObject
from app.actions import crossconnect_actions





log = logger.get_logger()



router = APIRouter(
    prefix="/api/v1/accounting/crossconnect",
    tags=["QCL Crossconnect APIs"],
)

order_counter = Counter('qcl_crossconnect_order_total', 'Total QCL crossconnect orders')
details_counter = Counter('qcl_crossconnect_details_total', 'Total QCL crossconnect details requests')
list_counter = Counter('qcl_crossconnect_list_total', 'Total QCL crossconnect list requests')

# Create a custom Prometheus Counter metric to count the number of cross-connect orders
# crossconnect_order_counter = Counter(
#     'crossconnect_orders_total',
#     'Total number of cross-connect orders processed'
# )

# # Create a custom Prometheus Counter metric to count errors (if needed)
# error_counter = Counter(
#     'crossconnect_order_errors_total',
#     'Total number of cross-connect order errors'
# )


@router.post("/qcl_crossconnect_order")
def process_crossconnect_order(
    request: QclOrderDataObject, background_tasks: BackgroundTasks
) -> dict:
    """
    API to order cross connects

    Args:
        request (Request): QCL data object with data needed to process the request
        background_tasks (BackgroundTasks): add background task

    Returns:
        dict: dictionary with lattice transaction id
    """
    log.info("Order crossconnect API called")
    qcl_data_obj = jsonable_encoder(request)
    log.debug(f"order cc data -> {qcl_data_obj}")
    generic_data = qcl_data_obj.get("qcl_generic_data")
    # transaction_generic_data = qcl_data_obj.get(
    #     "qcl_transaction_data"
    # ).get("generic_fields")
    transaction_source_data = qcl_data_obj.get(
        "qcl_transaction_data"
    ).get("source_fields")
    
    # generate transaction id
    qcl_transaction_id = transaction_manager.generate_lattice_transaaction_id()

    log.info(f"Transaction ID assigned -> {qcl_transaction_id}")
    data = {
        "lattice_transaction_id": qcl_transaction_id,
        "qcl_transaction_state": 0,
        "qcl_category" : Category.accounting,
        "qcl_sub_category" : AccountingSubCategory.crossconnect,
        "qcl_transaction_type_name": TransactionTypeName.cc_order,
        "qcl_transaction_type_number": TransactionTypeNumber.cc_order,
        "lattice_organisation_id": "qarbon",        # to be updated after authentication is implemented
        "lattice_user_id": "qarbon_user",           # to be updated after authentication is implemented
        "qcl_source_id": generic_data.get("qcl_source_id"),
        "qcl_destination_id": generic_data.get("qcl_destination_id"),
        "north_transaction_id": transaction_source_data.get("qcl_po_id"),
        "needs_north_update": True,
        "north_transaction_details_original": [],
        "north_transaction_details_qcl_formatted": [],
    }

    for inventory_item in transaction_source_data.get("qcl_item_details"):
        inventory_item_data = {
            "qcl_inventory_item_id": inventory_item.get("qcl_inventory_item_id"),
            "qcl_inventory_item_name": inventory_item.get("qcl_inventory_item_name"),
            "qcl_inventory_item_details": inventory_item.get(
                "qcl_crossconnect_details"
            ),
            "qcl_item_state": 0,
            "qcl_south_order_id": None,
            "qcl_asset_id": None,
            "qcl_item_status_message": "Order received in Lattice",
            "qcl_item_error_message": None
        }
        data["north_transaction_details_qcl_formatted"].append(inventory_item_data)
    log.debug(f"transation_order_cc_data --->{data}")
    log.debug(type(data))
    transaction_manager.add_new_transaction_data(data)
    log.debug("added transaction data")
    background_tasks.add_task(
        crossconnect_actions.run_async,
        crossconnect_actions.process_cross_connect_order,
        data
    )
    order_counter.inc()
    # new_transaction_id.inc(qcl_transaction_id)
    return {"lattice_transaction_id": qcl_transaction_id}



# @router.get("/metrics")
# def metrices():
#     return Response(
#         content= prometheus_client.generate_latest(),
#         media_type="text/plain",
#     )


@router.post("/qcl_crossconnect_details")
def get_cross_connect_details(request: QCLDataObject):
    """
    API to get cross connect details from data center

    Args:
        request (QCLDataObject): _description_

    Returns:
        _type_: _description_
    """
    log.info("Get crossconnect details API called")
    qcl_data_obj = jsonable_encoder(request)
    log.debug(f"get cc details data -> {qcl_data_obj}")
    data = {
        "qcl_destination_id": qcl_data_obj.get("qcl_generic_data").get(
            "qcl_destination_id"
        ),
        "qcl_cc_id": (
            qcl_data_obj.get("qcl_transaction_data")
            .get("source_fields")
            .get("qcl_cc_id")
        )
    }
    details_counter.inc()
    return crossconnect_actions.get_cc_details(data)


@router.post("/qcl_crossconnect_list")
def get_cross_connect_list(request: QCLDataObject):
    """
    API to get list of cross connects from data center

    Args:
        request (QCLDataObject): _description_

    Returns:
        _type_: _description_
    """
    log.info("Get crossconnect list API called")
    qcl_data_obj = jsonable_encoder(request)
    log.debug(f"get cc list data -> {qcl_data_obj}")
    data = {
        "qcl_destination_id": qcl_data_obj.get("qcl_generic_data").get(
            "qcl_destination_id"
        )
    }
    list_counter.inc()
    return crossconnect_actions.get_cc_list(data)





@router.post("/qcl_crossconnect_deinstall")
def order_deinstall_crossconnect(
    request: QclDeinstallDataObject, background_tasks: BackgroundTasks
) -> dict:
    """
    API to order deinstall cross connect

    Args:
        request (Request): QCL data object with data needed to process the request
        background_tasks (BackgroundTasks): add background task

    Returns:
        dict: dictionary with lattice transaction id
    """
    # add lattice transaction id if not present
    # this would be needed for transaction coming to QTH directly.
    log.info("Deinstall crossconnect API called")

    # qcl_data_obj = await request.body()
    # qcl_data_obj = json.loads(qcl_data_obj)
    qcl_data_obj = jsonable_encoder(request)
    log.debug(f"Deinstall cc requested. Body -> {qcl_data_obj}")

    generic_data = qcl_data_obj.get("qcl_generic_data")
    # transaction_generic_data = qcl_data_obj.get(
    #     "qcl_transaction_data"
    # ).get("generic_fields")
    transaction_source_data = qcl_data_obj.get(
        "qcl_transaction_data"
    ).get("source_fields")
    
    # generate transaction id
    qcl_transaction_id = transaction_manager.generate_lattice_transaaction_id()

    log.info(f"Transaction ID assigned -> {qcl_transaction_id}")
    data = {
        "lattice_transaction_id": qcl_transaction_id,
        "qcl_transaction_state": 0,
        "qcl_category" : Category.accounting,
        "qcl_sub_category" : AccountingSubCategory.crossconnect,
        "qcl_transaction_type_name": TransactionTypeName.cc_deinstall,
        "qcl_transaction_type_number": TransactionTypeNumber.cc_deinstall,
        "lattice_organisation_id": "qarbon",        # to be updated after authentication is implemented
        "lattice_user_id": "qarbon_user",           # to be updated after authentication is implemented
        "qcl_source_id": generic_data.get("qcl_source_id"),
        "qcl_destination_id": generic_data.get("qcl_destination_id"),
        "north_transaction_id": transaction_source_data.get("qcl_ia_id"),
        "needs_north_update": False,
        "north_transaction_details_original": [],
        "north_transaction_details_qcl_formatted": [],
    }
    for inventory_item in transaction_source_data.get("qcl_item_details"):
        inventory_item_data = {
            "qcl_inventory_item_id": inventory_item.get("qcl_inventory_item_id"),
            "qcl_inventory_item_name": inventory_item.get("qcl_inventory_item_name"),
            "qcl_inventory_item_details": inventory_item.get(
                "qcl_cc_deinstall_details"
            ),
            "qcl_item_state": 0,
            "qcl_south_order_id": None,
            "qcl_item_status_message": "Order received in Lattice",
            "qcl_item_error_message": None,
        }
        data["north_transaction_details_qcl_formatted"].append(inventory_item_data)

    transaction_manager.add_new_transaction_data(data)
    log.debug("added transaction data")
    background_tasks.add_task(
        crossconnect_actions.run_async,
        crossconnect_actions.process_deinstall_order,
        data
    )

    return {"lattice_transaction_id": qcl_transaction_id}


@router.post("/qcl_crossconnect_move")
def order_move_crossconnect(
    request: QCLDataObject, background_tasks: BackgroundTasks
) -> dict:
    """
    API to move a cross connect once it is installed

    Args:
        request (Request): QCL data object with data needed to process the request
        background_tasks (BackgroundTasks): add background task
    Returns:
        dict: dictionary with lattice transaction id
    """
    log.info("Move cross connect API called")
    qcl_data_obj = jsonable_encoder(request)
    log.debug(f"order cc data -> {qcl_data_obj}")
    generic_data = qcl_data_obj.get("qcl_generic_data")
    # transaction_generic_data = qcl_data_obj.get(
    #     "qcl_transaction_data"
    # ).get("generic_fields")
    transaction_source_data = qcl_data_obj.get(
        "qcl_transaction_data"
    ).get("source_fields")
    
    # generate transaction id
    qcl_transaction_id = transaction_manager.generate_lattice_transaaction_id()
        
    data = {
        "lattice_transaction_id": qcl_transaction_id,
        "qcl_transaction_state": 0,
        "qcl_category" : Category.accounting,
        "qcl_sub_category" : AccountingSubCategory.crossconnect,
        "qcl_transaction_type_name": TransactionTypeName.cc_move,
        "qcl_transaction_type_number": TransactionTypeNumber.cc_move,
        "lattice_organisation_id": "qarbon",        # to be updated after authentication is implemented
        "lattice_user_id": "qarbon_user",           # to be updated after authentication is implemented
        "qcl_source_id": generic_data.get("qcl_source_id"),
        "qcl_destination_id": generic_data.get("qcl_destination_id"),
        "north_transaction_id": transaction_source_data.get("qcl_ia_id"),
        "needs_north_update": False,
        "north_transaction_details_original": [],
        "north_transaction_details_qcl_formatted": [],
    }
    for inventory_item in transaction_source_data.get("qcl_item_details"):
        inventory_item_data = {
            "qcl_inventory_item_id": inventory_item.get("qcl_inventory_item_id"),
            "qcl_inventory_item_name": inventory_item.get("qcl_inventory_item_name"),
            "qcl_inventory_item_details": inventory_item.get("qcl_cc_move_details"),
            "qcl_item_state": 0,
            "qcl_south_order_id": None,
            "qcl_asset_id": None,
            "qcl_item_status_message": "Order received in Lattice",
            "qcl_item_error_message": None,
        }
        data["north_transaction_details_qcl_formatted"].append(inventory_item_data)

    transaction_manager.add_new_transaction_data(data)
    log.debug("added transaction data")
    background_tasks.add_task(
        crossconnect_actions.run_async,
        crossconnect_actions.process_move_order, 
        data
    )
    return {"lattice_transaction_id": qcl_transaction_id}


@router.post("/qcl_crossconnect_cancel")
async def request_cancel_crossconnct_order(
    request: Request, background_tasks: BackgroundTasks
) -> dict:
    """
    API to cancel cross connect order

    Args:
        request (Request): QCL data object with data needed to process the request
        background_tasks (BackgroundTasks): add background task

    Returns:
        dict:
    """
    # add lattice transaction id if not present
    # this would be needed for transaction coming to QTH directly.
    qcl_data_obj1 = await request.body()
    qcl_data_obj = json.loads(qcl_data_obj1)
    generic_data = qcl_data_obj.get("qcl_generic_data")
    # transaction_generic_data = qcl_data_obj.get(
    #     "qcl_transaction_data"
    # ).get("generic_fields")
    transaction_source_data = qcl_data_obj.get(
        "qcl_transaction_data"
    ).get("source_fields")
    
    # generate transaction id
    qcl_transaction_id = await transaction_manager.generate_lattice_transaaction_id()

    data = {
        "lattice_transaction_id": qcl_transaction_id,
        "qcl_transaction_state": 0,
        "qcl_category" : Category.accounting,
        "qcl_sub_category" : AccountingSubCategory.crossconnect,
        "qcl_transaction_type_name": TransactionTypeName.cc_cancel,
        "qcl_transaction_type_number": TransactionTypeNumber.cc_cancel,
        "lattice_organisation_id": generic_data.get("lattice_organisation_id"),
        "lattice_user_id": generic_data.get("lattice_user_id"),
        "qcl_source_id": generic_data.get("qcl_source_id"),
        "qcl_destination_id": generic_data.get("qcl_destination_id"),
        "north_transaction_id": transaction_source_data.get("qcl_ia_id"),
        "needs_north_update": False,
        "north_transaction_details_original": [],
        "north_transaction_details_qcl_formatted": [],
    }
    for inventory_item in transaction_source_data.get("qcl_item_details"):
        inventory_item_data = {
            "qcl_inventory_item_id": inventory_item.get("qcl_inventory_item_id"),
            "qcl_inventory_item_name": inventory_item.get("qcl_inventory_item_name"),
            "qcl_item_state": 0,
            "qcl_item_status_message": "Cancel order received in Lattice",
            "qcl_item_error_message": None,
        }
        data["north_transaction_details_qcl_formatted"].append(inventory_item_data)

    await transaction_manager.add_new_transaction_data(data)
    log.debug("added transaction data")
    background_tasks.add_task(crossconnect_actions.process_cancel_order, data)
    return {"lattice_transaction_id": qcl_transaction_id}
