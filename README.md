# API_deployment

## Information

This tool/project provide API for FHDA projects

## Requirements

Python v3.6
node v10.16.0
npm v6.9.0 or above

## Install

Suggestion: use your virtual environment as you with such as conda, virtualenv...etc

do the following:

```script
pip install -r requirements.txt
```

## Usage(@todo)

Activate your virtual environment if you have. Usually the command is `activate virtural_name`

## Development (@todo)

Suggestion: use your virtual environment as you with such as conda, virtualenv...etc

do the following:

```py
npm install
pip install -r requirements.txt
```
  
We require all contributor write docsting for other contributors easy to follow.  
One of software development process is TDD. We highly recommended you *write test before code*  
However, test is not require but recommended.  
The philosophy is **you must know exactly the detailed behavior of your code doing**.  

We use [pytest](https://docs.pytest.org/) to test our code.  
We use [pydocstring](http://pydocstyle.org/) to test our docstring.  
We use [autopep8](https://github.com/hhatto/autopep8) to formating our code.  
We use [pylint](https://pylint.org) as Python linter.  

## Coding Style

In general, we follow PEP8 Python coding style and Google pyguide
However, if PEP8 and Google pyguide has conflict style, PEP8 take place.

Some special rule:

1. max-line-length: 100

Please also write docstring for contributor easy to follow.
We follow Google docstring style(https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)

Reference:

1. https://www.python.org/dev/peps/pep-0008/
2. http://google.github.io/styleguide/pyguide.html

## Project Structure

    .
    API_deployment/  
    │  
    │  
    ├── docs/  
    │   ├── course/
    │   │   └── Get.md 
    │   ├── courseList/ 
    │   │   └── Get.md 
    │   └── departmentList/
    │       └── Get.md 
    │  
    ├── src/  
    │   └── app.py
    │  
    ├── config/  
    │   └── setting.config
    │  
    ├── tests/  
    ├── .gitignore
    ├── requirements.txt  
    └── README.md 

## Git Commit message

In general, we use "Semantic Commit Messages"

Reference:

1. https://gist.github.com/joshbuchea/6f47e86d2510bce28f8e7f42ae84c716
2. https://github.com/joelparkerhenderson/git_commit_message#begin-with-a-short-summary-line

## crawler.config format  
 
    [config]    
    quarter_value  = <quarter_value to be selected>  
    filename  = <filename>.csv  
    title  = <title of the csv file>  
       
    [campus]  
    username = <FHDA MyPortal username>
    password = <FHDA MyPortal password>
