from fastapi_utils.tasks import repeat_every


from app.config import transaction_poll_duration
from app.logger import get_logger
from app.managers.transaction_manager import transaction_manager
from app.managers.doc_db_manager import doc_db_manager
from app.managers.ms2_manager import Ms2Manager
from app.config import transaction_table_name


log = get_logger()


@repeat_every(seconds=transaction_poll_duration)
async def update_transactions_status():
    """
    Iterate over all the users' transactions to check latest status.
    Update the status to north side if there is a new update.
    """
    call_ms2 = Ms2Manager()
    log.info("*****Transactions update iterations started*****")
    order_cc_query = {
        "lattice_organisation_id": "qarbon",
        "lattice_user_id": "qarbon_user",
        "qcl_transaction_type_name": "QCL_CC_ORDER",
    }
    order_cc_transactions_list = await doc_db_manager.get_all_document_by_filter(
        transaction_table_name, order_cc_query
    )
    log.debug(f"data type -> {type(order_cc_transactions_list)}")
    await update_order_cc_transactions_status(order_cc_transactions_list, call_ms2)

    deinstall_cc_query = {
        "lattice_organisation_id": "qarbon",
        "lattice_user_id": "qarbon_user",
        "qcl_transaction_type_name": "QCL_CC_DEINSTALL",
    }
    deinstall_cc_transactions_list = await doc_db_manager.get_all_document_by_filter(
        transaction_table_name, deinstall_cc_query
    )
    await update_deinstall_cc_transactions_status(
        deinstall_cc_transactions_list, call_ms2
    )

    log.info("*****Transactions update iterations completed*****")


async def update_order_cc_transactions_status(
    transactions_list: list, call_ms2: Ms2Manager
):
    log.info("---Checking status update for order crossconnect requests---")
    # # log.debug(f"trans list data type -> {type(transactions_list)}")
    # # log.debug(f"{transactions_list}")
    try:
        for transaction in transactions_list:
            transaction_state = transaction.get("qcl_transaction_state")
            if transaction_state == 0:
                transaction_id = transaction.get("lattice_transaction_id")
                # transaction_state = transaction.get("qcl_transaction_state")
                po_id = transaction.get("north_transaction_id")
                order_data = transaction.get("north_transaction_details_qcl_formatted")
                item_count, item_completed, item_cancelled, item_closed = 0, 0, 0, 0
                order_message = "Order Status: "
                error_message = "Error Info: "
                for order in order_data:
                    # log.debug(f"{type(order)}")
                    item_name = order.get("qcl_inventory_item_name")
                    inventory_item_id = order.get("qcl_inventory_item_id")
                    item_status = order.get("qcl_item_status_message")
                    item_err_msg = order.get("qcl_item_error_message")
                    item_south_order_id = order.get("qcl_south_order_id")
                    north_id = transaction.get("qcl_source_id")
                    is_error = False
                    item_count += 1
                    if order.get("qcl_item_state") == 500:
                        item_completed += 1
                        item_closed += 1
                        order_message += f"[Item: {item_name} OrderID: {item_south_order_id} Status: {item_status}], "
                        data = {
                            "t_id": transaction_id,
                            "item_id": inventory_item_id,
                            "asset_id": order.get("qcl_asset_id"),
                            "po_id": po_id,
                        }
                        if await call_ms2.update_north_item_received(
                            data, transaction_id, north_id
                        ):
                            await transaction_manager.update_transaction_item_state(
                                transaction_id, inventory_item_id, 510
                            )
                        else:
                            await transaction_manager.update_transaction_item_state(
                                transaction_id, inventory_item_id, -510
                            )
                    elif order.get("qcl_item_state") == 510:
                        item_completed += 1
                        item_closed += 1
                        order_message += f"[Item: {item_name}, OrderID: {item_south_order_id}, Status: {item_status}], "
                    elif order.get("qcl_item_state") == 600:
                        item_cancelled += 1
                        item_closed += 1
                        order_message += f"[Item: {item_name}, OrderID: {item_south_order_id}, Status: {item_status}], "
                    elif order.get("qcl_item_state") == 200:
                        order_message += f"[Item: {item_name}, OrderID: {item_south_order_id}, Status: {item_status}], "
                    elif order.get("qcl_item_state") == 100:
                        order_message += (
                            f"[Item: {item_name} Status: Order recevived in Lattice], "
                        )
                    elif order.get("qcl_item_state") < 0:
                        is_error = True
                        error_message += f"{item_name} - {item_err_msg}, "
                        order_message += f"{item_name} - {item_status}, "
                # log.debug(f"Needs north update status: {transaction.get('needs_north_update')}")
                if transaction.get("needs_north_update"):
                    log.info("Needs status update to north side")
                    data = {
                        "t_id": transaction_id,
                        "po_id": po_id,
                        "message": {"status_message": order_message},
                    }
                    if is_error:
                        data["message"]["error_message"] = error_message

                    if await call_ms2.update_po_status_to_north(
                        data, transaction, north_id
                    ):
                        await transaction_manager.update_north_update_state(
                            transaction_id, False
                        )

                if item_count == item_cancelled:
                    await transaction_manager.update_transaction_status(
                        transaction_id, 600
                    )
                    # TODO mark void
                elif item_count == item_closed:
                    await transaction_manager.update_transaction_status(
                        transaction_id, 500
                    )
                    data = {"t_id": transaction_id, "po_id": po_id}
                    if await call_ms2.mark_north_po_complete(
                        data, transaction_id, north_id
                    ):
                        try:
                            await transaction_manager.update_transaction_status(
                                transaction_id, 510
                            )
                            # await transaction_manager.delete_transaction(transaction_id)
                        except:
                            await transaction_manager.update_transaction_status(
                                transaction_id, -510
                            )
                            log.error("Failed to remove transaction from db")

        log.info("---Completed iterating order crossconnect transactions---")
    except Exception as e:
        log.exception(f"Poll order cc transaction exception {e}")


