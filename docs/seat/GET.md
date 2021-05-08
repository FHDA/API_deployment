**```seat``` GET API**
----
This GET request takes in a json parameter with 3 variables. The `year`, `quarter`, `course_id` parameters are required. The server will return the enrollment info of course matching the course_id in defined quarter and year. Error will be returned if course if not found

* **URL**

  https://fhda-api-test.azurewebsites.net/seat

* **Method:**

  `GET`
  
*  **URL Params**

   `format: json`

   **Required:**
 
   `year=[integer]`  
   `quarter=[string]`  
   `course_id=[string]`

* **Success Response:**

  * **Code:** 200<br />
    **Content:** `json of department_list object (see example at Example section below)`
 
* **Error Response:**
  * **Code:** 404 NOT FOUND<br />
    **Content:** `{ error : "Entry Not Found" }`

* **Example Response:**
  * **Send Request:** 
    * **url**: https://fhda-api-test.azurewebsites.net/seat
    * **parameter**: `{"year": 2021,"quarter": "Fall","course_id": "00009"}`
  * **Received Response:** 
    ```json
    {
        "_id": {
            "$oid": "608f427a05f4bdaf90f07c84"
        },
        "UID": "00009",
        "latest": 1620001165,
        "fetch_time_datetime": [
            1620001165, ...
        ],
        "fetch_time": [
            "05/02/2021, 17:19:25", ...
        ],
        "act": [
            40, ...
        ],
        "rem": [
            0, ...
        ],
        "wl_rem": [
            10, ...
        ]
    }
    ```
