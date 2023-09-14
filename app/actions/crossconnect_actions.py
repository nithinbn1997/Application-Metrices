import requests
import asyncio
from fastapi.responses import Response


from app.managers.transaction_manager import transaction_manager
from app.managers.doc_db_manager import doc_db_manager
from app.config import attachment_table_name
from app.logger import get_logger
from app.url import (
    MS4_EQX_ORDER_CC,
    MS4_EQX_DEINSTALL_CC,
    MS4_EQX_CANCEL_CC,
    MS4_EQX_CC_DETAILS,
    MS4_EQX_CC_LIST,
    MS4_CYX_ORDER_CC,
    MS4_CYX_DEINSTALL_CC,
    MS4_CYX_UPLOAD_LOA,
    MS4_CYX_MOVE_CC,
    MS4_CYX_CC_DETAILS,
    MS4_CYX_CC_LIST,
    MS5_ADD_CC_ORDER,
    MS5_ADD_DEINSTALL_CC_ORDER,
)
from app.constants import EQX_ID, CYX_ID


log = get_logger()


def run_async(func, data):
    asyncio.run(func(data))


async def process_cross_connect_order(order_data):
    """_summary_

    Args:
        order_data (_type_): _description_
    """
    lattice_transaction_id = order_data.get("lattice_transaction_id")
    for item in order_data.get("north_transaction_details_qcl_formatted"):
        qcl_inventory_item_id = item.get("qcl_inventory_item_id")
        data = {
            "lattice_transaction_id": lattice_transaction_id,
            "qcl_inventory_item_id": qcl_inventory_item_id,
            "qcl_cc_details": item.get("qcl_inventory_item_details"),
        }

        if await send_order_request_to_south(
            data, order_data.get("qcl_destination_id")
        ):
            log.info(
                f"[{lattice_transaction_id}] Successfully sent order cross connect request to MS4"
            )
            await transaction_manager.update_transaction_item_state(
                lattice_transaction_id, qcl_inventory_item_id, 100
            )
        else:
            log.error(
                f"[{lattice_transaction_id}] Failed to send order cross connect request to MS4"
            )
            await transaction_manager.update_transaction_item_state(
                lattice_transaction_id, qcl_inventory_item_id, -100
            )
    await transaction_manager.update_north_update_state(lattice_transaction_id, True)


async def send_order_request_to_south(data, dest):
    """_summary_

    Args:
        data (_type_): _description_
        dest (_type_): _description_

    Returns:
        _type_: _description_
    """
    lattice_transaction_id = data.get("lattice_transaction_id")
    log.debug(f"data --------> {data}")
    if dest == EQX_ID:
        log.info(
            f"[{lattice_transaction_id}] Sending order equinix crossconnect request to MS4"
        )
        log.debug(f"url: {MS4_EQX_ORDER_CC}")
        cc_response = requests.post(MS4_EQX_ORDER_CC, json=data)
        if cc_response.status_code == 201:
            return True
        else:
            return False
    elif dest == CYX_ID:
        log.info(
            f"[{lattice_transaction_id}] Sending order cyxtera crossconnect request to MS4"
        )
        attachment_id = (
            data.get("qcl_cc_details").get("qcl_cc_z_side_details").get("qcl_cc_loa_attachment_id")
        )
        log.debug(f"LOA attachment id -> {attachment_id}")
        att_data = {"attachment_id": attachment_id}
        try:
            loa_data = await doc_db_manager.get_attachment(
                attachment_table_name, att_data
            )
            # log.debug(f"loa data -> {loa_data}")
            # log.debug(loa_data)
            attachment_obj = loa_data.get("file_obj")
        except Exception as ex:
            log.exception(f"Failed to get attachment data -> {ex}")
        upload_response = requests.post(
            MS4_CYX_UPLOAD_LOA, data=att_data, files=[("loa", attachment_obj)]
        )
        if upload_response.status_code == 200:
            log.debug("Uploaded attachment to MS4")
        cc_response = requests.post(MS4_CYX_ORDER_CC, json=data)
        if cc_response.status_code == 201:
            return True
        else:
            return False


