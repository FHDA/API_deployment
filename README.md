# FHDATime API Development

This API is currently used by the following frontend project:
- [FHDATime](https://github.com/FHDA/Frontend)

## Setup and Run
### Python Setup
Requirements:
- Python 3
- Install All Python Dependencies
```
$ pip install -r requirements.txt
```

### SQL Setup
#### Local Test
Setup corresponding SQL database following `/db_setup/setup_sql_db.sql` to test the server in local. 

### `.env` Sample Format
```
# MongoDB settings
Mongo_User=<mongo_username>
Mongo_Password=<mongo_password>
Mongo_DBName=<mongo_db_name>
Mongo_Postfix=<mongo_post_fix>

# Okta settings
okta_issuer=<okta_issuer_domain>
okta_client_id=<okta_client_id>

# SQL settings
sql_host=<sql_host>
sql_port=<sql_port>
sql_user=<sql_user>
sql_password=<sql_password>
sql_db_name=<sql_db_name>
```

### Start Server
```
$ python -m flask run
```

### Run Tests
```
$ pytest
```

## Contributions
### Git Message Style Guide
- [Semantic Commit Messages](https://gist.github.com/joshbuchea/6f47e86d2510bce28f8e7f42ae84c716)
- [How to Write a Great Git Commit Message](https://github.com/joelparkerhenderson/git-commit-message#begin-with-a-short-summary-line)

### Auto-formatting
Please use [Black](https://github.com/psf/black) to format your code automatically. 
```
$ pip install black
$ black .
```
