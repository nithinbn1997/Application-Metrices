import json

from fastapi import APIRouter, BackgroundTasks
from fastapi.requests import Request
from fastapi.encoders import jsonable_encoder

from app import logger
from app.config import transaction_table_name
from app.managers.doc_db_manager import doc_db_manager
from app.managers.transaction_manager import transaction_manager
from app.actions import crossconnect_actions
from app.constants import EQX_ID, CYX_ID
from app.schema.models import QCLDataObject
from app.schema.order_cc import QclOrderDataObject
from app.schema.deinstall_cc import QclDeinstallDataObject
from app.schema.common_schema import (
    Category,
    AccountingSubCategory,
    TransactionTypeName,
    TransactionTypeNumber
)

# from app.models import Order_Details

log = logger.get_logger()

router = APIRouter(
    prefix="/internal",
    tags=["INTERNAL_APIs"],
)


@router.post("/qth/update_cc_order_id")
async def update_south_cc_order_id(request: Request):
    """_summary_

    Args:
        order_details (Order_Details): _description_
    """
    order_details = await request.body()
    log.info(f"body data from the microservice four ---> {order_details}")
    order_details = json.loads(order_details)
    log.debug(f"after json serialization --> {order_details}")
    # order_details = jsonable_encoder(order_details)
    log.debug("Request Data --->", order_details)
    lattice_transaction_id = order_details.get("lattice_transaction_id")
    qcl_inventory_item_id = order_details.get("qcl_inventory_item_id")
    order_id = order_details.get("qcl_order_id")
    filter_query = {"lattice_transaction_id": lattice_transaction_id}
    trans_data = await doc_db_manager.get_document_by_filter(
        transaction_table_name, filter_query
    )
    items_data = trans_data.get("north_transaction_details_qcl_formatted")
    if order_id == "":
        for i, item in enumerate(items_data):
            error_message = order_details.get("qcl_error_message")
            if item.get("qcl_inventory_item_id") == qcl_inventory_item_id:
                update_query = {
                    "$set": {
                        f"north_transaction_details_qcl_formatted.{i}.qcl_item_status_message": "Please check error message",
                        f"north_transaction_details_qcl_formatted.{i}.qcl_item_error_message": error_message,
                        f"north_transaction_details_qcl_formatted.{i}.qcl_item_state": -200,
                    }
                }
                await doc_db_manager.update_document(
                    transaction_table_name, filter_query, update_query
                )
                await transaction_manager.update_north_update_state(
                    lattice_transaction_id, True
                )
                break
    else:
        for i, item in enumerate(items_data):
            if item.get("qcl_inventory_item_id") == qcl_inventory_item_id:
                update_query = {
                    "$set": {
                        f"north_transaction_details_qcl_formatted.{i}.qcl_item_status_message": "Order placed successfully",
                        f"north_transaction_details_qcl_formatted.{i}.qcl_south_order_id": order_id,
                        f"north_transaction_details_qcl_formatted.{i}.qcl_item_state": 200,
                    }
                }
                order_details["qcl_destination_id"] = trans_data.get(
                    "qcl_destination_id"
                )
                await doc_db_manager.update_document(
                    transaction_table_name, filter_query, update_query
                )
                await transaction_manager.update_north_update_state(
                    lattice_transaction_id, True
                )
                await crossconnect_actions.add_cc_order_to_ms5(order_details)
                break


