from fastapi.testclient import TestClient
from fastapi import HTTPException
from  app.main import app
import requests
import settings

client = TestClient(app)


payload = { "qcl_generic_data_object": {

        "lattice_organisation_id": "org_name",

        "lattice_user_id": "userid",

        "qcl_category": "accounting",

        "qcl_sub_category": "crossconnect",

        "qcl_transaction_data": {

        "qcl_transaction_type_number": "005010001012",

        "qcl_transaction_type_name": "QCL_ORDER_CC"

    },

    "qcl_source_id": "k",

    "qcl_destination_id": "EQX"

},

"qcl_transaction_specific_data_object": {

    "generic_fields": {},

    "source_specific_fields": {

    "qcl_po_id": "4182712000000183000",

    "qcl_item_details": [

        {

        "qcl_inventory_item_id": "4182712000000084077",

        "qcl_inventory_item_name": "Cross Connect",

        "qcl_crossconnect_details": {

 

                "qcl_cc_a_side_details": {

                    "qcl_cc_a_side_patch_panel_id": "PP:0632:1320739",

                    "qcl_cc_connection_service": "SINGLE_MODE_FIBRE",

                    "qcl_cc_media_type": "SINGLE_MODE_FIBRE",

                    "qcl_cc_protocol_type": "STM-64",

                    "qcl_cc_connector_type": "SC",

                    "qcl_cc_patch_panel_port_a": "7",

                    "qcl_cc_patch_panel_port_b": "3"

                },

                "qcl_cc_z_side_details": {

                    "qcl_cc_z_side_patch_panel_id":"PP:0203:1216125",

                    "qcl_cc_connector_type": "SC",

                    "qcl_cc_patch_panel_port_a": "2",

                    "qcl_cc_patch_panel_port_b": "7"

                }

           

        }

        }

    ]

    },

    "destination_specific_fields": {}

}

}


# def test_process_crossconnect_order1():
#     endpoint = settings.API_BASE_URL + settings.ORDER_SUB_URL
#     reponse = requests.post(endpoint, json=payload)
#     assert reponse.status_code == 404
#     assert reponse.json() == {"detail" : "Not Found"}


# def test_process_crossconnect_order():
#     endpoint = settings.API_BASE_URL + settings.DEINSTALL_ORDER_SUB_URL
#     reponse = requests.post(endpoint, json=payload)
#     assert reponse.status_code == 200
#     payload["qcl_generic_data_object"]["qcl_source_id"] == "ZOH"
#     payload["qcl_generic_data_object"]["qcl_source_id"] == "ONS"
#     payload["qcl_generic_data_object"]["qcl_destination_id"] == "EQX"
#     payload["qcl_generic_data_object"]["qcl_destination_id"] == "CYX"