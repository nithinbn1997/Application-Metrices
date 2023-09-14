# Details <small style="color: green;">POST</small>

## Details Order API

<span style="color: green;">POST</span>  
`/v1/accounting/orders/qcl_order_details`

Get Details of a Order

### **REQUEST**

#### **Path Parameters**
!!! note ""
    None

#### **Query Parameters**
!!! note ""
    None

#### **Request Body (application/json)**

=== "Schema"
    | Field        | Type           | Description   |
    | ---------: | :------------: | :------------ |
    |qcl_generic_data<large style="color: red;">*</large>|    dictionary      |      These are the common fields which are not specific to source or destination. E.g. time_initiated, lattice_username, etc.    |
    |qcl_source_id<large style="color: red;">*</large>|enum|An identifier indicating the source(north)  from which the transaction originated.Ex: <ul><li>ONS for Net Suite</li><li>ZOH for Zoho</li></ul>|
    |qcl_destination_id<large style="color: red;">*</large>|enum|An identifier indicating the destination to which the transaction is directed(south). Ex: <ul><li>EQX for Equinix</li><li>CYX for Cyxtera</li></ul>|
    |qcl_transaction_data<large style="color: red;">*</large>|dictionary|Data specific to a transaction in the Lattice|
    |generic_fields|dictionary|A dictionary containing generic fields associated with the item details.|
    |source_fields<large style="color: red;">*</large>|dictionary|A dictionary containing data specific to the source specific fields of the transaction.|
    |qcl_order_id<large style="color: red;">*|string|id of the order details you want to fetch|
    |destination_fields|dictionary|Fields containing information specific to the destination(south) of the transaction, if applicable|

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
                "qcl_order_id" : "string"
            },
            "destination_fields": {}
        }
    }
    ```
    </pre>


=== "Example(Cyxtera)"
    <pre>
    ```json
    {
        "qcl_generic_data": {
            "qcl_source_id": "ONS",
            "qcl_destination_id": "CYX"
        },
        "qcl_transaction_data": {
            "generic_fields": {},
            "source_fields": {
                "qcl_order_id" : "123fa1f4478131d09c522ae3846d4354"
            },
            "destination_fields": {}
        }
    }
    ```
    </pre>

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
                "qcl_order_id" : "1-226966307872"
            },
            "destination_fields": {}
        }
    }
    ```
    </pre>

## RESPONSE

=== "201"

    HTTP Status Code: <large style="color: green;">200</large>  
    Response object as per DataCenter

=== "400"
    HTTP Status Code: <large style="color: red;">400</large><br>
    Error Codes as per DataCenter

=== "500"
    HTTP Status Code: <large style="color: red;">500</large><br>
    Internal Server Error