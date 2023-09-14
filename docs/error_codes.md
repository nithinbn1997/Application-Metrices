# Error Codes

An unique string to differentiate various errors our software can produce.

## Definition

!!! abstract "Error Code"
    <h3>E[X1X2][Y1Y2][Z1Z2Z3]</h3>
    
An error string consists of three sections:  
    <ol>
        <li>`X1X2` : Error Category</li>
        <li>`Y1Y2` : Error Sub-Category</li>
        <li>`Z1Z2Z3`: Error Message</li>
    </ol>

## Error Categories
|Identifier| Category|
|---:|:---|
|01|Generic|
|10| User|
|20| Accounting|

## Error Codes & Messages

???+ abstract "01 Generic"
    |Code|Message|
    |---:|:----|
    |E-01-00-001| Invalid Source/North ID|
    |E-01-00-002| Invalid Destination/South ID|
    |E-01-00-003| Invalid North Credentials|
    |E-01-00-004| Invalid South Credentials|

???+ abstract "10 User"
    ???+ abstract "10 User"
        |Code|Message|
        |---:|:----|
        |E-10-10-101| User Doesn't Exist|
        |E-10-10-102| User Blocked|


    ???+ abstract "20 Authentication"
        |Code|Message|
        |---:|:----|
        |E-10-20-201| Invalid Password|
        |E-10-20-202| Invalid Token|
        |E-10-20-203| Token Expired|


    ???+ abstract "30 License"
        |Code|Message|
        |---:|:----|
        |E-10-30-301| License Expired|
        |E-10-30-302| Invalid License|

???+ abstract "20 Accounting"
    ???+ abstract "10 Cross Connect"
        |Code|Message|
        |---:|:----|
        |E-20-10-101| A Side Patch Panel not found|
        |E-20-10-102| Z Side Patch Panel not found|
        |E-20-10-103| A Side Patch Panel port is full|
        |E-20-10-104| Z Side Patch Panel port is full|
        |E-20-10-105| This Operation is not allowed|