async def update_deinstall_cc_transactions_status(
    transactions_list: list, call_ms2: Ms2Manager
):
    try:
        log.info("---Checking status update for deinstall crossconnect requests---")
        for transaction in transactions_list:
            transaction_state = transaction.get("qcl_transaction_state")
            if transaction_state == 0:
                # log.debug(type(transaction), transaction)
                transaction_id = transaction.get("lattice_transaction_id")
                # transaction_state = transaction.get("qcl_transaction_state")
                po_id = transaction.get("north_transaction_id")
                order_data = transaction.get("north_transaction_details_qcl_formatted")
                item_count, item_completed, item_cancelled, item_closed = 0, 0, 0, 0
                order_message = "Order Status: "
                error_message = "Error Info: "
                for order in order_data:
                    item_name = order.get("qcl_inventory_item_name")
                    inventory_item_id = order.get("qcl_inventory_item_id")
                    item_status = order.get("qcl_item_status_message")
                    item_err_msg = order.get("qcl_item_error_message")
                    item_south_order_id = order.get("qcl_south_order_id")
                    north_id = transaction.get("qcl_source_id")
                    is_error = False
                    item_count += 1
                    if order.get("qcl_item_state") == 500:
                        item_completed += 1
                        item_closed += 1
                        order_message += f"[Item: {item_name} OrderID: {item_south_order_id} Status: {item_status}], "
                        data = {
                            "t_id": transaction_id,
                            "item_id": inventory_item_id,
                        }
                        if await call_ms2.update_north_item_inactive(
                            data, transaction_id, north_id
                        ):
                            await transaction_manager.update_transaction_item_state(
                                transaction_id, inventory_item_id, 510
                            )
                        else:
                            await transaction_manager.update_transaction_item_state(
                                transaction_id, inventory_item_id, -510
                            )
                    elif order.get("qcl_item_state") == 510:
                        item_completed += 1
                        item_closed += 1
                        order_message += f"[Item: {item_name}, OrderID: {item_south_order_id}, Status: {item_status}], "
                    elif order.get("qcl_item_state") == 600:
                        item_cancelled += 1
                        item_closed += 1
                        order_message += f"[Item: {item_name}, OrderID: {item_south_order_id}, Status: {item_status}], "
                    elif (
                        order.get("qcl_item_state") == 200
                        or order.get("qcl_item_state") == 210
                    ):
                        order_message += f"[Item: {item_name}, OrderID: {item_south_order_id}, Status: {item_status}], "
                    elif order.get("qcl_item_state") == 100:
                        order_message += (
                            f"[Item: {item_name}, Status: Order recevived in Lattice], "
                        )
                    elif order.get("qcl_item_state") < 0:
                        is_error = True
                        error_message += f"[Item: {item_name} - {item_err_msg}], "
                        order_message += f"[Item: {item_name} - {item_status}], "

                # log.debug(f"Needs north update status: {transaction.get('needs_north_update')}")
                if transaction.get("needs_north_update"):
                    log.info("Needs status update to north side")
                    data = {
                        "t_id": transaction_id,
                        "ia_id": po_id,
                        "message": {"status_message": order_message},
                    }
                    if is_error:
                        data["message"]["error_message"] = error_message

                    if await call_ms2.update_ia_status_to_north(
                        data, transaction, north_id
                    ):
                        await transaction_manager.update_north_update_state(
                            transaction_id, False
                        )

                if item_count == item_cancelled:
                    await transaction_manager.update_transaction_status(
                        transaction_id, 600
                    )
                elif item_count == item_closed:
                    await transaction_manager.update_transaction_status(
                        transaction_id, 500
                    )

        log.info("---Completed iterating deinstall cc transactions---")

    except Exception as ex:
        log.exception(f"Poll deinstall cc transaction exception {ex}")
