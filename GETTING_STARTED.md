# Getting Started with NotionHelper

A comprehensive guide to using NotionHelper for basic Notion API operations.

## Table of Contents
1. [Installation & Setup](#installation--setup)
2. [Understanding Notion's Structure](#understanding-notions-structure)
3. [Basic Operations](#basic-operations)
4. [Working with Databases](#working-with-databases)
5. [Working with Data Sources](#working-with-data-sources)
6. [Working with Pages](#working-with-pages)
7. [File Operations](#file-operations)
8. [Data Retrieval & Analysis](#data-retrieval--analysis)

---

## Installation & Setup

### 1. Install NotionHelper

```bash
pip install notionhelper
```

### 2. Create a Notion Integration

1. Go to [https://www.notion.so/my-integrations](https://www.notion.so/my-integrations)
2. Click **"+ New integration"**
3. Give it a name (e.g., "My Python App")
4. Select the workspace where you want to use it
5. Copy the **"Internal Integration Secret"** (your API token)

### 3. Share Your Notion Pages/Databases

**IMPORTANT**: Your integration can only access pages and databases that have been explicitly shared with it.

To share a page or database:
1. Open the page/database in Notion
2. Click the **"Share"** button in the top-right
3. Click **"Invite"**
4. Search for your integration name
5. Click **"Invite"**

### 4. Store Your Token Securely

It's best practice to store your token as an environment variable:

**On macOS/Linux:**
```bash
export NOTION_TOKEN="secret_xxxxxxxxxxxxxxxxxxxx"
```

**On Windows (PowerShell):**
```powershell
$env:NOTION_TOKEN="secret_xxxxxxxxxxxxxxxxxxxx"
```

**Or use a `.env` file:**
```
NOTION_TOKEN=secret_xxxxxxxxxxxxxxxxxxxx
```

### 5. Initialize NotionHelper

```python
import os
from notionhelper import NotionHelper

# Get token from environment variable
notion_token = os.getenv("NOTION_TOKEN")

# Initialize the helper
helper = NotionHelper(notion_token)
```

---

## Understanding Notion's Structure

### API Version 2025-09-03 Changes

With the latest Notion API, the structure has changed:

```
Page (Parent)
  └── Database (Container)
       ├── Data Source 1 (Table with schema/properties)
       │    ├── Page 1
       │    ├── Page 2
       │    └── Page 3
       └── Data Source 2 (Another table)
            ├── Page 1
            └── Page 2
```

**Key Concepts:**
- **Database**: A container that holds one or more data sources
- **Data Source**: A table with a specific schema (columns/properties)
- **Page**: Individual rows in a data source, or standalone pages

**Important IDs:**
- `database_id`: Points to the container
- `data_source_id`: Points to a specific table (where you add pages)
- `page_id`: Points to individual pages

---

## Basic Operations

### Finding IDs in Notion

**To get a page, database, or data source ID:**

1. Open the item in Notion
2. Look at the URL in your browser:
   ```
   https://www.notion.so/My-Page-1234567890abcdef1234567890abcdef
                                  └── This is the ID ──────────┘
   ```
3. The ID is the 32-character string at the end (without hyphens)
4. Format with hyphens: `12345678-90ab-cdef-1234-567890abcdef`

### Searching for Pages and Databases

```python
# Search for all pages
pages = helper.notion_search_db(query="", filter_object_type="page")
for page in pages:
    print(f"Page: {page['id']}")

# Search for data sources
data_sources = helper.notion_search_db(query="", filter_object_type="data_source")
for ds in data_sources:
    print(f"Data Source: {ds['id']}")

# Search with a specific query
results = helper.notion_search_db(query="Project Tasks", filter_object_type="page")
```

---

## Working with Databases

### Retrieve a Database

```python
# Get the database container
database_id = "12345678-90ab-cdef-1234-567890abcdef"
database = helper.get_database(database_id)

print(f"Database Title: {database['title'][0]['plain_text']}")
print(f"Number of Data Sources: {len(database['data_sources'])}")

# List all data sources in the database
for ds in database['data_sources']:
    print(f"Data Source ID: {ds['id']}")
    print(f"Data Source Type: {ds['type']}")
```

### Create a New Database

```python
# Define the parent page where the database will be created
parent_page_id = "your-parent-page-id"

# Define the database properties (schema)
properties = {
    "Task Name": {"title": {}},  # This will be the title column
    "Status": {
        "select": {
            "options": [
                {"name": "Not Started", "color": "red"},
                {"name": "In Progress", "color": "yellow"},
                {"name": "Done", "color": "green"}
            ]
        }
    },
    "Due Date": {"date": {}},
    "Priority": {
        "select": {
            "options": [
                {"name": "Low", "color": "gray"},
                {"name": "Medium", "color": "blue"},
                {"name": "High", "color": "red"}
            ]
        }
    },
    "Notes": {"rich_text": {}}
}

# Create the database
new_db = helper.create_database(
    parent_page_id=parent_page_id,
    database_title="My Task Database",
    initial_data_source_properties=properties,
    initial_data_source_title="Main Tasks"
)

print(f"Created Database ID: {new_db['id']}")
print(f"Initial Data Source ID: {new_db['initial_data_source']['id']}")

# Save the data source ID for adding pages later
data_source_id = new_db['initial_data_source']['id']
```

---

## Working with Data Sources

### Retrieve a Data Source Schema

```python
data_source_id = "your-data-source-id"
data_source = helper.get_data_source(data_source_id)

print(f"Data Source Title: {data_source['title'][0]['plain_text']}")
print("\nProperties (Columns):")
for prop_name, prop_data in data_source['properties'].items():
    prop_type = prop_data['type']
    print(f"  - {prop_name}: {prop_type}")
```

### Update a Data Source

#### Rename a Column

```python
data_source_id = "your-data-source-id"

updated = helper.update_data_source(
    data_source_id,
    properties={
        "Old Column Name": {
            "name": "New Column Name"
        }
    }
)
print("Column renamed successfully!")
```

#### Add a New Column

```python
updated = helper.update_data_source(
    data_source_id,
    properties={
        "Email": {"email": {}},  # Add an email column
        "Phone": {"phone_number": {}},  # Add a phone column
        "Completed": {"checkbox": {}}  # Add a checkbox column
    }
)
print("New columns added!")
```

#### Remove a Column

```python
updated = helper.update_data_source(
    data_source_id,
    properties={
        "Column To Remove": None  # Set to None to remove
    }
)
print("Column removed!")
```

#### Update Select Options

```python
updated = helper.update_data_source(
    data_source_id,
    properties={
        "Status": {
            "select": {
                "options": [
                    {"name": "Backlog", "color": "gray"},
                    {"name": "To Do", "color": "red"},
                    {"name": "In Progress", "color": "yellow"},
                    {"name": "Review", "color": "blue"},
                    {"name": "Done", "color": "green"}
                ]
            }
        }
    }
)
print("Select options updated!")
```

---

## Working with Pages

### Create a New Page (Row)

**Basic Example:**

```python
data_source_id = "your-data-source-id"

# Define the page properties
page_properties = {
    "Task Name": {  # Title property
        "title": [
            {
                "text": {
                    "content": "Complete project documentation"
                }
            }
        ]
    },
    "Status": {  # Select property
        "select": {
            "name": "In Progress"
        }
    },
    "Due Date": {  # Date property
        "date": {
            "start": "2025-12-31"
        }
    },
    "Priority": {  # Select property
        "select": {
            "name": "High"
        }
    },
    "Notes": {  # Rich text property
        "rich_text": [
            {
                "text": {
                    "content": "Need to update README and add examples"
                }
            }
        ]
    }
}

# Create the page
new_page = helper.new_page_to_data_source(data_source_id, page_properties)
page_id = new_page['id']
print(f"Created page with ID: {page_id}")
```

**Property Type Examples:**

```python
# Number
"Age": {
    "number": 25
}

# Checkbox
"Completed": {
    "checkbox": True
}

# URL
"Website": {
    "url": "https://example.com"
}

# Email
"Contact": {
    "email": "user@example.com"
}

# Phone
"Phone": {
    "phone_number": "+1234567890"
}

# Multi-select
"Tags": {
    "multi_select": [
        {"name": "Urgent"},
        {"name": "Bug"},
        {"name": "Frontend"}
    ]
}

# Date with end date (range)
"Event Period": {
    "date": {
        "start": "2025-01-01",
        "end": "2025-01-07"
    }
}
```

### Retrieve a Page

```python
page_id = "your-page-id"
page_data = helper.get_page(page_id)

# Access properties
properties = page_data['properties']
print(f"Properties: {properties}")

# Access page content blocks
content = page_data['content']
print(f"Number of blocks: {len(content)}")
```

### Add Content to a Page

```python
page_id = "your-page-id"

# Define blocks to add
blocks = [
    {
        "object": "block",
        "type": "heading_1",
        "heading_1": {
            "rich_text": [
                {
                    "type": "text",
                    "text": {
                        "content": "Project Overview"
                    }
                }
            ]
        }
    },
    {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [
                {
                    "type": "text",
                    "text": {
                        "content": "This project aims to improve user experience by implementing new features."
                    }
                }
            ]
        }
    },
    {
        "object": "block",
        "type": "heading_2",
        "heading_2": {
            "rich_text": [
                {
                    "type": "text",
                    "text": {
                        "content": "Key Features"
                    }
                }
            ]
        }
    },
    {
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": {
            "rich_text": [
                {
                    "type": "text",
                    "text": {
                        "content": "Enhanced search functionality"
                    }
                }
            ]
        }
    },
    {
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": {
            "rich_text": [
                {
                    "type": "text",
                    "text": {
                        "content": "Improved mobile responsiveness"
                    }
                }
            ]
        }
    },
    {
        "object": "block",
        "type": "numbered_list_item",
        "numbered_list_item": {
            "rich_text": [
                {
                    "type": "text",
                    "text": {
                        "content": "Step 1: Research user needs"
                    }
                }
            ]
        }
    },
    {
        "object": "block",
        "type": "numbered_list_item",
        "numbered_list_item": {
            "rich_text": [
                {
                    "type": "text",
                    "text": {
                        "content": "Step 2: Design mockups"
                    }
                }
            ]
        }
    },
    {
        "object": "block",
        "type": "to_do",
        "to_do": {
            "rich_text": [
                {
                    "type": "text",
                    "text": {
                        "content": "Complete initial testing"
                    }
                }
            ],
            "checked": False
        }
    }
]

# Append blocks to the page
helper.append_page_body(page_id, blocks)
print("Content added to page successfully!")
```

---

## File Operations

### Upload and Attach a File

**Method 1: Two-step process**

```python
# Step 1: Upload the file
file_path = "/path/to/document.pdf"
upload_response = helper.upload_file(file_path)
file_upload_id = upload_response['id']

# Step 2: Attach to a page
page_id = "your-page-id"
attach_response = helper.attach_file_to_page(page_id, file_upload_id)
print("File attached successfully!")
```

**Method 2: One-step process (recommended)**

```python
page_id = "your-page-id"
file_path = "/path/to/document.pdf"

response = helper.one_step_file_to_page(page_id, file_path)
print("File uploaded and attached in one step!")
```

### Upload and Embed an Image

```python
page_id = "your-page-id"
image_path = "/path/to/image.png"

response = helper.one_step_image_embed(page_id, image_path)
print("Image embedded in page!")
```

### Attach File to a Property

Some databases have a "Files & Media" property where you can attach files.

```python
page_id = "your-page-id"
property_name = "Attachments"  # Name of your Files & Media property
file_path = "/path/to/document.pdf"
file_name = "Project Document.pdf"  # Display name

response = helper.one_step_file_to_page_property(
    page_id,
    property_name,
    file_path,
    file_name
)
print("File attached to property!")
```

### Upload Multiple Files to a Property

```python
page_id = "your-page-id"
property_name = "Documents"
file_paths = [
    "/path/to/document1.pdf",
    "/path/to/document2.docx",
    "/path/to/image.png"
]

response = helper.upload_multiple_files_to_property(page_id, property_name, file_paths)
print(f"Uploaded {len(file_paths)} files!")
```

---

## Data Retrieval & Analysis

### Get All Page IDs from a Data Source

```python
data_source_id = "your-data-source-id"
page_ids = helper.get_data_source_page_ids(data_source_id)

print(f"Found {len(page_ids)} pages:")
for page_id in page_ids:
    print(f"  - {page_id}")
```

### Get All Pages as JSON

```python
data_source_id = "your-data-source-id"

# Get all pages
all_pages = helper.get_data_source_pages_as_json(data_source_id)

# Get only first 10 pages
limited_pages = helper.get_data_source_pages_as_json(data_source_id, limit=10)

print(f"Retrieved {len(all_pages)} pages")
print(f"First page properties: {all_pages[0]}")
```

### Get All Pages as Pandas DataFrame

**This is perfect for data analysis!**

```python
import pandas as pd

data_source_id = "your-data-source-id"

# Get all pages as a DataFrame
df = helper.get_data_source_pages_as_dataframe(data_source_id)

print(df.head())
print(f"\nDataFrame shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")
```

**With pagination:**

```python
# Get only first 50 pages
df = helper.get_data_source_pages_as_dataframe(data_source_id, limit=50)

# Get pages without IDs
df = helper.get_data_source_pages_as_dataframe(
    data_source_id,
    include_page_ids=False
)
```

**Data Analysis Example:**

```python
# Get the data
df = helper.get_data_source_pages_as_dataframe(data_source_id)

# Filter completed tasks
completed = df[df['Status'] == 'Done']
print(f"Completed tasks: {len(completed)}")

# Group by status
status_counts = df['Status'].value_counts()
print("\nTasks by status:")
print(status_counts)

# Find high priority tasks
high_priority = df[df['Priority'] == 'High']
print(f"\nHigh priority tasks: {len(high_priority)}")

# Export to CSV
df.to_csv('notion_tasks.csv', index=False)
print("Exported to CSV!")

# Calculate statistics
if 'Completion Rate' in df.columns:
    avg_completion = df['Completion Rate'].mean()
    print(f"Average completion rate: {avg_completion:.2f}%")
```

---

## Complete Example: Task Manager

Here's a complete example that creates a task management system:

```python
import os
from notionhelper import NotionHelper
from datetime import datetime, timedelta

# Initialize
notion_token = os.getenv("NOTION_TOKEN")
helper = NotionHelper(notion_token)

# 1. Create a task database
parent_page_id = "your-parent-page-id"

properties = {
    "Task": {"title": {}},
    "Status": {
        "select": {
            "options": [
                {"name": "Backlog", "color": "gray"},
                {"name": "To Do", "color": "red"},
                {"name": "In Progress", "color": "yellow"},
                {"name": "Done", "color": "green"}
            ]
        }
    },
    "Priority": {
        "select": {
            "options": [
                {"name": "Low", "color": "gray"},
                {"name": "Medium", "color": "blue"},
                {"name": "High", "color": "red"}
            ]
        }
    },
    "Due Date": {"date": {}},
    "Assignee": {"rich_text": {}},
    "Completed": {"checkbox": {}}
}

db = helper.create_database(
    parent_page_id=parent_page_id,
    database_title="Team Tasks",
    initial_data_source_properties=properties
)

data_source_id = db['initial_data_source']['id']
print(f"Created database with data source: {data_source_id}")

# 2. Add some tasks
tasks = [
    {
        "Task": "Design homepage mockup",
        "Status": "In Progress",
        "Priority": "High",
        "Due Date": (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d"),
        "Assignee": "Alice",
        "Completed": False
    },
    {
        "Task": "Write API documentation",
        "Status": "To Do",
        "Priority": "Medium",
        "Due Date": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
        "Assignee": "Bob",
        "Completed": False
    },
    {
        "Task": "Set up CI/CD pipeline",
        "Status": "Done",
        "Priority": "High",
        "Due Date": (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d"),
        "Assignee": "Charlie",
        "Completed": True
    }
]

for task in tasks:
    page_props = {
        "Task": {
            "title": [{"text": {"content": task["Task"]}}]
        },
        "Status": {
            "select": {"name": task["Status"]}
        },
        "Priority": {
            "select": {"name": task["Priority"]}
        },
        "Due Date": {
            "date": {"start": task["Due Date"]}
        },
        "Assignee": {
            "rich_text": [{"text": {"content": task["Assignee"]}}]
        },
        "Completed": {
            "checkbox": task["Completed"]
        }
    }

    new_page = helper.new_page_to_data_source(data_source_id, page_props)
    print(f"Created task: {task['Task']}")

# 3. Retrieve and analyze
df = helper.get_data_source_pages_as_dataframe(data_source_id)
print("\n=== Task Summary ===")
print(f"Total tasks: {len(df)}")
print(f"\nBy Status:")
print(df['Status'].value_counts())
print(f"\nBy Priority:")
print(df['Priority'].value_counts())
print(f"\nCompleted: {df['Completed'].sum()}")
print(f"In Progress: {len(df[df['Status'] == 'In Progress'])}")
```

---

## Common Patterns

### Bulk Add Pages

```python
import pandas as pd

# Read from CSV
df = pd.read_csv('tasks.csv')

for _, row in df.iterrows():
    page_props = {
        "Task": {
            "title": [{"text": {"content": str(row['task_name'])}}]
        },
        "Status": {
            "select": {"name": str(row['status'])}
        },
        "Priority": {
            "select": {"name": str(row['priority'])}
        }
    }

    helper.new_page_to_data_source(data_source_id, page_props)
    print(f"Added: {row['task_name']}")
```

### Sync Data Between Notion and CSV

```python
# Export from Notion
df = helper.get_data_source_pages_as_dataframe(data_source_id)
df.to_csv('notion_export.csv', index=False)
print("Exported to CSV")

# Import to Notion
df = pd.read_csv('import_data.csv')
for _, row in df.iterrows():
    # Create page from row data
    pass
```

### Update Multiple Pages

```python
# Get all pages
page_ids = helper.get_data_source_page_ids(data_source_id)

# Note: There's no built-in batch update in the current version
# You would need to update pages individually using the Notion API
```

---

## Troubleshooting

### Common Errors

**1. "object not found"**
- Make sure you've shared the page/database with your integration
- Check that the ID is correct

**2. "body failed validation"**
- Check property names match exactly (case-sensitive)
- Verify property types match the schema
- Ensure select options exist in the database

**3. "Unauthorized"**
- Check your API token is correct
- Make sure the token is properly set in environment variables

**4. "Could not find database"**
- You might be using a `database_id` instead of a `data_source_id`
- Get the data source ID from the database object

### Best Practices

1. **Always use environment variables for tokens**
2. **Share resources with your integration before accessing**
3. **Use data_source_id when creating pages, not database_id**
4. **Handle errors with try-except blocks**
5. **Test with a single page before bulk operations**
6. **Use limit parameter when testing to avoid retrieving too much data**

---

## Next Steps

Now that you understand the basics:

1. Explore the [Complete ML Experiment Tracking Guide](README.md#machine-learning-experiment-tracking)
2. Check out advanced features in the [README](README.md)
3. Review the [Notion API Documentation](https://developers.notion.com)

---

**Need Help?**
- Check the [README.md](README.md) for complete function reference
- Visit [Notion API JSON Builder](https://notioinapiassistant.streamlit.app) for help with property JSON
