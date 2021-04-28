**Course GET API**
----
This GET request takes in a json parameter with 3 variables. The `year`, `quarter`, 'course_id' parameters are required to find a specific course. The server will return the specific course with defined `course_id` in defined quarter and year. Error will be returned if course if not found

* **URL**

  http://fhda-api-test.azurewebsites.net/course

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
    **Content:** `json of Course object (see example at Example section below)`
 
* **Error Response:**
  * **Code:** 404 NOT FOUND<br />
    **Content:** `{ error : "Entry Not Found" }`

* **Example Response:**
  * **Send Request:** 
    * **url**: http://fhda-api-test.azurewebsites.net/course
    * **parameter**: `{"year": 2010,"quarter": "Fall","course_id": "00002"}`
  * **Received Response:** 
    ```json
    {
        "_id": {
            "$oid": "607884f8237536b4bbf8c398"
        },
        "UID": "00002",
        "crn": "00002",
        "courseNum": "D001A",
        "sectionNum": "01",
        "campus": "DA",
        "numCredit": 5.0,
        "courseTitle": "FINAN ACCOUNTNG I",
        "days": "MTWRF",
        "startTime": "08:30 am",
        "endTime": "09:20 am",
        "cap": 40,
        "wlCap": 15,
        "instructorName": "Mary,Amelia,Breen",
        "startDate": "09/20",
        "endDate": "12/10",
        "location": "DA L84",
        "attribute": ""
    }
    ```