@router.post("/qth/update_deinstall_cc_order_id")
async def update_deinstall_cc_order_id(request: Request):
    """_summary_

    Args:
        order_details (Order_Details): _description_
    """
    try:
        order_details = await request.body()
        log.info(f"body data from the microservice four ---> {order_details}")
        order_details = json.loads(order_details)
        log.debug(f"after json serialization --> {order_details}")
        # order_details = jsonable_encoder(order_details)
        log.debug(f"Request Data ---> {order_details}")
        lattice_transaction_id = order_details.get("lattice_transaction_id")
        qcl_inventory_item_id = order_details.get("qcl_inventory_item_id")
        order_id = order_details.get("qcl_order_id")
        filter_query = {"lattice_transaction_id": lattice_transaction_id}
        trans_data = await doc_db_manager.get_document_by_filter(
            transaction_table_name, filter_query
        )
        items_data = trans_data.get("north_transaction_details_qcl_formatted")
        if order_id == "":
            for i, item in enumerate(items_data):
                error_message = order_details.get("qcl_error_message")
                if item.get("qcl_inventory_item_id") == qcl_inventory_item_id:
                    update_query = {
                        "$set": {
                            f"north_transaction_details_qcl_formatted.{i}.qcl_item_status_message": "Please check error message",
                            f"north_transaction_details_qcl_formatted.{i}.qcl_item_error_message": error_message,
                            f"north_transaction_details_qcl_formatted.{i}.qcl_item_state": -200,
                        }
                    }
                    await doc_db_manager.update_document(
                        transaction_table_name, filter_query, update_query
                    )
                    await transaction_manager.update_north_update_state(
                        lattice_transaction_id, True
                    )
                    break
        else:
            for i, item in enumerate(items_data):
                if item.get("qcl_inventory_item_id") == qcl_inventory_item_id:
                    update_query = {
                        "$set": {
                            f"north_transaction_details_qcl_formatted.{i}.qcl_item_status_message": "Order placed successfully",
                            f"north_transaction_details_qcl_formatted.{i}.qcl_south_order_id": order_id,
                            f"north_transaction_details_qcl_formatted.{i}.qcl_item_state": 200,
                        }
                    }
                    order_details["qcl_destination_id"] = trans_data.get(
                        "qcl_destination_id"
                    )
                    await doc_db_manager.update_document(
                        transaction_table_name, filter_query, update_query
                    )
                    await transaction_manager.update_north_update_state(
                        lattice_transaction_id, True
                    )
                    if await crossconnect_actions.add_deinstall_order_to_ms5(
                        order_details
                    ):
                        update_query = {
                            "$set": {
                                f"north_transaction_details_qcl_formatted.{i}.qcl_item_state": 210
                            }
                        }
                        await doc_db_manager.update_document(
                            transaction_table_name, filter_query, update_query
                        )
                    break

    except Exception as ex:
        log.exception(f"Error updating deinstall order id/status -> {ex}")


@router.post("/qth/order_cc_status_updated")
async def update_order_cc_item_status(request: Request):
    """_summary_

    Args:
        order_details (Order_Details): _description_
    """
    log.info("Order CC status updated")
    order_details = await request.body()
    order_details = json.loads(order_details)
    lattice_transaction_id = order_details.get("lattice_transaction_id")
    qcl_inventory_item_id = order_details.get("qcl_inventory_item_id")
    qcl_order_status = order_details.get("qcl_order_status")
    filter_query = {"lattice_transaction_id": lattice_transaction_id}
    log.info(
        f"[{lattice_transaction_id}] Received order cross connect "
        "status update from MS5"
    )
    log.debug(f"data ---> {order_details}")
    trans_data = await doc_db_manager.get_document_by_filter(
        transaction_table_name, filter_query
    )
    items_data = trans_data.get("north_transaction_details_qcl_formatted")
    item_found = False
    for i, item in enumerate(items_data):
        if item.get("qcl_inventory_item_id") == qcl_inventory_item_id:
            item_found = True
            break
    if not item_found:
        log.error(f"Item not found in transaction")
        return

    if order_details.get("qcl_destination_id") == EQX_ID:
        if order_details.get("qcl_order_status") == "CLOSED":
            update_query = {
                "$set": {
                    f"north_transaction_details_qcl_formatted.{i}.qcl_item_status_message": qcl_order_status,
                    f"north_transaction_details_qcl_formatted.{i}.qcl_asset_id": order_details.get(
                        "qcl_asset_id"
                    ),
                }
            }
            await doc_db_manager.update_document(
                transaction_table_name, filter_query, update_query
            )
            await transaction_manager.update_transaction_item_state(
                lattice_transaction_id, qcl_inventory_item_id, 500
            )
        else:
            update_query = {
                "$set": {
                    f"north_transaction_details_qcl_formatted.{i}.qcl_item_status_message": qcl_order_status,
                }
            }
            await doc_db_manager.update_document(
                transaction_table_name, filter_query, update_query
            )
            if order_details.get("qcl_order_status") == "CANCELLED":
                await transaction_manager.update_transaction_item_state(
                    lattice_transaction_id, qcl_inventory_item_id, 600
                )
        await doc_db_manager.update_document(
            transaction_table_name, filter_query, update_query
        )

    elif order_details.get("qcl_destination_id") == CYX_ID:
        if order_details.get("qcl_order_status") == "CLOSED COMPLETE":
            update_query = {
                "$set": {
                    f"north_transaction_details_qcl_formatted.{i}.qcl_item_status_message": qcl_order_status,
                    f"north_transaction_details_qcl_formatted.{i}.qcl_asset_id": order_details.get(
                        "qcl_order_id"
                    ),
                }
            }
            await doc_db_manager.update_document(
                transaction_table_name, filter_query, update_query
            )
            await transaction_manager.update_transaction_item_state(
                lattice_transaction_id, qcl_inventory_item_id, 500
            )
        else:
            update_query = {
                "$set": {
                    f"north_transaction_details_qcl_formatted.{i}.qcl_item_status_message": qcl_order_status,
                }
            }
            await doc_db_manager.update_document(
                transaction_table_name, filter_query, update_query
            )
            if order_details.get("qcl_order_status") == "CLOSED CANCELLED":
                await transaction_manager.update_transaction_item_state(
                    lattice_transaction_id, qcl_inventory_item_id, 600
                )
        await doc_db_manager.update_document(
            transaction_table_name, filter_query, update_query
        )

    await transaction_manager.update_north_update_state(lattice_transaction_id, True)


