# Delete <small style="color: red;">DELETE</small>

## Attachment Upload API

<span style="color: green;">DELETE</span>  
`/v1/attachments/delete/{attachment_id}`

Attachment Upload API for generic file uploads. Example: Letter of authorization(LOA) for cyxtera.

### **REQUEST**

#### **Path Parameters**
!!! note ""
    |Field|Type|Description|
    |---:|:---:|:---|
    |attachment_id|string|attachment id to be deleted|

#### **Query Parameters**
!!! note ""
    None

#### **Request Body** (application/json)

!!! note ""
    None

## RESPONSE

=== "204"

    HTTP Status Code: <large style="color: green;">204</large>

    === "Schema"

        | Field                 | Type   | Description          |
        | --------------------: | :----: | :------------------- |
        | attachment_id| string | attachment ID of the deleted file|

    === "Example"
        <pre>
        ```json
        {
            "attachment_id" : "a6c17b151baec99064ca0e93cc4bcbd2"
        }
        ```

=== "400"
    HTTP Status Code: <large style="color: red;">400</large><br>
    Error Codes

=== "404"
    HTTP Status Code: <large style="color: red;">422</large><br>
    Attachment not found

=== "500"
    HTTP Status Code: <large style="color: red;">500</large><br>
    Internal Server Error