async def add_cc_order_to_ms5(order_details: dict) -> bool:
    order_details["qcl_asset_id"] = ""
    order_details["qcl_order_status"] = ""
    order_details["qcl_delete_status"] = False
    log.debug(f"Adding order to MS5 for polling: {MS5_ADD_CC_ORDER}")
    response = requests.post(MS5_ADD_CC_ORDER, json=order_details)
    if response.status_code == 200:
        return True
    else:
        return False


async def add_deinstall_order_to_ms5(order_details: dict) -> bool:
    order_details["qcl_order_status"] = ""
    order_details["qcl_delete_status"] = False
    log.info("Adding deinstall order to MS5 for polling")
    log.debug(
        f"Adding deinstall order to MS5 for polling: {MS5_ADD_DEINSTALL_CC_ORDER}"
    )
    log.debug(f"ms5 deinstall data -> {order_details}")
    response = requests.post(MS5_ADD_DEINSTALL_CC_ORDER, json=order_details)
    log.debug(f"ms5 add poll response -> {response.status_code}")
    if response.status_code == 200:
        log.info("Successfully added deinstall order to MS5 for polling")
        return True
    else:
        log.error("Failed to add deinstall order to MS5 for polling")
        return False


async def process_deinstall_order(order_data):
    lattice_transaction_id = order_data.get("lattice_transaction_id")
    for item in order_data.get("north_transaction_details_qcl_formatted"):
        qcl_inventory_item_id = item.get("qcl_inventory_item_id")
        data = {
            "lattice_transaction_id": lattice_transaction_id,
            "qcl_inventory_item_id": qcl_inventory_item_id,
            "qcl_cc_deinstall_details": item.get("qcl_inventory_item_details"),
        }
        if await send_deinstall_request_to_south(
            data, order_data.get("qcl_destination_id")
        ):
            log.info(
                f"[{lattice_transaction_id}] Deinstall CC request to MS4 successfull"
            )
            await transaction_manager.update_transaction_item_state(
                lattice_transaction_id, qcl_inventory_item_id, 100
            )
        else:
            log.error(f"[{lattice_transaction_id}] Deinstall CC request to MS4 failed")
            await transaction_manager.update_transaction_item_state(
                lattice_transaction_id, qcl_inventory_item_id, -100
            )
    await transaction_manager.update_north_update_state(lattice_transaction_id, True)


async def process_cancel_order(order_data):
    lattice_transaction_id = order_data.get("lattice_transaction_id")
    for item in order_data.get("north_transaction_details_qcl_formatted"):
        qcl_inventory_item_id = item.get("qcl_inventory_item_id")
        data = {
            "lattice_transaction_id": lattice_transaction_id,
            "qcl_inventory_item_id": qcl_inventory_item_id,
            "qcl_cc_details": item.get("qcl_inventory_item_details"),
        }

        if await send_cancel_request_to_south(
            data, order_data.get("qcl_destination_id")
        ):
            log.debug("Cancel CC request to MS4 successfull")
            await transaction_manager.update_transaction_item_state(
                lattice_transaction_id, qcl_inventory_item_id, 100
            )
        else:
            log.debug("Cancel CC request to MS4 successfull")
            await transaction_manager.update_transaction_item_state(
                lattice_transaction_id, qcl_inventory_item_id, -100
            )
    await transaction_manager.update_north_update_state(lattice_transaction_id, True)


async def process_move_order(order_data):
    lattice_transaction_id = order_data.get("lattice_transaction_id")
    for item in order_data.get("north_transaction_details_qcl_formatted"):
        qcl_inventory_item_id = item.get("qcl_inventory_item_id")
        data = {
            "lattice_transaction_id": lattice_transaction_id,
            "qcl_inventory_item_id": qcl_inventory_item_id,
            "qcl_cc_details": item.get("qcl_inventory_item_details"),
        }

        if await send_move_request_to_south(data, order_data.get("qcl_destination_id")):
            log.debug("Move CC request to MS4 successfull")
            await transaction_manager.update_transaction_item_state(
                lattice_transaction_id, qcl_inventory_item_id, 100
            )
        else:
            log.debug("Move CC request to MS4 failed")
            await transaction_manager.update_transaction_item_state(
                lattice_transaction_id, qcl_inventory_item_id, -100
            )
    await transaction_manager.update_north_update_state(lattice_transaction_id, True)


