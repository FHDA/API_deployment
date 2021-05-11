**```seat_list``` GET API**
----
This GET request takes in a json parameter with 2 variables. The `year` and `quarter` parameters are required to find a list of all enrollment info. The server will return the enrollment info of all courses in the defined quarter.

* **URL**

  https://fhda-api-test.azurewebsites.net/seat_list

* **Method:**

  `GET`
  
*  **URL Params**

   `format: json`

   **Required:**
 
   `year=[integer]`  
   `quarter=[string]`
   

* **Success Response:**

  * **Code:** 200<br />
  
    **Content:**  
    ```json
    {
        "00004": {
            "_id": {
                "$oid": "608a4011c310fbdccf2895fb"
            },
            "UID": "00004",
            "latest": 1620001017,
            "fetch_time_datetime": [
                1619556994,
                1619557994,
                1620001017, ...
            ],
            "fetch_time": [
                "04/27/2021, 13:56:34",
                "04/27/2021, 14:13:14",
                "05/02/2021, 17:16:57", ...
            ],
            "act": [
                34,
                34,
                34, ...
            ],
            "rem": [
                6,
                6,
                6, ...
            ],
            "wl_rem": [
                10,
                10,
                10, ...
            ]
        },  
        ......
    }
 
* **Error Response:**

  * **Code:** 404 NOT FOUND<br />
    **Content:** `{ error : "Entry Not Found" }`