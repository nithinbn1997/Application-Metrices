# Move <small style="color: green;">POST</small>

## Move Cross Connect API

<span style="color: green;">POST</span>  
`/v1/accounting/crossconnect/qcl_crossconnect_move`

Move a cross connect order

### **REQUEST**

#### **Path Parameters**
!!! note ""
    None

#### **Query Parameters**
!!! note ""
    None

#### **Request Body** (application/json)

!!! note
    Equinix doesn't support move transaction

!!! tip
    * If the move type is z-side and the datacenter requires LOA(Letter of Authorization), use attachment API to upload pdf.
    And use the `attachment_id` as `qcl_loa_attachment_id`  
    * A-side move do not require LOA.


=== "Schema"
    |Field|Type|Description|
    |--:|:--:|:--|
    |qcl_generic_data<large style="color: red;">*</large>|dictionary|These are the common fields which are not specific to source or destination. E.g. time_initiated, lattice_username, etc.|
    |qcl_source_id<large style="color: red;">*</large>|string|An identifier indicating the source from which the transaction originated(North).|
    |qcl_destination_id<large style="color: red;">*</large>|string|An identifier (CYX) indicating the destination to which the transaction is directed.|
    |qcl_transaction_data<large style="color: red;">*</large>|dictionary|A dictionary containing transaction-specific data.|
    |generic_fields<large style="color: red;">*</large>|dictionary|A dictionary containing generic fields associated with the transaction.|
    |source_fields<large style="color: red;">*</large>|dictionary|A dictionary containing source-specific fields related to the transaction.|
    |qcl_cc_move_type|string|The type of move (a-side/z-side)associated with the cross-connect.|
    |qcl_cc_port_id|string|The identifier of the port associated with the cross-connect.|
    |qcl_cc_id|string|An identifier associated with the cross-connect.|
    |qcl_cc_loa_attachment_id| string| A unique attachment id given when file uploaded via upload attachment API |
    |qcl_cc_move_request_date|string|The date **YYYY-MM-DD** when the request to move the cross-connect was initiated.|
    |original_item_details|dictionary|Details related to the original item details before conversion in the transaction.(if this API is called from MS1 )|
    |destination_fields|dictionary|A dictionary containing data specific to the destination of the transaction.|



=== "Example [Cyxtera]"
    <pre>
    ```json
    {
        "qcl_generic_data": {
            "qcl_source_id": "ONS",
            "qcl_destination_id": "CYX"
        },
        "qcl_transaction_data": {
            "generic_fields": {
            },
            "source_fields": {
                "qcl_cc_move_type": "a",
                "qcl_cc_port_id": "12",
                "qcl_cc_id": "123456",
                "qcl_cc_loa_attachment_id": "a6c17b151baec99064ca0e93cc4bcbd2",
                "qcl_cc_move_request_date": "2023-08-23"
            },
            "destination_fields": {}
        }
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
    Message: Internal Server Error