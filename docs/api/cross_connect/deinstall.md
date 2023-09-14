# Deinstall <small style="color: green;">POST</small>

## Deinstall Cross Connect API

<span style="color: green;">POST</span>  
`/v1/accounting/crossconnect/qcl_crossconnect_deinstall`

Deinstall an existing cross connect order

### **REQUEST**

#### **Path Parameters**
!!! note ""
    None

#### **Query Parameters**
!!! note ""
    None

#### **Request Body** (application/json)

=== "Schema"
    |Field|Type|Description|
    |----:|:-----:|:------|
    |qcl_generic_data<large style="color: red;">*</large>|dictionary|These are the common fields which are not specific to source or destination. E.g. time_initiated, lattice_username, etc.|
    |qcl_source_id<large style="color: red;">*</large>|string|An identifier indicating the source from which the transaction originated(North).|
    |qcl_destination_id<large style="color: red;">*</large>|string|An identifier indicating the destination to which the transaction is directed(south)|
    |source_fields<large style="color: red;">*</large>|dictionary|A dictionary containing data specific to the source specific fields of the transaction.|
    |qcl_ia_id<large style="color: red;">*</large>|string|An identifier (ia_id) associated with the inventory adjustment relevant to the transaction in the Lattice system|
    |qcl_item_details<large style="color: red;">*</large>|list of objects|Details about the specific item being transacted, including qcl-translated and original details.|
    |qcl_inventory_item_id<large style="color: red;">*</large>|string|An id for the inventory item of a particular IA|
    |qcl_inventory_item_name<large style="color: red;">*</large>|string|The name (Cross Connect) of the inventory item of a particular IA|
    |qcl_cc_deinstall_details<large style="color: red;">|dictionary|Deinstall details|
    |qcl_cc_deinstall_id<large style="color: red;">*</large>|string|deinstall id: Incase of EQX it is asset id where as in case of CYX it is order id|
    |qcl_cc_removal_date<large style="color: red;">*</large>|string| Requested date **YYYY-MM-DD** for the deinstall completion|
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
                "qcl_ia_id": "string",
                "qcl_item_details": [
                    {
                        "qcl_inventory_item_id": "string",
                        "qcl_inventory_item_name": "string",
                        "qcl_cc_deinstall_details": {
                            "qcl_cc_deinstall_id": "string",
                            "qcl_cc_removal_date": "string"
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


=== "Example(Cyxtera)"
    ```json
    {
        "qcl_generic_data": {
            "qcl_source_id": "ZOH",
            "qcl_destination_id": "CYX"
        },
        "qcl_transaction_data": {
            "generic_fields": {
            },
            "source_fields": {
                "qcl_ia_id": "4182712000000214073",
                "qcl_item_details": [
                    {
                        "qcl_inventory_item_id": "4182712000000084077",
                        "qcl_inventory_item_name": "Cross Connect",
                        "qcl_cc_deinstall_details": {
                            "qcl_cc_deinstall_id": "aca458f5475c71d09c522ae3846d435f",
                            "qcl_cc_removal_date": "2023-08-30"
                        }
                    }
                ]
            },
            "destination_fields": {}
        }
    }
    ```

=== "Example(Equinix)"
    ```json
    {
        "qcl_generic_data": {
            "qcl_source_id": "ONS",
            "qcl_destination_id": "EQX"
        },
        "qcl_transaction_data": {
            "generic_fields": {
            },
            "source_fields": {
                "qcl_ia_id": "4182712000000214073",
                "qcl_item_details": [
                    {
                        "qcl_inventory_item_id": "4182712000000084077",
                        "qcl_inventory_item_name": "Cross Connect",
                        "qcl_cc_deinstall_details": {
                            "qcl_cc_deinstall_id": "aca458f5475c71d09c522ae3846d435f",
                            "qcl_cc_removal_date": "2023-08-30"
                        }
                    }
                ]
            },
            "destination_fields": {}
        }
    }
    ```
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