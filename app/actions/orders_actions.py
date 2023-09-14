import requests
from fastapi.responses import Response


from app.logger import get_logger
from app.constants import EQX_ID, CYX_ID
from app.url import (
    MS4_EQX_ORDER_DETAILS,
    MS4_EQX_ORDER_LIST,
    MS4_CYX_ORDER_DETAILS,
    MS4_CYX_ORDER_LIST,
)


log = get_logger()


def get_order_details(data: dict):
    """
    Call MS4 to get order details from south

    Args:
        data (dict): _description_
    """
    dest = data.get("qcl_destination_id")
    qcl_order_id = data.get("qcl_order_id")
    try:
        if dest == EQX_ID:
            url = f"{MS4_EQX_ORDER_DETAILS}/{qcl_order_id}"
            order_detail_response = requests.get(url)
        elif dest == CYX_ID:
            url = f"{MS4_CYX_ORDER_DETAILS}/{qcl_order_id}"
            order_detail_response = requests.get(url)

        order_detail_response = order_detail_response.json()
        if order_detail_response.get("status"):
            return order_detail_response.get("data")
        else:
            return Response(content=order_detail_response.get("data"), status_code=400)

    except Exception as ex:
        log.exception(f"Error while calling MS4 for order details -> {ex}")


def get_order_list(data: dict):
    """
    Call MS4 to get list of orders from south

    Args:
        data (dict): _description_

    Returns:
        tuple: _description_
    """
    dest = data.get("qcl_destination_id")
    try:
        if dest == EQX_ID:
            order_list_response = requests.get(MS4_EQX_ORDER_LIST)
        elif dest == CYX_ID:
            order_list_response = requests.get(MS4_CYX_ORDER_LIST)

        order_list_response = order_list_response.json()
        if order_list_response.get("status"):
            return order_list_response.get("data")
        else:
            return Response(content=order_list_response.get("data"), status_code=400)

    except Exception as ex:
        log.exception(f"Error while calling MS4 for order list -> {ex}")
