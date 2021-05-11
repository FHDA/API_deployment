**```department``` GET API**
----
This GET request takes in a json parameter with 3 variables. The `year`, `quarter`, `department` parameters are required. The server will return the list of courses in defined department and in defined quarter and year. Error will be returned if course if not found

* **URL**

  https://fhda-api-test.azurewebsites.net/department

* **Method:**

  `GET`
  
*  **URL Params**

   `format: json`

   **Required:**
 
   `year=[integer]`  
   `quarter=[string]`  
   `department=[string]`

* **Success Response:**

  * **Code:** 200<br />
    **Content:** `json of department_list object (see example at Example section below)`
 
* **Error Response:**
  * **Code:** 404 NOT FOUND<br />
    **Content:** `{ error : "Entry Not Found" }`

* **Example Response:**
  * **Send Request:** 
    * **url**: https://fhda-api-test.azurewebsites.net/department
    * **parameter**: `{"year": 2021,"quarter": "Fall","department": "ACCT"}`
  * **Received Response:** 
    ```json
    {
        "25883": {
            "UID": "25883",
            "crn": "25883",
            "courseNum": "D001A",
            "sectionNum": "01Z",
            "campus": "DA",
            "numCredit": 5.0,
            "courseTitle": "Financial Accounting I",
            "days": "ONLINE",
            "startTime": "08:30 am",
            "endTime": "10:20 am",
            "instructorName": "Timothy Paul  Ratchford (P)",
            "startDate": "09/21",
            "endDate": "12/11",
            "location": "DA ONLINE",
            "attribute": "",
            "lab": [
                {
                    "UID": "25883L",
                    "days": "ONLINE",
                    "time": "TBA",
                    "startDate": "09/21",
                    "endDate": "12/11",
                    "instructor": "Timothy Paul  Ratchford ",
                    "location": "DA ONLINE"
                }
            ]
        },
        ......
    }
    ```
