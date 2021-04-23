**CourseList GET API**
----
This GET request takes in a json parameter with 2 variables. The `year` and `quarter` parameters are required to find a list of course. The server will return the name of all departments in the defined.

* **URL**

  http://fhda-api-test.azurewebsites.net/departments

* **Method:**

  `GET`
  
*  **URL Params**

   `format: json`

   **Required:**
 
   `year=[integer]`  
   `quarter=[string]`
   

* **Success Response:**

  * **Code:** 200<br />
  
    **Content:** `["ACCT", "BUS", ...]`
 
* **Error Response:**

  * **Code:** 404 NOT FOUND<br />
    **Content:** `{ error : "Entry Not Found" }`