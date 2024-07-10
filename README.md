# Django Application Setup and API Endpoints

## Setup Instructions

```bash
# Create a Virtual Environment
virtualenv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install Dependencies
pip install -r requirements.txt

# Apply Migrations
python manage.py migrate

# Create a Superuser
python manage.py createsuperuser

# Run the Development Server
python manage.py runserver
```

## API Endpoints

### Authentication

#### Obtain Token
```http
POST /api/v1/token
Payload: {"username": "yourusername", "password": "yourpassword"}
```

### User Profile

*Headers: Authorization: Bearer access_token*

#### Get User Profile
```http
GET /api/v1/me
```

#### Update User Profile
```http
PATCH /api/v1/update-me
Payload: {"first_name": "NewFirstName", "last_name": "NewLastName"}
```

#### Delete User
```http
DELETE /api/v1/user/<int:id>/delete_user
```

### Products List

#### List Products
```http
GET /api/v1/products
Filters: name, min_price, max_price
Pagination: page=int
```



## Running Tests
```bash
python manage.py test
```

P.S:

```bash
./manage.py generate_products -- this command will generate 10 products in the database for testing purposes.
```