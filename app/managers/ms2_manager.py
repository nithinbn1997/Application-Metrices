import requests

from app.constants import ZOH_ID, ONS_ID
from app.logger import get_logger
from app.url import (
    MS2_ONS_UPDATE_PO_STATUS,
    MS2_ONS_UPDATE_IA_STATUS,
    MS2_ONS_MARK_ONS_PO_COMPLETE,
    MS2_ONS_MARK_ITEM_RECEIVED,
    MS2_ONS_MARK_ITEM_INACTIVE,
    MS2_ZOHO_UPDATE_PO_STATUS,
    MS2_ZOHO_UPDATE_IA_STATUS,
    MS2_ZOHO_MARK_ITEM_RECEIVED,
    MS2_ZOHO_MARK_ITEM_INACTIVE
)

log = get_logger()

class Ms2Manager():
    async def update_north_item_received(self, data : dict, transaction_id : str, north_id : str) -> bool:
        """
        Update status of item as received in north and update order/asset id

        Args:
            data (dict): Item details for marking received
            transaction_id (str): lattice transaction id
            north_id (str): QCL north id

        Returns:
            bool: True if item marked received, else false
        """    
        if north_id == ONS_ID:
            log.info(f"[{transaction_id}] Sending Request to MS2 to"
                     "mark PO item received in ONS")
            log.debug(f"[{transaction_id}] Sending mark PO item received "
                      f"to MS2 for ONS -> {MS2_ONS_MARK_ITEM_RECEIVED}")
            
            response = requests.post(MS2_ONS_MARK_ITEM_RECEIVED, json=data)
            if response.status_code == 200:
                log.debug("MS2 ONS mark item received successful")
                return True
            else:
                log.error("MS2 ONS mark item received failed")
                return False
        
        elif north_id == ZOH_ID:
            log.info(f"[{transaction_id}] Sending Request to MS2 to"
                     "mark PO item received in ZOHO")
            log.debug(f"[{transaction_id}] Sending mark PO item complete "
                      f"to MS2 for ZOHO -> {MS2_ZOHO_MARK_ITEM_RECEIVED}")
            
            response = requests.post(MS2_ZOHO_MARK_ITEM_RECEIVED, json=data)
            if response.status_code == 200:
                log.debug("MS2 ZOHO mark item received successful")
                return True
            else:
                log.debug("MS2 ZOHO mark item received failed")
                return False

    async def mark_north_po_complete(self, data : dict, transaction_id : str, north_id : str) -> bool:
        """
        Update north side transaction(PO) to complete state

        Args:
            data (dict): PO details to mark PO complete
            transaction_id (str): lattice transaction id
            north_id (str): QCL north id

        Returns:
            bool: True if PO was marked complete, else false
        """
        log.debug(f"[{transaction_id}] Updating PO status to complete")
        log.debug(f"[{transaction_id}] data -> {data}")
        if north_id == ONS_ID:
            log.info(f"[{transaction_id}] Sending Request to MS2 to"
                     "mark PO complete in ONS")
            log.debug(f"[{transaction_id}] Sending mark PO complete "
                      f"to MS2 for ONS -> {MS2_ONS_MARK_ONS_PO_COMPLETE}")
            
            response = requests.post(MS2_ONS_MARK_ONS_PO_COMPLETE, json=data)
            if response.status_code == 200:
                log.debug("MS2 mark PO complete successful")
                return True
            else:
                log.error("MS2 mark PO complete failed")
                return False
        # elif north_id == ZOH_ID:
        #     log.debug(f"[{transaction_id}] Sending mark PO complete to "
        #               "MS2 for ZOHO -> {MS2_MARK_ZOHO_PO_COMPLETE}")
        #     response = requests.post(MS2_MARK_ZOHO_PO_COMPLETE, json=data)
        #     if response.status_code == 200:
        #         log.debug(response.json())
        #         return True
        #     else:
        #         return False

    async def update_po_status_to_north(self, data : dict, transaction_id : str, north_id : str) -> bool:
        """
        Update the PO status to north side.

        Args:
            data (dict): status message and error message
            transaction_id (str): lattice transaction id
            north_id (str): QCL north id

        Returns:
            bool: True if status was updated successfully, else False
        """    
        # log.debug(f"Calling MS2 API {MS2_UPDATE_ONS_PO_STATUS}")
        log.debug(f"[{transaction_id}] Updating status message to north")
        log.debug(f"[{transaction_id}] data -> {data}")
        if north_id == ONS_ID:
            log.info(f"[{transaction_id}] Sending Request to MS2 to"
                     "update PO status in ONS")
            log.debug(f"[{transaction_id}] Sending status update "
                      f"to MS2 for ONS -> {MS2_ONS_UPDATE_PO_STATUS}")
            
            response = requests.post(MS2_ONS_UPDATE_PO_STATUS, json=data)
            if response.status_code == 200:
                log.debug(response.json())
                return True
            else:
                return False
        elif north_id == ZOH_ID:
            log.info(f"[{transaction_id}] Sending Request to MS2 to"
                     "update PO status in ZOHO")
            log.debug(f"[{transaction_id}] Sending status update to "
                      f"MS2 for ZOHO -> {MS2_ZOHO_UPDATE_PO_STATUS}")
            
            response = requests.post(MS2_ZOHO_UPDATE_PO_STATUS, json=data)
            if response.status_code == 200:
                log.debug(response.json())
                return True
            else:
                return False
            

    async def update_ia_status_to_north(self, data : dict, transaction_id : str, north_id : str) -> bool:
        """
        Update the IA status to north side.

        Args:
            data (dict): status message and error message
            transaction_id (str): lattice transaction id
            north_id (str): QCL north id

        Returns:
            bool: True if status was updated successfully, else False
        """    
        # log.debug(f"Calling MS2 API {MS2_UPDATE_ONS_PO_STATUS}")
        log.info(f"[{transaction_id}] Sending Request to MS2 to"
                     "update IA status in ONS")
        log.debug(f"[{transaction_id}] Updating IA status message to north")
        log.debug(f"[{transaction_id}] data -> {data}")
        if north_id == ONS_ID:
            log.debug(f"[{transaction_id}] Sending IA status update to "
                      f"MS2 for ONS -> {MS2_ONS_UPDATE_IA_STATUS}")
            
            response = requests.post(MS2_ONS_UPDATE_IA_STATUS, json=data)
            if response.status_code == 200:
                log.debug(response.json())
                return True
            else:
                return False
        elif north_id == ZOH_ID:
            log.info(f"[{transaction_id}] Sending Request to MS2 to"
                     "update IA status in ZOHO")
            log.debug(f"[{transaction_id}] Sending IA status update to "
                      f"MS2 for ZOHO -> {MS2_ZOHO_UPDATE_IA_STATUS}")
            
            response = requests.post(MS2_ZOHO_UPDATE_IA_STATUS, json=data)
            if response.status_code == 200:
                log.debug(response.json())
                return True
            else:
                return False
            
    
    async def update_north_item_inactive(self, data : dict, transaction_id : str, north_id : str) -> bool:
        """
        Update status of item as inactive in north and update order/asset id

        Args:
            data (dict): Item details for marking inactive
            transaction_id (str): lattice transaction id
            north_id (str): QCL north id

        Returns:
            bool: True if item marked inactive, else false
        """    
        if north_id == ONS_ID:
            log.info(f"[{transaction_id}] Sending Requesto to MS2 for"
                     "marking ONS item inactive")
            log.debug(f"[{transaction_id}] Sending mark PO item inactive to "
                      f"MS2 for ONS -> {MS2_ONS_MARK_ITEM_INACTIVE}")
            try:
                response = requests.post(MS2_ONS_MARK_ITEM_INACTIVE, json=data)
                if response.status_code == 200:
                    log.debug("Successfully marked item inactive in ONS")
                    return True
                else:
                    log.error("Failed to marked item inactive in ONS")
                    return False
            except Exception as ex:
                log.exception(f"Failed to call MS2 to mark item inactive. Error -> {ex}")
        
        elif north_id == ZOH_ID:
            log.info(f"[{transaction_id}] Sending Requesto to MS2 for"
                     "marking ZOHO item inactive")
            log.debug(f"[{transaction_id}] Sending mark PO item inactive "
                      f"to MS2 for ZOHO -> {MS2_ZOHO_MARK_ITEM_INACTIVE}")
            
            response = requests.post(MS2_ZOHO_MARK_ITEM_INACTIVE, json=data)
            if response.status_code == 200:
                log.debug("Successfully marked item inactive in ZOHO")
                return True
            else:
                log.error("Failed to marked item inactive in ZOHO")
                return False