@router.post("/qth/deinstall_cc_status_updated")
async def update_deinstall_cc_item_order_status(request: Request):
    """_summary_

    Args:
        order_details (Order_Details): _description_
    """
    order_details = await request.body()
    order_details = json.loads(order_details)
    lattice_transaction_id = order_details.get("lattice_transaction_id")
    qcl_inventory_item_id = order_details.get("qcl_inventory_item_id")
    qcl_order_status = order_details.get("qcl_order_status")
    filter_query = {"lattice_transaction_id": lattice_transaction_id}
    log.info(
        f"[{lattice_transaction_id}] Received deinstall order status update from MS5"
    )
    trans_data = await doc_db_manager.get_document_by_filter(
        transaction_table_name, filter_query
    )
    log.debug(trans_data)
    items_data = trans_data.get("north_transaction_details_qcl_formatted")
    item_found = False
    for i, item in enumerate(items_data):
        if item.get("qcl_inventory_item_id") == qcl_inventory_item_id:
            item_found = True
            break
    if not item_found:
        log.error(f"Item not found in transaction")
        return

    if order_details.get("qcl_destination_id") == EQX_ID:
        if order_details.get("qcl_order_status") == "CLOSED":
            update_query = {
                "$set": {
                    f"north_transaction_details_qcl_formatted.{i}.qcl_item_status_message": qcl_order_status,
                }
            }
            await doc_db_manager.update_document(
                transaction_table_name, filter_query, update_query
            )
            await transaction_manager.update_transaction_item_state(
                lattice_transaction_id, qcl_inventory_item_id, 500
            )

        else:
            update_query = {
                "$set": {
                    f"north_transaction_details_qcl_formatted.{i}.qcl_item_status_message": qcl_order_status,
                }
            }
            await doc_db_manager.update_document(
                transaction_table_name, filter_query, update_query
            )
            if order_details.get("qcl_order_status") == "CANCELLED":
                await transaction_manager.update_transaction_item_state(
                    lattice_transaction_id, qcl_inventory_item_id, 600
                )
        await doc_db_manager.update_document(
            transaction_table_name, filter_query, update_query
        )

    elif order_details.get("qcl_destination_id") == CYX_ID:
        if order_details.get("qcl_order_status") == "CLOSED COMPLETE":
            update_query = {
                "$set": {
                    f"north_transaction_details_qcl_formatted.{i}.qcl_item_status_message": qcl_order_status,
                }
            }
            await doc_db_manager.update_document(
                transaction_table_name, filter_query, update_query
            )
            await transaction_manager.update_transaction_item_state(
                lattice_transaction_id, qcl_inventory_item_id, 500
            )
        else:
            update_query = {
                "$set": {
                    f"north_transaction_details_qcl_formatted.{i}.qcl_item_status_message": qcl_order_status,
                }
            }
            await doc_db_manager.update_document(
                transaction_table_name, filter_query, update_query
            )
            if order_details.get("qcl_order_status") == "CLOSED CANCELLED":
                await transaction_manager.update_transaction_item_state(
                    lattice_transaction_id, qcl_inventory_item_id, 600
                )
        await doc_db_manager.update_document(
            transaction_table_name, filter_query, update_query
        )

    await transaction_manager.update_north_update_state(lattice_transaction_id, True)


