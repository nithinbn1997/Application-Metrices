# Order <small style="color: green;">POST</small>

## Order Cross Connect API

<span style="color: green;">POST</span>  
`/v1/accounting/crossconnect/qcl_crossconnect_order`

Order a Cross Connect Order

### **REQUEST**

#### **Path Parameters**
!!! note ""
    None

#### **Query Parameters**
!!! note ""
    None

#### **Request Body** (application/json)

!!! tip
    If the datacenter requires LOA(Letter of Authorization) attachment for creating cross connect order, use attachment API to upload pdf.
    And use the `attachment_id` as `qcl_loa_attachment_id` 

=== "Schema"
    | Field        | Type           | Description   |
    | ---------: | :------------: | :------------ |
    |qcl_generic_data<large style="color: red;">*</large>|    dictionary      |      These are the common fields which are not specific to source or destination. E.g. time_initiated, lattice_username, etc.|
    |qcl_source_id<large style="color: red;">*</large>|enum|An identifier indicating the source(north)  from which the transaction originated.Ex: <ul><li>ONS for Net Suite</li><li>ZOH for Zoho</li></ul>|
    |qcl_destination_id<large style="color: red;">*</large>|enum|An identifier indicating the destination to which the transaction is directed(south). Ex: <ul><li>EQX for Equinix</li><li>CYX for Cyxtera</li></ul>|
    |qcl_transaction_data<large style="color: red;">*</large>|dictionary|Data specific to a transaction in the Lattice|
    |generic_fields|dictionary|A dictionary containing generic fields associated with the item details.|
    |source_fields<large style="color: red;">*</large>|dictionary|A dictionary containing data specific to the source specific fields of the transaction.|
    |qcl_po_id<large style="color: red;">*</large>|string|An identifier (po_id) associated with the purchase order relevant to the transaction in the Lattice system|
    |qcl_item_details<large style="color: red;">*</large>|list of object|Details about the specific item being transacted, including qcl-translated and original details.|
    |qcl_inventory_item_id<large style="color: red;">*</large>|string|An id for the inventory item of a particular PO|
    |qcl_inventory_item_name<large style="color: red;">*</large>|string|The name (Cross Connect) of the inventory item of a particular PO within the Lattice system.|
    |qcl_crossconnect_details<large style="color: red;">*</large>|dictionary|Specific information about the cross-connect item, including details about both the "A side", "Z side", or any other depending on the South of the connection.|
    |qcl_cc_request_date|string|The date **YYYY-MM-DD** when the request to move the cross-connect was initiated. Mandatory for cyxtera|
    |qcl_cc_a_side_details<large style="color: red;">*</large>|string|Details related to the "A side" of the cross-connect, including connection service, media type, protocol type, connector type, and patch panel port details etc.|
    |qcl_cc_account_id|string|Account Id (4bcead931bc4a4102ea7a60abc4bcb77) of "A side" of the cross-connect. Mandatory for cyxtera|
    |qcl_cc_pod_id|string|Pod Id (8e72a4d0db35d30057d69c78db96194d) of "A side" of the cross-connect. Mandatory for cyxtera|
    |qcl_cc_model_id|string|Model Id (b696079bdbdd5740f9889274db961906) of "A side" of the cross-connect. Mandatory for cyxtera  |
    |qcl_cc_port_id|string|Port Id (a6c17b151baec99064ca0e93cc4bcbd2) of "A side" of the cross-connect. Mandatory for cyxtera|
    |qcl_cc_a_side_patch_panel_id|string|Patch panel of the of "A side" of the cross-connect. Mandatory for Equinix |
    |qcl_cc_connection_service|string|The type of connection service (SINGLE_MODE_FIBER) associated with the "A side" of the cross-connect. Mandatory for Equinix|
    |qcl_cc_media_type|string|The type of media (SINGLE_MODE_FIBER) used for the connection on the "A side" of the cross-connect. Mandatory for Equinix|
    |qcl_cc_protocol_type|string|The protocol type (STM-64) used for the connection on the "A side" of the cross-connect.  Mandatory for Equinix|
    |qcl_cc_connector_type|string|The type of connector (SC) used for the connection on the "A side" of the cross-connect.  Mandatory for Equinix|
    |qcl_cc_patch_panel_port_a|integer|The port number (1) on the patch panel corresponding to the "A side" of the cross-connect. Optional for Equinix|
    |qcl_cc_patch_panel_port_b|integer|The port number (2) on the patch panel corresponding to the "A side" of the cross-connect.Optional for Equinix|
    |qcl_cc_z_side_details<large style="color: red;">*</large>|string|Details related to the "Z side" of the cross-connect, including patch panel ID, connector type, and patch panel port details|
    |qcl_cc_z_side_patch_panel_id|string|The identifier (17K7R1SH1) of the patch panel on the "Z side" of the cross-connect.  Mandatory for Equinix|
    |qcl_cc_z_side_provider_name|string| Z Side provider name (Lumen). Mandatory for cyxtera|
    |qcl_cc_loa_attachment_id| string| A unique attachment id given when file uploaded via upload attachment API. Mandatory for cyxtera |
    |qcl_cc_connector_type|string|The type of connector (SC) used for the connection on the "Z side" of the cross-connect. Mandatory for Equinix|
    |qcl_cc_patch_panel_port_a|integer|The port number (3) on the patch panel corresponding to the "Z side" of the cross-connect. Optional for Equinix|
    |qcl_cc_patch_panel_port_b|integer|The port number (4) on the patch panel corresponding to the "Z side" of the cross-connect. Optional for Equinix|
    |original_item_details|dictionary|Details related to the original item details before conversion in the transaction.(if this API is called from MS1 )|
    |destination_fields|dictionary|Fields containing information specific to the destination(south) of the transaction, if applicable.|

