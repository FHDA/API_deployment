**CourseList GET API**
----
This GET request takes in a json parameter with 3 variables. The `year` and `quarter` parameters are required to find a list of course, and `department` parameter is optional (leave as *null* if not using). The server will return all courses in a specific quarter if only `year` and `quarter` parameters are defined, and will return all courses in a specific department if all parameters are defined.

* **URL**

  http://fhda-api-test.azurewebsites.net/courses

* **Method:**

  `GET`
  
*  **URL Params**

   `format: json`

   **Required:**
 
   `year=[integer]`  
   `quarter=[string]`

   **Optional:**
 
   `department=[string]`

* **Success Response:**

  * **Code:** 200<br />
  
    **Content:** `{ <course_uid1> : <course1_json>, <course_uid2> : <course2_json>, ...}`
 
* **Error Response:**

  * **Code:** 404 NOT FOUND<br />
    **Content:** `{ error : "Entry Not Found" }`