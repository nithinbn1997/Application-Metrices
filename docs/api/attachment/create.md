# Create <small style="color: green;">POST</small>

## Attachment Upload API

<span style="color: green;">POST</span>  
`/v1/attachments/upload`

Attachment Upload API for generic file uploads. Example: Letter of authorization(LOA) for cyxtera.

### **REQUEST**

#### **Path Parameters**
!!! note ""
    None

#### **Query Parameters**
!!! note ""
    None

#### **Request Body** (multipart/form-data)

!!! note "Note"
    Only one file is allowed per request and a Maximum size of 10 MB

=== "Schema"
    | Field        | Type           | Description   |
    | ---------: | :------------: | :------------ |
    |file| file | A file object of type pdf.<br> **Max file size allowed 10MB**|

## RESPONSE

=== "200"

    HTTP Status Code: <large style="color: green;">200</large>

    === "Schema"

        | Field                 | Type   | Description          |
        | --------------------: | :----: | :------------------- |
        | attachment_id| string | Unique attachment ID|

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

=== "413"
    HTTP Status Code: <large style="color: red;">413</large><br>
    Attachment too large

=== "422"
    HTTP Status Code: <large style="color: red;">422</large><br>
    Data Validation Error
    Invalid File type

=== "500"
    HTTP Status Code: <large style="color: red;">500</large><br>
    Internal Server Error