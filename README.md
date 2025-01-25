# WordPress Page Manager

## Project Overview

WordPress Page Manager is a Python-based application designed to interact with WordPress REST API, providing seamless management of WordPress pages through a command-line interface.

## Features

- Create new WordPress pages with custom titles and buttons
- Modify existing pages
- Delete pages
- List available pages
- Persistent storage of page information using SQLite

## Project Structure

```
wordpress_api_client/
│
├── wordpress_api_client/
│   ├── __init__.py               # Package initialization
│   ├── client.py                 # WordPress API Client class
│   └── config.py                 # Configuration settings
│   ├── auth.py               # Authentication management
│   ├── endpoints/
│   │   ├── __init__.py           # Endpoints module initialization
│   │   ├── posts.py              # Posts management
│   │   ├── pages.py              # Pages management
│   ├── interactions/
│   │   ├── __init__.py           # Endpoints module initialization
│   │   ├── posts.py              # Posts interaction interaction
│   │   ├── pages.py              # Pages interaction
│   │   ├── exceptions.py         # Custom exceptions
│   ├── ui/
│   │   ├── __init__.py           # Endpoints module initialization
│   │   ├── button.py             #Button element html
│   │   ├── container.py          #container element html
│   │   ├── image.py              #image element html
│   │   ├── text.py               #text element html
│   │   ├── exceptions.py         # Custom exceptions


│
├── main.py                       # Main application entry point
└── requirements.txt              # Project dependencies
```

## Prerequisites

- Python 3.7+
- WordPress site with REST API enabled
- Dependencies listed in `requirements.txt`

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. Set up your WordPress site's base URL in `config.py`
2. Configure authentication credentials if required

## Usage

Run the application:
```bash
python main.py
```

### Available Operations

1. Create a new page with buttons
2. Modify an existing page
3. Delete a page
4. List all pages
5. Exit the application

## Key Components

- `WordPressApiClient`: Handles API interactions
- `PagesEndpoint`: Manages page-specific operations
- SQLite Database: Stores page metadata locally

### Detailed Component Breakdown

#### WordPressApiClient
- Manages API connection to WordPress
- Handles authentication
- Provides base methods for API interactions

#### PagesEndpoint
- Specific methods for page-related operations
- Create, read, update, and delete page functionalities
- Interacts with WordPress REST API endpoints

#### SQLite Database
- Local storage for page metadata
- Tracks created pages
- Provides offline page management

## Code Examples

### Creating a Page
```python
# Example of creating a page with buttons
create_page_with_buttons()
```

### Modifying a Page
```python
# Example of modifying an existing page
modify_existing_page()
```

## Error Handling

The application includes custom exception handling for:
- API connection errors
- Authentication failures
- Page creation/modification issues


## Security

- Supports WordPress authentication
- Secure API interaction
- Local data storage with SQLite


- Ensure WordPress REST API is enabled
- Check network connectivity
- Verify authentication credentials
- Review error messages in console

## Dependencies

- `requests` for API calls
-  `python-dotenv `


