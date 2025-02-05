# Restaurant Kitchen Management System

## Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/ihorhalyskiy/kitchen_service
    ```

2. Navigate to the project directory:
    ```bash
    cd kitchen_service
    ```

3. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    venv\Scripts\activate (on Windows)
    source venv/bin/activate (on macOS)
    ```

4. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

5. Start the server:
    ```bash
    python manage.py runserver
    ```

## Basic functions

### Main Functions:
- **Home Page**: Displays the user login form.
- **Registration**: Allows users to create a new account.
- **Kitchen Info**: Displays general information about dishes, chefs, ingredients, and prices.

### Functions for Dishes:
- **View Dishes**: Displays a list of all dishes.
- **Add Dishes**: Allows adding new dishes.
- **Delete Dishes**: Allows deleting dishes.

### Functions for Chefs:
- **View Cooks**: Displays a list of all chefs.
- **Add Assigned Cooks**: Allows assigning cooks to dishes.
- **Delete Assigned Cooks**: Allows removing assigned cooks from dishes.
- **View Assigned Cooks**: Displays a list of cooks and the dishes they prepare.

### Functions for Ingredients:
- **View Ingredients**: Displays a list of all ingredients.
- **Add Ingredients**: Allows adding new ingredients.
- **Delete Ingredients**: Allows deleting ingredients.

### Functions for Dish Types:
- **View Dish Types**: Displays a list of all dish types.
- **Add Dish Types**: Allows adding new dish types.
- **Delete Dish Types**: Allows deleting dish types.

## Tasks

1. Create a superuser:
    ```bash
    python manage.py createsuperuser --username TestAdmin --email testadmin@example.com
    ```
    Password: `test123`

2. Create a chef for functionality testing:
    ```
    username='chef01', password='Test1234567890'
    ```

3. **Creating Models:**
    - `Cook` model for managing chefs, inherited from `AbstractUser`.
    - `DishType` model for managing dish types.
    - `Ingredient` model for managing ingredients.
    - `Dish` model for managing dishes with fields for name, description, price, ingredients, chefs, and dish type.

4. **Implementing Functionality:**
    - Home page with user login form.
    - User registration.
    - Kitchen info for displaying general information about the kitchen.
    - Functions for adding, viewing, and deleting dishes.
    - Functions for adding, viewing, and deleting ingredients.
    - Functions for adding, viewing, and deleting dish types.
    - Functions for assigning, viewing, and deleting chefs from dishes.

5. **Testing:**
    - Writing unit tests for models.
    - Writing tests for functionality (views).

### Running Tests:
    ```bash
    python manage.py test
    ```

## Authors

Created by Ihor Halytskiy in 2025.
