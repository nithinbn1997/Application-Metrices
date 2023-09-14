# Cancel <small style="color: green;">POST</small>

## Cancel Cross Connect API

<span style="color: green;">POST</span>  
`/v1/accounting/crossconnect/qcl_crossconnect_cancel`

Cancel an ongoing cross connect order

### **REQUEST**

#### **Path Parameters**
!!! note ""
    None

#### **Query Parameters**
!!! note ""
    None

#### **Request Body** (application/json)

!!! note
    Cyxtera doesn't support cancel transaction

=== "Schema"
    | Field        | Type           | Description   |
    | ---------: | :------------: | :------------ |
    |qcl_generic_data<large style="color: red;">*</large>|    dictionary      |      These are the common fields which are not specific to source or destination. E.g. time_initiated, lattice_username, etc.    |
    |qcl_source_id<large style="color: red;">*</large>|enum|An identifier indicating the source(north)  from which the transaction originated.Ex: <ul><li>ONS for Net Suite</li><li>ZOH for Zoho</li></ul>|
    |qcl_destination_id<large style="color: red;">*</large>|enum|An identifier indicating the destination to which the transaction is directed(south). Ex: <ul><li>EQX for Equinix</li><li>CYX for Cyxtera</li></ul>|
    |qcl_transaction_data<large style="color: red;">*</large>|dictionary||
    |generic_fields|dictionary|A dictionary containing generic fields associated with the item details.|
    |source_fields<large style="color: red;">*</large>|dictionary|A dictionary containing data specific to the source specific fields of the transaction.|
    |qcl_ia_id<large style="color: red;">*</large>|string|An identifier (ia_id) associated with the inventory adjustment relevant to the transaction in the Lattice system|
    |qcl_item_details<large style="color: red;">*</large>|list of objects|Details about the specific item being transacted, including qcl-translated and original details.|
    |qcl_cc_inventory_item_id<large style="color: red;">*</large>|string|An id for the inventory item of a particular PO within the Lattice system.|
    |qcl_cc_inventory_item_name<large style="color: red;">*</large>|string|The name (Cross Connect) of the inventory item of a particular PO within the Lattice system.|
    |original_item_details|dictionary|Details related to the original item details before conversion in the transaction.(if this API is called from MS1 )|
    |destination_fields|dictionary|Fields containing information specific to the destination(south) of the transaction, if applicable.|

=== "Example(Equinix)"
    <pre>
    ```json
    {
        "qcl_generic_data": {
            "qcl_source_id": "ZOH",
            "qcl_destination_id": "EQX"
        },
        "qcl_transaction_data": {
            "generic_fields": {},
            "source_fields": {
            "qcl_ia_id": "4182712000000183000",
            "qcl_item_details": [
                {
                "qcl_cc_inventory_item_id": "4182712000000084077",
                "qcl_cc_inventory_item_name": "Cross Connect"
                }
            ],
            }
        },
        "destination_fields": {}
    }
    ```
    </pre>


## RESPONSE

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