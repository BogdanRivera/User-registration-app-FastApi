# FastAPI Users Registration App
This is a simple CRUD (Create, Read, Update, Delete) application built with FastAPI, a modern web framework for building APIs with Python. The application uses SQLAlchemy to interact with a database for performing CRUD operations.

## Features

- **Create:** Allows users to create new records in the database.
- **Read:** Enables users to retrieve information from the database.
- **Update:** Allows users to modify existing records in the database.
- **Delete:** Enables users to delete records from the database.

## Technologies Used

- [FastAPI](https://fastapi.tiangolo.com/): FastAPI is a modern, fast (high-performance) web framework for building APIs with Python.
- [SQLAlchemy](https://www.sqlalchemy.org/): SQLAlchemy is the Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your_username/fastapi-crud.git
    ```

2. Navigate to the project directory:

    ```bash
    cd yourDirection
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the FastAPI server:

    ```bash
    uvicorn main:app --reload
    ```

2. Access the API documentation at [http://localhost:8000/docs](http://localhost:8000/docs) to explore and test the available endpoints.
3. If you want to use all the routes, you need to log in with an account. Alternatively, if you want to use them for the first time, you must delete the database (data.sqlite).

You have 2 options for this step:

a. If you delete the database:
The system will start without any registered users, so you don't need to worry about the initial email and password (it can be anything or default). Once this step is done, it's necessary to register a user. This user will be automatically registered as an administrator. After registering the user, you must log out of the account and log in again with the registered account to use the application and its routes.

b. If there is already a registered user in the database, you must log in. You can try with this user:
User: "bogdanrivera@gmail.com"
Password: "1234"

In either case, the following steps are necessary:

I. Go to the login path:
![login](https://github.com/BogdanRivera/User-registration-app-FastApi-Backend/assets/121648408/97c7f6cd-cda3-4815-87e7-936187d5ff8e).

II. Log in depending on the steps chosen above:
![loginauth](https://github.com/BogdanRivera/User-registration-app-FastApi-Backend/assets/121648408/a33275b7-e284-4932-977b-2dcb05c9c819)

III. Copy the body response: 
![bodyResponse](https://github.com/BogdanRivera/User-registration-app-FastApi-Backend/assets/121648408/2e0813c8-340f-4c3e-8315-7b66ca574a35)

IV. Go to Authorize button: 
![AuthorizeButton](https://github.com/BogdanRivera/User-registration-app-FastApi-Backend/assets/121648408/1c2de27a-0288-4d53-9fe1-6cda0bc8df0e).


and copy the body response, then 'Authorize': 


[validator](https://github.com/BogdanRivera/User-registration-app-FastApi-Backend/assets/121648408/df1e0ec8-1b87-45a2-9f3d-a910308194d6)



V. All is ready to use the aplication!!

## Demo: 
You can find the demo application here: [User Registration App](https://user-registration-app-fastapi-backend.onrender.com/) 

## Contributing

Contributions are welcome! If you have any suggestions, feature requests, or bug reports, please open an issue or submit a pull request.