async def send_deinstall_request_to_south(data: dict, dest: str) -> bool:
    """
    Send deinstall cross connect request to MS4

    Args:
        data (dict): _description_
        dest (str): _description_

    Returns:
        bool: _description_
    """
    log.debug("Sending order to MS4")
    if dest == EQX_ID:
        log.debug(f"url: {MS4_EQX_DEINSTALL_CC}")
        deinstall_cc_response = requests.post(MS4_EQX_DEINSTALL_CC, json=data)
        if deinstall_cc_response.status_code == 201:
            return True
        else:
            return False
    elif dest == CYX_ID:
        log.debug(f"url: {MS4_CYX_DEINSTALL_CC}")
        deinstall_cc_response = requests.post(MS4_CYX_DEINSTALL_CC, json=data)
        if deinstall_cc_response.status_code == 201:
            return True
        else:
            return False


async def send_move_request_to_south(data, dest):
    """
    Send move cross connect request to MS4

    Args:
        data (_type_): _description_
        dest (_type_): _description_

    Returns:
        _type_: _description_
    """
    log.debug("Sending order to MS4")
    if dest == CYX_ID:
        cc_response = requests.post(MS4_CYX_MOVE_CC, json=data)
        if cc_response.status_code == 201:
            return True
        else:
            return False
    
    elif dest == EQX_ID:
        # move is not supported by Equinix 
        pass
        


async def send_cancel_request_to_south(data, dest):
    """
    Send cancel cross connect request to MS4

    Args:
        data (_type_): _description_
        dest (_type_): _description_

    Returns:
        _type_: _description_
    """
    log.debug("Sending order to MS4")
    if dest == EQX_ID:
        log.debug(f"url: {MS4_EQX_CANCEL_CC}")
        cc_response = requests.post(MS4_EQX_CANCEL_CC, json=data)
        if cc_response.status_code == 201:
            return True
        else:
            return False


def get_cc_details(data: dict):
    """
    Call MS4 to get CC details from south

    Args:
        data (dict): _description_
    """
    dest = data.get("qcl_destination_id")
    qcl_cc_id = data.get("qcl_cc_id")
    try:
        if dest == EQX_ID:
            log.debug(f"Calling MS4 to get EQX cc details -> {MS4_EQX_CC_DETAILS}")
            url = f"{MS4_EQX_CC_DETAILS}/{qcl_cc_id}"
            cc_detail_response = requests.get(url)
        elif dest == CYX_ID:
            log.debug(f"Calling MS4 to get CYX cc details -> {MS4_EQX_CC_DETAILS}")
            url = f"{MS4_CYX_CC_DETAILS}/{qcl_cc_id}"
            cc_detail_response = requests.get(url)

        cc_detail_response = cc_detail_response.json()
        if cc_detail_response.get("status"):
            return cc_detail_response.get("data")
        else:
            return Response(content=cc_detail_response.get("data"), status_code=400)

    except Exception as ex:
        log.exception(f"Error while calling MS4 for CC details -> {ex}")


def get_cc_list(data: dict):
    """
    Call MS4 to get list of CC from south

    Args:
        data (dict): _description_

    Returns:
        tuple: _description_
    """
    dest = data.get("qcl_destination_id")
    try:
        if dest == EQX_ID:
            log.debug(f"Calling MS4 to get EQX cc list -> {MS4_EQX_CC_LIST}")
            cc_list_response = requests.get(MS4_EQX_CC_LIST)
        elif dest == CYX_ID:
            log.debug(f"Calling MS4 to get CYX cc list -> {MS4_CYX_CC_LIST}")
            cc_list_response = requests.get(MS4_CYX_CC_LIST)

        cc_list_response = cc_list_response.json()
        if cc_list_response.get("status"):
            return cc_list_response.get("data")
        else:
            return Response(content=cc_list_response.get("data"), status_code=400)

    except Exception as ex:
        log.exception(f"Error while calling MS4 for CC list -> {ex}")
