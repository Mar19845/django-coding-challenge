# Django Coding Challenge

## Setup

Clone this repository using GIT. I recommend you use Github Desktop or VS Code (see point 1 in Development)

To run this project you need to install any recent version of Python. Preferably Python 3.9+ After that you are advised to create a virtual environment so that your dependencies are contained within the workspace. **On Windows, make sure to add Python to your PATH, you may need to logout or reboot to run python**

Once you have Python installed and working, you can install the project dependencies by running `pip install -r requirements.txt`. This will install everything for you, then you can run migrations with `python manage.py migrate` (make sure to run this command within the nimblestore directory). If successful you should see a new file called `db.sqlite3` in your work directory.

Lastly you should be able to run the server with `python manage.py runserver` which will let you see a very basic webpage in https://127.0.0.1:8000 (Open this link in your browser), this page will help you test your work, I recommend you open the web inspector and switch to the network tab to see what is happening. If you want you can find the source for this page in the `nimblestore/checkout/templates/index.html` file. You do NOT need to edit anything on it.

## Development

Here are some general guides and also some tips:

1. Install VS Code (optional) [here](https://code.visualstudio.com/)
2. Install recommended extensions (Python, SonarLint)
3. Use Google as much as you need to, find official sources and documentations, examples and tutorials are good sources.
4. You CAN use AI, in fact I encourage you to do so.

Once you start creating models, you will need to create and run migrations, the commands you'll need are:

```bash
python manage.py makemigrations
python manage.py migrate
```

## Documentation

- **Docstrings**: Please provide docstrings for your functions and classes using the [Google style guide](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html). This helps others understand the purpose and usage of your code.
- **README**: Update the README file to include instructions on how to set up and run the project, as well as any other relevant information. This ensures that anyone who uses your project can easily get started.

## Unit Tests

- **Unit Tests with pytest**: Write unit tests for your code using `pytest`. Ensure you cover different scenarios, including edge cases.
  To run your tests, use the command:
  ```bash
  pytest
  ```
  Create a `tests` directory in your project and add your test files there. Follow the convention of naming your test files starting with `test_`.

## Pre-commit Hooks

- **Pre-commit**: Install `pre-commit` to ensure code quality before commits. Pre-commit hooks can automatically format your code and run tests before each commit. `pre-commit` should have been installed by the previous commmands, yet you still have to run the following:
  Initialize the pre-commit hooks with:
  ```bash
  pre-commit install
  ```
  Now, every time you make a commit, `pre-commit` will run the defined hooks to ensure code quality.

## Problem Statement

Your company has a Django application that stores product information. Each product has a name, price, and quantity available. Your task is to create three API endpoints:

1. `GET /api/products/`: This endpoint should return a list of all products, with each product's name, price, and quantity available.

2. `POST /api/order/`: This endpoint should accept a list of products and quantities, calculate the total cost of the order, and return it. If a product doesn't exist or there isn't enough quantity available, it should return an appropriate error message.

3. `PUT /api/products/<id>/` or `PATCH /api/products/<id>/`: These endpoints should allow for editing the details of a product. The `PUT` method should update all fields of the product, while the `PATCH` method should allow partial updates.

You can search globally for `TODO` to find the files you must edit to complete this assignment.

Good Luck,
Juan Mora


## Set up

Follow these steps to configure and run a Django project:
1. Create and Activate a Virtual Environment

A virtual environment allows you to isolate the project dependencies.

    1. Open your terminal or command prompt.
    2. Navigate to the directory where you want to create the virtual environment.
    3. Run the following command to create the virtual environment:
```bash
    python -m venv env
```
    4. Activate the virtual environment:
- On Windows
```bash
    .\env\Scripts\activate
```
- On macOS/Linux:
```bash
    source env/bin/activate
```

2. Install Dependencies
Once the virtual environment is activated:

    1. Make sure you are in the directory containing the requirements.txt file.
    2. Run the following command to install the required dependencies:
```bash
    pip install -r requirements.txt
```

3. Run the Django Project
To start Django’s development server:

    1. Navigate to the directory containing the manage.py file.
    2. Run the following command:
```bash
    python manage.py runserver
```

4. Access the Project in Your Browser

Once the server is running, open the following URL in your web browser:
```bash
    http://127.0.0.1:8000/
```