# Notion API Examples (API Version 2025-09-03)

This document provides example JSON payloads for interacting with the Notion API, specifically focusing on database and data source management under API version `2025-09-03`.

## 1. Create a New Database with an Initial Data Source

This example demonstrates how to create a new Notion database, which acts as a container, along with its first data source (table). The `initial_data_source` object is crucial here for defining the schema of your first table.

**Endpoint:** `POST /v1/databases`

**Payload Example:**

```json
{
  "parent": {
    "type": "page_id",
    "page_id": "YOUR_PARENT_PAGE_ID"
  },
  "title": [
    {
      "type": "text",
      "text": {
        "content": "My Project Tracker"
      }
    }
  ],
  "icon": {
    "type": "emoji",
    "emoji": "📊"
  },
  "cover": {
    "type": "external",
    "external": {
      "url": "https://www.notion.so/images/page-cover/gradients_1.jpg"
    }
  },
  "initial_data_source": {
    "title": [
      {
        "type": "text",
        "text": {
          "content": "Tasks"
        }
      }
    ],
    "properties": {
      "Task Name": {
        "title": {}
      },
      "Status": {
        "select": {
          "options": [
            {
              "name": "Not Started",
              "color": "red"
            },
            {
              "name": "In Progress",
              "color": "blue"
            },
            {
              "name": "Completed",
              "color": "green"
            }
          ]
        }
      },
      "Due Date": {
        "date": {}
      },
      "Priority": {
        "multi_select": {
          "options": [
            {
              "name": "High",
              "color": "orange"
            },
            {
              "name": "Medium",
              "color": "yellow"
            },
            {
              "name": "Low",
              "color": "gray"
            }
          ]
        }
      },
      "Assigned To": {
        "people": {}
      },
      "Notes": {
        "rich_text": {}
      },
      "Estimated Hours": {
        "number": {
          "format": "number"
        }
      },
      "URL": {
        "url": {}
      },
      "Checkbox": {
        "checkbox": {}
      }
    }
  }
}
```

**Key points:**
*   Replace `"YOUR_PARENT_PAGE_ID"` with the actual ID of the Notion page where you want to create this database.
*   `title` at the top level is for the database container.
*   `initial_data_source.title` is for the first data source (table) within the database.
*   `initial_data_source.properties` defines the columns (schema) of your first table. A `title` property (e.g., "Task Name") is mandatory for any data source.
*   **Important Note on Property Definitions:** When defining properties in the `properties` object (for both database creation and data source updates), the value for each property type should be an empty object `{}`, not a rich text array or other content. For example:
    *   For a `title` property: `"My Title Column": {"title": {}}` (NOT `"My Title Column": {"title": [{"text": {"content": "Some text"}}]}`)
    *   For a `rich_text` property: `"My Text Column": {"rich_text": {}}` (NOT `"My Text Column": {"rich_text": [{"text": {"content": "Some text"}}]}`)
    The rich text arrays are used when *creating or updating pages* (rows) within a data source, not when defining the data source's schema.

## 2. Add a New Data Source to an Existing Database

This example shows how to add an additional data source (another table) to a database that already exists. This is useful for creating multi-source databases.

**Endpoint:** `POST /v1/data_sources`

**Payload Example:**

```json
{
  "parent": {
    "type": "database_id",
    "database_id": "YOUR_EXISTING_DATABASE_ID"
  },
  "title": [
    {
      "type": "text",
      "text": {
        "content": "Project Members"
      }
    }
  ],
  "icon": {
    "type": "emoji",
    "emoji": "👥"
  },
  "properties": {
    "Member Name": {
      "title": {}
    },
    "Role": {
      "select": {
        "options": [
          {
            "name": "Developer",
            "color": "blue"
          },
          {
            "name": "Designer",
            "color": "purple"
          },
          {
            "name": "Manager",
            "color": "green"
          }
        ]
      }
    },
    "Email": {
      "email": {}
    },
    "Phone Number": {
      "phone_number": {}
    }
  }
}
```

**Key points:**
*   Replace `"YOUR_EXISTING_DATABASE_ID"` with the ID of the database to which you want to add this new data source.
*   The `parent.type` must be `"database_id"`.
*   The `title` here is for the new data source itself.
*   `properties` defines the schema for this new table.

## 3. Update a Data Source's Properties

This example demonstrates how to modify the schema (properties/columns) of an existing data source. You can rename properties, add new ones, or remove existing ones.

**Endpoint:** `PATCH /v1/data_sources/{data_source_id}`

**Payload Example (Renaming, Adding, and Removing Properties):**

```json
{
  "properties": {
    "Old Property Name": {
      "name": "New Property Name"
    },
    "New Text Property": {
      "rich_text": {}
    },
    "Status": {
      "select": {
        "options": [
          {
            "name": "To Do",
            "color": "gray"
          },
          {
            "name": "In Progress",
            "color": "blue"
          },
          {
            "name": "Done",
            "color": "green"
          },
          {
            "name": "Blocked",
            "color": "red"
          }
        ]
      }
    },
    "Property To Remove": null
  }
}
```

**Key points:**
*   Replace `{data_source_id}` in the URL with the actual ID of the data source you want to update.
*   To rename a property, provide its current name (or ID) as the key and an object with the new `name` as its value.
*   To add a new property, provide its desired name as the key and its type definition (e.g., `"rich_text": {}`) as the value.
*   To remove a property, provide its name (or ID) as the key and `null` as its value.
*   For `select` and `multi_select` properties, you can update their options by providing the full `options` array. Existing options not included will be removed, and new ones will be added.
