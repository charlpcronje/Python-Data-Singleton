# DataSingleton

DataSingleton is a Python package that provides a singleton class for managing data and plugins. It offers a unified interface to access various functionalities such as configuration management, request handling, environment variables, logging, module loading, database querying, API integration, data storage, and bitwise operations.

## Installation

```shell
mkdir data_singleton && cd data_singleton && git clone https://github.com/charlpcronje/Python-Data-Singleton.git .
```

## Usage
Importing the DataSingleton

```py
from data_singleton import DataSingleton

data = DataSingleton()
```

## Configuration Management

```py
# Get a configuration value
app_name = data.config.app_name

# Get a configuration value with a default
debug_mode = data.config.debug_mode or False
```

## Request Handling
```py
# Get request data
username = data.request.form.username

# Get request headers
api_key = data.request.headers.api_key
```

## Environment Variables

```py
# Get an environment variable
api_url = data.env.API_URL

# Get an environment variable with a default
secret_key = data.env.SECRET_KEY or 'default_secret_key'
```

## Logging
```py
# Log info message
data.logging.log_info('Info message')

# Log warning message
data.logging.log_warning('Warning message')

# Log error message
data.logging.log_error('Error message')
```

## Module Loading
```py
# Load a module
module = data.deferred_module.load_module('module.name')
```

### Database Querying
```py
# Query a database model
user = data.model_query.query(User, id=1)

# Query a database model with multiple filters
orders = data.model_query.query(Order, user_id=1, status='pending')
```

### API Integration
```py
# Make a GET request to an API endpoint
response = data.api.get('users', params={'page': 1})

# Make a POST request to an API endpoint
response = data.api.post('users', json={'name': 'John', 'email': 'john@example.com'})
```

### Data Storage
```py
# Set a value in the storage
data.storage.set('key', 'value')

# Get a value from the storage
value = data.storage.get('key')

# Get a value from the storage with a default
value = data.storage.get('key', default='default_value')
```

### Bitwise Operations
```py
# Set a bit at a specific index
value = data.bitwise.set_bit(0b1010, 2)  # Result: 0b1110

# Clear a bit at a specific index
value = data.bitwise.clear_bit(0b1010, 1)  # Result: 0b1000

# Check if a bit is set at a specific index
is_set = data.bitwise.is_bit_set(0b1010, 2)  # Result: True
```

### Configuration
The DataSingleton package can be configured using environment variables or a .env file. Each plugin has its own set of configurable settings.

### Config Plugin
- `CONFIG_FILE:` Path to the configuration file (default: `config.json`)

### Logging Plugin
- `LOG_LEVEL:` Logging level (default: INFO)
- `LOG_FILE:` Path to the log file (default: data_singleton.log)
- `LOG_FORMAT:` Logging format (default: %(asctime)s - %(name)s - %(levelname)s - %(message)s)

### Model Query Plugin
- `DB_URL:` Database URL for SQLAlchemy (default: None)
- API Plugin
- `API_BASE_URL:` Base URL for the API (default: None)
- Storage Plugin
- `STORAGE_FILE:` Path to the storage file (default: data_storage.db)

### Extending the DataSingleton
The DataSingleton package is designed to be extensible. You can create your own plugins by creating a new Python file in the `plugins/` directory and defining a plugin class that inherits from `BasePlugin`. The plugin class should implement the `initialize` method to set up any necessary configurations or initializations.

For example, to create a new plugin called `custom_plugin`:

1. Create a new file `custom_plugin.py` in the `plugins/` directory.
2. Define the plugin class:

```py
from data_singleton.base import BasePlugin

class CustomPlugin(BasePlugin):
    def initialize(self):
        # Plugin initialization code
        pass

    # Plugin methods
```

3. The plugin will be automatically loaded and available through the DataSingleton instance:
python

```py
data = DataSingleton()
data.custom_plugin.method()
```

## Some more usage instructions

1. Accessing storage values:
   - To get a value from storage, you can use `data.storage.get('key')` or `data.get('key')`.
   - To set a value in storage, you can use `data.storage.set('key', 'value')` or `data.set('key', 'value')`.
   - To access a specific value directly, you can use `data.user.id` to get the value of `id` and `data.user.id = 1` to set the value.

2. Accessing configuration values:
   - To get the `db` object from the `settings.json` file located at `./app/config/settings.json`, you can use `data.app.config.settings.db`.

3. Querying database models:
   - To get the user with an ID of 1 from the database, you can use `data.models.users.id(1)`.

4. Accessing environment variables:
   - To get the value of `SALT` from the `.env` file, you can use `data.env.SALT`.

5. Loading Python modules and calling module methods:
   - To load a Python module located at `app/services/db_service.py`, you can use `data.app.services.db_service`.
   - To run the `query` method in the `db_service` module, you can use `data.app.services.db_service.query()`.

6. Accessing request data:
   - The `request` keyword is used to access values sent to the application during an API request.
   - The request data is scoped per request, meaning each request will have its own set of request data.
   - You can access request data using `data.request.form.key` for form data, `data.request.headers.key` for request headers, and so on.

All the usage patterns you mentioned are valid and supported by the DataSingleton package. The package provides a unified and intuitive way to access various functionalities using dot notation and attribute access.

Feel free to use the DataSingleton package in your application and leverage its features for configuration management, database querying, environment variable access, module loading, request handling, and more.

If you have any further questions or need assistance with specific use cases, please let me know!