=== "Example Schema"
    <pre>
    ```json
    {
        "qcl_generic_data": {
            "qcl_source_id": "enum",
            "qcl_destination_id": "enum"
        },
        "qcl_transaction_data": {
            "generic_fields": {},
            "source_fields": {
                "qcl_po_id": "string",
                "qcl_item_details": [
                    {
                        "qcl_inventory_item_id": "string",
                        "qcl_inventory_item_name": "string",
                        "qcl_crossconnect_details": {
                            "qcl_cc_request_date": "string",
                            "qcl_cc_a_side_details": {
                                "qcl_cc_account_id": "string",
                                "qcl_cc_pod_id": "string",
                                "qcl_cc_model_id": "string",
                                "qcl_cc_port_id": "string",
                                "qcl_cc_a_side_patch_panel_id": "string",
                                "qcl_cc_connection_service": "string",
                                "qcl_cc_media_type": "string",
                                "qcl_cc_protocol_type": "string",
                                "qcl_cc_connector_type": "string",
                                "qcl_cc_patch_panel_port_a": "string",
                                "qcl_cc_patch_panel_port_b": "string"
                            },
                            "qcl_cc_z_side_details": {
                                "qcl_cc_z_side_patch_panel_id": "string",
                                "qcl_cc_connector_type": "string",
                                "qcl_cc_patch_panel_port_a": "string",
                                "qcl_cc_patch_panel_port_b": "string",
                                "qcl_cc_z_side_provider_name": "string",
                                "qcl_cc_loa_attachment_id": "string"
                            }
                        },
                        "original_item_details": [
                            "string"
                        ]
                    }
                ]
            },
            "destination_fields": {}
        }
    }
    ```
    </pre>


=== "Example (Cyxtera)"
    <pre>
    ```json
    {
        "qcl_generic_data": {
            "qcl_source_id": "ZOH",
            "qcl_destination_id": "CYX"
        },
        "qcl_transaction_data": {
            "generic_fields": {},
            "source_fields": {
                "qcl_po_id": "4182712000000183000",
                "qcl_item_details": [
                    {
                        "qcl_inventory_item_id": "4182712000000084077",
                        "qcl_inventory_item_name": "Cross Connect",
                        "qcl_crossconnect_details": {
                            "qcl_cc_request_date": "2023-08-30",
                            "qcl_cc_a_side_details": {
                                "qcl_cc_account_id": "4bcead931bc4a4102ea7a60abc4bcb77",
                                "qcl_cc_pod_id": "8e72a4d0db35d30057d69c78db96194d",
                                "qcl_cc_model_id": "b696079bdbdd5740f9889274db961906",
                                "qcl_cc_port_id": "a6c17b151baec99064ca0e93cc4bcbd2"
                            },
                            "qcl_cc_z_side_details": {
                                "qcl_cc_z_side_provider_name": "Lumen",
                                "qcl_cc_loa_attachment_id": "a6c17b151baec99064ca0e93cc4bcbd2"
                            }
                        }
                    }
                ]
            },
            "destination_fields": {}
        }
    }
    ```
    </pre>

=== "Example (Equinix)"
    <pre> 
    ```json
    {
        "qcl_generic_data": {
            "qcl_source_id": "ONS",
            "qcl_destination_id": "EQX"
        },
        "qcl_transaction_data": {
            "generic_fields": {},
            "source_fields": {
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
                                "qcl_cc_z_side_patch_panel_id": "PP:0203:1216125",
                                "qcl_cc_connector_type": "SC",
                                "qcl_cc_patch_panel_port_a": "2",
                                "qcl_cc_patch_panel_port_b": "7"
                            }
                        }
                    }
                ]
            },
            "destination_fields": {}
        }
    }
    ```
    </pre>

### **RESPONSE**

=== "201"

    HTTP Status Code: <large style="color: green;">201</large>

    === "Schema"

        | Field                 | Type   | Description          |
        | --------------------: | :----: | :------------------- |
        | lattice_transaction_id| string | Unique Transaction ID|

    === "Example"
        <pre>
        ```json
        {
            "lattice_transaction_id" : "a6c17b151baec99064ca0e93cc4bcbd2"
        }
        ```

=== "400"
    HTTP Status Code: <large style="color: red;">400</large><br>
    Error Codes

=== "422"
    HTTP Status Code: <large style="color: red;">422</large><br>
    Data Validation Error

=== "500"
    HTTP Status Code: <large style="color: red;">500</large><br>
    Internal Server Error