@router.post("/qth/move_cc_status_updated")
async def update_move_cc_item_order_status(request: Request):
    """_summary_

    Args:
        order_details (Order_Details): _description_
    """
    order_details = await request.body()
    order_details = json.loads(order_details)
    lattice_transaction_id = order_details.get("lattice_transaction_id")
    qcl_inventory_item_id = order_details.get("qcl_inventory_item_id")
    qcl_order_status = order_details.get("qcl_order_status")
    filter_query = {"lattice_transaction_id": lattice_transaction_id}
    log.debug(type(lattice_transaction_id))
    trans_data = await doc_db_manager.get_document_by_filter(
        transaction_table_name, filter_query
    )
    log.debug(trans_data)
    items_data = trans_data.get("north_transaction_details_qcl_formatted")
    item_found = False
    for i, item in enumerate(items_data):
        if item.get("qcl_inventory_item_id") == qcl_inventory_item_id:
            item_found = True
            break
    if not item_found:
        log.error(f"Item not found in transaction")
        return

    if order_details.get("qcl_destination_id") == EQX_ID:
        if order_details.get("qcl_order_status") == "CLOSED":
            update_query = {
                "$set": {
                    f"north_transaction_details_qcl_formatted.{i}.qcl_item_status_message": qcl_order_status,
                    f"north_transaction_details_qcl_formatted.{i}.qcl_asset_id": order_details.get(
                        "qcl_asset_id"
                    ),
                }
            }
            await doc_db_manager.update_document(
                transaction_table_name, filter_query, update_query
            )
            await transaction_manager.update_transaction_item_state(
                lattice_transaction_id, qcl_inventory_item_id, 500
            )
        else:
            update_query = {
                "$set": {
                    f"north_transaction_details_qcl_formatted.{i}.qcl_item_status_message": qcl_order_status,
                }
            }
            await doc_db_manager.update_document(
                transaction_table_name, filter_query, update_query
            )
            if order_details.get("qcl_order_status") == "CANCELLED":
                await transaction_manager.update_transaction_item_state(
                    lattice_transaction_id, qcl_inventory_item_id, 600
                )
        await doc_db_manager.update_document(
            transaction_table_name, filter_query, update_query
        )

    elif order_details.get("qcl_destination_id") == CYX_ID:
        if order_details.get("qcl_order_status") == "CLOSED COMPLETE":
            update_query = {
                "$set": {
                    f"north_transaction_details_qcl_formatted.{i}.qcl_item_status_message": qcl_order_status,
                    f"north_transaction_details_qcl_formatted.{i}.qcl_asset_id": order_details.get(
                        "qcl_order_id"
                    ),
                }
            }
            await doc_db_manager.update_document(
                transaction_table_name, filter_query, update_query
            )
            await transaction_manager.update_transaction_item_state(
                lattice_transaction_id, qcl_inventory_item_id, 500
            )
        else:
            update_query = {
                "$set": {
                    f"north_transaction_details_qcl_formatted.{i}.qcl_item_status_message": qcl_order_status,
                }
            }
            await doc_db_manager.update_document(
                transaction_table_name, filter_query, update_query
            )
            if order_details.get("qcl_order_status") == "CLOSED CANCELLED":
                await transaction_manager.update_transaction_item_state(
                    lattice_transaction_id, qcl_inventory_item_id, 600
                )
        await doc_db_manager.update_document(
            transaction_table_name, filter_query, update_query
        )

    await transaction_manager.update_north_update_state(lattice_transaction_id, True)
    
    
@router.post("/qth/qcl_crossconnect_order")
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
    if generic_data.get("lattice_transaction_id") is None:
        qcl_transaction_id = transaction_manager.generate_lattice_transaaction_id()
    else:
        qcl_transaction_id = generic_data.get("lattice_transaction_id")

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

    transaction_manager.add_new_transaction_data(data)
    log.debug("added transaction data")
    background_tasks.add_task(
        crossconnect_actions.run_async,
        crossconnect_actions.process_cross_connect_order,
        data
    )
    return {"lattice_transaction_id": qcl_transaction_id}


@router.post("/qth/qcl_crossconnect_deinstall")
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
    if generic_data.get("lattice_transaction_id") is None:
        qcl_transaction_id = transaction_manager.generate_lattice_transaaction_id()
    else:
        qcl_transaction_id = generic_data.get("lattice_transaction_id")

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


@router.post("/qth/qcl_crossconnect_move")
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
    if generic_data.get("lattice_transaction_id") is None:
        qcl_transaction_id = (
            transaction_manager.generate_lattice_transaaction_id()
        )
    else:
        qcl_transaction_id = generic_data.get("lattice_transaction_id")
        
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


@router.post("/qth/qcl_crossconnect_cancel")
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
    if generic_data.get("lattice_transaction_id") is None:
        qcl_transaction_id = (
            await transaction_manager.generate_lattice_transaaction_id()
        )
    else:
        qcl_transaction_id = generic_data.get("lattice_transaction_id")
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
