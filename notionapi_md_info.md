# Block
Notion API Overview
Discover how to leverage Notion's Public API to build integrations.
Suggest Edits
Using Notion's API for Integrations

A Notion workspace is a collaborative environment where teams can organize work, manage projects, and store information in a highly customizable way. Notion's REST API facilitates direct interactions with workspace elements through programming. Key functionalities include:

Pages: Create, update, and retrieve page content.
Databases and Data Sources: Manage databases, data source properties, entries, and schemas.
Users: Access user profiles and permissions.
Comments: Handle page and inline comments.
Content Queries: Search through workspace content.
Authentication: Secure integrations with OAuth 2.0.
Link Previews: Customize how links appear when shared.
To make interactions within Notion workspaces programmatically, you must associate these actions with a Notion user. Notion facilitates this by allowing API requests to be linked to a "bot" user.

Developers create integrations to define a bot's capabilities, including authenticating API requests, deciding when to make requests, and setting the bot's read/write permissions. Essentially, using Notion's Public API involves creating an integration that outlines how a bot interacts with your workspace and assigns REST API requests to the bot.

There are two primary integration types:

Internal: For private workspace workflows and automations.
Public: For broader, shareable functionalities, including Link Previews.
For further details on integration possibilities and API specifics, proceed with the guide or consult the API reference. Check out our demos for practical examples.

What is a Notion Integration?

A Notion integration, sometimes referred as a connection, enables developers to programmatically interact with Notion workspaces. These integrations facilitate linking Notion workspace data with other applications or the automation of workflows within Notion.

Integrations are installed in Notion workspaces and require explicit permission from users to access Notion pages and databases.

1800
Create Notion integrations that unlock new possibilities for teams.

Notion users have access to a vast library of existing integrations to enrich their experience further. For developers interested in creating custom solutions, Notion supports the development of both internal and public integrations. Both utilize the Notion API for workspace interactions.

Let's explore internal and public integrations.

Internal vs. Public Integrations

Notion integrations come in two types: Internal and Public. Understanding the differences between them helps in choosing the right approach for your development needs.

Internal Integrations are exclusive to a single workspace, accessible only to its members. They are ideal for custom workspace automations and workflows.
Public Integrations are designed for a wider audience, usable across any Notion workspace. They cater to broad use cases and follow the OAuth 2.0 protocol for workspace access.
🔑
Public integrations must undergo a Notion security review before publishing.
Key Differences

Feature	Internal Integrations	Public Integrations
Scope	Confined to a single, specific workspace.	Available across multiple, unrelated workspaces.
User Access	Only accessible by members of the workspace where it's installed.	Accessible by any Notion user, regardless of their workspace.
Creation	Created by Workspace Owners within the integration dashboard.	Created by Workspace Owners within the integration dashboard.
Permissions	Workspace members explicitly grant access to their pages or databases via Notion’s UI.	Users authorize access to their pages during the OAuth flow, or by sharing pages directly with the integration.
OAuth Protocol	Not applicable, as access is limited to a single workspace.	Uses the OAuth 2.0 protocol to securely access information across multiple workspaces.
Dashboard Visibility	Visible to Workspace Owners in the integration dashboard, including integrations created by others.	-
What You Can Build: Integration Use Cases

Notion’s REST API opens up a world of possibilities for integrations, ranging from enhancing internal workflow to creating public-facing applications. Here’s a closer look at some of the innovative integrations developers have built with Notion:

Data Integrations

Data integrations leverage the Notion API to automate data flow between Notion and other systems.

Automated Notifications: Develop integrations that monitor Notion databases for changes. Upon detecting a change, these integrations can automatically send notifications various communication channels.
Github Synchronization: Create integrations that keep Notion issues in sync with GitHub issues.
External Data Import: Build integrations that import data from external sources directly into Notion databases. This can include importing customer data, project updates, or any other relevant information.
🔗
Examples:

Create an integration
Working with comments
Working with databases
Working with files and media
Working with page content
Link Preview Integrations

Enhance the sharing experience within Notion with Link preview integrations, offering a glimpse into the content of shared links:

Link preview of a GitHub PR
Link Preview of a GitHub PR.

Create integrations that allow for the customization of how shared links are presented in Notion, providing context and enhancing engagement.

🔑
Link Preview Integrations differ from public integrations. Review the Link Preview guide.
🛑
To build a Link Preview integration, developers must first apply for access to the feature through the Notion Link Preview API request form.

Link Preview integrations published for distribution require a review from Notion's platform and security teams.
🔗
Quick Links

Introduction to Link Preview integrations
Build a Link Preview integration
API reference docs for the Link Preview unfurl attribute object
Help Centre
Identity Management Integrations (Enterprise Plans ONLY)

For enterprise-level workspaces, Notion offers advanced identity management capabilities:

SCIM API for User and Group Management: Utilize the SCIM API to automate the provisioning and management of users and groups within enterprise workspaces, streamlining administrative tasks.
SAML SSO for Enhanced Security: Implement Single Sign-On (SSO) using SAML for a secure and convenient authentication process, simplifying access for users across the enterprise.
🔗
Quick Links

Provision users and groups with SCIM
SAML SSO configuration
Starting Your Integration Journey

Embarking on building an integration with Notion? Begin with our foundational Build your first integration guide. As you become more familiar with the basics, expand your knowledge and skills with in-depth guides on Authorization, Page content, and Databases.

Key resources

Notion SDK for JavaScript: Leverage our SDK designed for JavaScript environments to simplify interactions with the REST API, making development more efficient.
Technology Partner Program: Have you developed a public integrations? Join our Technology Partner Program for access to dedicated support, exclusive distribution channels, and marketing opportunities.
Explore these resources and join the Notion Devs Slack community to share your projects, gain insights from fellow developers, and discover new ways to enhance Notion with integrations.

Upgrading to Version 2025-09-03
Learn how to upgrade your Notion API integrations to the latest API version
Suggest Edits
We’ve released Notion API version 2025‑09‑03, introducing first-class support for multi-source databases. This enables a single database to contain multiple linked data sources — unlocking powerful new workflows.

For more information about data sources, see our FAQs.

However, this change is not backwards-compatible. Most existing database integrations must be updated to prevent disruptions.

❗️
Code changes required

If your integration is still using a previous API version and a user adds another data source to a database, the following API actions will fail:

Create page when using the database as the parent
Database read, write, or query
Writing relation properties that point to that database
What’s changing

Most API operations that used database_id now require a data_source_id
Several database endpoints have moved or been restructured to support the new data model
What this guide covers

A breakdown of what’s new and why it changed
A step-by-step migration checklist to safely update your integrations
Upgrade checklist

Use this checklist to see exactly what must change before you bump Notion-Version to 2025-09-03.

Required steps across all of your integrations

Add a discovery step to fetch and store the data_source_id to use in subsequent API calls.
Start sending data_source_id when creating pages or defining relations
Migrate database endpoints to data sources.
If you use the Search API, update result handling to process data source objects and possible multiple results per database
If using the TypeScript SDK, upgrade to the correct version and set the new version in your client
If using webhooks, handle the new shape and bump your subscription version
📘
Developer action required

These steps primarily require code changes in your repositories or low-code platform. They cannot be fully completed through the Notion integration management UI.
Step-by-step guide

Step 1: Add a discovery step to fetch and store the data_source_id

First, identify the parts of your system that process database IDs. These may include:

Responses of list and search APIs, e.g. Search.
Database IDs provided directly by users of your system, or hard-coded based on URLs in the Notion app.
Events for integration webhooks (covered in the Webhook changes section below).
For each entry point that uses database IDs, start your migration process by introducing an API call to the new Get Database API (GET /v1/databases/:database_id) endpoint to retrieve a list of child data_sources. For this new call, make sure to use the 2025-09-03 version in the Notion-Version header, even if the rest of your API calls haven't been updated yet.

Get Database (JSON)
Get Database (JS SDK)

// GET /v1/databases/{database_id}
// Notion-Version: "2025-09-03"
// --- RETURNS -->
{
  "object": "database",
  "id": "{database_id}",
  "title": [/* ... */],
  "parent": {
    "type": "page_id",
    "page_id": "255104cd-477e-808c-b279-d39ab803a7d2"
  },
  "is_inline": false,
  "in_trash": false,
  "created_time": "2025-08-07T10:11:07.504-07:00",
  "last_edited_time": "2025-08-10T15:53:11.386-07:00",
  "data_sources": [
    {
      "id": "{data_source_id}",
      "name": "My Task Tracker"
    }
  ],
  "icon": null,
  "cover": null,
  // ...
}
To get a data source ID in the Notion app, the settings menu for a database includes a "Copy data source ID" button under "Manage data sources":



Having access to the data source ID (or rather, IDs, once Notion users start adding 2nd sources for their existing databases) for a database lets you continue onto the next few steps.

Step 2: Provide data source IDs when creating pages or relations

Some APIs that accept database_id in the body parameters now support providing a specific data_source_id instead. This works for any API version, meaning you can switch over at your convenience, before or after upgrading these API requests to use 2025-09-03:

Creating a page with a database (now: data source) parent
Defining a database relation property that points to another database (now: data source)
Create page

In the Create a page API, look for calls that look like this:

Create Page (JSON)
Create Page (TS SDK)

// POST /v1/pages
{
  "parent": {
    "type": "database_id",
    "database_id": "..."
  }
}
Change these to use data_source_id parents instead, using the code from Step 1 to get the ID of a database's data source:

Create Page (JSON)
Create Page (TS SDK)

// POST /v1/pages
{
  "parent": {
    "type": "data_source_id",
    "data_source_id": "..."
  }
}
Create or update database

For database relation properties, the API will include both a database_id and data_source_id fields in the read path instead of just a database_id.

In the write path, switch your integration to only provide the data_source_id in request objects.

Relation property response example

"Projects": {
  "id": "~pex",
  "name": "Projects",
  "type": "relation",
  "relation": {
    "database_id": "6c4240a9-a3ce-413e-9fd0-8a51a4d0a49b",
    "data_source_id": "a42a62ed-9b51-4b98-9dea-ea6d091bc508",
    "dual_property": {
      "synced_property_name": "Tasks",
      "synced_property_id": "JU]K"
    }
  }
}
Note that database mentions in rich text will continue to reference the database, not the data source.

Step 3: Migrate database endpoints to data sources

The next step is to migrate each existing use of database APIs to their new data source equivalents, taking into account the differences between the old /v1/databases APIs and new /v1/data_sources APIs:

Return very similar responses, but with object: "data_source", starting from 2025-09-03
Accept a specific data source ID in query, body, and path parameters, not a database ID
Exist under the /v1/data_sources namespace, starting from version 2025-09-03
Require a custom API request with notion.request if you're using the TypeScript SDK, since we won't upgrade to SDK v5 until you get to Step 4 (below).
The following APIs are affected. Each of them is covered by a sub-section below, with more specific Before vs. After explanations and code snippets:

Retrieve a database
Query a database
Create a database
Update a database
Search
Retrieve database

Before (2022-06-28):

Retrieving a database with multiple data sources fails with a validation_error message.
For relation properties: across all API versions, both the database_id and data_source_id are now included in the response object.
Retrieve Database (JSON)
Query Database (TS SDK)

// GET /v1/databases/:database_id
{
  // ...
}
After (2025-09-03):

The Retrieve Database API is now repurposed to return a list of data_sources (each with an id and name, as described in Step 1).
The Retrieve Data Source API is the new home for getting up-to-date information on the properties (schema) of each data source under a database.
The object field is always "data_source" and the id is specific to the data source.
The parent object now identifies the database_id immediate parent of the data source.
The database's parent (i.e. the data source's grandparent) is included as a separate field, database_parent, on the data source response.
You can't use a database ID with the retrieve data source API, or vice-versa. The two types of IDs are not interchangeable.
Retrieve Data Source (JSON)
Retrieve Data Source (TS SDK)

// Get `data_source_id` from Step 1
//
// GET /v1/data_sources/:data_source_id
{
  "object": "data_source",
  "id": "bc1211ca-e3f1-4939-ae34-5260b16f627c",
  "created_time": "2021-07-08T23:50:00.000Z",
  "last_edited_time": "2021-07-08T23:50:00.000Z",
  "properties": {
    "In stock": {
      "id": "fk%5EY",
      "name": "In stock",
      "type": "checkbox",
      "checkbox": {}
    },
    "Name": {
      "id": "title",
      "name": "Name",
      "type": "title",
      "title": {}
    }
  },
  "parent": {
    "type": "database_id",
    "database_id": "6ee911d9-189c-4844-93e8-260c1438b6e4"
  },
  "database_parent": {
    "type": "page_id",
    "page_id": "98ad959b-2b6a-4774-80ee-00246fb0ea9b"
  },
  // ... (other properties omitted)
}
Query databases

Before (2022-06-28):

Query Database (JSON)
Query Database (TS SDK)

// PATCH /v1/databases/:database_id/query
{
  // ...
}
After (2025-09-03):

When you update the API version, the path of this API changes, and now accepts a data source ID. With the TS SDK, you'll have to switch this to temporarily use a custom notion.request(...), until you upgrade to the next major version as part of Step 4.

Query Data Source (JSON)
Query Data Source (TS SDK)

// PATCH /v1/data_sources/:data_source_id/query
{
  // ...
}
Create database

Before (2022-06-28):

In 2022-06-28, the Create Database API created a database and data source, along with its initial default view.
For relation properties: across all API versions, both the database_id and data_source_id are now included in the response object.
When providing relation properties in a request, you can either use database_id, data_source_id, or both, prior to making the API version upgrade.
We recommend starting by switching your integration over to passing only a data_source_id for relation objects even in 2022-06-28 to precisely identify the data source to use for the relation and be ready for the 2025-09-03 behavior.
Create Database (JSON)
Create Database (TS SDK)

// POST /v1/databases
{
  "parent": {"type": "page_id", "page_id": "..."},
  "properties": {...},
  // ...
}
After (2025-09-03):

Continue to use the Create Database API even after upgrading, when you want to create both a database and its initial data source.
properties for the initial data source you're creating now go under initial_data_source[properties] to better separate data source specific properties vs. ones that apply to the entire database.
Other parameters apply to the database and continue to be specified at the top-level when creating a database (icon, cover, title).
Only use the new Create Data Source API to add an additional data source (with a new set of properties) to an existing database.
For relation properties: You can no longer provide a database_id. Notion continues to include both the database_id and data_source_id in the response for convenience, but the request object must only contain data_source_id.
Create Database with initial data source (JSON)
Create Database with initial data source (TS SDK)

// POST /v1/databases
{
  "initial_data_source": {
    "properties": {
      // ... (Data source properties behave the same as database properties previously)
    }
  },
  "parent": {"type": "workspace", "workspace": true} | {"type": "page_id", "page_id": "..."},
  "title": [...],
  "icon": {"type": "emoji", "emoji": "🚀"} | ...
}
Update database

Before (2022-06-28):

In 2022-06-28, the Update Database API was used to update attributes that related to both a database and its data source under the hood. For example, is_inline relates to the database, but properties defines the schema of a specific data source.
For relation properties: across all API versions, both the database_id and data_source_id are now included in the response object.
When providing relation properties in a request, you can either use database_id, data_source_id, or both, prior to making the API version upgrade.
We recommend starting by switching your integration over to passing only a data_source_id for relation objects even in 2022-06-28 to precisely identify the data source to use for the relation and be ready for the 2025-09-03 behavior.
Update Database (JSON)
Update Database (TS SDK)

// PATCH /v1/databases/:database_id
{
  "icon": {
    "file_upload": {"id": "..."}
  },
  "properties": {
    "Restocked (new)": {
      "type": "checkbox",
      "checkbox": {}
    },
    "In stock": null
  },
  "title": [{"text": {"content": "New Title"}}]
}
After (2025-09-03):

Continue to use the Update Database API for attributes that apply to the database: parent, title, is_inline, icon, cover, in_trash.
parent can be used to move an existing database to a different page, or (for public integrations), to the workspace level as a private page. This is a new feature in Notion's API.
cover is not supported when is_inline is true.
Switch over to the Update Data Source API to modify attributes that apply to a specific data source: properties (to change database schema), in_trash (to archive or unarchive a specific data source under a database), title.
Changes to one data source's properties doesn't affect the schema for other data source, even if they share a common database.
For relation properties: You can no longer provide a database_id. Notion continues to include both the database_id and data_source_id in the response for convenience, but the request object (to Update Data Source) must only contain data_source_id.
Example for updating a data source's title and properties (adding one new property and removing another):

Update Data Source (JSON)
Update Data Source (TS SDK)

// PATCH /v1/data_sources/:data_source_id
{
  "properties": {
    "Restocked (new)": {
      "type": "checkbox",
      "checkbox": {}
    },
    "In stock": null
  },
  "title": [{"text": {"content": "New Title"}}]
}
Example for updating a database's parent (to move it), and switch it to be inline under the parent page:

Update Data Source (JSON)
Update Data Source (TS SDK)

// PATCH /v1/databases/:database_id
{
  "parent": {"type": "page_id", "page_id": "NEW-PAGE-ID"},
  "is_inline": true
}
Step 4: Handle search results with data sources

Before (2022-06-28):

If any Notion users add a second data source to a database, existing integrations will not see any search results for that database.
After (2025-09-03):

The Search API now only accepts filter["value"] = "page" | "data_source" instead of "page" | "database" when providing a filter["type"] = "object". Make sure to update the body parameters accordingly when upgrading to 2025-09-03.
Currently, the search behavior remains the same. The provided query is matched against the database title, not the data source title.
Similarly, the search API response returns data source IDs & objects.
Aside from the IDs and object: "data_source" in these entries, the rest of the object shape of search is unchanged.
Since results operate at the data source level, they continue to include properties (database schema) as before.
If there are multiple data sources, all of them are included in the search response. Each of them will have a different data source ID.
Step 5: Upgrade SDK (if applicable)

📘
Introducing @notionhq/client v5

v5 of the SDK is now available:

NPM link
GitHub release link
If you see an even newer version (e.g. v5.0.2) at the time you're following these steps, we recommend upgrading directly to the latest version to unlock more enhancements and bugfixes, making the upgrade smoother.
If you're using Notion's TypeScript SDK, and have completed all of the steps above to rework your usage of Notion's endpoints to fit the 2025-09-03 suite of endpoints manually, we recommend completing the migration by upgrading to the next major version release, v5.0.0, via your package.json file (or other version management toolchain.)

The code snippets under Step 3 include the relevant syntax for the new notion.dataSources.* and notion.databases.* methods to assist in your upgrade. Go through each area where you used a manual notion.request(...) call, and switch it over to use one of the dedicated methods. Make sure you're setting the Notion version at initialization time to 2025-09-03.

Note that the List databases (deprecated) endpoint, which has been removed since version 2022-02-22, is no longer included as of v5 of the SDK.

Step 6: Upgrade webhooks (if applicable)

Introducing webhook versioning

When creating, editing, or viewing an integration webhook subscription in Notion's integration settings, there's a new option to set the API version that applies to events delivered to your webhook URL:

Screenshot of the integration webhook "Edit subscription" form, with the new "API version" dropdown menu.
Screenshot of the integration webhook "Edit subscription" form, with the new "API version" dropdown menu.

For new webhook endpoints, we recommend starting with the most recent version. For existing webhook subscriptions, you'll need to carefully introduce support for the added and changed webhook types. Ensure your webhook handler can accept both old & new event payloads before using the "Edit subscription" form to upgrade to the 2025-09-03 API version.

After you've tested your webhook endpoint to ensure the new events are being handled correctly for some period of time (for example, a few hours), you can clean up your system to only expect events with the updated shape. Read on below for specific details on what's changed in 2025-09-03.

New and modified event types

New data_source specific events have been added, and the corresponding existing database events now apply at the database level.

Here's a breakdown of how event types change names or behavior when upgraded to 2025-09-03:

Old Name	New Name	Description
database.content_updated	data_source.content_updated	Data source's content updates
database.schema_updated	data_source.schema_updated	Data source's schema updates
N/A (new event)	data_source.created	New data source is added to an existing database

entity.type is "data_source"
N/A (new event)	data_source.moved	Data source is moved to a different database

entity.type is "data_source"
N/A (new event)	data_source.deleted	Data source is deleted from a database

entity.type is "data_source"
N/A (new event)	data_source.undeleted	Data source is undeleted

entity.type is "data_source"
database.created	(unchanged)	New database is created with a default data source
database.moved	(unchanged)	Database is moved to different parent (i.e. page)
database.deleted	(unchanged)	Database is deleted from its parent
database.undeleted	(unchanged)	Database is undeleted
Updates to parent data

With the 2025-09-03 version, all webhooks for entities that can have data sources as parents now include a new field data_source_id under the data.parent object.

This applies to:

Page events (page.*)
Data source events (the data_source.* ones listed above)
Database events (database.*), but only in rarer cases where databases are directly parented by another database (i.e. wikis)
For example, when a Notion user creates a page within a data source using the Notion app, the resulting page.created event has the following example shape (note the new data.parent.data_source_id field):

JSON

{
  "id": "367cba44-b6f3-4c92-81e7-6a2e9659efd4",
  "timestamp": "2024-12-05T23:55:34.285Z",
  "workspace_id": "13950b26-c203-4f3b-b97d-93ec06319565",
  "workspace_name": "Quantify Labs",
  "subscription_id": "29d75c0d-5546-4414-8459-7b7a92f1fc4b",
  "integration_id": "0ef2e755-4912-8096-91c1-00376a88a5ca",
  "type": "page.created",
  "authors": [
    {
      "id": "c7c11cca-1d73-471d-9b6e-bdef51470190",
      "type": "person"
    }
  ],
  "accessible_by": [
    {
      "id": "556a1abf-4f08-40c6-878a-75890d2a88ba",
      "type": "person"
    },
    {
      "id": "1edc05f6-2702-81b5-8408-00279347f034",
      "type": "bot"
    }
  ],
  "attempt_number": 1,
  "entity": {
    "id": "153104cd-477e-809d-8dc4-ff2d96ae3090",
    "type": "page"
  },
  "data": {
    "parent": {
      "id": "36cc9195-760f-4fff-a67e-3a46c559b176",
      "type": "database",
      "data_source_id": "98024f3c-b1d3-4aec-a301-f01e0dacf023"
    }
  }
}
For compatibility with multi-source databases, use the provided parent.data_source_id to distinguish which data source the page lives in.
Updated about 22 hours ago

FAQs: Version 2025-09-03
Commonly asked questions about data sources and how to migrate to Notion's API version 2025-09-03
Suggest Edits
What is a datasource and how does it relate to a database?

In September 2025, Notion is launching several features to improve what you can do with databases. This includes support for multiple data sources under a single database, each of which can have a different set of properties (schemas). The database becomes a container for one or more data sources.

Diagram of the new Notion API data model.
A database is a parent of one or more data sources, each of which parents zero or more pages.
Previously, databases could only have one data source, so the concepts were combined in the API until 2025
Diagram of the new Notion API data model.
A database is a parent of one or more data sources, each of which parents zero or more pages.
Previously, databases could only have one data source, so the concepts were combined in the API until 2025

To learn more about data sources in the Notion app and related features, visit our help center page.

Is a datasource a new concept?

Prior to this release, databases were limited to one data source, so the data source ID was hidden. Now that multiple data sources are supported, we need a way to identify the specific data source for a request. Starting from the 2025-09-03 API version, Notion is providing a new set of APIs under /v1/data_sources for managing each data source. Most of your integration's existing database operations should move to this set of APIs.

The /v1/databases family of endpoints now refers to the database (container) as of 2025-09-03. To discover the data sources available for a database, the database object includes a data_sources array, each having an id and a name. The data source ID can then by used with the /v1/data_sources APIs.

How does this impact database URLs?

The concept of a database ID in the Notion app stays the same, and continues to be shown in the URL for a database followed by the ID of the specific view you're looking at. For example, in a link like https://notion.so/workspace/248104cd477e80fdb757e945d38000bd?v=148104cd477e80bb928f000ce197ddf2:

248104cd-477e-80fd-b757-e945d38000bd is the database (container) ID.
148104cd477e80bb928f000ce197ddf2 is the database view (managing views is not currently supported in the API).
Note: The ID of the specific data source you're looking at isn't embedded in the URL, but will be listed in a separate dropdown menu.
Can I see an example of how parent & child relationships work?

Here's a diagram of a scenario where a workspace has a top-level page that has a database with two data sources:

Diagram showing a page in a workspace with a database child. The database has two data sources, each of which have two rows (child pages).
Diagram showing a page in a workspace with a database child. The database has two data sources, each of which have two rows (child pages).

Going from top to bottom, here's a simplified run-through of how the API objects connect to one another:

Parent Page:
parent is {"type": "workspace", "workspace": "true"}
No changes to how the page's Block children work.
Database:
parent is {"type": "page_id", "page_id": "<id of Parent Page>"}
data_sources is [{"id": "...", "name": "Data Source"}, {"id": "...", "name": "Data Source"}]
Data Source:
parent is {"type": "database_id", "database_id": "<id of Database>"}
database_parent is {"type": "page_id", "page_id": "<id of Parent Page>"}
Page:
parent is {"type": "data_source_id", "data_source_id": "<id of Data Source>"}
No changes to how the page's Block children work.
How do permissions work for data sources?

User and bot permissions are managed at the database level, not per data source. This means that the level of access a Notion user or integration has (or doesn't have) is the same across all data sources in a database.

How do these changes work with wikis?

Unlike other databases, wikis won't support multiple data sources as part of the September 2025 launch. For this reason, and due to limited support in Notion's API, we recommend using alternative ways to structure your knowledge in Notion that don't involve wikis.

However, for completeness, here's a diagram of how parent/child relationships work in an example wiki scenario:

Diagram showing single-source databases nested under one another as part of a wiki structure.
Diagram showing single-source databases nested under one another as part of a wiki structure.

Which APIs are & aren't affected?

Each family of APIs is summarized in the table below.
Ones that are affected are marked in bold in the first column, and the 2025-09-03 changes are outlined in the second column.
Ones that aren't affected are listed as "None" (some of which have explanatory comments as to why they aren't affected.)
Endpoints	Changes
Authentication	None
Blocks	None
Pages	parent is a data_source_id instead of a database_id
Databases	Modified to act on the entire database (container) instead of its data sources via Create, Retrieve, or Update; see migration guide details above

Creating a database and its initial data source works the same way, but properties must be nested under initial_data_source as of 2025-09-03
Data Sources	New set of APIs for operating on individual data sources under a database via Create, Update, Query, or Retrieve
Comments	None (comments can only have blocks or pages as parents, not databases or data sources, so they aren't affected)
File Uploads	None
Search	Filter value parameter refers to "data_source" instead of "database"; response results include each "data_source" object instead of "database" objects
Users	None

When can I start using the 2025-09-03 version?

The API version is already available to use for Notion API requests as of late August. We recommend starting the upgrade process detailed above at your earliest convenience if your integration is affected by the changes.

If your workspace is connected to any public integrations (rather than an internal bot owned by you or your business), they may not have upgraded yet. If you rely on important workflows or automations, contact the third-party for any questions or issues regarding their timeline & support for databases with multiple sources.

Notes on API versions

As a reminder, API versioning is determined by providing a mandatory Notion-Version HTTP header with each API request. If you're using the TypeScript SDK, you might be configuring the version in one place where the Notion client is instantiated, or passing it explicitly for each request. You can follow the rest of this guide incrementally, upgrading each use of the API at a time at your convenience.

We're also extending the concept of API versioning to integration webhooks to allow Notion to introduce backwards-incompatible changes without affecting your endpoint until you upgrade the API version in the integration settings. Ensure your webhook URL can handle events of both the old and new shape for a short period of time before making the upgrade.

How long will the 2022-06-28 version continue to work?

We don't currently have any process for halting support of old Notion API versions. If we introduce a "minimum versioning" program in the future, we'll communicate this with all affected users with ample notice period (e.g. 6 months) and start with versions that came before 2022-06-28.

However, even though API integrations continue to work, we recommend upgrading to 2025-09-03 as soon as possible. That way, your system is ready for in-app creation of data sources, gains new functionality when working with databases, and you can help Notion's support teams better handle any questions or requests you have by making sure you're up-to-date.

Behavior for existing integrations

Integrations using the 2022-06-28 API version (or older) will continue to work with existing databases in Notion that have a single data source. Webhooks will also generally continue to be delivered without any changes to the format.

However, if any Notion users create a second data source for a database in a workspace that's connected to your integration (starting on September 3, 2025), your database IDs are no longer precise enough for Notion to process the request.

Until you follow this guide to upgrade, Notion responds to requests involving a database ID with multiple data sources with validation errors that look like:

JSON Response

{
  "code": "validation_error",
  "status": 400,
  "message": "Databases with multiple data sources are not supported in this API version.",
  "object": "error",
  "additional_data": {
    "error_type": "multiple_data_sources_for_database",
    "database_id": "27a5d30a-1728-4a1e-a788-71341f22fb97",
    "child_data_source_ids": [
      "164b19c5-58e5-4a47-a3a9-c905d9519c65",
      "25c104cd-477e-8047-836b-000b4aa4bc94"
    ],
    "minimum_api_version": "2025-09-03"
  }
}
The additional_data in the response can help you identify the relevant data source IDs to use instead, as you upgrade your integration.

Why is this the first version upgrade since 2022?

We aim to improve functionality in our API through backwards-compatible features first and foremost. We've shipped several changes since 2022, including the File Upload API, but generally aim to avoid having large sets of users have to go through a detailed upgrade progress when possible.

With these new changes to the Notion app, we want our integration partners, developer community, ambassadors, champions, and everyone else making great tools to unlock the power of multiple-source database containers. This involves rethinking what a "database ID" in the API can do and repurposing API endpoints, necessitating the 2025-09-03 version release.
Updated about 22 hours ago

WHAT’S NEXT
Upgrade your integrations, learn more about integration webhooks, and stay tuned for any future updates to Notion's API:



A block object represents a piece of content within Notion. The API translates the headings, toggles, paragraphs, lists, media, and more that you can interact with in the Notion UI as different [block type objects](https://developers.notion.com/reference/block#block-type-objects).

 For example, the following block object represents a `Heading 2` in the Notion UI:

```json Example Block Object
{
	"object": "block",
	"id": "c02fc1d3-db8b-45c5-a222-27595b15aea7",
	"parent": {
		"type": "page_id",
		"page_id": "59833787-2cf9-4fdf-8782-e53db20768a5"
	},
	"created_time": "2022-03-01T19:05:00.000Z",
	"last_edited_time": "2022-07-06T19:41:00.000Z",
	"created_by": {
		"object": "user",
		"id": "ee5f0f84-409a-440f-983a-a5315961c6e4"
	},
	"last_edited_by": {
		"object": "user",
		"id": "ee5f0f84-409a-440f-983a-a5315961c6e4"
	},
	"has_children": false,
	"archived": false,
  "in_trash": false,
	"type": "heading_2",
	"heading_2": {
		"rich_text": [
			{
				"type": "text",
				"text": {
					"content": "Lacinato kale",
					"link": null
				},
				"annotations": {
					"bold": false,
					"italic": false,
					"strikethrough": false,
					"underline": false,
					"code": false,
					"color": "green"
				},
				"plain_text": "Lacinato kale",
				"href": null
			}
		],
		"color": "default",
    "is_toggleable": false
	}
}
```

Use the [Retrieve block children](https://developers.notion.com/reference/get-block-children) endpoint to list all of the blocks on a page.

# Keys

> 📘
>
> Fields marked with an \* are available to integrations with any capabilities. Other properties require read content capabilities in order to be returned from the Notion API. Consult the [integration capabilities reference](https://developers.notion.com/reference/capabilities) for details.

[block:parameters]
{
  "data": {
    "h-0": "Field",
    "h-1": "Type",
    "h-2": "Description",
    "h-3": "Example value",
    "0-0": "`object`\\*",
    "0-1": "`string`",
    "0-2": "Always `\"block\"`.",
    "0-3": "`\"block\"`",
    "1-0": "`id`\\*",
    "1-1": "`string` (UUIDv4)",
    "1-2": "Identifier for the block.",
    "1-3": "`\"7af38973-3787-41b3-bd75-0ed3a1edfac9\"`",
    "2-0": "`parent`",
    "2-1": "`object`",
    "2-2": "Information about the block's parent. See [Parent object](ref:parent-object).",
    "2-3": "`{ \"type\": \"block_id\", \"block_id\": \"7d50a184-5bbe-4d90-8f29-6bec57ed817b\" }`",
    "3-0": "`type`",
    "3-1": "`string` (enum)",
    "3-2": "Type of block. Possible values are:  \n  \n- [`\"bookmark\"`](https://developers.notion.com/reference/block#bookmark)\n- [`\"breadcrumb\"`](https://developers.notion.com/reference/block#breadcrumb)\n- [`\"bulleted_list_item\"`](https://developers.notion.com/reference/block#bulleted-list-item)\n- [`\"callout\"`](https://developers.notion.com/reference/block#callout)\n- [`\"child_database\"`](https://developers.notion.com/reference/block#child-database)\n- [`\"child_page\"`](https://developers.notion.com/reference/block#child-page)\n- [`\"column\"`](https://developers.notion.com/reference/block#column-list-and-column)\n- [`\"column_list\"`](https://developers.notion.com/reference/block#column-list-and-column)\n- [`\"divider\"`](https://developers.notion.com/reference/block#divider)\n- [`\"embed\"`](https://developers.notion.com/reference/block#embed)\n- [`\"equation\"`](https://developers.notion.com/reference/block#equation)\n- [`\"file\"`](https://developers.notion.com/reference/block#file)\n- [`\"heading_1\"`](https://developers.notion.com/reference/block#heading-1)\n- [`\"heading_2\"`](https://developers.notion.com/reference/block#heading-2)\n- [`\"heading_3\"`](https://developers.notion.com/reference/block#heading-3)\n- [`\"image\"`](https://developers.notion.com/reference/block#image)\n- [`\"link_preview\"`](https://developers.notion.com/reference/block#link-preview)\n- [`\"numbered_list_item\"`](https://developers.notion.com/reference/block#numbered-list-item)\n- [`\"paragraph\"`](https://developers.notion.com/reference/block#paragraph)\n- [`\"pdf\"`](https://developers.notion.com/reference/block#pdf)\n- [`\"quote\"`](https://developers.notion.com/reference/block#quote)\n- [`\"synced_block\"`](https://developers.notion.com/reference/block#synced-block)\n- [`\"table\"`](https://developers.notion.com/reference/block#table)\n- [`\"table_of_contents\"`](https://developers.notion.com/reference/block#table-of-contents)\n- [`\"table_row\"`](https://developers.notion.com/reference/block#table-row)\n- [`\"template\"`](https://developers.notion.com/reference/block#template)\n- [`\"to_do\"`](https://developers.notion.com/reference/block#to-do)\n- [`\"toggle\"`](https://developers.notion.com/reference/block#toggle-blocks)\n- `\"unsupported\"`\n- [`\"video\"`](https://developers.notion.com/reference/block#video)",
    "3-3": "`\"paragraph\"`",
    "4-0": "`created_time`",
    "4-1": "`string` ([ISO 8601 date time](https://en.wikipedia.org/wiki/ISO_8601))",
    "4-2": "Date and time when this block was created. Formatted as an [ISO 8601 date time](https://en.wikipedia.org/wiki/ISO_8601) string.",
    "4-3": "`\"2020-03-17T19:10:04.968Z\"`",
    "5-0": "`created_by`",
    "5-1": "[Partial User](ref:user)",
    "5-2": "User who created the block.",
    "5-3": "`{\"object\": \"user\",\"id\": \"45ee8d13-687b-47ce-a5ca-6e2e45548c4b\"}`",
    "6-0": "`last_edited_time`",
    "6-1": "`string` ([ISO 8601 date time](https://en.wikipedia.org/wiki/ISO_8601))",
    "6-2": "Date and time when this block was last updated. Formatted as an [ISO 8601 date time](https://en.wikipedia.org/wiki/ISO_8601) string.",
    "6-3": "`\"2020-03-17T19:10:04.968Z\"`",
    "7-0": "`last_edited_by`",
    "7-1": "[Partial User](ref:user)",
    "7-2": "User who last edited the block.",
    "7-3": "`{\"object\": \"user\",\"id\": \"45ee8d13-687b-47ce-a5ca-6e2e45548c4b\"}`",
    "8-0": "`archived`",
    "8-1": "`boolean`",
    "8-2": "The archived status of the block.",
    "8-3": "`false`",
    "9-0": "`in_trash`",
    "9-1": "`boolean`",
    "9-2": "Whether the block has been deleted. ",
    "9-3": "`false`",
    "10-0": "`has_children`",
    "10-1": "`boolean`",
    "10-2": "Whether or not the block has children blocks nested within it.",
    "10-3": "`true`",
    "11-0": "`{type}`",
    "11-1": "[`block type object`](https://developers.notion.com/reference/block#block-type-objects)",
    "11-2": "An object containing type-specific block information.",
    "11-3": "Refer to the [block type object section](https://developers.notion.com/reference/block#block-type-objects) for examples of each block type."
  },
  "cols": 4,
  "rows": 12,
  "align": [
    "left",
    "left",
    "left",
    "left"
  ]
}
[/block]


### Block types that support child blocks

Some block types contain nested blocks. The following block types support child blocks:

- [Bulleted list item](https://developers.notion.com/reference/block#bulleted-list-item)
- [Callout](https://developers.notion.com/reference/block#callout)
- [Child database](https://developers.notion.com/reference/block#child-database)
- [Child page](https://developers.notion.com/reference/block#child-page)
- [Column](https://developers.notion.com/reference/block#column-list-and-column)
- [Heading 1](https://developers.notion.com/reference/block#heading-1), when the `is_toggleable` property is `true`
- [Heading 2](https://developers.notion.com/reference/block#heading-2), when the `is_toggleable` property is `true`
- [Heading 3](https://developers.notion.com/reference/block#heading-3), when the `is_toggleable` property is `true`
- [Numbered list item](https://developers.notion.com/reference/block#numbered-list-item)
- [Paragraph](https://developers.notion.com/reference/block#paragraph)
- [Quote](https://developers.notion.com/reference/block#quote)
- [Synced block](https://developers.notion.com/reference/block#synced-block)
- [Table](https://developers.notion.com/reference/block#table)
- [Template](https://developers.notion.com/reference/block#template)
- [To do](https://developers.notion.com/reference/block#to-do)
- [Toggle](https://developers.notion.com/reference/block#toggle-blocks)

> 📘 The API does not support all block types.
>
> Only the block type objects listed in the reference below are supported. Any unsupported block types appear in the structure, but contain a `type` set to `"unsupported"`.

# Block type objects

Every block object has a key corresponding to the value of `type`. Under the key is an object with type-specific block information.

> 📘
>
> Many block types support rich text. In cases where it is supported, a [`rich_text` object](https://developers.notion.com/reference/rich-text) will be included in the block `type` object. All `rich_text` objects will include a `plain_text` property, which provides a convenient way for developers to access unformatted text from the Notion block.

## Audio

Audio block objects contain a [file object](https://developers.notion.com/reference/file-object) detailing information about the audio file.

```json Example Audio block object
{
  "type": "audio",
  //...other keys excluded
  "audio": {
    "type": "external",
    "external": {
      "url": "https://companywebsite.com/files/sample.mp3"
    }
  }
}
```

### Supported audio types

The following file types can be attached with external URLs in the API as well as in the Notion app UI:

- `.mp3`
- `.wav`
- `.ogg`
- `.oga`
- `.m4a`

A wider set of audio files is [supported in the File Upload API](ref:working-with-files-and-media#supported-file-types) and can be attached using a `file_upload` ID.

### Supported file upload types

See the [file upload reference](ref:file-upload#file-types-and-sizes) for a list of supported file extensions and content types when attaching a File Upload to a block.

Audio blocks only support file types in the "audio" section of the table.

## Bookmark

Bookmark block objects contain the following information within the `bookmark` property:

| Field     | Type                                             | Description                   |
| :-------- | :----------------------------------------------- | :---------------------------- |
| `caption` | array of [rich text objects](ref:rich-text) text | The caption for the bookmark. |
| `url`     | string                                           | The link for the bookmark.    |

```json Example Bookmark block object
{
  //...other keys excluded
  "type": "bookmark",
  //...other keys excluded
  "bookmark": {
    "caption": [],
    "url": "https://companywebsite.com"
  }
}
```

## Breadcrumb

Breadcrumb block objects do not contain any information within the `breadcrumb` property.

```json Example Breadcrumb block object
{
  //...other keys excluded
  "type": "breadcrumb",
  //...other keys excluded
  "breadcrumb": {}
}
```

## Bulleted list item

Bulleted list item block objects contain the following information within the `bulleted_list_item` property:

[block:parameters]
{
  "data": {
    "h-0": "Field",
    "h-1": "Type",
    "h-2": "Description",
    "0-0": "`rich_text`",
    "0-1": "`array` of [rich text objects](ref:rich-text)",
    "0-2": "The rich text in the `bulleted_list_item` block.",
    "1-0": "`color`",
    "1-1": "`string` (enum)",
    "1-2": "The color of the block. Possible values are:  \n  \n- `\"blue\"`\n- `\"blue_background\"`\n- `\"brown\"`\n- `\"brown_background\"`\n- `\"default\"`\n- `\"gray\"`\n- `\"gray_background\"`\n- `\"green\"`\n- `\"green_background\"`\n- `\"orange\"`\n- `\"orange_background\"`\n- `\"yellow\"`\n- `\"green\"`\n- `\"pink\"`\n- `\"pink_background\"`\n- `\"purple\"`\n- `\"purple_background\"`\n- `\"red\"`\n- `\"red_background\"`\n- `\"yellow_background\"`",
    "2-0": "`children`",
    "2-1": "`array` of [block objects](ref:block)",
    "2-2": "The nested child blocks (if any) of the `bulleted_list_item` block."
  },
  "cols": 3,
  "rows": 3,
  "align": [
    "left",
    "left",
    "left"
  ]
}
[/block]


```json Example Bulleted list item block object
{
  //...other keys excluded
  "type": "bulleted_list_item",
  //...other keys excluded
  "bulleted_list_item": {
    "rich_text": [{
      "type": "text",
      "text": {
        "content": "Lacinato kale",
        "link": null
      }
      // ..other keys excluded
    }],
    "color": "default",
    "children":[{
      "type": "paragraph"
      // ..other keys excluded
    }]
  }
}
```

## Callout

Callout block objects contain the following information within the `callout` property:

[block:parameters]
{
  "data": {
    "h-0": "Field",
    "h-1": "Type",
    "h-2": "Description",
    "0-0": "`rich_text`",
    "0-1": "`array` of [rich text objects](ref:rich-text)",
    "0-2": "The rich text in the `callout` block.",
    "1-0": "`icon`",
    "1-1": "`object`",
    "1-2": "An [emoji](https://developers.notion.com/reference/emoji-object) or [file](https://developers.notion.com/reference/file-object) object that represents the callout's icon. If the callout does not have an icon.",
    "2-0": "`color`",
    "2-1": "`string` (enum)",
    "2-2": "The color of the block. Possible values are:  \n  \n- `\"blue\"`\n- `\"blue_background\"`\n- `\"brown\"`\n- `\"brown_background\"`\n- `\"default\"`\n- `\"gray\"`\n- `\"gray_background\"`\n- `\"green\"`\n- `\"green_background\"`\n- `\"orange\"`\n- `\"orange_background\"`\n- `\"yellow\"`\n- `\"green\"`\n- `\"pink\"`\n- `\"pink_background\"`\n- `\"purple\"`\n- `\"purple_background\"`\n- `\"red\"`\n- `\"red_background\"`\n- `\"yellow_background\"`"
  },
  "cols": 3,
  "rows": 3,
  "align": [
    "left",
    "left",
    "left"
  ]
}
[/block]


```json Example Callout block object
{
  //...other keys excluded
	"type": "callout",
   // ..other keys excluded
   "callout": {
   	"rich_text": [{
      "type": "text",
      "text": {
        "content": "Lacinato kale",
        "link": null
      }
      // ..other keys excluded
    }],
     "icon": {
       "emoji": "⭐"
     },
     "color": "default"
   }
}
```

## Child database

Child database block objects contain the following information within the `child_database` property:

| Field   | Type     | Description                           |
| :------ | :------- | :------------------------------------ |
| `title` | `string` | The plain text title of the database. |

```json Example Child database block
{
  //...other keys excluded
  "type": "child_database",
  //...other keys excluded
  "child_database": {
    "title": "My database"
  }
}
```

> 📘 Creating and updating `child_database` blocks
>
> To create or update `child_database` type blocks, use the [Create a database](ref:create-a-database) and the [Update a database](ref:update-a-database) endpoints, specifying the ID of the parent page in the `parent` body param.

## Child page

Child page block objects contain the following information within the `child_page` property:

| Field   | Type     | Description                         |
| :------ | :------- | :---------------------------------- |
| `title` | `string` | The plain text `title` of the page. |

```json Example Child page block object
{
  //...other keys excluded
  "type": "child_page",
  //...other keys excluded
  "child_page": {
    "title": "Lacinato kale"
  }
}
```

> 📘 Creating and updating `child_page` blocks
>
> To create or update `child_page` type blocks, use the [Create a page](https://developers.notion.com/reference/post-page) and the [Update page](https://developers.notion.com/reference/patch-page) endpoints, specifying the ID of the parent page in the `parent` body param.

## Code

Code block objects contain the following information within the `code` property:

| Field       | Type                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | Description                                           |
| :---------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------- |
| `caption`   | `array` of [Rich text object](ref:rich-text) text objects                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | The rich text in the caption of the code block.       |
| `rich_text` | `array` of [Rich text object](ref:rich-text) text objects                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | The rich text in the code block.                      |
| `language`  | - `"abap"` - `"arduino"` - `"bash"` - `"basic"` - `"c"` - `"clojure"` - `"coffeescript"` - `"c++"` - `"c#"` - `"css"` - `"dart"` - `"diff"` - `"docker"` - `"elixir"` - `"elm"` - `"erlang"` - `"flow"` - `"fortran"` - `"f#"` - `"gherkin"` - `"glsl"` - `"go"` - `"graphql"` - `"groovy"` - `"haskell"` - `"html"` - `"java"` - `"javascript"` - `"json"` - `"julia"` - `"kotlin"` - `"latex"` - `"less"` - `"lisp"` - `"livescript"` - `"lua"` - `"makefile"` - `"markdown"` - `"markup"` - `"matlab"` - `"mermaid"` - `"nix"` - `"objective-c"` - `"ocaml"` - `"pascal"` - `"perl"` - `"php"` - `"plain text"` - `"powershell"` - `"prolog"` - `"protobuf"` - `"python"` - `"r"` - `"reason"` - `"ruby"` - `"rust"` - `"sass"` - `"scala"` - `"scheme"` - `"scss"` - `"shell"` - `"sql"` - `"swift"` - `"typescript"` - `"vb.net"` - `"verilog"` - `"vhdl"` - `"visual basic"` - `"webassembly"` - `"xml"` - `"yaml"` - `"java/c/c++/c#"` | The language of the code contained in the code block. |

```json Example Code block object
{
  // ... other keys excluded
  "type": "code",
  // ... other keys excluded
  "code": {
    "caption": [],
    "rich_text": [{
      "type": "text",
      "text": {
        "content": "const a = 3"
      }
    }],
    "language": "javascript"
  }
}
```

## Column list and column

Column lists are parent blocks for columns. They do not contain any information within the `column_list` property.

```json Example Column list block object
{
  // ... other keys excluded
  "type": "column_list",
  // ... other keys excluded
  "column_list": {}
}
```

Columns are parent blocks for any block types listed in this reference except for other `column`s. They do not require any information within the `column` property, but a `width_ratio` number between 0 and 1 can be provided to customize the width of a column relative to others in the same column list. When omitted, the default is to use equal widths for all columns. When provided, `width_ratio`s should add up to 1.

Columns can only be appended to `column_list`s.

```json Example Column object
{
  // ... other keys excluded
  "type": "column",
  // ... other keys excluded
  "column": {
    "width_ratio": 0.25
  }
}
```

When creating a `column_list` block via [Append block children](https://developers.notion.com/reference/patch-block-children), the `column_list` must have at least two `column`s, and each `column` must have at least one child.

### Retrieve the content in a column list

Follow these steps to fetch the content in a `column_list`:

1. Get the `column_list` ID from a query to [Retrieve block children](https://developers.notion.com/reference/get-block-children) for the parent page.

2. Get the `column` children from a query to Retrieve block children for the `column_list`.

3. Get the content in each individual `column` from a query to Retrieve block children for the unique `column` ID.

## Divider

Divider block objects do not contain any information within the `divider` property.

```json Example Divider block object
{
  //...other keys excluded
  "type": "divider",
  //...other keys excluded
  "divider": {}
}
```

## Embed

Embed block objects include information about another website displayed within the Notion UI. The `embed` property contains the following information:

| Field | Type     | Description                                            |
| :---- | :------- | :----------------------------------------------------- |
| `url` | `string` | The link to the website that the embed block displays. |

```json Example Embed block object
{
  //...other keys excluded
  "type": "embed",
  //...other keys excluded
  "embed": {
    "url": "https://companywebsite.com"
  }
}
```

> 🚧 Differences in embed blocks between the Notion app and the API
>
> The Notion app uses a 3rd-party service, iFramely, to validate and request metadata for embeds given a URL. This works well in a web app because Notion can kick off an asynchronous request for URL information, which might take seconds or longer to complete, and then update the block with the metadata in the UI after receiving a response from iFramely.
>
> We chose not to call iFramely when creating embed blocks in the API because the API needs to be able to return faster than the UI, and because the response from iFramely could actually cause us to change the block type. This would result in a slow and potentially confusing experience as the block in the response would not match the block sent in the request.
>
> The result is that embed blocks created via the API may not look exactly like their counterparts created in the Notion app.

> 👍
>
> Vimeo video links can be embedded in a Notion page via the public API using the embed block type.
>
> For example, the following object can be passed to the [Append block children endpoint](https://developers.notion.com/reference/patch-block-children):
>
> ```json
> {
>   "children": [
>     {
>       "embed": {
>         "url": "https://player.vimeo.com/video/226053498?h=a1599a8ee9"
>       }
>     }
>   ]
> }
> ```
>
> For other video sources, see [Supported video types](https://developers.notion.com/reference/block#supported-video-types).

## Equation

Equation block objects are represented as children of [paragraph](https://developers.notion.com/reference/block#paragraph) blocks. They are nested within a [rich text object](https://developers.notion.com/reference/rich-text) and contain the following information within the `equation` property:

| Field        | Type     | Description                |
| :----------- | :------- | :------------------------- |
| `expression` | `string` | A KaTeX compatible string. |

```json Example Equation object
{
  //...other keys excluded
  "type": "equation",
  //...other keys excluded
  "equation": {
    "expression": "e=mc^2"
  }
}
```

## File

File block objects contain the following information within the `file` property:

[block:parameters]
{
  "data": {
    "h-0": "Field",
    "h-1": "Type",
    "h-2": "Description",
    "0-0": "`caption`",
    "0-1": "`array` of [rich text objects](ref:rich-text)",
    "0-2": "The caption of the file block.",
    "1-0": "`type`",
    "1-1": "One of:  \n  \n- `\"file\"`\n- `\"external\"`\n- `\"file_upload\"`",
    "1-2": "Type of file. This enum value indicates which of the following three objects are populated.",
    "2-0": "`file`",
    "2-1": "[Notion-hosted file object](ref:file-object#notion-hosted-files)",
    "2-2": "A file object that details information about the file contained in the block: a temporary download `url` and `expiry_time`. After the `expiry_time`, fetch the block again from the API to get a new `url`.  \n  \nOnly valid as a parameter if copied verbatim from the `file` field of a recent block API response from Notion. To attach a file, provide a `type` of `file_upload` instead.",
    "3-0": "`external`",
    "3-1": "[External file object](ref:file-object#external-files)",
    "3-2": "An object with a `url` property, identifying a publicly accessible URL.",
    "4-0": "`file_upload`",
    "4-1": "[File upload object](ref:file#file-uploads)",
    "4-2": "An object with the `id` of a [FileUpload](ref:file-upload) to attach to the block. After attaching, the API response responds with a type of `file`, not `file_upload`, so your integration can access a download `url`.",
    "5-0": "`name`",
    "5-1": "`string`",
    "5-2": "The name of the file, as shown in the Notion UI. Note that the UI may auto-append `.pdf` or other extensions.  \n  \nWhen attaching a `file_upload`, the `name` parameter is not required."
  },
  "cols": 3,
  "rows": 6,
  "align": [
    "left",
    "left",
    "left"
  ]
}
[/block]


```json Example File block
{
  // ... other keys excluded
  "type": "file",
  // ... other keys excluded
  "file": {
    "caption": [],
    "type": "external",
    "external": {
      "url": "https://companywebsite.com/files/doc.txt"
    },
    "name": "doc.txt"
  }
}
```

## Headings

All heading block objects, `heading_1`, `heading_2`, and `heading_3`, contain the following information within their corresponding objects:

[block:parameters]
{
  "data": {
    "h-0": "Field",
    "h-1": "Type",
    "h-2": "Description",
    "0-0": "`rich_text`",
    "0-1": "`array` of [rich text objects](ref:rich-text)",
    "0-2": "The rich text of the heading.",
    "1-0": "`color`",
    "1-1": "`string` (enum)",
    "1-2": "The color of the block. Possible values are:  \n  \n- `\"blue\"`\n- `\"blue_background\"`\n- `\"brown\"`\n- `\"brown_background\"`\n- `\"default\"`\n- `\"gray\"`\n- `\"gray_background\"`\n- `\"green\"`\n- `\"green_background\"`\n- `\"orange\"`\n- `\"orange_background\"`\n- `\"yellow\"`\n- `\"green\"`\n- `\"pink\"`\n- `\"pink_background\"`\n- `\"purple\"`\n- `\"purple_background\"`\n- `\"red\"`\n- `\"red_background\"`\n- `\"yellow_background\"`",
    "2-0": "`is_toggleable`",
    "2-1": "`boolean`",
    "2-2": "Whether or not the heading block is a toggle heading or not. If `true`, then the heading block toggles and can support children. If `false`, then the heading block is a static heading block."
  },
  "cols": 3,
  "rows": 3,
  "align": [
    "left",
    "left",
    "left"
  ]
}
[/block]


```json Example Heading 1 block object
{
  //...other keys excluded
  "type": "heading_1",
  //...other keys excluded
  "heading_1": {
    "rich_text": [{
      "type": "text",
      "text": {
        "content": "Lacinato kale",
        "link": null
      }
    }],
    "color": "default",
    "is_toggleable": false
  }
}
```

```json Example Heading 2 block object
{
  //...other keys excluded
  "type": "heading_2",
  //...other keys excluded
  "heading_2": {
    "rich_text": [{
      "type": "text",
      "text": {
        "content": "Lacinato kale",
        "link": null
      }
    }],
    "color": "default",
    "is_toggleable": false
  }
}
```

```json Example Heading 3 block object
{
  //...other keys excluded
  "type": "heading_3",
  //...other keys excluded
  "heading_3": {
    "rich_text": [{
      "type": "text",
      "text": {
        "content": "Lacinato kale",
        "link": null
      }
    }],
    "color": "default",
    "is_toggleable": false
  }
}
```

## Image

Image block objects contain a [file object](https://developers.notion.com/reference/file-object) detailing information about the image.

```json Example Image block object
{
  // ... other keys excluded
  "type": "image",
  // ... other keys excluded
  "image": {
    "type": "external",
    "external": {
      "url": "https://website.domain/images/image.png"
    }
  }
}
```

### Supported external image types

The image must be directly hosted. In other words, the `url` cannot point to a service that retrieves the image. The following image types are supported:

- `.bmp`
- `.gif`
- `.heic`
- `.jpeg`
- `.jpg`
- `.png`
- `.svg`
- `.tif`
- `.tiff`

### Supported file upload types

See the [file upload reference](ref:file-upload#file-types-and-sizes) for a list of supported file extensions and content types when attaching a File Upload to a block.

Image blocks only support file types in the "image" section of the table.

## Link Preview

[Link Preview](https://developers.notion.com/docs/link-previews) block objects contain the originally pasted `url`:

```json Example Link preview block object
{
  //...other keys excluded
  "type": "link_preview",
  //...other keys excluded
  "link_preview": {
    "url": "https://github.com/example/example-repo/pull/1234"
  }
}
```

> 🚧
>
> The `link_preview` block can only be returned as part of a response. The API does not support creating or appending `link_preview` blocks.

## Mention

A mention block object is a child of a [rich text object](https://developers.notion.com/reference/rich-text) that is nested within a [paragraph block object](https://developers.notion.com/reference/block#paragraph). This block type represents any `@` tag in the Notion UI, for a user, date, Notion page, Notion database, or a miniaturized version of a [Link Preview](https://developers.notion.com/reference/unfurl-attribute-object).

A mention block object contains the following fields:

[block:parameters]
{
  "data": {
    "h-0": "Field",
    "h-1": "Type",
    "h-2": "Description",
    "0-0": "`type`",
    "0-1": "`\"database\"`  \n  \n`\"date\"`  \n  \n`\"link_preview\"`  \n  \n`\"page\"`  \n  \n`\"user\"`",
    "0-2": "A constant string representing the type of the mention.",
    "1-0": "`\"database\"`  \n  \n`\"date\"`  \n  \n`\"link_preview\"`  \n  \n`\"page\"`  \n  \n`\"user\"`",
    "1-1": "`object`",
    "1-2": "An object with type-specific information about the mention."
  },
  "cols": 3,
  "rows": 2,
  "align": [
    "left",
    "left",
    "left"
  ]
}
[/block]


```json Example Mention object
{
  //...other keys excluded
  "type": "page",
  "page": {
    "id": "3c612f56-fdd0-4a30-a4d6-bda7d7426309"
  }
}
```

## Numbered list item

Numbered list item block objects contain the following information within the `numbered_list_item` property:

[block:parameters]
{
  "data": {
    "h-0": "Field",
    "h-1": "Type",
    "h-2": "Description",
    "0-0": "`rich_text`",
    "0-1": "`array` of [rich text objects](ref:rich-text)",
    "0-2": "The rich text displayed in the `numbered_list_item` block.",
    "1-0": "`color`",
    "1-1": "`string` (enum)",
    "1-2": "The color of the block. Possible values are:  \n  \n- `\"blue\"`\n- `\"blue_background\"`\n- `\"brown\"`\n- `\"brown_background\"`\n- `\"default\"`\n- `\"gray\"`\n- `\"gray_background\"`\n- `\"green\"`\n- `\"green_background\"`\n- `\"orange\"`\n- `\"orange_background\"`\n- `\"yellow\"`\n- `\"green\"`\n- `\"pink\"`\n- `\"pink_background\"`\n- `\"purple\"`\n- `\"purple_background\"`\n- `\"red\"`\n- `\"red_background\"`\n- `\"yellow_background\"`",
    "2-0": "`children`",
    "2-1": "`array` of [block objects](ref:block)",
    "2-2": "The nested child blocks (if any) of the `numbered_list_item` block."
  },
  "cols": 3,
  "rows": 3,
  "align": [
    "left",
    "left",
    "left"
  ]
}
[/block]


```json Example Numbered list item block
{
  //...other keys excluded
  "type": "numbered_list_item",
  "numbered_list_item": {
    "rich_text": [
      {
        "type": "text",
        "text": {
          "content": "Finish reading the docs",
          "link": null
        }
      }
    ],
    "color": "default"
  }
}
```

## Paragraph

Paragraph block objects contain the following information within the `paragraph` property:

[block:parameters]
{
  "data": {
    "h-0": "Field",
    "h-1": "Type",
    "h-2": "Description",
    "0-0": "`rich_text`",
    "0-1": "`array` of [rich text objects](ref:rich-text)",
    "0-2": "The rich text displayed in the paragraph block.",
    "1-0": "`color`",
    "1-1": "`string` (enum)",
    "1-2": "The color of the block. Possible values are:  \n  \n- `\"blue\"`\n- `\"blue_background\"`\n- `\"brown\"`\n- `\"brown_background\"`\n- `\"default\"`\n- `\"gray\"`\n- `\"gray_background\"`\n- `\"green\"`\n- `\"green_background\"`\n- `\"orange\"`\n- `\"orange_background\"`\n- `\"yellow\"`\n- `\"green\"`\n- `\"pink\"`\n- `\"pink_background\"`\n- `\"purple\"`\n- `\"purple_background\"`\n- `\"red\"`\n- `\"red_background\"`\n- `\"yellow_background\"`",
    "2-0": "`children`",
    "2-1": "`array` of [block objects](ref:block)",
    "2-2": "The nested child blocks (if any) of the `paragraph` block."
  },
  "cols": 3,
  "rows": 3,
  "align": [
    "left",
    "left",
    "left"
  ]
}
[/block]


```json Example Paragraph block object
{
  //...other keys excluded
  "type": "paragraph",
  //...other keys excluded
  "paragraph": {
    "rich_text": [{
      "type": "text",
      "text": {
        "content": "Lacinato kale",
        "link": null
      }
    }],
    "color": "default"
}
```

```json Example Paragraph block object with a child Mention block object
{
//...other keys excluded
	"type": "paragraph",
  	"paragraph":{
  		"rich_text": [
    		{
      		"type": "mention",
      		"mention": {
        		"type": "date",
        		"date": {
          		"start": "2023-03-01",
          		"end": null,
          		"time_zone": null
        		}
      		},
      		"annotations": {
        		"bold": false,
        		"italic": false,
        		"strikethrough": false,
        		"underline": false,
        		"code": false,
        		"color": "default"
      		},
      		"plain_text": "2023-03-01",
      		"href": null
    		},
    		{
          "type": "text",
      		"text": {
        		"content": " ",
        		"link": null
      		},
      		"annotations": {
        		"bold": false,
        		"italic": false,
        		"strikethrough": false,
        		"underline": false,
        		"code": false,
        		"color": "default"
      		},
      		"plain_text": " ",
      		"href": null
    		}
  		],
  		"color": "default"
  	}
}
```

## PDF

A PDF block object represents a PDF that has been embedded within a Notion page. It contains the following fields:

[block:parameters]
{
  "data": {
    "h-0": "Property",
    "h-1": "Type",
    "h-2": "Description",
    "0-0": "`caption`",
    "0-1": "`array` of [rich text objects](ref:rich-text)",
    "0-2": "A caption, if provided, for the PDF block.",
    "1-0": "`type`",
    "1-1": "One of:  \n  \n- `\"file\"`\n- `\"external\"`\n- `\"file_upload\"`",
    "1-2": "A constant string representing the type of PDF. `file` indicates a Notion-hosted file, and `external` represents a third-party link. `file_upload` is only valid when providing parameters to attach a [File Upload](ref:file-upload) to a PDF block.",
    "2-0": "`external` \\|  \n`file` \\|  \n`file_upload`",
    "2-1": "[file object](https://developers.notion.com/reference/file-object)",
    "2-2": "An object containing type-specific information about the PDF."
  },
  "cols": 3,
  "rows": 3,
  "align": [
    "left",
    "left",
    "left"
  ]
}
[/block]


```json
{
  //...other keys excluded
  "type": "pdf",
  //...other keys excluded
  "pdf": {
    "type": "external",
    "external": {
      "url": "https://website.domain/files/doc.pdf"
    }
  }
}
```

### Supported file upload types

See the [file upload reference](ref:file-upload#file-types-and-sizes) for a list of supported file extensions and content types when attaching a File Upload to a block.

PDF blocks only support a type of `.pdf`.

## Quote

Quote block objects contain the following information within the `quote` property:

[block:parameters]
{
  "data": {
    "h-0": "Field",
    "h-1": "Type",
    "h-2": "Description",
    "0-0": "`rich_text`",
    "0-1": "`array` of [rich text objects](ref:rich-text)",
    "0-2": "The rich text displayed in the quote block.",
    "1-0": "`color`",
    "1-1": "`string` (enum)",
    "1-2": "The color of the block. Possible values are:  \n  \n- `\"blue\"`\n- `\"blue_background\"`\n- `\"brown\"`\n- `\"brown_background\"`\n- `\"default\"`\n- `\"gray\"`\n- `\"gray_background\"`\n- `\"green\"`\n- `\"green_background\"`\n- `\"orange\"`\n- `\"orange_background\"`\n- `\"yellow\"`\n- `\"green\"`\n- `\"pink\"`\n- `\"pink_background\"`\n- `\"purple\"`\n- `\"purple_background\"`\n- `\"red\"`\n- `\"red_background\"`\n- `\"yellow_background\"`",
    "2-0": "`children`",
    "2-1": "`array` of [block objects](ref:block)",
    "2-2": "The nested child blocks, if any, of the quote block."
  },
  "cols": 3,
  "rows": 3,
  "align": [
    "left",
    "left",
    "left"
  ]
}
[/block]


```json Example Quote block
{
	//...other keys excluded
	"type": "quote",
   //...other keys excluded
   "quote": {
   	"rich_text": [{
      "type": "text",
      "text": {
        "content": "To be or not to be...",
        "link": null
      },
    	//...other keys excluded
    }],
    //...other keys excluded
    "color": "default"
   }
}
```

## Synced block

Similar to the Notion UI, there are two versions of a `synced_block` object: the original block that was created first and doesn't yet sync with anything else, and the duplicate block or blocks synced to the original.

> 📘
>
> An original synced block must be created before corresponding duplicate block or blocks can be made.

### Original synced block

Original synced block objects contain the following information within the `synced_block` property:

| Field         | Type                                  | Description                                                                                                                  |
| :------------ | :------------------------------------ | :--------------------------------------------------------------------------------------------------------------------------- |
| `synced_from` | `null`                                | The value is always `null` to signify that this is an original synced block that does not refer to another block.            |
| `children`    | `array` of [block objects](ref:block) | The nested child blocks, if any, of the `synced_block` block. These blocks will be mirrored in the duplicate `synced_block`. |

```json Example Original synced block
{
    //...other keys excluded
  	"type": "synced_block",
    "synced_block": {
        "synced_from": null,
        "children": [
            {
                "callout": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": "Callout in synced block"
                            }
                        }
                    ]
                }
            }
        ]
    }
}
```

### Duplicate synced block

Duplicate synced block objects contain the following information within the `synced_from` object:

[block:parameters]
{
  "data": {
    "h-0": "Field",
    "h-1": "Type",
    "h-2": "Description",
    "0-0": "`type`",
    "0-1": "`string` (enum)",
    "0-2": "The type of the synced from object.  \n  \nPossible values are:  \n  \n- `\"block_id\"`",
    "1-0": "`block_id`",
    "1-1": "`string` (UUIDv4)",
    "1-2": "An identifier for the original `synced_block`."
  },
  "cols": 3,
  "rows": 2,
  "align": [
    "left",
    "left",
    "left"
  ]
}
[/block]


```json Example Duplicate synced block object
{
    //...other keys excluded
  	"type": "synced_block",
    "synced_block": {
        "synced_from": {
            "block_id": "original_synced_block_id"
        }
    }
}
```

> 🚧
>
> The API does not supported updating synced block content.

## Table

Table block objects are parent blocks for table row children. Table block objects contain the following fields within the `table` property:

[block:parameters]
{
  "data": {
    "h-0": "Field",
    "h-1": "Type",
    "h-2": "Description",
    "0-0": "`table_width`",
    "0-1": "`integer`",
    "0-2": "The number of columns in the table.  \n  \n**Note that this cannot be changed via the public API once a table is created.**",
    "1-0": "`has_column_header`",
    "1-1": "`boolean`",
    "1-2": "Whether the table has a column header. If `true`, then the first row in the table appears visually distinct from the other rows.",
    "2-0": "`has_row_header`",
    "2-1": "`boolean`",
    "2-2": "Whether the table has a header row. If `true`, then the first column in the table appears visually distinct from the other columns."
  },
  "cols": 3,
  "rows": 3,
  "align": [
    "left",
    "left",
    "left"
  ]
}
[/block]


```json Example Table block object
{
  //...other keys excluded
  "type": "table",
  "table": {
    "table_width": 2,
    "has_column_header": false,
    "has_row_header": false
  }
}
```

> 🚧 `table_width` can only be set when the table is first created.
>
> Note that the number of columns in a table can only be set when the table is first created. Calls to the Update block endpoint to update `table_width` fail.

### Table rows

Follow these steps to fetch the `table_row`s of a `table`:

1. Get the `table` ID from a query to [Retrieve block children](https://developers.notion.com/reference/get-block-children) for the parent page.

2. Get the `table_rows` from a query to Retrieve block children for the `table`.

A `table_row` block object contains the following fields within the `table_row` property:

| Property | Type                                                   | Description                                                                                        |
| :------- | :----------------------------------------------------- | :------------------------------------------------------------------------------------------------- |
| `cells`  | `array` of array of [rich text objects](ref:rich-text) | An array of cell contents in horizontal display order. Each cell is an array of rich text objects. |

```json Example Table row block object
{
  //...other keys excluded
  "type": "table_row",
  "table_row": {
    "cells": [
      [
        {
          "type": "text",
          "text": {
            "content": "column 1 content",
            "link": null
          },
          "annotations": {
            "bold": false,
            "italic": false,
            "strikethrough": false,
            "underline": false,
            "code": false,
            "color": "default"
          },
          "plain_text": "column 1 content",
          "href": null
        }
      ],
      [
        {
          "type": "text",
          "text": {
            "content": "column 2 content",
            "link": null
          },
          "annotations": {
            "bold": false,
            "italic": false,
            "strikethrough": false,
            "underline": false,
            "code": false,
            "color": "default"
          },
          "plain_text": "column 2 content",
          "href": null
        }
      ],
      [
        {
          "type": "text",
          "text": {
            "content": "column 3 content",
            "link": null
          },
          "annotations": {
            "bold": false,
            "italic": false,
            "strikethrough": false,
            "underline": false,
            "code": false,
            "color": "default"
          },
          "plain_text": "column 3 content",
          "href": null
        }
      ]
    ]
  }
}
```

> 📘
>
> When creating a table block via the [Append block children](ref:patch-block-children) endpoint, the `table` must have at least one `table_row` whose `cells` array has the same length as the `table_width`.

## Table of contents

Table of contents block objects contain the following information within the `table_of_contents` property:

[block:parameters]
{
  "data": {
    "h-0": "Property",
    "h-1": "Type",
    "h-2": "Description",
    "0-0": "`color`",
    "0-1": "`string` (enum)",
    "0-2": "The color of the block. Possible values are:  \n  \n- `\"blue\"`\n- `\"blue_background\"`\n- `\"brown\"`\n- `\"brown_background\"`\n- `\"default\"`\n- `\"gray\"`\n- `\"gray_background\"`\n- `\"green\"`\n- `\"green_background\"`\n- `\"orange\"`\n- `\"orange_background\"`\n- `\"yellow\"`\n- `\"green\"`\n- `\"pink\"`\n- `\"pink_background\"`\n- `\"purple\"`\n- `\"purple_background\"`\n- `\"red\"`\n- `\"red_background\"`\n- `\"yellow_background\"`"
  },
  "cols": 3,
  "rows": 1,
  "align": [
    "left",
    "left",
    "left"
  ]
}
[/block]


```json Example Table of contents block object
{
  //...other keys excluded
	"type": "table_of_contents",
  "table_of_contents": {
  	"color": "default"
  }
}
```

## Template

> ❗️ Deprecation Notice
>
> As of March 27, 2023 creation of template blocks will no longer be supported.

Template blocks represent [template buttons](https://www.notion.so/help/template-buttons) in the Notion UI.

Template block objects contain the following information within the `template` property:

| Field       | Type                                          | Description                                                                                                                    |
| :---------- | :-------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------- |
| `rich_text` | `array` of [rich text objects](ref:rich-text) | The rich text displayed in the title of the template.                                                                          |
| `children`  | `array` of [block objects](ref:block)         | The nested child blocks, if any, of the template block. These blocks are duplicated when the template block is used in the UI. |

```json Example Template block object
{
  //...other keys excluded
  "template": {
    "rich_text": [
      {
        "type": "text",
        "text": {
          "content": "Add a new to-do",
          "link": null
        },
        "annotations": {
          //...other keys excluded
        },
        "plain_text": "Add a new to-do",
        "href": null
      }
    ]
  }
}
```

## To do

To do block objects contain the following information within the `to_do` property:

[block:parameters]
{
  "data": {
    "h-0": "Field",
    "h-1": "Type",
    "h-2": "Description",
    "0-0": "`rich_text`",
    "0-1": "`array` of [rich text objects](ref:rich-text)",
    "0-2": "The rich text displayed in the To do block.",
    "1-0": "`checked`",
    "1-1": "`boolean` (optional)",
    "1-2": "Whether the To do is checked.",
    "2-0": "`color`",
    "2-1": "`string` (enum)",
    "2-2": "The color of the block. Possible values are:  \n  \n- `\"blue\"`\n- `\"blue_background\"`\n- `\"brown\"`\n- `\"brown_background\"`\n- `\"default\"`\n- `\"gray\"`\n- `\"gray_background\"`\n- `\"green\"`\n- `\"green_background\"`\n- `\"orange\"`\n- `\"orange_background\"`\n- `\"yellow\"`\n- `\"green\"`\n- `\"pink\"`\n- `\"pink_background\"`\n- `\"purple\"`\n- `\"purple_background\"`\n- `\"red\"`\n- `\"red_background\"`\n- `\"yellow_background\"`",
    "3-0": "`children`",
    "3-1": "`array` of [block objects](ref:block)",
    "3-2": "The nested child blocks, if any, of the To do block."
  },
  "cols": 3,
  "rows": 4,
  "align": [
    "left",
    "left",
    "left"
  ]
}
[/block]


```json Example To do block object
{
  //...other keys excluded
  "type": "to_do",
  "to_do": {
    "rich_text": [{
      "type": "text",
      "text": {
        "content": "Finish Q3 goals",
        "link": null
      }
    }],
    "checked": false,
    "color": "default",
    "children":[{
      "type": "paragraph"
      // ..other keys excluded
    }]
  }
}
```

## Toggle blocks

Toggle block objects contain the following information within the `toggle` property:

[block:parameters]
{
  "data": {
    "h-0": "Field",
    "h-1": "Type",
    "h-2": "Description",
    "0-0": "`rich_text`",
    "0-1": "`array` of [rich text objects](ref:rich-text)",
    "0-2": "The rich text displayed in the Toggle block.",
    "1-0": "`color`",
    "1-1": "`string` (enum)",
    "1-2": "The color of the block. Possible values are:  \n  \n- `\"blue\"`\n- `\"blue_background\"`\n- `\"brown\"`\n- `\"brown_background\"`\n- `\"default\"`\n- `\"gray\"`\n- `\"gray_background\"`\n- `\"green\"`\n- `\"green_background\"`\n- `\"orange\"`\n- `\"orange_background\"`\n- `\"yellow\"`\n- `\"green\"`\n- `\"pink\"`\n- `\"pink_background\"`\n- `\"purple\"`\n- `\"purple_background\"`\n- `\"red\"`\n- `\"red_background\"`\n- `\"yellow_background\"`",
    "2-0": "`children`",
    "2-1": "`array` of [block objects](ref:block)",
    "2-2": "The nested child blocks, if any, of the Toggle block."
  },
  "cols": 3,
  "rows": 3,
  "align": [
    "left",
    "left",
    "left"
  ]
}
[/block]


```json Toggle Block
{
  //...other keys excluded
  "type": "toggle",
  "toggle": {
    "rich_text": [{
      "type": "text",
      "text": {
        "content": "Additional project details",
        "link": null
      }
      //...other keys excluded
    }],
    "color": "default",
    "children":[{
      "type": "paragraph"
      // ..other keys excluded
    }]
  }
}
```

## Video

Video block objects contain a [file object](https://developers.notion.com/reference/file-object) detailing information about the video.

```json Example Video block object
{
  "type": "video",
  //...other keys excluded
  "video": {
    "type": "external",
    "external": {
      "url": "https://companywebsite.com/files/video.mp4"
    }
  }
}
```

### Supported video types

- `.amv`
- `.asf`
- `.avi`
- `.f4v`
- `.flv`
- `.gifv`
- `.mkv`
- `.mov`
- `.mpg`
- `.mpeg`
- `.mpv`
- `.mp4`
- `.m4v`
- `.qt`
- `.wmv`
- YouTube video links that include `embed` or `watch`.
  E.g. `https://www.youtube.com/watch?v=[id]`, `https://www.youtube.com/embed/[id]`

> 📘
>
> Vimeo video links are not currently supported by the video block type. However, they can be embedded in Notion pages using the `embed` block type. See [Embed](https://developers.notion.com/reference/block#embed) for more information.

### Supported file upload types

See the [file upload reference](ref:file-upload#file-types-and-sizes) for a list of supported file extensions and content types when attaching a File Upload to a block.

Video blocks only support file types in the "video" section of the table.

# Rich text

Notion uses rich text to allow users to customize their content. Rich text refers to a type of document where content can be styled and formatted in a variety of customizable ways. This includes styling decisions, such as the use of italics, font size, and font color, as well as formatting, such as the use of hyperlinks or code blocks.

Notion includes rich text objects in [block objects](https://developers.notion.com/reference/block) to indicate how blocks in a page are represented. [Blocks](https://developers.notion.com/reference/block) that support rich text will include a rich text object; however, not all block types offer rich text.

When blocks are retrieved from a page using the [Retrieve a block](https://developers.notion.com/reference/retrieve-a-block) or [Retrieve block children](https://developers.notion.com/reference/get-block-children) endpoints, an array of rich text objects will be included in the block object (when available). Developers can use this array to retrieve the plain text (`plain_text`) for the block or get all the rich text styling and formatting options applied to the block.

```json An example rich text object
{
  "type": "text",
  "text": {
    "content": "Some words ",
    "link": null
  },
  "annotations": {
    "bold": false,
    "italic": false,
    "strikethrough": false,
    "underline": false,
    "code": false,
    "color": "default"
  },
  "plain_text": "Some words ",
  "href": null
}
```

> 📘
>
> Many [block types](https://developers.notion.com/reference/block#block-type-objects) support rich text. In cases where it is supported, a `rich_text` object will be included in the block `type` object. All `rich_text` objects will include a `plain_text` property, which provides a convenient way for developers to access unformatted text from the Notion block.

Each rich text object contains the following fields.

[block:parameters]
{
  "data": {
    "h-0": "Field",
    "h-1": "Type",
    "h-2": "Description",
    "h-3": "Example value",
    "0-0": "`type`",
    "0-1": "`string` (enum)",
    "0-2": "The type of this rich text object. Possible type values are: `\"text\"`, `\"mention\"`, `\"equation\"`.",
    "0-3": "`\"text\"`",
    "1-0": "`text` \\| `mention` \\| `equation`",
    "1-1": "`object`",
    "1-2": "An object containing type-specific configuration.  \n  \nRefer to the rich text type objects section below for details on type-specific values.",
    "1-3": "Refer to the rich text type objects section below for examples.",
    "2-0": "`annotations`",
    "2-1": "`object`",
    "2-2": "The information used to style the rich text object. Refer to the annotation object section below for details.",
    "2-3": "Refer to the annotation object section below for examples.",
    "3-0": "`plain_text`",
    "3-1": "`string`",
    "3-2": "The plain text without annotations.",
    "3-3": "`\"Some words \"`",
    "4-0": "`href`",
    "4-1": "`string` (optional)",
    "4-2": "The URL of any link or Notion mention in this text, if any.",
    "4-3": "`\"https://www.notion.so/Avocado-d093f1d200464ce78b36e58a3f0d8043\"`"
  },
  "cols": 4,
  "rows": 5,
  "align": [
    "left",
    "left",
    "left",
    "left"
  ]
}
[/block]

## The annotation object

All rich text objects contain an `annotations` object that sets the styling for the rich text. `annotations` includes the following fields:

[block:parameters]
{
  "data": {
    "h-0": "Property",
    "h-1": "Type",
    "h-2": "Description",
    "h-3": "Example value",
    "0-0": "`bold`",
    "0-1": "`boolean`",
    "0-2": "Whether the text is **bolded**.",
    "0-3": "`true`",
    "1-0": "`italic`",
    "1-1": "`boolean`",
    "1-2": "Whether the text is _italicized_.",
    "1-3": "`true`",
    "2-0": "`strikethrough`",
    "2-1": "`boolean`",
    "2-2": "Whether the text is struck through.",
    "2-3": "`false`",
    "3-0": "`underline`",
    "3-1": "`boolean`",
    "3-2": "Whether the text is underlined.",
    "3-3": "`false`",
    "4-0": "`code`",
    "4-1": "`boolean`",
    "4-2": "Whether the text is `code style`.",
    "4-3": "`true`",
    "5-0": "`color`",
    "5-1": "`string` (enum)",
    "5-2": "Color of the text. Possible values include:  \n  \n- `\"blue\"`  \n- `\"blue_background\"`  \n- `\"brown\"`  \n- `\"brown_background\"`  \n- `\"default\"`  \n- `\"gray\"`  \n- `\"gray_background\"`  \n- `\"green\"`  \n- `\"green_background\"`  \n- `\"orange\"`  \n-`\"orange_background\"`  \n- `\"pink\"`  \n- `\"pink_background\"`  \n- `\"purple\"`  \n- `\"purple_background\"`  \n- `\"red\"`  \n- `\"red_background”`  \n- `\"yellow\"`  \n- `\"yellow_background\"`",
    "5-3": "`\"green\"`"
  },
  "cols": 4,
  "rows": 6,
  "align": [
    "left",
    "left",
    "left",
    "left"
  ]
}
[/block]

## Rich text type objects

### Equation

Notion supports inline LaTeX equations as rich text object’s with a type value of `"equation"`. The corresponding equation type object contains the following:

| Field        | Type     | Description                                        | Example value                                  |
| :----------- | :------- | :------------------------------------------------- | :--------------------------------------------- |
| `expression` | `string` | The LaTeX string representing the inline equation. | `"\frac{{ - b \pm \sqrt {b^2 - 4ac} }}{{2a}}"` |

#### Example rich text `equation` object

```json
{
  "type": "equation",
  "equation": {
    "expression": "E = mc^2"
  },
  "annotations": {
    "bold": false,
    "italic": false,
    "strikethrough": false,
    "underline": false,
    "code": false,
    "color": "default"
  },
  "plain_text": "E = mc^2",
  "href": null
}
```

### Mention

Mention objects represent an inline mention of a database, date, link preview mention, page, template mention, or user. A mention is created in the Notion UI when a user types `@` followed by the name of the reference.

If a rich text object’s `type` value is `"mention"`, then the corresponding `mention` object contains the following:

[block:parameters]
{
  "data": {
    "h-0": "Field",
    "h-1": "Type",
    "h-2": "Description",
    "h-3": "Example value",
    "0-0": "`type`",
    "0-1": "`string` (enum)",
    "0-2": "The type of the inline mention. Possible values include:  \n  \n- `\"database\"`  \n- `\"date\"`  \n- `\"link_preview\"`  \n- `\"page\"`  \n- `\"template_mention\"`  \n- `\"user\"`",
    "0-3": "`\"user\"`",
    "1-0": "`database` \\| `date` \\| `link_preview` \\| `page` \\| `template_mention` \\| `user`",
    "1-1": "`object`",
    "1-2": "An object containing type-specific configuration. Refer to the mention type object sections below for details.",
    "1-3": "Refer to the mention type object sections below for example values."
  },
  "cols": 4,
  "rows": 2,
  "align": [
    "left",
    "left",
    "left",
    "left"
  ]
}
[/block]

#### Database mention type object

Database mentions contain a database reference within the corresponding `database` field. A database reference is an object with an `id` key and a string value (UUIDv4) corresponding to a database ID.

If an integration doesn’t have [access](https://developers.notion.com/reference/capabilities) to the mentioned database, then the mention is returned with just the ID. The `plain_text` value that would be a title appears as `"Untitled"` and the annotation object’s values are defaults.

_Example rich text `mention` object for a `database` mention_

```json
{
  "type": "mention",
  "mention": {
    "type": "database",
    "database": {
      "id": "a1d8501e-1ac1-43e9-a6bd-ea9fe6c8822b"
    }
  },
  "annotations": {
    "bold": false,
    "italic": false,
    "strikethrough": false,
    "underline": false,
    "code": false,
    "color": "default"
  },
  "plain_text": "Database with test things",
  "href": "https://www.notion.so/a1d8501e1ac143e9a6bdea9fe6c8822b"
}
```

#### Date mention type object

Date mentions contain a [date property value object](https://developers.notion.com/reference/property-value-object#date-property-values) within the corresponding `date` field.

_Example rich text `mention` object for a `date` mention_

```json
{
  "type": "mention",
  "mention": {
    "type": "date",
    "date": {
      "start": "2022-12-16",
      "end": null
    }
  },
  "annotations": {
    "bold": false,
    "italic": false,
    "strikethrough": false,
    "underline": false,
    "code": false,
    "color": "default"
  },
  "plain_text": "2022-12-16",
  "href": null
}
```

#### Link Preview mention type object

If a user opts to share a [Link Preview](https://developers.notion.com/docs/link-previews) as a mention, then the API handles the Link Preview mention as a rich text object with a `type` value of `link_preview`. Link preview rich text mentions contain a corresponding `link_preview` object that includes the `url` that is used to create the Link Preview mention.

_Example rich text `mention` object for a `link_preview` mention_

```json
{
  "type": "mention",
  "mention": {
    "type": "link_preview",
    "link_preview": {
      "url": "https://workspace.slack.com/archives/C04PF0F9QSD/z1671139297838409?thread_ts=1671139274.065079&cid=C03PF0F9QSD"
    }
  },
  "annotations": {
    "bold": false,
    "italic": false,
    "strikethrough": false,
    "underline": false,
    "code": false,
    "color": "default"
  },
  "plain_text": "https://workspace.slack.com/archives/C04PF0F9QSD/z1671139297838409?thread_ts=1671139274.065079&cid=C03PF0F9QSD",
  "href": "https://workspace.slack.com/archives/C04PF0F9QSD/z1671139297838409?thread_ts=1671139274.065079&cid=C03PF0F9QSD"
}
```

#### Page mention type object

Page mentions contain a page reference within the corresponding `page` field. A page reference is an object with an `id` property and a string value (UUIDv4) corresponding to a page ID.

If an integration doesn’t have [access](https://developers.notion.com/reference/capabilities) to the mentioned page, then the mention is returned with just the ID. The `plain_text` value that would be a title appears as `"Untitled"` and the annotation object’s values are defaults.

_Example rich text `mention` object for a `page` mention_

```json
{
  "type": "mention",
  "mention": {
    "type": "page",
    "page": {
      "id": "3c612f56-fdd0-4a30-a4d6-bda7d7426309"
    }
  },
  "annotations": {
    "bold": false,
    "italic": false,
    "strikethrough": false,
    "underline": false,
    "code": false,
    "color": "default"
  },
  "plain_text": "This is a test page",
  "href": "https://www.notion.so/3c612f56fdd04a30a4d6bda7d7426309"
}
```

#### Template mention type object

The content inside a [template button](https://www.notion.so/help/template-buttons) in the Notion UI can include placeholder date and user mentions that populate when a template is duplicated. Template mention type objects contain these populated values.

Template mention rich text objects contain a `template_mention` object with a nested `type` key that is either `"template_mention_date"` or `"template_mention_user"`.

If the `type` key is `"template_mention_date"`, then the rich text object contains the following `template_mention_date` field:

| Field                   | Type            | Description                                                                   | Example value |
| :---------------------- | :-------------- | :---------------------------------------------------------------------------- | :------------ |
| `template_mention_date` | `string` (enum) | The type of the date mention. Possible values include: `"today"` and `"now"`. | `"today"`     |

_Example rich text `mention` object for a `template_mention_date` mention _

```json
{
  "type": "mention",
  "mention": {
    "type": "template_mention",
    "template_mention": {
      "type": "template_mention_date",
      "template_mention_date": "today"
    }
  },
  "annotations": {
    "bold": false,
    "italic": false,
    "strikethrough": false,
    "underline": false,
    "code": false,
    "color": "default"
  },
  "plain_text": "@Today",
  "href": null
}
```

If the type key is `"template_mention_user"`, then the rich text object contains the following `template_mention_user` field:

| Field                   | Type            | Description                                                      | Example value |
| :---------------------- | :-------------- | :--------------------------------------------------------------- | :------------ |
| `template_mention_user` | `string` (enum) | The type of the user mention. The only possible value is `"me"`. | `"me"`        |

_Example rich text `mention` object for a `template_mention_user` mention _

```json
{
  "type": "mention",
  "mention": {
    "type": "template_mention",
    "template_mention": {
      "type": "template_mention_user",
      "template_mention_user": "me"
    }
  },
  "annotations": {
    "bold": false,
    "italic": false,
    "strikethrough": false,
    "underline": false,
    "code": false,
    "color": "default"
  },
  "plain_text": "@Me",
  "href": null
}
```

#### User mention type object

If a rich text object’s `type` value is `"user"`, then the corresponding user field contains a [user object](https://developers.notion.com/reference/user).

> 📘
>
> If your integration doesn’t yet have access to the mentioned user, then the `plain_text` that would include a user’s name reads as `"@Anonymous"`. To update the integration to get access to the user, update the integration capabilities on the integration settings page.

_Example rich text `mention` object for a `user` mention_

```json
{
  "type": "mention",
  "mention": {
    "type": "user",
    "user": {
      "object": "user",
      "id": "b2e19928-b427-4aad-9a9d-fde65479b1d9"
    }
  },
  "annotations": {
    "bold": false,
    "italic": false,
    "strikethrough": false,
    "underline": false,
    "code": false,
    "color": "default"
  },
  "plain_text": "@Anonymous",
  "href": null
}
```

### Text

If a rich text object’s `type` value is `"text"`, then the corresponding `text` field contains an object including the following:

[block:parameters]
{
  "data": {
    "h-0": "Field",
    "h-1": "Type",
    "h-2": "Description",
    "h-3": "Example value",
    "0-0": "`content`",
    "0-1": "`string`",
    "0-2": "The actual text content of the text.",
    "0-3": "`\"Some words \"`",
    "1-0": "`link`",
    "1-1": "`object` (optional)",
    "1-2": "An object with information about any inline link in this text, if included.  \n  \nIf the text contains an inline link, then the object key is `url` and the value is the URL’s string web address.  \n  \nIf the text doesn’t have any inline links, then the value is `null`.",
    "1-3": "`{\n  \"url\": \"https://developers.notion.com/\"\n}`"
  },
  "cols": 4,
  "rows": 2,
  "align": [
    "left",
    "left",
    "left",
    "left"
  ]
}
[/block]

#### Example rich text `text` object without link

```json
{
  "type": "text",
  "text": {
    "content": "This is an ",
    "link": null
  },
  "annotations": {
    "bold": false,
    "italic": false,
    "strikethrough": false,
    "underline": false,
    "code": false,
    "color": "default"
  },
  "plain_text": "This is an ",
  "href": null
}
```

#### Example rich `text` text object with link

```json
{
  "type": "text",
  "text": {
    "content": "inline link",
    "link": {
      "url": "https://developers.notion.com/"
    }
  },
  "annotations": {
    "bold": false,
    "italic": false,
    "strikethrough": false,
    "underline": false,
    "code": false,
    "color": "default"
  },
  "plain_text": "inline link",
  "href": "https://developers.notion.com/"
}
```

> 📘 Rich text object limits
>
> Refer to the request limits documentation page for information about [limits on the size of rich text objects](https://developers.notion.com/reference/request-limits#limits-for-property-values).
>


# Page

The Page object contains the [page property values](https://developers.notion.com/reference/page-property-values) of a single Notion page.

```json Example page object
{
    "object": "page",
    "id": "be633bf1-dfa0-436d-b259-571129a590e5",
    "created_time": "2022-10-24T22:54:00.000Z",
    "last_edited_time": "2023-03-08T18:25:00.000Z",
    "created_by": {
        "object": "user",
        "id": "c2f20311-9e54-4d11-8c79-7398424ae41e"
    },
    "last_edited_by": {
        "object": "user",
        "id": "9188c6a5-7381-452f-b3dc-d4865aa89bdf"
    },
    "cover": null,
    "icon": {
        "type": "emoji",
        "emoji": "🐞"
    },
    "parent": {
        "type": "data_source_id",
        "data_source_id": "a1d8501e-1ac1-43e9-a6bd-ea9fe6c8822b"
    },
    "archived": true,
    "in_trash": true,
    "properties": {
        "Due date": {
            "id": "M%3BBw",
            "type": "date",
            "date": {
                "start": "2023-02-23",
                "end": null,
                "time_zone": null
            }
        },
        "Status": {
            "id": "Z%3ClH",
            "type": "status",
            "status": {
                "id": "86ddb6ec-0627-47f8-800d-b65afd28be13",
                "name": "Not started",
                "color": "default"
            }
        },
        "Title": {
            "id": "title",
            "type": "title",
            "title": [
                {
                    "type": "text",
                    "text": {
                        "content": "Bug bash",
                        "link": null
                    },
                    "annotations": {
                        "bold": false,
                        "italic": false,
                        "strikethrough": false,
                        "underline": false,
                        "code": false,
                        "color": "default"
                    },
                    "plain_text": "Bug bash",
                    "href": null
                }
            ]
        }
    },
    "url": "https://www.notion.so/Bug-bash-be633bf1dfa0436db259571129a590e5",
		"public_url": "https://jm-testing.notion.site/p1-6df2c07bfc6b4c46815ad205d132e22d"
}
```

All pages have a [Parent](ref:parent-object). If the parent is a [data source](ref:data-source), the property values conform to the schema laid out in the data source's [properties](ref:property-object). Otherwise, the only property value is the `title`.

Page content is available as [blocks](ref:block). The content can be read using [retrieve block children](ref:get-block-children) and appended using [append block children](ref:patch-block-children).

## Page object properties

> 📘
>
> Properties marked with an \* are available to integrations with any capabilities. Other properties require read content capabilities in order to be returned from the Notion API. For more information on integration capabilities, see the [capabilities guide](ref:capabilities).

[block:parameters]
{
  "data": {
    "h-0": "Property",
    "h-1": "Type",
    "h-2": "Description",
    "h-3": "Example value",
    "0-0": "`object`\\*",
    "0-1": "`string`",
    "0-2": "Always `\"page\"`.",
    "0-3": "`\"page\"`",
    "1-0": "`id`\\*",
    "1-1": "`string` (UUIDv4)",
    "1-2": "Unique identifier of the page.",
    "1-3": "`\"45ee8d13-687b-47ce-a5ca-6e2e45548c4b\"`",
    "2-0": "`created_time`",
    "2-1": "`string` ([ISO 8601 date and time](https://en.wikipedia.org/wiki/ISO_8601))",
    "2-2": "Date and time when this page was created. Formatted as an [ISO 8601 date time](https://en.wikipedia.org/wiki/ISO_8601) string.",
    "2-3": "`\"2020-03-17T19:10:04.968Z\"`",
    "3-0": "`created_by`",
    "3-1": "[Partial User](ref:user)",
    "3-2": "User who created the page.",
    "3-3": "`{\"object\": \"user\",\"id\": \"45ee8d13-687b-47ce-a5ca-6e2e45548c4b\"}`",
    "4-0": "`last_edited_time`",
    "4-1": "`string` ([ISO 8601 date and time](https://en.wikipedia.org/wiki/ISO_8601))",
    "4-2": "Date and time when this page was updated. Formatted as an [ISO 8601 date time](https://en.wikipedia.org/wiki/ISO_8601) string.",
    "4-3": "`\"2020-03-17T19:10:04.968Z\"`",
    "5-0": "`last_edited_by`",
    "5-1": "[Partial User](ref:user)",
    "5-2": "User who last edited the page.",
    "5-3": "`{\"object\": \"user\",\"id\": \"45ee8d13-687b-47ce-a5ca-6e2e45548c4b\"}`",
    "6-0": "`archived`",
    "6-1": "`boolean`",
    "6-2": "The archived status of the page.",
    "6-3": "`false`",
    "7-0": "`in_trash`",
    "7-1": "`boolean`",
    "7-2": "Whether the page is in Trash. ",
    "7-3": "`false`",
    "8-0": "`icon`",
    "8-1": "[File Object](ref:file-object) (`type` of `\"external\"` or `\"file_upload\"` are supported) or [Emoji object](ref:emoji-object)",
    "8-2": "Page icon.",
    "8-3": "",
    "9-0": "`cover`",
    "9-1": "[File object](ref:file-object) (`type` of `\"external\"` or `\"file_upload\"` are supported)",
    "9-2": "Page cover image.",
    "9-3": "",
    "10-0": "`properties`",
    "10-1": "`object`",
    "10-2": "Property values of this page. As of version `2022-06-28`, `properties` only contains the ID of the property; in prior versions `properties` contained the values as well.  \n  \nIf `parent.type` is `\"page_id\"` or `\"workspace\"`, then the only valid key is `title`.  \n  \nIf `parent.type` is `\"data_source_id\"`, then the keys and values of this field are determined by the [`properties`](https://developers.notion.com/reference/property-object)  of the [data source](ref:data-source) this page belongs to.  \n  \n`key` string  \nName of a property as it appears in Notion.  \n  \n`value` object  \nSee [Property value object](https://developers.notion.com/reference/property-value-object).",
    "10-3": "`{ \"id\": \"A%40Hk\" }`",
    "11-0": "`parent`",
    "11-1": "`object`",
    "11-2": "Information about the page's parent. See [Parent object](ref:parent-object).",
    "11-3": "`{ \"type\": \"data_source_id\", \"data_source_id\": \"d9824bdc-8445-4327-be8b-5b47500af6ce\" }`",
    "12-0": "`url`",
    "12-1": "`string`",
    "12-2": "The URL of the Notion page.",
    "12-3": "`\"https://www.notion.so/Avocado-d093f1d200464ce78b36e58a3f0d8043\"`",
    "13-0": "`public_url`",
    "13-1": "`string`",
    "13-2": "The public page URL if the page has been published to the web. Otherwise, `null`.",
    "13-3": "`\"https://jm-testing.notion.site/p1-6df2c07bfc6b4c46815ad205d132e22d\"1`"
  },
  "cols": 4,
  "rows": 14,
  "align": [
    "left",
    "left",
    "left",
    "left"
  ]
}
[/block]

# Page properties

## Overview

A [page object](https://developers.notion.com/reference/page) is made up of page properties that contain data about the page.

When you send a request to [Create a page](https://developers.notion.com/reference/post-page), set the page properties in the `properties` object body parameter.

[Retrieve a page](https://developers.notion.com/reference/retrieve-a-page) surfaces the identifier, type, and value of a page’s properties.

[Retrieve a page property item](https://developers.notion.com/reference/retrieve-a-page-property)  returns information about a single property ID. Especially for formulas, rollups, and relations, Notion recommends using this API to ensure you get an accurate, up-to-date property value that isn't truncating any results. Refer to [Page property items](ref:property-item-object) for specific API shape details when using this endpoint.

An [Update page](https://developers.notion.com/reference/patch-page) query modifies the page property values specified in the `properties` object body param.

> 👍 Pages that live in a data source are easier to query and manage
>
> **Page properties** are most useful when interacting with a page that is an entry in a data source, represented as a row in the Notion app UI.
>
> If a page is not part of a data source, then its only available property is its `title`.

## Attributes

Each page property value object contains the following fields:

[block:parameters]
{
  "data": {
    "h-0": "Field",
    "h-1": "Type",
    "h-2": "Description",
    "h-3": "Example value",
    "0-0": "`id`",
    "0-1": "`string`",
    "0-2": "An underlying identifier for the property. Historically, this may be a UUID, but newer IDs are a short ID that's always URL-encoded in the API and in [integration webhooks](ref:webhooks).  \n  \n`id` may be used in place of name when creating or updating pages.  \n  \n`id` remains constant when the property name changes.",
    "0-3": "`\"f%5C%5C%3Ap\"`",
    "1-0": "`type`",
    "1-1": "`string` (enum)",
    "1-2": "The type of the property in the page object. Possible type values are:  \n  \n- [`checkbox`](#checkbox)\n- [`created_by`](#created-by)\n- [`created_time`](#created-time)\n- [`date`](#date)\n- [`email`](#email)\n- [`files`](#files)\n- [`formula`](#formula)\n- [`last_edited_by`](#last-edited-by)\n- [`last_edited_time`](#last-edited-time)\n- [`multi_select`](#multi-select)\n- [`number`](#number)\n- [`people`](#people)\n- [`phone_number`](#phone-number)\n- [`relation`](#relation)\n- [`rollup`](#rollup)\n- [`rich_text`](#rich-text)\n- [`select`](#select)\n- [`status`](#status)\n- [`title`](#title)\n- [`url`](#url)\n- [`unique_id`](#unique-id)\n- [`verification`](#verification)Refer to specific type sections below for details on type-specific values.",
    "1-3": "`\"rich_text\"`",
    "2-0": "[`checkbox`](#checkbox)  \n[`created_by`](#created-by)  \n[`created_time`](#created-time)  \n[`date`](#date)  \n[`email`](#email)  \n[`files`](#files)  \n[`formula`](#formula)  \n[`last_edited_by`](#last-edited-by)  \n[`last_edited_time`](#last-edited-time)  \n[`multi_select`](#multi-select)  \n[`number`](#number)  \n[`people`](#people)  \n[`phone_number`](#phone-number)  \n[`relation`](#relation)  \n[`rollup`](#rollup)  \n[`rich_text`](#rich-text)  \n[`select`](#select)  \n[`status`](#status)  \n[`title`](#title)  \n[`url`](#url)  \n[`unique_id`](#unique-id)  \n[`verification`](#verification)",
    "2-1": "`object`",
    "2-2": "A type object that contains data specific to the page property type, including the page property value.  \n  \nRefer to the [type objects section](#type-objects) for descriptions and examples of each type.",
    "2-3": "`\"checkbox\": true`"
  },
  "cols": 4,
  "rows": 3,
  "align": [
    "left",
    "left",
    "left",
    "left"
  ]
}
[/block]


> 📘 Size limits for page property values
>
> For information about size limitations for specific page property objects, refer to the [limits for property values documentation](https://developers.notion.com/reference/request-limits#limits-for-property-values).

When returned from the [Retrieve page property item](changelog:retrieve-page-property-values) API, there's an additional field, `object`, which is always the string `"property_item"`, as described in [Page property items](ref:property-item-object).

## Type objects

### Checkbox

| Field      | Type      | Description                                                      | Example value |
| :--------- | :-------- | :--------------------------------------------------------------- | :------------ |
| `checkbox` | `boolean` | Whether the checkbox is checked (`true`) or unchecked (`false`). | `true`        |

#### Example `properties` body param for a POST or PATCH page request that creates or updates a `checkbox` page property value

```json
{
  "properties": {
    "Task completed": {
      "checkbox": true
    }
  }
}
```

#### Example `checkbox` page property value as returned in a GET page request

```json
{
  "Task completed": {
    "id": "ZI%40W",
    "type": "checkbox",
    "checkbox": true
  }
}
```

### Created by

[block:parameters]
{
  "data": {
    "h-0": "Field",
    "h-1": "Type",
    "h-2": "Description",
    "h-3": "Example value",
    "0-0": "`created_by`",
    "0-1": "`object`",
    "0-2": "A [user object](https://developers.notion.com/reference/user) containing information about the user who created the page.  \n  \n`created_by` can’t be updated.",
    "0-3": "Refer to the example response objects below."
  },
  "cols": 4,
  "rows": 1,
  "align": [
    "left",
    "left",
    "left",
    "left"
  ]
}
[/block]


#### Example `created_by` page property value as returned in a GET page request

```json
{
  "created_by": {
    "object": "user",
    "id": "c2f20311-9e54-4d11-8c79-7398424ae41e"
  }
}
```

### Created time

[block:parameters]
{
  "data": {
    "h-0": "Field",
    "h-1": "Type",
    "h-2": "Description",
    "h-3": "Example value",
    "0-0": "`created_time`",
    "0-1": "`string` ([ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) date and time)",
    "0-2": "The date and time that the page was created.  \n  \nThe `created_time` value can’t be updated.",
    "0-3": "`\"2022-10-12T16:34:00.000Z\"`"
  },
  "cols": 4,
  "rows": 1,
  "align": [
    "left",
    "left",
    "left",
    "left"
  ]
}
[/block]


#### Example `created_time` page property value as returned in a GET page request

```json
{
  "Created time": {
    "id": "eB_%7D",
    "type": "created_time",
    "created_time": "2022-10-24T22:54:00.000Z"
  }
}
```

### Date

If the `type` of a page property value is `"date"`, then the property value contains a `"date"` object with the following fields:

[block:parameters]
{
  "data": {
    "h-0": "Field",
    "h-1": "Type",
    "h-2": "Description",
    "h-3": "Example value",
    "0-0": "`end`",
    "0-1": "`string` ([ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) date and time)",
    "0-2": "(Optional) A string representing the end of a date range.  \n  \nIf the value is `null`, then the date value is not a range.",
    "0-3": "`\"2020-12-08T12:00:00Z\"`",
    "1-0": "`start`",
    "1-1": "`string` ([ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) date and time)",
    "1-2": "A date, with an optional time.  \n  \nIf the `date` value is a range, then `start` represents the start of the range.",
    "1-3": "`\"2020-12-08T12:00:00Z”`"
  },
  "cols": 4,
  "rows": 2,
  "align": [
    "left",
    "left",
    "left",
    "left"
  ]
}
[/block]


#### Example `properties` body param for a POST or PATCH page request that creates or updates a date page property value

```json
{
  "properties": {
    "Due date": {
      "date": {
        "start": "2023-02-23"
      }
    }
  }
}
```

#### Example `date` page property value as returned in a GET page request

```json
{
  "Due date": {
    "id": "M%3BBw",
    "type": "date",
    "date": {
      "start": "2023-02-07",
      "end": null,
      "time_zone": null
    }
  }
}
```

### Email

| Field   | Type     | Description                           | Example value          |
| :------ | :------- | :------------------------------------ | :--------------------- |
| `email` | `string` | A string describing an email address. | `"ada@makenotion.com"` |

#### Example `properties` body param for a POST or PATCH page request that creates or updates an `email` page property value

```json
{
  "properties": {
    "Email": {
      "email": "ada@makenotion.com"
    }
  }
}
```

#### Example `email` page property value as returned in a GET page request

```json
{
  "Email": {
    "id": "y%5C%5E_",
    "type": "email",
    "email": "ada@makenotion.com"
  }
}
```

### Files

| Field   | Type                                                                         | Description                                                 | Example value                                |
| :------ | :--------------------------------------------------------------------------- | :---------------------------------------------------------- | :------------------------------------------- |
| `files` | array of [file objects](https://developers.notion.com/reference/file-object) | An array of objects containing information about the files. | Refer to the example response objects below. |

#### Example creation or update of `files` property

The following is an example `properties` body parameter for a `POST` or `PATCH` page request that creates or updates a `files` page property value.

When providing an `external` URL, the `name` parameter is required.

When providing a `file_upload`, the `name` is optional and defaults to the `filename` of the original [File Upload](ref:file-upload).

```json
{
  "properties": {
    "Blueprint": {
      "files": [
        {
          "name": "Project Alpha blueprint",
          "external": {
            "url": "https://www.figma.com/file/g7eazMtXnqON4i280CcMhk/project-alpha-blueprint?node-id=0%3A1&t=nXseWIETQIgv31YH-1"
          }
        }
      ]
    }
  }
}
```

#### Example `files` page property value as returned in a GET page request

```json
{
  "Blueprint": {
    "id": "tJPS",
    "type": "files",
    "files": [
      {
        "name": "Project blueprint",
        "type": "external",
        "external": {
          "url": "https://www.figma.com/file/g7eazMtXnqON4i280CcMhk/project-alpha-blueprint?node-id=0%3A1&t=nXseWIETQIgv31YH-1"
        }
      }
    ]
  }
}
```

> 📘 Array parameter overwrites the entire existing value
>
> When updating a `files` page property value, the value is overwritten by the new array of `files` passed.
>
> If you pass a `file` object containing a file hosted by Notion, it remains one of the files. To remove any file, don't pass it in the update request.

### Formula

Formula property value objects represent the result of evaluating a formula described in the
[data source's properties](<ref:data source>).

If the `type` of a page property value is `"formula"`, then the property value contains a `"formula"` object with the following fields:

[block:parameters]
{
  "data": {
    "h-0": "Field",
    "h-1": "Type",
    "h-2": "Description",
    "h-3": "Example value",
    "0-0": "`boolean` \\|\\| `date` \\|\\| `number` \\|\\| `string`",
    "0-1": "`boolean` \\|\\| `date` \\|\\| `number` \\|\\| `string`",
    "0-2": "The value of the result of the formula.  \n  \nThe value can’t be updated directly via the API.",
    "0-3": "42",
    "1-0": "`type`",
    "1-1": "`string` (enum)",
    "1-2": "A string indicating the data type of the result of the formula. Possible `type` values are:  \n  \n- `boolean`\n- `date`\n- `number`\n- `string`",
    "1-3": "`\"number\"`"
  },
  "cols": 4,
  "rows": 2,
  "align": [
    "left",
    "left",
    "left",
    "left"
  ]
}
[/block]


#### Example `formula` page property value as returned in a GET page request

```json
{
  "Days until launch": {
    "id": "CSoE",
    "type": "formula",
    "formula": {
      "type": "number",
      "number": 56
    }
  }
}
```

> 📘
>
> The [Retrieve a page endpoint](https://developers.notion.com/reference/retrieve-a-page) returns a maximum of 25 inline page or person references for a `formula` property. If a `formula` property includes more than 25 references, then you can use the [Retrieve a page property item endpoint](https://developers.notion.com/reference/retrieve-a-page-property) for the specific `formula` property to get its complete list of references.

### Icon

> 📘 Page icon and cover are not nested under `properties`
>
> The `icon` and `cover` parameters and fields in the [Create a page](ref:post-page) and [Update page properties](ref:patch-page) APIs are top-level are not nested under `properties`.

| Field  | Type      | Description | Example value                                |
| :----- | :-------- | :---------- | :------------------------------------------- |
| `icon` | an object | Icon object | Refer to the example response objects below. |

#### Example emoji `icon` property value as returned in GET page request

```json
{
  "icon": {
    "type": "emoji",
    "emoji":"😀"
  }
}
```

#### Example uploaded `icon` page property value as returned in a GET page request

```json
{
  "icon": {
    "type":"file",
    "file": {
      "url": "https://local-files-secure.s3.us-west-2.amazonaws.com/13950b26-c203-4f3b-b97d-93ec06319565/a7084c4c-3e9a-4324-af99-34e0cb7f8fe7/notion.jpg?...",
      "expiry_time": "2024-12-03T19:44:56.932Z"
    }
  }
}
```

#### Example updating a page icon to an uploaded file

After uploading an image using the [File Upload API](file-upload#file-types-and-sizes), use the File Upload's ID in the [Create a page](ref:post-page) or [Update page properties](ref:patch-page) API to attach it as a page icon. For example:

```json
{
  "icon": {
    "type": "file_upload",
    "file_upload": {
      "id": "43833259-72ae-404e-8441-b6577f3159b4"
    }
  }
}
```

To attach a file upload as a page cover rather than an icon, use the create or update page APIs with the `cover` parameter, nesting a `file_upload` parameter the same way as the `icon` example.

### Last edited by

[block:parameters]
{
  "data": {
    "h-0": "Field",
    "h-1": "Type",
    "h-2": "Description",
    "h-3": "Example value",
    "0-0": "`last_edited_by`",
    "0-1": "`object`",
    "0-2": "A [user object](https://developers.notion.com/reference/user) containing information about the user who last updated the page.  \n  \n`last_edited_by` can’t be updated.",
    "0-3": "Refer to the example response objects below."
  },
  "cols": 4,
  "rows": 1,
  "align": [
    "left",
    "left",
    "left",
    "left"
  ]
}
[/block]


#### Example `last_edited_by` page property value as returned in a GET page request

```json
{
  "Last edited by column name": {
    "id": "uGNN",
    "type": "last_edited_by",
    "last_edited_by": {
      "object": "user",
      "id": "9188c6a5-7381-452f-b3dc-d4865aa89bdf",
      "name": "Test Integration",
      "avatar_url": "https://s3-us-west-2.amazonaws.com/public.notion-static.com/3db373fe-18f6-4a3c-a536-0f061cb9627f/leplane.jpeg",
      "type": "bot",
      "bot": {}
    }
  }
}
```

### Last edited time

[block:parameters]
{
  "data": {
    "h-0": "Field",
    "h-1": "Type",
    "h-2": "Description",
    "h-3": "Example value",
    "0-0": "`last_edited_time`",
    "0-1": "`string` ([ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) date and time)",
    "0-2": "The date and time that the page was last edited.  \n  \nThe `last_edited_time` value can’t be updated.",
    "0-3": "`\"2022-10-12T16:34:00.000Z\"`"
  },
  "cols": 4,
  "rows": 1,
  "align": [
    "left",
    "left",
    "left",
    "left"
  ]
}
[/block]


#### Example `last_edited_time` page property value as returned in a GET page request

```json
{
  "Last edited time": {
    "id": "%3Defk",
    "type": "last_edited_time",
    "last_edited_time": "2023-02-24T21:06:00.000Z"
  }
}
```

### Multi-select

If the `type` of a page property value is `"multi_select"`, then the property value contains a `"multi_select"` array with the following fields:

[block:parameters]
{
  "data": {
    "h-0": "Field",
    "h-1": "Type",
    "h-2": "Description",
    "h-3": "Example value",
    "0-0": "`color`",
    "0-1": "`string` (enum)",
    "0-2": "Color of the option. Possible `\"color\"` values are:   \n  \n- `blue`  \n  - `brown`\n- `default`\n- `gray`\n- `green`\n- `orange`\n- `pink\"`\n- `\"purple`\n- `red`\n- `yellow`Defaults to `default`. The `color` value can’t be updated via the API.",
    "0-3": "`\"red\"`",
    "1-0": "`id`",
    "1-1": "`string`",
    "1-2": "The ID of the option.  \n  \nYou can use `id` or `name` to update a multi-select property.",
    "1-3": "`\"b3d773ca-b2c9-47d8-ae98-3c2ce3b2bffb\"`",
    "2-0": "`name`",
    "2-1": "`string`",
    "2-2": "The name of the option as it appears in Notion.  \n  \nIf the multi-select [data source property](ref:property-object) does not yet have an option by that name, then the name will be added to the data source schema if the integration also has write access to the parent data source.  \n  \nNote: Commas (`\",\"`) are not valid for select values.",
    "2-3": "`\"JavaScript\"`"
  },
  "cols": 4,
  "rows": 3,
  "align": [
    "left",
    "left",
    "left",
    "left"
  ]
}
[/block]


#### Example `properties` body param for a POST or PATCH page request that creates or updates a `multi_select` page property value

```json
{
  "properties": {
    "Programming language": {
      "multi_select": [
        {
          "name": "TypeScript"
        },
        {
          "name": "Python"
        }
      ]
    }
  }
}
```

#### Example `multi_select` page property value as returned in a GET page request

```json
{
  "Programming language": {
    "id": "QyRn",
    "name": "Programming language",
    "type": "multi_select",
    "multi_select": [
      {
        "id": "tC;=",
        "name": "TypeScript",
        "color": "purple"
      },
      {
        "id": "e4413a91-9f84-4c4a-a13d-5b4b3ef870bb",
        "name": "JavaScript",
        "color": "red"
      },
      {
        "id": "fc44b090-2166-40c8-8c58-88f2d8085ec0",
        "name": "Python",
        "color": "gray"
      }
    ]
  }
}
```

> 📘
>
> If you want to add a new option to a multi-select property via the [Update page](https://developers.notion.com/reference/patch-page) or [Update data source](ref:update-a-data-source) endpoint, then your integration needs write access to the parent database.

### Number

| Field    | Type     | Description                       | Example value |
| :------- | :------- | :-------------------------------- | :------------ |
| `number` | `number` | A number representing some value. | `1234`        |

#### Example `properties` body param for a POST or PATCH page request that creates or updates a `number` page property value

```json
{
  "properties": {
    "Number of subscribers": {
      "number": 42
    }
  }
}
```

#### Example `number` page property value as returned in a GET page request

```json
{
  "Number of subscribers": {
    "id": "WPj%5E",
    "name": "Number of subscribers",
    "type": "number",
    "number": {
      "format": "number"
    }
  }
}
```

### People

| Field    | Type                                                                  | Description               | Example value                                |
| :------- | :-------------------------------------------------------------------- | :------------------------ | :------------------------------------------- |
| `people` | array of [user objects](https://developers.notion.com/reference/user) | An array of user objects. | Refer to the example response objects below. |

#### Example `properties` body param for a POST or PATCH page request that creates or updates a `people` page property value

```json
{
  "properties": {
    "Stakeholders": {
      "people": [{
        "object": "user",
        "id": "c2f20311-9e54-4d11-8c79-7398424ae41e"
      }]
    }
  }
}
```

#### Example `people` page property value as returned in a GET page request

```json
{
  "Stakeholders": {
    "id": "%7BLUX",
    "type": "people",
    "people": [
      {
        "object": "user",
        "id": "c2f20311-9e54-4d11-8c79-7398424ae41e",
        "name": "Kimberlee Johnson",
        "avatar_url": null,
        "type": "person",
        "person": {
          "email": "hello@kimberlee.dev"
        }
      }
    ]
  }
}
```

> 📘 Retrieve individual property items to avoid truncation
>
> The [Retrieve a page endpoint](https://developers.notion.com/reference/retrieve-a-page) can’t be guaranteed to return more than 25 people per `people` page property. If a `people` page property includes more than 25 people, then you can use the [Retrieve a page property item endpoint](https://developers.notion.com/reference/retrieve-a-page-property) for the specific `people` property to get a complete list of people.

### Phone number

| Field          | Type     | Description                                                               | Example value    |
| :------------- | :------- | :------------------------------------------------------------------------ | :--------------- |
| `phone_number` | `string` | A string representing a phone number. No phone number format is enforced. | `"415-867-5309"` |

#### Example `properties` body param for a POST or PATCH page request that creates or updates a `phone_number` page property value

```json
{
  "properties": {
    "Contact phone number": {
      "phone_number": "415-202-4776"
    }
  }
}
```

#### Example `phone_number` page property value as returned in a GET page request

```json
{
  "Example phone number property": {
    "id": "%5DKhQ",
    "name": "Example phone number property",
    "type": "phone_number",
    "phone_number": {}
  }
}
```

### Relation

| Field      | Type                        | Description                                                                                                                                                                                   | Example value                                |
| :--------- | :-------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------- |
| `has_more` | `boolean`                   | If a `relation` has more than 25 references, then the `has_more` value for the relation in the response object is `true`. If a relation doesn’t exceed the limit, then `has_more` is `false`. | Refer to the example response objects below. |
| `relation` | an array of page references | An array of related page references. A page reference is an object with an `id` key and a string value corresponding to a page ID in another data source.                                     | Refer to the example response objects below. |

#### Example `properties` body param for a POST or PATCH page request that creates or updates a `relation` page property value

```json
{
  "properties": {
    "Related tasks": {
      "relation": [
        {
          "id": "dd456007-6c66-4bba-957e-ea501dcda3a6"
        },
        {
          "id": "0c1f7cb2-8090-4f18-924e-d92965055e32"
        }
      ]
    }
  }
}
```

#### Example `relation` page property value as returned in a GET page request

```json
{
  "Related tasks": {
    "id": "hgMz",
    "type": "relation",
    "relation": [
      {
        "id": "dd456007-6c66-4bba-957e-ea501dcda3a6"
      },
      {
        "id": "0c1f7cb2-8090-4f18-924e-d92965055e32"
      }
    ],
    "has_more": false
  }
}
```

> 📘 To update a `relation` property value via the API, share the related parent database with the integration.
>
> If a `relation` property value is unexpectedly empty, then make sure that you have shared the original source database for the data source that the `relation` points to with the integration.
>
> Ensuring correct permissions is also important for complete results for `rollup` and `formula` properties.

### Rollup

If the `type` of a page property value is `"rollup"`, then the property value contains a `"rollup"` object with the following fields:

[block:parameters]
{
  "data": {
    "h-0": "Field",
    "h-1": "Type",
    "h-2": "Description",
    "h-3": "Example value",
    "0-0": "`array` \\|\\| `date` \\|\\| `incomplete` \\|\\| `number` \\|\\| `unsupported`",
    "0-1": "Corresponds to the field.  \n  \nFor example, if the field is `number`, then the type of the value is `number`.",
    "0-2": "The value of the calculated rollup.  \n  \nThe value can't be directly updated via the API.",
    "0-3": "`1234`",
    "1-0": "`function`",
    "1-1": "`string` (enum)",
    "1-2": "The function that is evaluated for every page in the relation of the rollup. Possible `\"function\"` values are:  \n  \n- `average`\n- `checked`\n- `count`\n- `count_per_group`\n- `count_values`\n- `date_range`\n- `earliest_date`\n- `empty`\n- `latest_date`\n- `max`\n- `median`\n- `min`\n- `not_empty`\n- `percent_checked`\n- `percent_empty`\n- `percent_not_empty`\n- `percent_per_group`\n- `percent_unchecked`\n- `range`\n- `show_original`\n- `show_unique`\n- `sum`\n- `unchecked`\n- `unique`",
    "1-3": "`\"sum\"`",
    "2-0": "`type`",
    "2-1": "`array` \\|\\| `date` \\|\\| `incomplete` \\|\\| `number` \\|\\| `unsupported`",
    "2-2": "The value type of the calculated rollup.",
    "2-3": "`number`"
  },
  "cols": 4,
  "rows": 3,
  "align": [
    "left",
    "left",
    "left",
    "left"
  ]
}
[/block]


#### Example `rollup` page property value as returned in a GET page request

```json
{
  "Number of units": {
    "id": "hgMz",
    "type": "rollup",
    "rollup": {
      "type": "number",
      "number": 2,
      "function": "count"
    }
  }
}
```

> 🚧 For rollup properties with more than 25 references, use the Retrieve a page property endpoint
>
> Both the [Retrieve a page](https://developers.notion.com/reference/retrieve-a-page) and [Retrieve a page property](https://developers.notion.com/reference/retrieve-a-page-property) endpoints will return information related to the page properties. In cases where a rollup property has more than 25 references, the [Retrieve a page property](https://developers.notion.com/reference/retrieve-a-page-property) endpoint must but used.
>
> Learn more about rollup properties in Notion’s [Help Center](https://developers.notion.com/reference/page-property-values#rollup).

> 🚧 The API does not support updating `rollup` page property values.
>
> To change a page's `rollup` property, use the Notion UI.

### Rich text

| Field       | Type                                                                               | Description                                                                        | Example value                                |
| :---------- | :--------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------- | :------------------------------------------- |
| `rich_text` | an array of [rich text objects](https://developers.notion.com/reference/rich-text) | An array of [rich text objects](https://developers.notion.com/reference/rich-text) | Refer to the example response objects below. |

#### Example `properties` body param for a POST or PATCH page request that creates or updates a  `rich_text` page property value

```json
{
  "properties": {
    "Description": {
      "rich_text": [
        {
          "type": "text",
          "text": {
            "content": "There is some ",
            "link": null
          },
          "annotations": {
            "bold": false,
            "italic": false,
            "strikethrough": false,
            "underline": false,
            "code": false,
            "color": "default"
          },
          "plain_text": "There is some ",
          "href": null
        },
        {
          "type": "text",
          "text": {
            "content": "text",
            "link": null
          },
          "annotations": {
            "bold": true,
            "italic": false,
            "strikethrough": false,
            "underline": false,
            "code": false,
            "color": "default"
          },
          "plain_text": "text",
          "href": null
        },
        {
          "type": "text",
          "text": {
            "content": " in this property!",
            "link": null
          },
          "annotations": {
            "bold": false,
            "italic": false,
            "strikethrough": false,
            "underline": false,
            "code": false,
            "color": "default"
          },
          "plain_text": " in this property!",
          "href": null
        }
      ]
    }
  }
}
```

#### Example `rich_text` page property value as returned in a GET page request

```json
{
  "Description": {
    "id": "HbZT",
    "type": "rich_text",
    "rich_text": [
      {
        "type": "text",
        "text": {
          "content": "There is some ",
          "link": null
        },
        "annotations": {
          "bold": false,
          "italic": false,
          "strikethrough": false,
          "underline": false,
          "code": false,
          "color": "default"
        },
        "plain_text": "There is some ",
        "href": null
      },
      {
        "type": "text",
        "text": {
          "content": "text",
          "link": null
        },
        "annotations": {
          "bold": true,
          "italic": false,
          "strikethrough": false,
          "underline": false,
          "code": false,
          "color": "default"
        },
        "plain_text": "text",
        "href": null
      },
      {
        "type": "text",
        "text": {
          "content": " in this property!",
          "link": null
        },
        "annotations": {
          "bold": false,
          "italic": false,
          "strikethrough": false,
          "underline": false,
          "code": false,
          "color": "default"
        },
        "plain_text": " in this property!",
        "href": null
      }
    ]
  }
}
```

> 📘
>
> The [Retrieve a page endpoint](https://developers.notion.com/reference/retrieve-a-page) returns a maximum of 25 populated inline page or person references for a `rich_text` property. If a `rich_text` property includes more than 25 references, then you can use the [Retrieve a page property item endpoint](https://developers.notion.com/reference/retrieve-a-page-property) for the specific `rich_text` property to get its complete list of references.

### Select

If the type of a page property value is `select`, then the property value contains a `select` object with the following fields:

[block:parameters]
{
  "data": {
    "h-0": "Property",
    "h-1": "Type",
    "h-2": "Description",
    "h-3": "Example value",
    "0-0": "`color`",
    "0-1": "`string` (enum)",
    "0-2": "The color of the option. Possible `\"color\"` values are:   \n  \n- `blue`  \n  - `brown`\n- `default`\n- `gray`\n- `green`\n- `orange`\n- `pink`\n- `purple`\n- `red`\n- yellow\\`Defaults to `default`. The `color` value can’t be updated via the API.",
    "0-3": "`red`",
    "1-0": "`id`",
    "1-1": "`string` ",
    "1-2": "The ID of the option.  \n  \nYou can use `id` or `name` to [update](https://developers.notion.com/reference/patch-page) a select property.",
    "1-3": "`\"b3d773ca-b2c9-47d8-ae98-3c2ce3b2bffb\"`",
    "2-0": "`name`",
    "2-1": "`string`",
    "2-2": "The name of the option as it appears in Notion.  \n  \nIf the select [data source property](ref:property-object) doesn't have an option by that name yet, then the name is added to the data source schema if the integration also has write access to the parent data source.  \n  \nNote: Commas (`\",\"`) are not valid for select values.",
    "2-3": "`\"jQuery\"`"
  },
  "cols": 4,
  "rows": 3,
  "align": [
    "left",
    "left",
    "left",
    "left"
  ]
}
[/block]


#### Example `properties` body param for a POST or PATCH page request that creates or updates a  `select` page property value

```json
{
  "properties": {
    "Department": {
      "select": {
        "name": "Marketing"
      }
    }
  }
}
```

#### Example select page property value as returned in a GET page request

```json
{
  "Department": {
    "id": "Yc%3FJ",
    "type": "select",
    "select": {
      "id": "ou@_",
      "name": "jQuery",
      "color": "purple"
    }
  }
}
```

### Status

If the type of a page property value is `status`, then the property value contains a `status` object with the following fields:

[block:parameters]
{
  "data": {
    "h-0": "Property",
    "h-1": "Type",
    "h-2": "Description",
    "h-3": "Example value",
    "0-0": "`color`",
    "0-1": "`string` (enum)",
    "0-2": "The color of the option. Possible `\"color\"` values are:   \n  \n- `blue`  \n  - `brown`\n- `default`\n- `gray`\n- `green`\n- `orange`\n- `pink`\n- `purple`\n- `red`\n- `yellow`Defaults to `default`. The `color` value can’t be updated via the API.",
    "0-3": "`\"red\"`",
    "1-0": "`id`",
    "1-1": "`string` ",
    "1-2": "`string`",
    "1-3": "`\"b3d773ca-b2c9-47d8-ae98-3c2ce3b2bffb\"`",
    "2-0": "`name`",
    "2-1": "`string`",
    "2-2": "The name of the option as it appears in Notion.",
    "2-3": "`\"In progress\"`"
  },
  "cols": 4,
  "rows": 3,
  "align": [
    "left",
    "left",
    "left",
    "left"
  ]
}
[/block]


#### Example `properties` body param for a POST or PATCH page request that creates or updates a `status` page property value

```json
{
  "properties": {
    "Status": {
      "status": {
        "name": "Not started"
      }
    }
  }
}
```

#### Example `status` page property value as returned in a GET page request

```json
{
  "Status": {
    "id": "Z%3ClH",
    "type": "status",
    "status": {
      "id": "539f2705-6529-42d8-a215-61a7183a92c0",
      "name": "In progress",
      "color": "blue"
    }
  }
}
```

### Title

| Field   | Type                                                                               | Description                                                                         | Example value                                |
| :------ | :--------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------- | :------------------------------------------- |
| `title` | an array of [rich text objects](https://developers.notion.com/reference/rich-text) | An array of [rich text objects](https://developers.notion.com/reference/rich-text). | Refer to the example response objects below. |

#### Example `properties` body param for a POST or PATCH page request that creates or updates a `title` page property value

```json
{
  "properties": {
    "Title": {
      "id": "title",
      "type": "title",
      "title": [
        {
          "type": "text",
          "text": {
            "content": "A better title for the page",
            "link": null
          },
          "annotations": {
            "bold": false,
            "italic": false,
            "strikethrough": false,
            "underline": false,
            "code": false,
            "color": "default"
          },
          "plain_text": "This is also not done",
          "href": null
        }
      ]
    }
  }
}
```

#### Example `title` page property value as returned in a GET page request

```json
{
  "Title": {
    "id": "title",
    "type": "title",
    "title": [
      {
        "type": "text",
        "text": {
          "content": "A better title for the page",
          "link": null
        },
        "annotations": {
          "bold": false,
          "italic": false,
          "strikethrough": false,
          "underline": false,
          "code": false,
          "color": "default"
        },
        "plain_text": "This is also not done",
        "href": null
      }
    ]
  }
}
```

> 📘
>
> The [Retrieve a page endpoint](https://developers.notion.com/reference/retrieve-a-page) returns a maximum of 25 inline page or person references for a `title` property. If a `title` property includes more than 25 references, then you can use the [Retrieve a page property item endpoint](https://developers.notion.com/reference/retrieve-a-page-property) for the specific `title` property to get its complete list of references.

### URL

| Field | Type     | Description                            | Example value                      |
| :---- | :------- | :------------------------------------- | :--------------------------------- |
| `url` | `string` | A string that describes a web address. | `"https://developers.notion.com/"` |

#### Example `properties` body param for a POST or PATCH page request that creates or updates a `url` page property value

```json
{
  "properties": {
    "Website": {
      "url": "https://developers.notion.com/"
    }
  }
}
```

#### Example `url` page property value as returned in a GET page request

```json
{
  "Website": {
    "id": "bB%3D%5B",
    "type": "url",
    "url": "https://developers.notion.com/"
  }
}
```

### Unique ID

| Field    | Type               | Description                                        | Example value |
| -------- | ------------------ | -------------------------------------------------- | ------------- |
| `number` | `number`           | The ID count (auto-incrementing).                  | 3             |
| `prefix` | `string` or `null` | An optional prefix to be applied to the unique ID. | "RL"          |

> 👍
>
> Unique IDs can be read using the API with a [GET page](https://developers.notion.com/reference/retrieve-a-page) request, but they cannot be updated with the API, since they are auto-incrementing.

#### Example `url` page property value as returned in a GET page request

```json
{
  "test-ID": {
    "id": "tqqd",
    "type": "unique_id",
    "unique_id": {
      "number": 3,
      "prefix": "RL",
    },
  },
}
```

### Verification

The verification status of a page in a wiki database. Pages can be verified or unverified, and verifications can have an optional expiration date set.

The verification status cannot currently be set or updated via the public API.

> 📘
>
> The `verification` property is only available for pages that are part of a [wiki database](https://developers.notion.com/docs/working-with-databases#wiki-databases). To learn more about wiki databases and verifying pages, see our [Help Center article](https://www.notion.so/help/wikis-and-verified-pages#verifying-pages).

| Field         | Type                                                                  | Description                                                                                                                                                                                                                                                     | Example value                                |
| ------------- | --------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------- |
| `state`       | `string`                                                              | The verification state of the page. `"verified"` or `"unverified"`.                                                                                                                                                                                             | `"unverified"`                               |
| `verified_by` | [User](https://developers.notion.com/reference/user) object or `null` | If the page if verified, a [User](https://developers.notion.com/reference/user) object will be included to indicate the user who verified the page.                                                                                                             | Refer to the example response objects below. |
| `date`        | Object or `null`                                                      | If the page is verified, the date object will include the date the verification started (`start`). If an expiration date is set for the verification, an end date (`end`) will be included. ([ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) date and time.) | Refer to the example response objects below. |

#### Example `verification` page property values as returned in a GET page request

##### Unverified

```json
{
  Verification: {
    id: "fpVq",
    type: "verification",
    verification: { state: "unverified", verified_by: null, date: null },
  },
}
```

##### Verified with no expiration date set

```json
{
  Verification: {
    id: "fpVq",
    type: "verification",
    verification: {
      state: "verified",
      verified_by: {
        object: "user",
        id: "01e46064-d5fb-4444-8ecc-ad47d076f804",
        name: "User Name",
        avatar_url: null,
        type: "person",
        person: {},
      },
      date: { start: "2023-08-01T04:00:00.000Z", end: null, time_zone: null },
    },
  },
}
```

##### Verified with 90-day expiration date

```json
{
  Verification: {
    id: "fpVq",
    type: "verification",
    verification: {...},
      date: {
        start: "2023-08-01T04:00:00.000Z",
        end: "2023-10-30T04:00:00.000Z",
        time_zone: null,
      },
    },
  },
}
```

## Paginated page properties

The `title`, `rich_text`, `relation` and `people` page properties are returned as a paginated `list` object of individual `property_item` objects.

An abridged set of the the properties found in the `list` object is below. Refer to the [pagination documentation](https://developers.notion.com/reference/intro#pagination) for additional information.

| Field           | Type               | Description                                                   | Example value                                                                                                                      |
| :-------------- | :----------------- | :------------------------------------------------------------ | :--------------------------------------------------------------------------------------------------------------------------------- |
| `object`        | `"list"`           | Always `"list"`.                                              | `"list"`                                                                                                                           |
| `type`          | `"property_item"`  | Always `"property_item"`.                                     | `"property_item"`                                                                                                                  |
| `results`       | `list`             | List of `property_item` objects.                              | `[{"object": "property_item", "id": "vYdV", "type": "relation", "relation": { "id": "535c3fb2-95e6-4b37-a696-036e5eac5cf6"}}... ]` |
| `property_item` | `object`           | A `property_item` object that describes the property.         | `{"id": "title", "next_url": null, "type": "title", "title": {}}`                                                                  |
| `next_url`      | `string` or `null` | The URL the user can request to get the next page of results. | `"http://api.notion.com/v1/pages/0e5235bf86aa4efb93aa772cce7eab71/properties/vYdV?start_cursor=LYxaUO&page_size=25"`               |

# Page property items

## Overview

A `property_item` object describes the identifier, type, and value of a page property. It's returned from the [Retrieve a page property item](ref:retrieve-a-page-property)  API.

Generally, the details on this page are the same as those in [Page properties](ref:page-property-values), but with tweaks and additional information specific to the retrieve page property item endpoint, such as [value pagination](#paginated-property-values) .

## Common fields

Each page property item object contains the following keys. In addition, it will contain a key corresponding with the value of `type`. The value is an object containing type-specific data. The type-specific data are described in the sections below.

[block:parameters]
{
  "data": {
    "h-0": "Property",
    "h-1": "Type",
    "h-2": "Description",
    "h-3": "Example value",
    "0-0": "`object`",
    "0-1": "`\"property_item\"`",
    "0-2": "Always `\"property_item\"`.",
    "0-3": "`\"property_item\"`",
    "1-0": "`id`",
    "1-1": "`string`",
    "1-2": "Underlying identifier for the property. This identifier is guaranteed to remain constant when the property name changes. It may be a UUID, but is often a short random string.  \n  \nThe `id` may be used in place of `name` when creating or updating pages.",
    "1-3": "`\"f%5C%5C%3Ap\"`",
    "2-0": "`type`",
    "2-1": "`string` (enum)",
    "2-2": "Type of the property. Possible values are `\"rich_text\"`, `\"number\"`, `\"select\"`, `\"multi_select\"`, `\"date\"`, `\"formula\"`, `\"relation\"`, `\"rollup\"`, `\"title\"`, `\"people\"`, `\"files\"`, `\"checkbox\"`, `\"url\"`, `\"email\"`, `\"phone_number\"`, `\"created_time\"`, `\"created_by\"`, `\"last_edited_time\"`, and `\"last_edited_by\"`.",
    "2-3": "`\"rich_text\"`"
  },
  "cols": 4,
  "rows": 3,
  "align": [
    "left",
    "left",
    "left",
    "left"
  ]
}
[/block]


## Paginated values

The [`title`, `rich_text`, `relation` and `people`](https://developers.notion.com/reference/retrieve-a-page-property#paginated-properties) property items of are returned as a paginated `list` object of individual `property_item` objects in the results. An abridged set of the the properties found in the `list` object are found below; see the [Pagination](ref:pagination) documentation for additional information.

| Property        | Type               | Description                                                   | Example value                                                                                                                      |
| :-------------- | :----------------- | :------------------------------------------------------------ | :--------------------------------------------------------------------------------------------------------------------------------- |
| `object`        | `"list"`           | Always `"list"`.                                              | `"list"`                                                                                                                           |
| `type`          | `"property_item"`  | Always `"property_item"`.                                     | `"property_item"`                                                                                                                  |
| `results`       | `list`             | List of `property_item` objects.                              | `[{"object": "property_item", "id": "vYdV", "type": "relation", "relation": { "id": "535c3fb2-95e6-4b37-a696-036e5eac5cf6"}}... ]` |
| `property_item` | `object`           | A `property_item` object that describes the property.         | `{"id": "title", "next_url": null, "type": "title", "title": {}}`                                                                  |
| `next_url`      | `string` or `null` | The URL the user can request to get the next page of results. | `"http://api.notion.com/v1/pages/0e5235bf86aa4efb93aa772cce7eab71/properties/vYdV?start_cursor=LYxaUO&page_size=25"`               |

## Title

Title property value objects contain an array of [rich text objects](ref:rich-text) within the `title` property.

```json Title property value
{
  "Name": {
    "object": "list",
    "results": [
      {
        "object": "property_item",
        "id": "title",
        "type": "title",
        "title": {
          "type": "text",
          "text": {
            "content": "The title",
            "link": null
          },
          "annotations": {
            "bold": false,
            "italic": false,
            "strikethrough": false,
            "underline": false,
            "code": false,
            "color": "default"
          },
          "plain_text": "The title",
          "href": null
        }
      }
    ],
    "next_cursor": null,
    "has_more": false,
    "type": "property_item",
    "property_item": {
      "id": "title",
      "next_url": null,
      "type": "title",
      "title": {}
    }
  }
}
```

## Rich text

Rich text property value objects contain an array of [rich text objects](ref:rich-text) within the `rich_text` property.

```json Rich text property value
{
  "Details": {
    "object": "list",
    "results": [
      {
        "object": "property_item",
        "id": "NVv%5E",
        "type": "rich_text",
        "rich_text": {
          "type": "text",
          "text": {
            "content": "Some more text with ",
            "link": null
          },
          "annotations": {
            "bold": false,
            "italic": false,
            "strikethrough": false,
            "underline": false,
            "code": false,
            "color": "default"
          },
          "plain_text": "Some more text with ",
          "href": null
        }
      },
      {
        "object": "property_item",
        "id": "NVv%5E",
        "type": "rich_text",
        "rich_text": {
          "type": "text",
          "text": {
            "content": "fun formatting",
            "link": null
          },
          "annotations": {
            "bold": false,
            "italic": true,
            "strikethrough": false,
            "underline": false,
            "code": false,
            "color": "default"
          },
          "plain_text": "fun formatting",
          "href": null
        }
      }
    ],
    "next_cursor": null,
    "has_more": false,
    "type": "property_item",
    "property_item": {
      "id": "NVv^",
      "next_url": null,
      "type": "rich_text",
      "rich_text": {}
    }
  }
}
```

## Number

Number property value objects contain a number within the `number` property.

```json Number property value
{
  "Quantity": {
    "object": "property_item",
    "id": "XpXf",
    "type": "number",
    "number": 1234
  }
}
```

## Select

Select property value objects contain the following data within the `select` property:

[block:parameters]
{
  "data": {
    "h-0": "Property",
    "h-1": "Type",
    "h-2": "Description",
    "h-3": "Example value",
    "0-0": "`id`",
    "0-1": "`string` (UUIDv4)",
    "0-2": "ID of the option.  \n  \nWhen updating a select property, you can use either `name` or `id`.",
    "0-3": "`\"b3d773ca-b2c9-47d8-ae98-3c2ce3b2bffb\"`",
    "1-0": "`name`",
    "1-1": "`string`",
    "1-2": "Name of the option as it appears in Notion.  \n  \nIf the select [database property](https://developers.notion.com/reference/property-object) does not yet have an option by that name, it will be added to the database schema if the integration also has write access to the parent database.  \n  \nNote: Commas (\",\") are not valid for select values.",
    "1-3": "`\"Fruit\"`",
    "2-0": "`color`",
    "2-1": "`string` (enum)",
    "2-2": "Color of the option. Possible values are: `\"default\"`, `\"gray\"`, `\"brown\"`, `\"red\"`, `\"orange\"`, `\"yellow\"`, `\"green\"`, `\"blue\"`, `\"purple\"`, `\"pink\"`. Defaults to `\"default\"`.  \n  \nNot currently editable.",
    "2-3": "`\"red\"`"
  },
  "cols": 4,
  "rows": 3,
  "align": [
    "left",
    "left",
    "left",
    "left"
  ]
}
[/block]


```json Select property value
{
  "Option": {
    "object": "property_item",
    "id": "%7CtzR",
    "type": "select",
    "select": {
      "id": "64190ec9-e963-47cb-bc37-6a71d6b71206",
      "name": "Option 1",
      "color": "orange"
    }
  }
}
```

## Multi-select

Multi-select property value objects contain an array of multi-select option values within the `multi_select` property.

### Option values

[block:parameters]
{
  "data": {
    "h-0": "Property",
    "h-1": "Type",
    "h-2": "Description",
    "h-3": "Example value",
    "0-0": "`id`",
    "0-1": "`string` (UUIDv4)",
    "0-2": "ID of the option.  \n  \nWhen updating a multi-select property, you can use either `name` or `id`.",
    "0-3": "`\"b3d773ca-b2c9-47d8-ae98-3c2ce3b2bffb\"`",
    "1-0": "`name`",
    "1-1": "`string`",
    "1-2": "Name of the option as it appears in Notion.  \n  \nIf the multi-select [database property](https://developers.notion.com/reference/property-object) does not yet have an option by that name, it will be added to the database schema if the integration also has write access to the parent database.  \n  \nNote: Commas (\",\") are not valid for select values.",
    "1-3": "`\"Fruit\"`",
    "2-0": "`color`",
    "2-1": "`string` (enum)",
    "2-2": "Color of the option. Possible values are: `\"default\"`, `\"gray\"`, `\"brown\"`, `\"red\"`, `\"orange\"`, `\"yellow\"`, `\"green\"`, `\"blue\"`, `\"purple\"`, `\"pink\"`. Defaults to `\"default\"`.  \n  \nNot currently editable.",
    "2-3": "`\"red\"`"
  },
  "cols": 4,
  "rows": 3,
  "align": [
    "left",
    "left",
    "left",
    "left"
  ]
}
[/block]


```json Multi-select property value
{
  "Tags": {
    "object": "property_item",
    "id": "z%7D%5C%3C",
    "type": "multi_select",
    "multi_select": [
      {
        "id": "91e6959e-7690-4f55-b8dd-d3da9debac45",
        "name": "A",
        "color": "orange"
      },
      {
        "id": "2f998e2d-7b1c-485b-ba6b-5e6a815ec8f5",
        "name": "B",
        "color": "purple"
      }
    ]
  }
}
```

## Date

Date property value objects contain the following data within the `date` property:

[block:parameters]
{
  "data": {
    "h-0": "Property",
    "h-1": "Type",
    "h-2": "Description",
    "h-3": "Example value",
    "0-0": "`start`",
    "0-1": "string ([ISO 8601 date and time](https://en.wikipedia.org/wiki/ISO_8601))",
    "0-2": "An ISO 8601 format date, with optional time.",
    "0-3": "`\"2020-12-08T12:00:00Z\"`",
    "1-0": "`end`",
    "1-1": "string (optional, [ISO 8601 date and time](https://en.wikipedia.org/wiki/ISO_8601))",
    "1-2": "An ISO 8601 formatted date, with optional time. Represents the end of a date range.  \n  \nIf `null`, this property's date value is not a range.",
    "1-3": "`\"2020-12-08T12:00:00Z\"`",
    "2-0": "`time_zone`",
    "2-1": "string (optional, enum)",
    "2-2": "Time zone information for `start` and `end`. Possible values are extracted from the [IANA database](https://www.iana.org/time-zones) and they are based on the time zones from [Moment.js](https://momentjs.com/timezone/).  \n  \nWhen time zone is provided, `start` and `end` should not have any [UTC offset](https://en.wikipedia.org/wiki/UTC_offset). In addition, when time zone  is provided, `start` and `end` cannot be dates without time information.  \n  \nIf `null`, time zone information will be contained in [UTC offset](https://en.wikipedia.org/wiki/UTC_offset)s in `start` and `end`.",
    "2-3": "`\"America/Los_Angeles\"`"
  },
  "cols": 4,
  "rows": 3,
  "align": [
    "left",
    "left",
    "left",
    "left"
  ]
}
[/block]


```json Date property value
{
  "Shipment Time": {
    "object": "property_item",
    "id": "i%3Ahj",
    "type": "date",
    "date": {
      "start": "2021-05-11T11:00:00.000-04:00",
      "end": null,
      "time_zone": null
    }
  }
}
```

## Formula

Formula property value objects represent the result of evaluating a formula described in the
[database's properties](https://developers.notion.com/reference/property-object). These objects contain a `type` key and a key corresponding with the value of `type`. The value is an object containing type-specific data. The type-specific data are described in the sections below.

| Property | Type            | Description                                                                                            |
| :------- | :-------------- | :----------------------------------------------------------------------------------------------------- |
| `type`   | `string` (enum) | The type of the formula result. Possible values are `"string"`, `"number"`, `"boolean"`, and `"date"`. |

### String formula

String formula property values contain an optional string within the `string` property.

### Number formula

Number formula property values contain an optional number within the `number` property.

### Boolean formula

Boolean formula property values contain a boolean within the `boolean` property.

### Date formula

Date formula property values contain an optional [date property value](#date-property-values) within the `date` property.

```json Formula Property Value
{
  "Formula": {
    "object": "property_item",
    "id": "KpQq",
    "type": "formula",
    "formula": {
      "type": "number",
      "number": 1234
    }
  }
}
```

## Relation

Relation property value objects contain an array of `relation` property items with page references within the `relation` property. A page reference is an object with an `id` property which is a string value (UUIDv4) corresponding to a page ID in another database.

```json Relation property value
{
  "Project": {
    "object": "list",
    "results": [
      {
        "object": "property_item",
        "id": "vYdV",
        "type": "relation",
        "relation": {
          "id": "535c3fb2-95e6-4b37-a696-036e5eac5cf6"
        }
      }
    ],
    "next_cursor": null,
    "has_more": true,
    "type": "property_item",
    "property_item": {
      "id": "vYdV",
      "next_url": null,
      "type": "relation",
      "relation": {}
    }
  }
}
```

## Rollup

Rollup property value objects represent the result of evaluating a rollup described in the
[data source's properties](ref:property-object). The property is returned as a `list` object of type `property_item` with a list of `relation` items used to computed the rollup under `results`.

A `rollup` property item is also returned under the `property_type` key that describes the rollup aggregation and computed result.

In order to avoid timeouts, if the rollup has a with a large number of aggregations or properties the endpoint returns a `next_cursor` value that is used to determinate the aggregation value _so far_ for the subset of relations that have been paginated through.

Once `has_more` is `false`, then the final rollup value is returned.  See the [Pagination documentation](ref:pagination) for more information on pagination in the Notion API.

Computing the values of following aggregations are _not_ supported. Instead the endpoint returns a list of `property_item` objects for the rollup:

- `show_unique` (Show unique values)
- `unique` (Count unique values)
- `median`(Median)

[block:parameters]
{
  "data": {
    "h-0": "Property",
    "h-1": "Type",
    "h-2": "Description",
    "0-0": "`type`",
    "0-1": "`string` (enum)",
    "0-2": "The type of rollup. Possible values are `\"number\"`, `\"date\"`, `\"array\"`, `\"unsupported\"` and `\"incomplete\"`.",
    "1-0": "`function`",
    "1-1": "`string` (enum)",
    "1-2": "Describes the aggregation used.  \nPossible values include: `count`,  `count_values`,  `empty`,  `not_empty`,  `unique`,  `show_unique`,  `percent_empty`,  `percent_not_empty`,  `sum`,  `average`,  `median`,  `min`,  `max`,  `range`,  `earliest_date`,  `latest_date`,  `date_range`,  `checked`,  `unchecked`,  `percent_checked`,  `percent_unchecked`,  `count_per_group`,  `percent_per_group`,  `show_original`"
  },
  "cols": 3,
  "rows": 2,
  "align": [
    "left",
    "left",
    "left"
  ]
}
[/block]


### Number rollup

Number rollup property values contain a number within the `number` property.

### Date rollup

Date rollup property values contain a [date property value](#date-property-values) within the `date` property.

### Array rollup

Array rollup property values contain an array of `property_item` objects within the `results` property.

### Incomplete rollup

Rollups with an aggregation with more than one page of aggregated results will return a `rollup` object of type `"incomplete"`. To obtain the final value paginate through the next values in the rollup using the `next_cursor` or `next_url` property.

```json Rollup Property Value
{
  "Rollup": {
    "object": "list",
    "results": [
      {
        "object": "property_item",
        "id": "vYdV",
        "type": "relation",
        "relation": {
          "id": "535c3fb2-95e6-4b37-a696-036e5eac5cf6"
        }
      }...
    ],
    "next_cursor": "1QaTunT5",
    "has_more": true,
    "type": "property_item",
    "property_item": {
      "id": "y}~p",
      "next_url": "http://api.notion.com/v1/pages/0e5235bf86aa4efb93aa772cce7eab71/properties/y%7D~p?start_cursor=1QaTunT5&page_size=25",
      "type": "rollup",
      "rollup": {
        "function": "sum",
        "type": "incomplete",
        "incomplete": {}
      }
    }
  }
}
```

## People

People property value objects contain an array of [user objects](ref:user) within the `people` property.

```json People property value
{
  "Owners": {
    "object": "property_item",
    "id": "KpQq",
    "type": "people",
    "people": [
      {
        "object": "user",
        "id": "285e5768-3fdc-4742-ab9e-125f9050f3b8",
        "name": "Example Avo",
        "avatar_url": null,
        "type": "person",
        "person": {
          "email": "avo@example.com"
        }
      }
    ]
  }
}
```

## Files

File property value objects contain an array of file references within the `files` property. A file reference is an object with a [File Object](ref:file-object) and `name` property, with a string value corresponding to a filename of the original file upload (e.g. `"Whole_Earth_Catalog.jpg"`).

```json
{
  "Files": {
    "object": "property_item",
    "id": "KpQq",
    "type": "files",
    "files": [
      {
        "type": "external",
        "name": "Space Wallpaper",
        "external": "https://website.domain/images/space.png"
      }
    ]
  }
}
```

## Checkbox

Checkbox property value objects contain a boolean within the `checkbox` property.

```json Checkbox property value
{
  "Done?": {
    "object": "property_item",
    "id": "KpQq",
    "type": "checkbox",
    "checkbox": true
  }
}
```

## URL

URL property value objects contain a non-empty string within the `url` property. The string describes a web address (i.e. `"http://worrydream.com/EarlyHistoryOfSmalltalk/"`).

```json URL property value
{
  "Website": {
    "object": "property_item",
    "id": "KpQq",
    "type": "url",
    "url": "https://notion.so/notiondevs"
  }
}
```

## Email

Email property value objects contain a string within the `email` property. The string describes an email address (i.e. `"hello@example.org"`).

```json Email property value
{
  "Shipper's Contact": {
    "object": "property_item",
    "id": "KpQq",
    "type": "email",
    "email": "hello@test.com"
  }
}
```

## Phone number

Phone number property value objects contain a string within the `phone_number` property. No structure is enforced.

```json Phone number property value
{
  "Shipper's No.": {
    "object": "property_item",
    "id": "KpQq",
    "type": "phone_number",
    "phone_number": "415-000-1111"
  }
}
```

## Created time

Created time property value objects contain a string within the `created_time` property. The string contains the date and time when this page was created. It is formatted as an [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) date time string (i.e. `"2020-03-17T19:10:04.968Z"`).

```json Created time property value
{
  "Created Time": {
    "object": "property_item",
    "id": "KpQq",
    "type": "create_time",
  	"created_time": "2020-03-17T19:10:04.968Z"
  }
}
```

## Created by

Created by property value objects contain a [user object](ref:user) within the `created_by` property. The user object describes the user who created this page.

```json Created by property value
{
  "Created By": {
    "created_by": {
      "object": "user",
      "id": "23345d4f-cf71-4a70-89a5-226c95a6eaae",
      "name": "Test User",
      "type": "person",
      "person": {
        "email": "avo@example.org"
      }
    }
  }
}
```
```json Created by property value (using ID)
{
  "dsEa": {
    "created_by": {
			"object": "user",
			"id": "71e95936-2737-4e11-b03d-f174f6f13087"
  	}
  }
}
```

## Last edited time

Last edited time property value objects contain a string within the `last_edited_time` property. The string contains the date and time when this page was last updated. It is formatted as an [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) date time string (i.e. `"2020-03-17T19:10:04.968Z"`).

```json Last edited time property value
{
  "Last Edited Time": {
  	"last_edited_time": "2020-03-17T19:10:04.968Z"
  }
}
```
```json Last edited time property value (using ID)
{
  "as0w": {
  	"last_edited_time": "2020-03-17T19:10:04.968Z"
  }
}
```

## Last edited by

Last edited by property value objects contain a [user object](ref:user) within the `last_edited_by` property. The user object describes the user who last updated this page.

```json Last edited by property value
{
  "Last Edited By": {
    "last_edited_by": {
      "object": "user",
      "id": "23345d4f-cf71-4a70-89a5-226c95a6eaae",
      "name": "Test User",
      "type": "person",
      "person": {
        "email": "avo@example.org"
      }
    }
  }
}
```
```json Last edited by property value (using ID)
{
  "as12": {
    "last_edited_by": {
			"object": "user",
			"id": "71e95936-2737-4e11-b03d-f174f6f13087"
  	}
  }
}
```

# Database

Learn more about Notion's database object.

A **database** is an object that contains one or more [data sources](ref:data-sources). Databases can either be displayed inline in the parent page (`is_inline: true`) or as a full page (`is_inline: false`). The properties (schema) of each data source under a database can be maintained independently, and each data source has its own set of rows (pages).

Individual data sources don't have permissions settings, so the set of Notion users and bots that have access to data source children is managed through **databases**.

Databases that exist at the workspace level must be full-page databases, not inline. For easier permission management, we typically recommend having at least one level of parent page in between a database and the top-level workspace root.

## Object fields

> 📘 Changed as of 2025-09-03
>
> In September 2025, the [Data source](ref:data-source) object was introduced, and includes the `properties` that used to exist here at the database level.
>
> [block:image]{"images":[{"image":["https://files.readme.io/6dc5c7eccb432e908290e2642c84579936d55ee79c6cd60a5b0807e70cdeb55a-image.png",null,"Diagram of the new Notion API data model: databases parent one or more data sources, each of which parents zero or more pages."],"align":"center","border":true,"caption":"Diagram of the new Notion API data model.  \nA database is a parent of one or more data sources, each of which parents zero or more pages.  \nPreviously, databases could only have one data source, so the concepts were combined in the API until 2025."}]}[/block]
>
> After [upgrading your API](doc:upgrade-guide-2025-09-03) integration to `2025-09-03`, the new database object shape is displayed, including an array of child `data_sources` but **not** the data source `properties`.

[block:parameters]
{
  "data": {
    "h-0": "Field",
    "h-1": "Type",
    "h-2": "Description",
    "h-3": "Example value",
    "0-0": "`object`",
    "0-1": "`string`",
    "0-2": "Always `\"database\"`.",
    "0-3": "`\"database\"`",
    "1-0": "`id`",
    "1-1": "`string` (UUID)",
    "1-2": "Unique identifier for the database.",
    "1-3": "`\"2f26ee68-df30-4251-aad4-8ddc420cba3d\"`",
    "2-0": "`data_sources`",
    "2-1": "array of data source objects",
    "2-2": "List of child data sources, each of which is a JSON object with an `id` and `name`.  \n  \nUse [Retrieve a data source](ref:retrieve-a-data-source) to get more details on the data source, including its `properties`.",
    "2-3": "`[{\"id\": \"c174b72c-d782-432f-8dc0-b647e1c96df6\", \"name\": \"Tasks data source\"}]`",
    "3-0": "`created_time`",
    "3-1": "`string` ([ISO 8601 date and time](https://en.wikipedia.org/wiki/ISO_8601))",
    "3-2": "Date and time when this database was created. Formatted as an [ISO 8601 date time](https://en.wikipedia.org/wiki/ISO_8601) string.",
    "3-3": "`\"2020-03-17T19:10:04.968Z\"`",
    "4-0": "`created_by`",
    "4-1": "[Partial User](ref:user)",
    "4-2": "User who created the database.",
    "4-3": "`{\"object\": \"user\",\"id\": \"45ee8d13-687b-47ce-a5ca-6e2e45548c4b\"}`",
    "5-0": "`last_edited_time`",
    "5-1": "`string` ([ISO 8601 date and time](https://en.wikipedia.org/wiki/ISO_8601))",
    "5-2": "Date and time when this database was updated. Formatted as an [ISO 8601 date time](https://en.wikipedia.org/wiki/ISO_8601) string.",
    "5-3": "`\"2020-03-17T21:49:37.913Z\"`",
    "6-0": "`last_edited_by`",
    "6-1": "[Partial User](ref:user)",
    "6-2": "User who last edited the database.",
    "6-3": "`{\"object\": \"user\",\"id\": \"45ee8d13-687b-47ce-a5ca-6e2e45548c4b\"}`",
    "7-0": "`title`",
    "7-1": "array of [rich text objects](ref:rich-text)",
    "7-2": "Name of the database as it appears in Notion.  \nSee [rich text object](ref:rich-text)) for a breakdown of the properties.",
    "7-3": "`\"title\": [\n        {\n            \"type\": \"text\",\n            \"text\": {\n                \"content\": \"Can I create a URL property\",\n                \"link\": null\n            },\n            \"annotations\": {\n                \"bold\": false,\n                \"italic\": false,\n                \"strikethrough\": false,\n                \"underline\": false,\n                \"code\": false,\n                \"color\": \"default\"\n            },\n            \"plain_text\": \"Can I create a URL property\",\n            \"href\": null\n        }\n    ]`",
    "8-0": "`description`",
    "8-1": "array of [rich text objects](ref:rich-text)",
    "8-2": "Description of the database as it appears in Notion.  \nSee [rich text object](ref:rich-text)) for a breakdown of the properties.",
    "8-3": "",
    "9-0": "`icon`",
    "9-1": "[File Object](ref:file-object) or [Emoji object](ref:emoji-object)",
    "9-2": "Page icon.",
    "9-3": "",
    "10-0": "`cover`",
    "10-1": "[File object](ref:file-object) ",
    "10-2": "Page cover image.",
    "10-3": "",
    "11-0": "`parent`",
    "11-1": "`object`",
    "11-2": "Information about the database's parent. See [Parent object](ref:parent-object).",
    "11-3": "`{ \"type\": \"page_id\", \"page_id\": \"af5f89b5-a8ff-4c56-a5e8-69797d11b9f8\" }`",
    "12-0": "`url`",
    "12-1": "`string`",
    "12-2": "The URL of the Notion database.",
    "12-3": "`\"https://www.notion.so/668d797c76fa49349b05ad288df2d136\"`",
    "13-0": "`archived`",
    "13-1": "`boolean`",
    "13-2": "The archived status of the  database.",
    "13-3": "`false`",
    "14-0": "`in_trash`",
    "14-1": "`boolean`",
    "14-2": "Whether the database has been deleted.",
    "14-3": "`false`",
    "15-0": "`is_inline`",
    "15-1": "`boolean`",
    "15-2": "Has the value `true` if the database appears in the page as an inline block. Otherwise has the value `false` if the database appears as a child page.",
    "15-3": "`false`",
    "16-0": "`public_url`",
    "16-1": "`string`",
    "16-2": "The public page URL if the page has been published to the web. Otherwise, `null`.",
    "16-3": "`\"https://jm-testing.notion.site/p1-6df2c07bfc6b4c46815ad205d132e22d\"1`"
  },
  "cols": 4,
  "rows": 17,
  "align": [
    "left",
    "left",
    "left",
    "left"
  ]
}
[/block]

# Data source

Learn more about Notion's data source object.

**Data sources** are the individual tables of data that live under a Notion database. [Pages](ref:page) are the items (or children) in a data source. [Page property values](ref:page#property-value-object) must conform to the [property objects](ref:property-object) laid out in the parent data source object.

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/6dc5c7eccb432e908290e2642c84579936d55ee79c6cd60a5b0807e70cdeb55a-image.png",
        null,
        "Diagram of the new Notion API data model: databases parent one or more data sources, each of which parents zero or more pages."
      ],
      "align": "center",
      "border": true,
      "caption": "Diagram of the new Notion API data model.  \nA database is a parent of one or more data sources, each of which parents zero or more pages.  \nPreviously, databases could only have one data source, so the concepts were combined in the API until 2025."
    }
  ]
}
[/block]


As of API version `2025-09-03`, there's a suite of APIs for managing data sources:

- [Create a data source](ref:create-a-data-source): add an additional data source for an existing [Database](ref:database)
- [Update a data source](ref:update-a-data-source): update attributes, such as the `properties`, of a data source
- [Retrieve a data source](ref:retrieve-a-data-source)
- [Query a data source](ref:query-a-data-source)

## Object fields

> 📘
>
> Properties marked with an asterisk (\*) are available to integrations with any capabilities. Other properties require read content capabilities in order to be returned from the Notion API. For more information on integration capabilities, see the [capabilities guide](ref:capabilities).

[block:parameters]
{
  "data": {
    "h-0": "Field",
    "h-1": "Type",
    "h-2": "Description",
    "h-3": "Example value",
    "0-0": "`object`\\*",
    "0-1": "`string`",
    "0-2": "Always `\"data_source\"`.",
    "0-3": "`\"data_source\"`",
    "1-0": "`id`\\*",
    "1-1": "`string` (UUID)",
    "1-2": "Unique identifier for the data source.",
    "1-3": "`\"2f26ee68-df30-4251-aad4-8ddc420cba3d\"`",
    "2-0": "`properties`\\*",
    "2-1": "`object`",
    "2-2": "Schema of properties for the data source as they appear in Notion.  \n  \n`key` string  \nThe name of the property as it appears in Notion.  \n  \n`value` object  \nA [Property object](https://developers.notion.com/reference/property-object).",
    "2-3": "",
    "3-0": "`parent`",
    "3-1": "`object`",
    "3-2": "Information about the data source's parent database. See [Parent object](ref:parent-object).",
    "3-3": "`{\"type\": \"database_id\", \"database_id\": \"842a0286-cef0-46a8-abba-eac4c8ca644e\"}`",
    "4-0": "`database_parent`",
    "4-1": "`object`",
    "4-2": "Information about the database's parent (in other words, the the data source's grandparent). See [Parent object](ref:parent-object) .",
    "4-3": "`{ \"type\": \"page_id\", \"page_id\": \"af5f89b5-a8ff-4c56-a5e8-69797d11b9f8\" }`",
    "5-0": "`created_time`",
    "5-1": "`string` ([ISO 8601 date and time](https://en.wikipedia.org/wiki/ISO_8601))",
    "5-2": "Date and time when this data source was created. Formatted as an [ISO 8601 date time](https://en.wikipedia.org/wiki/ISO_8601) string.",
    "5-3": "`\"2020-03-17T19:10:04.968Z\"`",
    "6-0": "`created_by`",
    "6-1": "[Partial User](ref:user)",
    "6-2": "User who created the data source.",
    "6-3": "`{\"object\": \"user\", \"id\": \"45ee8d13-687b-47ce-a5ca-6e2e45548c4b\"}`",
    "7-0": "`last_edited_time`",
    "7-1": "`string` ([ISO 8601 date and time](https://en.wikipedia.org/wiki/ISO_8601))",
    "7-2": "Date and time when this data source was updated. Formatted as an [ISO 8601 date time](https://en.wikipedia.org/wiki/ISO_8601) string.",
    "7-3": "`\"2020-03-17T21:49:37.913Z\"`",
    "8-0": "`last_edited_by`",
    "8-1": "[Partial User](ref:user)",
    "8-2": "User who last edited the data source.",
    "8-3": "`{\"object\": \"user\",\"id\": \"45ee8d13-687b-47ce-a5ca-6e2e45548c4b\"}`",
    "9-0": "`title`",
    "9-1": "array of [rich text objects](ref:rich-text)",
    "9-2": "Name of the data source as it appears in Notion.  \nSee [rich text object](ref:rich-text)) for a breakdown of the properties.",
    "9-3": "`[  \n  {  \n    \"type\": \"text\",  \n    \"text\": {  \n      \"content\": \"Can I create a URL property\",  \n      \"link\": null  \n    },  \n    \"annotations\": {  \n      \"bold\": false,  \n      \"italic\": false,  \n      \"strikethrough\": false,  \n      \"underline\": false,  \n      \"code\": false,  \n      \"color\": \"default\"  \n    },  \n    \"plain_text\": \"Can I create a URL property\",  \n    \"href\": null  \n  }  \n]`",
    "10-0": "`description`",
    "10-1": "array of [rich text objects](ref:rich-text)",
    "10-2": "Description of the data source as it appears in Notion.  \nSee [rich text object](ref:rich-text)) for a breakdown of the properties.",
    "10-3": "",
    "11-0": "`icon`",
    "11-1": "[File Object](ref:file-object) or [Emoji object](ref:emoji-object)",
    "11-2": "Data source icon.",
    "11-3": "",
    "12-0": "`archived`",
    "12-1": "`boolean`",
    "12-2": "The archived status of the  data source.",
    "12-3": "`false`",
    "13-0": "`in_trash`",
    "13-1": "`boolean`",
    "13-2": "Whether the data source has been deleted.",
    "13-3": "`false`"
  },
  "cols": 4,
  "rows": 14,
  "align": [
    "left",
    "left",
    "left",
    "left"
  ]
}
[/block]


> 🚧 Maximum schema size recommendation
>
> Notion recommends a maximum schema size of **50KB**. Updates to database schemas that are too large will be blocked to help maintain database performance.
>
# Data source properties

Data source property objects are rendered in the Notion UI as data columns.

All [data source objects](ref:data-source) include a child `properties` object. This `properties` object is composed of individual data source property objects. These property objects define the data source schema and are rendered in the Notion UI as data columns.

> 📘 Data source rows
>
> If you’re looking for information about how to use the API to work with data source rows, then refer to the [page property values](https://developers.notion.com/reference/property-value-object) documentation. The API treats data source rows as pages.

Every data source property object contains the following keys:

[block:parameters]
{
  "data": {
    "h-0": "Field",
    "h-1": "Type",
    "h-2": "Description",
    "h-3": "Example value",
    "0-0": "`id`",
    "0-1": "`string`",
    "0-2": "An identifier for the property, usually a short string of random letters and symbols.  \n  \nSome automatically generated property types have special human-readable IDs. For example, all Title properties have an `id` of `\"title\"`.",
    "0-3": "`\"fy:{\"`",
    "1-0": "`name`",
    "1-1": "`string`",
    "1-2": "The name of the property as it appears in Notion.",
    "1-3": "",
    "2-0": "`description`",
    "2-1": "`string`",
    "2-2": "The description of a property as it appear in Notion. ",
    "2-3": "",
    "3-0": "`type`",
    "3-1": "`string` (enum)",
    "3-2": "The type that controls the behavior of the property. Possible values are:  \n  \n\\- `\"checkbox\"`  \n  \n- `\"created_by\"`\n- `\"created_time\"`\n- `\"date\"`\n- `\"email\"`\n- `\"files\"`\n- `\"formula\"`\n- `\"last_edited_by\"`\n- `\"last_edited_time\"`\n- `\"multi_select\"`\n- `\"number\"`\n- `\"people\"`\n- `\"phone_number\"`\n- `\"relation\"`\n- `\"rich_text\"`\n- `\"rollup\"`\n- `\"select\"`\n- `\"status\"`\n- `\"title\"`\n- `\"url\"`",
    "3-3": "`\"rich_text\"`"
  },
  "cols": 4,
  "rows": 4,
  "align": [
    "left",
    "left",
    "left",
    "left"
  ]
}
[/block]


Each data source property object also contains a type object. The key of the object is the `type` of the object, and the value is an object containing type-specific configuration. The following sections detail these type-specific objects along with example property objects for each type.

## Checkbox

A checkbox data source property is rendered in the Notion UI as a column that contains checkboxes. The `checkbox` type object is empty; there is no additional property configuration.

```json Example checkbox data source property object
"Task complete": {
  "id": "BBla",
  "name": "Task complete",
  "type": "checkbox",
  "checkbox": {}
}
```

## Created by

A created by data source property is rendered in the Notion UI as a column that contains people mentions of each row's author as values.

The `created_by` type object is empty. There is no additional property configuration.

```json Example created by data source property object
"Created by": {
  "id": "%5BJCR",
  "name": "Created by",
  "type": "created_by",
  "created_by": {}
}
```

## Created time

A created time data source property is rendered in the Notion UI as a column that contains timestamps of when each row was created as values.

The `created_time` type object is empty. There is no additional property configuration.

```json Example created time data source property object
"Created time": {
  "id": "XcAf",
  "name": "Created time",
  "type": "created_time",
  "created_time": {}
}
```

## Date

A date data source property is rendered in the Notion UI as a column that contains date values.

The `date` type object is empty; there is no additional configuration.

```json Example date data source property object
"Task due date" {
  "id": "AJP%7D",
  "name": "Task due date",
  "type": "date",
  "date": {}
}
```

## Email

An email data source property is represented in the Notion UI as a column that contains email values.

The `email` type object is empty. There is no additional property configuration.

```json Example email data source property object
"Contact email": {
  "id": "oZbC",
  "name": "Contact email",
  "type": "email",
  "email": {}
}
```

## Files

A files data source property is rendered in the Notion UI as a column that has values that are either files uploaded directly to Notion or external links to files. The `files` type object is empty; there is no additional configuration.

```json Example files data source property object
"Product image": {
  "id": "pb%3E%5B",
  "name": "Product image",
  "type": "files",
  "files": {}
}
```

## Formula

A formula data source property is rendered in the Notion UI as a column that contains values derived from a provided expression.

The `formula` type object defines the expression in the following fields:

[block:parameters]
{
  "data": {
    "h-0": "Field",
    "h-1": "Type",
    "h-2": "Description",
    "h-3": "Example value",
    "0-0": "`expression`",
    "0-1": "`string`",
    "0-2": "The formula that is used to compute the values for this property.  \n  \nRefer to the Notion help center for [information about formula syntax](https://www.notion.so/help/formulas).",
    "0-3": "`{{notion:block_property:BtVS:00000000-0000-0000-0000-000000000000:8994905a-074a-415f-9bcf-d1f8b4fa38e4}}/2`"
  },
  "cols": 4,
  "rows": 1,
  "align": [
    "left",
    "left",
    "left",
    "left"
  ]
}
[/block]


```json Example formula data source property object
"Updated price": {
  "id": "YU%7C%40",
  "name": "Updated price",
  "type": "formula",
  "formula": {
    "expression": "{{notion:block_property:BtVS:00000000-0000-0000-0000-000000000000:8994905a-074a-415f-9bcf-d1f8b4fa38e4}}/2"
  }
}
```

## Last edited by

A last edited by data source property is rendered in the Notion UI as a column that contains people mentions of the person who last edited each row as values.

The `last_edited_by` type object is empty. There is no additional property configuration.

## Last edited time

A last edited time data source property is rendered in the Notion UI as a column that contains timestamps of when each row was last edited as values.

The `last_edited_time` type object is empty. There is no additional property configuration.

```json Example last edited time data source property object
"Last edited time": {
  "id": "jGdo",
  "name": "Last edited time",
  "type": "last_edited_time",
  "last_edited_time": {}
}
```

## Multi-select

A multi-select data source property is rendered in the Notion UI as a column that contains values from a range of options. Each row can contain one or multiple options.

The `multi_select` type object includes an array of `options` objects. Each option object details settings for the option, indicating the following fields:

[block:parameters]
{
  "data": {
    "h-0": "Field",
    "h-1": "Type",
    "h-2": "Description",
    "h-3": "Example value",
    "0-0": "`color`",
    "0-1": "`string` (enum)",
    "0-2": "The color of the option as rendered in the Notion UI. Possible values include:  \n  \n\\- `blue`  \n  \n- `brown`\n- `default`\n- `gray`\n- `green`\n- `orange`\n- `pink`\n- `purple`\n- `red`\n- `yellow`",
    "0-3": "`\"blue\"`",
    "1-0": "`id`",
    "1-1": "`string`",
    "1-2": "An identifier for the option, which does not change if the name is changed. An `id` is sometimes, but not _always_, a UUID.",
    "1-3": "`\"ff8e9269-9579-47f7-8f6e-83a84716863c\"`",
    "2-0": "`name`",
    "2-1": "`string`",
    "2-2": "The name of the option as it appears in Notion.  \n  \n**Notes**: Commas (\",\") are not valid for multi-select properties. Names **MUST** be unique across options, ignoring case. For example, you can't have two options that are named `\"apple\"` and `\"APPLE\"`.",
    "2-3": "`\"Fruit\"`"
  },
  "cols": 4,
  "rows": 3,
  "align": [
    "left",
    "left",
    "left",
    "left"
  ]
}
[/block]


```json Example multi-select data source property
"Store availability": {
  "id": "flsb",
  "name": "Store availability",
  "type": "multi_select",
  "multi_select": {
    "options": [
      {
        "id": "5de29601-9c24-4b04-8629-0bca891c5120",
        "name": "Duc Loi Market",
        "color": "blue"
      },
      {
        "id": "385890b8-fe15-421b-b214-b02959b0f8d9",
        "name": "Rainbow Grocery",
        "color": "gray"
      },
      {
        "id": "72ac0a6c-9e00-4e8c-80c5-720e4373e0b9",
        "name": "Nijiya Market",
        "color": "purple"
      },
      {
        "id": "9556a8f7-f4b0-4e11-b277-f0af1f8c9490",
        "name": "Gus's Community Market",
        "color": "yellow"
      }
    ]
  }
}
```

## Number

A number data source property is rendered in the Notion UI as a column that contains numeric values. The `number` type object contains the following fields:

[block:parameters]
{
  "data": {
    "h-0": "Field",
    "h-1": "Type",
    "h-2": "Description",
    "h-3": "Example value",
    "0-0": "`format`",
    "0-1": "`string` (enum)",
    "0-2": "The way that the number is displayed in Notion. Potential values include:  \n  \n\\- `argentine_peso`  \n  \n- `baht`\n- `australian_dollar`\n- `canadian_dollar`\n- `chilean_peso`\n- `colombian_peso`\n- `danish_krone`\n- `dirham`\n- `dollar`\n- `euro`\n- `forint`\n- `franc`\n- `hong_kong_dollar`\n- `koruna`\n- `krona`\n- `leu`\n- `lira`\n- `mexican_peso`\n- `new_taiwan_dollar`\n- `new_zealand_dollar`\n- `norwegian_krone`\n- `number`\n- `number_with_commas`\n- `percent`\n- `philippine_peso`\n- `pound`\n- `peruvian_sol`\n- `rand`\n- `real`\n- `ringgit`\n- `riyal`\n- `ruble`\n- `rupee`\n- `rupiah`\n- `shekel`\n- `singapore_dollar`\n- `uruguayan_peso`\n- `yen`,\n- `yuan`\n- `won`\n- `zloty`",
    "0-3": "`\"percent\"`"
  },
  "cols": 4,
  "rows": 1,
  "align": [
    "left",
    "left",
    "left",
    "left"
  ]
}
[/block]


```json Example number data source property object
"Price"{
  "id": "%7B%5D_P",
  "name": "Price",
  "type": "number",
  "number": {
    "format": "dollar"
  }
}
```

## People

A people data source property is rendered in the Notion UI as a column that contains people mentions.  The `people` type object is empty; there is no additional configuration.

```json Example people data source property object
"Project owner": {
  "id": "FlgQ",
  "name": "Project owner",
  "type": "people",
  "people": {}
}
```

## Phone number

A phone number data source property is rendered in the Notion UI as a column that contains phone number values.

The `phone_number` type object is empty. There is no additional property configuration.

```json Example phone number data source property object
"Contact phone number": {
  "id": "ULHa",
  "name": "Contact phone number",
  "type": "phone_number",
  "phone_number": {}
}
```

## Relation

A relation data source property is rendered in the Notion UI as column that contains [relations](https://www.notion.so/help/relations-and-rollups), references to pages in another data source, as values.

The `relation` type object contains the following fields:

[block:parameters]
{
  "data": {
    "h-0": "Field",
    "h-1": "Type",
    "h-2": "Description",
    "h-3": "Example value",
    "0-0": "`data_source_id`",
    "0-1": "`string` (UUID)",
    "0-2": "The data source that the relation property refers to.  \n  \nThe corresponding linked page values must belong to the data source in order to be valid.",
    "0-3": "`\"668d797c-76fa-4934-9b05-ad288df2d136\"`",
    "1-0": "`synced_property_id`",
    "1-1": "`string`",
    "1-2": "The `id` of the corresponding property that is updated in the related data source when this property is changed.",
    "1-3": "`\"fy:{\"`",
    "2-0": "`synced_property_name`",
    "2-1": "`string`",
    "2-2": "The `name` of the corresponding property that is updated in the related data source when this property is changed.",
    "2-3": "`\"Ingredients\"`"
  },
  "cols": 4,
  "rows": 3,
  "align": [
    "left",
    "left",
    "left",
    "left"
  ]
}
[/block]


```json Example relation data source property object
"Projects": {
  "id": "~pex",
  "name": "Projects",
  "type": "relation",
  "relation": {
    "data_source_id": "6c4240a9-a3ce-413e-9fd0-8a51a4d0a49b",
    "dual_property": {
      "synced_property_name": "Tasks",
      "synced_property_id": "JU]K"
    }
  }
}
```

> 📘 Database relations must be shared with your integration
>
> To retrieve properties from data source [relations](https://www.notion.so/help/relations-and-rollups#what-is-a-database-relation), the related database must be shared with your integration in addition to the database being retrieved. If the related database is not shared, properties based on relations will not be included in the API response.
>
> Similarly, to update a data source relation property via the API, share the related database with the integration.

## Rich text

A rich text data source property is rendered in the Notion UI as a column that contains text values. The `rich_text` type object is empty; there is no additional configuration.

```json Example rich text data source property object
"Project description": {
  "id": "NZZ%3B",
  "name": "Project description",
  "type": "rich_text",
  "rich_text": {}
}
```

## Rollup

A rollup data source property is rendered in the Notion UI as a column with values that are rollups, specific properties that are pulled from a related data source.

The `rollup` type object contains the following fields:

[block:parameters]
{
  "data": {
    "h-0": "Field",
    "h-1": "Type",
    "h-2": "Description",
    "h-3": "Example value",
    "0-0": "`function`",
    "0-1": "`string` (enum)",
    "0-2": "The function that computes the rollup value from the related pages.  \n  \nPossible values include:  \n  \n\\- `average`  \n  \n- `checked`\n- `count_per_group`\n- `count`\n- `count_values`\n- `date_range`\n- `earliest_date`\n- `empty`\n- `latest_date`\n- `max`\n- `median`\n- `min`\n- `not_empty`\n- `percent_checked`\n- `percent_empty`\n- `percent_not_empty`\n- `percent_per_group`\n- `percent_unchecked`\n- `range`\n- `unchecked`\n- `unique`\n- `show_original`\n- `show_unique`\n- `sum`",
    "0-3": "`\"sum\"`",
    "1-0": "`relation_property_id`",
    "1-1": "`string`",
    "1-2": "The `id` of the related data source property that is rolled up.",
    "1-3": "`\"fy:{\"`",
    "2-0": "`relation_property_name`",
    "2-1": "`string`",
    "2-2": "The `name` of the related data source property that is rolled up.",
    "2-3": "`Tasks\"`",
    "3-0": "`rollup_property_id`",
    "3-1": "`string`",
    "3-2": "The `id` of the rollup property.",
    "3-3": "`\"fy:{\"`",
    "4-0": "`rollup_property_name`",
    "4-1": "`string`",
    "4-2": "The `name` of the rollup property.",
    "4-3": "`\"Days to complete\"`"
  },
  "cols": 4,
  "rows": 5,
  "align": [
    "left",
    "left",
    "left",
    "left"
  ]
}
[/block]


```json Example rollup data source property object
"Estimated total project time": {
  "id": "%5E%7Cy%3C",
  "name": "Estimated total project time",
  "type": "rollup",
  "rollup": {
    "rollup_property_name": "Days to complete",
    "relation_property_name": "Tasks",
    "rollup_property_id": "\\nyY",
    "relation_property_id": "Y]<y",
    "function": "sum"
  }
}
```

## Select

A select data source property is rendered in the Notion UI as a column that contains values from a selection of options. Only one option is allowed per row.

The `select` type object contains an array of objects representing the available options. Each option object includes the following fields:

[block:parameters]
{
  "data": {
    "h-0": "Field",
    "h-1": "Type",
    "h-2": "Description",
    "h-3": "Example value",
    "0-0": "`color`",
    "0-1": "`string` (enum)",
    "0-2": "The color of the option as rendered in the Notion UI. Possible values include:  \n  \n\\- `blue`  \n  \n- `brown`\n- `default`\n- `gray`\n- `green`\n- `orange`\n- `pink`\n- `purple`\n- `red`\n- `yellow`",
    "0-3": "\\- `\"red\"`",
    "1-0": "`id`",
    "1-1": "`string`",
    "1-2": "An identifier for the option. It doesn't change if the name is changed. These are sometimes, but not _always_, UUIDs.",
    "1-3": "`\"ff8e9269-9579-47f7-8f6e-83a84716863c\"`",
    "2-0": "`name`",
    "2-1": "`string`",
    "2-2": "The name of the option as it appears in the Notion UI.  \n  \n**Notes**: Commas (\",\") are not valid for select properties. Names **MUST** be unique across options, ignoring case. For example, you can't have two options that are named `\"apple\"` and `\"APPLE\"`.",
    "2-3": "`\"Fruit\"`"
  },
  "cols": 4,
  "rows": 3,
  "align": [
    "left",
    "left",
    "left",
    "left"
  ]
}
[/block]


```json Example select data source property object
"Food group": {
  "id": "%40Q%5BM",
  "name": "Food group",
  "type": "select",
  "select": {
    "options": [
      {
        "id": "e28f74fc-83a7-4469-8435-27eb18f9f9de",
        "name": "🥦Vegetable",
        "color": "purple"
      },
      {
        "id": "6132d771-b283-4cd9-ba44-b1ed30477c7f",
        "name": "🍎Fruit",
        "color": "red"
      },
      {
        "id": "fc9ea861-820b-4f2b-bc32-44ed9eca873c",
        "name": "💪Protein",
        "color": "yellow"
      }
    ]
  }
}
```

## Status

A status data source property is rendered in the Notion UI as a column that contains values from a list of status options. The `status` type object includes an array of `options` objects and an array of `groups` objects.

The `options` array is a sorted list of list of the available status options for the property. Each option object in the array has the following fields:

[block:parameters]
{
  "data": {
    "h-0": "Field",
    "h-1": "Type",
    "h-2": "Description",
    "h-3": "Example value",
    "0-0": "`color`",
    "0-1": "`string` (enum)",
    "0-2": "The color of the option as rendered in the Notion UI. Possible values include:  \n  \n\\- `blue`  \n  \n- `brown`\n- `default`\n- `gray`\n- `green`\n- `orange`\n- `pink`\n- `purple`\n- `red`\n- `yellow`",
    "0-3": "`\"green\"`",
    "1-0": "`id`",
    "1-1": "`string`",
    "1-2": "An identifier for the option. The `id` does not change if the `name` is changed. It is sometimes, but not _always_, a UUID.",
    "1-3": "`\"ff8e9269-9579-47f7-8f6e-83a84716863c\"`",
    "2-0": "`name`",
    "2-1": "`string`",
    "2-2": "The name of the option as it appears in the Notion UI.  \n  \n**Notes**: Commas (\",\") are not valid for select properties. Names **MUST** be unique across options, ignoring case. For example, you can't have two options that are named `\"In progress\"` and `\"IN PROGRESS\"`.",
    "2-3": "`\"In progress\"`"
  },
  "cols": 4,
  "rows": 3,
  "align": [
    "left",
    "left",
    "left",
    "left"
  ]
}
[/block]


A group is a collection of options. The `groups` array is a sorted list of the available groups for the property. Each group object in the array has the following fields:

[block:parameters]
{
  "data": {
    "h-0": "Field",
    "h-1": "Type",
    "h-2": "Description",
    "h-3": "Example value",
    "0-0": "`color`",
    "0-1": "`string` (enum)",
    "0-2": "The color of the option as rendered in the Notion UI. Possible values include:  \n  \n\\- `blue`  \n  \n- `brown`\n- `default`\n- `gray`\n- `green`\n- `orange`\n- `pink`\n- `purple`\n- `red`\n- `yellow`",
    "0-3": "`\"purple\"`",
    "1-0": "`id`",
    "1-1": "`string`",
    "1-2": "An identifier for the option. The `id` does not change if the `name` is changed. It is sometimes, but not _always_, a UUID.",
    "1-3": "`\"ff8e9269-9579-47f7-8f6e-83a84716863c\"`",
    "2-0": "`name`",
    "2-1": "`string`",
    "2-2": "The name of the option as it appears in the Notion UI.  \n  \n**Note**: Commas (\",\") are not valid for status values.",
    "2-3": "`\"To do\"`",
    "3-0": "`option_ids`",
    "3-1": "an array of `string`s (UUID)",
    "3-2": "A sorted list of `id`s of all of the options that belong to a group.",
    "3-3": "Refer to the example `status` object below."
  },
  "cols": 4,
  "rows": 4,
  "align": [
    "left",
    "left",
    "left",
    "left"
  ]
}
[/block]


```json Example status data source property object
"Status": {
  "id": "biOx",
  "name": "Status",
  "type": "status",
  "status": {
    "options": [
      {
        "id": "034ece9a-384d-4d1f-97f7-7f685b29ae9b",
        "name": "Not started",
        "color": "default"
      },
      {
        "id": "330aeafb-598c-4e1c-bc13-1148aa5963d3",
        "name": "In progress",
        "color": "blue"
      },
      {
        "id": "497e64fb-01e2-41ef-ae2d-8a87a3bb51da",
        "name": "Done",
        "color": "green"
      }
    ],
    "groups": [
      {
        "id": "b9d42483-e576-4858-a26f-ed940a5f678f",
        "name": "To-do",
        "color": "gray",
        "option_ids": [
          "034ece9a-384d-4d1f-97f7-7f685b29ae9b"
        ]
      },
      {
        "id": "cf4952eb-1265-46ec-86ab-4bded4fa2e3b",
        "name": "In progress",
        "color": "blue",
        "option_ids": [
          "330aeafb-598c-4e1c-bc13-1148aa5963d3"
        ]
      },
      {
        "id": "4fa7348e-ae74-46d9-9585-e773caca6f40",
        "name": "Complete",
        "color": "green",
        "option_ids": [
          "497e64fb-01e2-41ef-ae2d-8a87a3bb51da"
        ]
      }
    ]
  }
}
```

> 🚧 It is not possible to update a status data source property's `name` or `options` values via the API.
>
> Update these values from the Notion UI, instead.

## Title

A title data source property controls the title that appears at the top of a page when a data source row is opened. The `title` type object itself is empty; there is no additional configuration.

```json Example title data source property object
"Project name": {
  "id": "title",
  "name": "Project name",
  "type": "title",
  "title": {}
}
```

> 🚧 All data sources require one, and only one, `title` property.
>
> The API throws errors if you send a request to [Create a data source](ref:create-a-data-source) or [Create a database](ref:database-create) without a `title` property, or if you attempt to [Update a data source](ref:update-a-data-source) to add or remove a `title` property.

> 📘 Title data source property vs. data source title
>
> A `title` data source property is a type of column in a data source.
>
> A data source `title` defines the title of the data source and is found on the [data source object](ref:data-source).
>
> Every data source requires both a data source `title` and a `title` data source property. This ensures that we have both:
>
> - An overall title to display when viewing the database or data source in the Notion app
> - A title property for each page under the data source, so page titles can be displayed in the Notion app

## URL

A URL data source property is represented in the Notion UI as a column that contains URL values.

The `url` type object is empty. There is no additional property configuration.

```json Example URL data source property object
"Project URL": {
  "id": "BZKU",
  "name": "Project URL",
  "type": "url",
  "url": {}
}
```

## Unique ID

A unique ID data source property records values that are automatically incremented, and enforced to be unique across all pages in a data source. This can be useful for task or bug report IDs (e.g. TASK-1234), or other similar types of identifiers that must be unique.

The `unique_id` type object can contain an optional `prefix` attribute, which is a common prefix assigned to pages in the data source. When a `prefix` is set, a special URL (for example, `notion.so/TASK-1234`) is generated to be able to look up a page easily by the ID. Learn more in our [help center documentation](https://www.notion.com/help/unique-id) or [Notion Academy lesson](https://www.notion.com/help/notion-academy/lesson/unique-id-property).

```json Example unique ID data source property object
"Task ID": {
  "prefix": "TASK"
}
```

# Parent

Learn more about different parent objects that link together a workspace's entities in Notion's API.

[Pages](ref:page), [databases](ref:database), [data sources](ref:data-source), [comments](ref:comment-object) and [blocks](ref:block) are either located inside other pages, databases, data sources, and blocks, or are located at the top level of a workspace. This location is known as the "parent". Parent information is represented by a consistent `parent` object throughout the API.

General parenting rules:

- Pages can be parented by other pages, data sources, blocks, or by the whole workspace.
  - _Prior to [API version 2025-09-03](doc:upgrade-guide-2025-09-03), page parents were databases, not data sources._
- Blocks can be parented by pages, data sources, or blocks.
- Databases can be parented by pages, blocks, or by the whole workspace.
  - _For wikis, databases can also have a data source parent._
- Data sources are parented by databases.
  - _Linked or externally synced external data sources may have data source parents, but aren't thoroughly supported in Notion's API._

> 🚧 Exceptions apply
>
> These parenting rules reflect the possible response you may receive when retrieving information about pages, databases, and blocks via Notion’s REST API in the latest APIversion.
>
> If you are creating new pages, databases, or blocks via Notion’s public REST API, the parenting rules may vary. For example, the parent of a database currently must be a page if it is [created](https://developers.notion.com/reference/create-a-database) via the API.
>
> Refer to the API reference documentation for creating [pages](ref:post-page), [databases](ref:database-create), [data sources](ref:create-a-data-source), and [blocks](ref:patch-block-children) for more information on current parenting rules.

### Database parent

Database parents most commonly show up for [Data source](ref:data-source) objects.

| Property      | Type              | Description                                                       | Example values                           |
| :------------ | :---------------- | :---------------------------------------------------------------- | :--------------------------------------- |
| `type`        | `string`          | Always `"database_id"`.                                           | `"database_id"`                          |
| `database_id` | `string` (UUIDv4) | The ID of the [database](ref:database) that this page belongs to. | `"b8595b75-abd1-4cad-8dfe-f935a8ef57cb"` |

```json Database parent example
{
  "type": "database_id",
  "database_id": "d9824bdc-8445-4327-be8b-5b47500af6ce"
}
```

### Data source parent

Data source parents most commonly show up for [Page](ref:page) objects.

| Property         | Type              | Description                                                                                                           | Example values                           |
| :--------------- | :---------------- | :-------------------------------------------------------------------------------------------------------------------- | :--------------------------------------- |
| `type`           | `string`          | Always `"data_source_id"`.                                                                                            | `"data_source_id"`                       |
| `data_source_id` | `string` (UUIDv4) | The ID of the [data source](ref:data-source)  that this page belongs to.                                              | `"1a44be12-0953-4631-b498-9e5817518db8"` |
| `database_id`    | `string` (UUIDv4) | The ID of the [database](ref:database) that the data source belongs to, provided in the API response for convenience. | `"b8595b75-abd1-4cad-8dfe-f935a8ef57cb"` |

```json Data source parent example
{
  "type": "data_source_id",
  "data_source_id": "1a44be12-0953-4631-b498-9e5817518db8",
  "database_id": "d9824bdc-8445-4327-be8b-5b47500af6ce"
}
```

### Page parent

| Property  | Type              | Description                                               | Example values                           |
| :-------- | :---------------- | :-------------------------------------------------------- | :--------------------------------------- |
| `type`    | `string`          | Always `"page_id"`.                                       | `"page_id"`                              |
| `page_id` | `string` (UUIDv4) | The ID of the [page](ref:page) that this page belongs to. | `"59833787-2cf9-4fdf-8782-e53db20768a5"` |

```json Page parent example
{
  "type": "page_id",
  "page_id": "59833787-2cf9-4fdf-8782-e53db20768a5"
}
```

### Workspace parent

A page or database with a workspace parent is a top-level page within a Notion workspace. Team-level pages are also currently represented as having a workspace parent in the API.

The workspace `parent` object contains the following keys:

| Property    | Type      | Description           | Example values |
| :---------- | :-------- | :-------------------- | :------------- |
| `type`      | `type`    | Always `"workspace"`. | `"workspace"`  |
| `workspace` | `boolean` | Always `true`.        | `true`         |

```json Workspace parent example
{
  "type": "workspace",
  "workspace": true
}
```

### Block parent

A page may have a block parent if it is created inline in a chunk of text, or is located beneath another block like a toggle or bullet block. The `parent` property is an object containing the following keys:

| Property   | Type              | Description                                               | Example values                           |
| :--------- | :---------------- | :-------------------------------------------------------- | :--------------------------------------- |
| `type`     | `type`            | Always `"block_id"`.                                      | `"block_id"`                             |
| `block_id` | `string` (UUIDv4) | The ID of the [page](ref:page) that this page belongs to. | `"ea29285f-7282-4b00-b80c-32bdbab50261"` |

```json Block parent example
{
  "type": "block_id",
  "block_id": "7d50a184-5bbe-4d90-8f29-6bec57ed817b"
}
```

# Here is some tested implementation of the new Notion API in Python

With the recent Notion API update (version `2025-09-03`), the concepts of databases and data sources have been separated. A database now acts as a container for one or more data sources, which hold the actual tables of data. This allows for more complex and interconnected data management within Notion.

To create a new data source, you have two primary options depending on your needs: creating a completely new database with an initial data source, or adding a data source to an existing database.

### Creating a New Database with an Initial Data Source

For most use cases where you want to create a new table of data, you will use the `POST /v1/databases` endpoint. With the `2025-09-03` API version, this endpoint creates both the database container and its first data source in a single call.

The key change in the request body is that the `properties` of the new data source are now nested under an `initial_data_source` object. Other top-level properties in the request, such as `title`, `icon`, and `cover`, apply to the database container itself.

Here is an example of a `POST` request to `/v1/databases` to create a new database with an initial data source for a simple task tracker:

```json
{
  "parent": {
    "type": "page_id",
    "page_id": "YOUR_PAGE_ID"
  },
  "title": [
    {
      "type": "text",
      "text": {
        "content": "My New Task Database"
      }
    }
  ],
  "icon": {
    "type": "emoji",
    "emoji": "🚀"
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
            }
          ]
        }
      },
      "Due Date": {
        "date": {}
      }
    }
  }
}
```

**In this example:**

  * `parent`: Specifies the page where the new database will be created. Replace `"YOUR_PAGE_ID"` with the actual ID of the parent page.
  * `title`: Sets the title of the database container.
  * `icon`: Sets an emoji as the icon for the database.
  * `initial_data_source`: This new object contains the details for the first data source within the database.
      * `title`: Sets the title of the data source itself, which will appear as the tab name in the Notion UI.
      * `properties`: Defines the schema of the data source with three properties:
          * "Task Name": A `title` property, which is a required property for all data sources.
          * "Status": A `select` property with three options for tracking task progress.
          * "Due Date": A `date` property to assign deadlines.

### Adding a Data Source to an Existing Database

If you already have a database and want to add another table of data to it, you can use the `POST /v1/data_sources` endpoint. This is useful for creating multi-source databases.

To use this endpoint, you need the ID of the parent database. The request body will contain the `title` and `properties` for the new data source.

Here is an example of a `POST` request to `/v1/data_sources`:

```json
{
  "database_id": "YOUR_DATABASE_ID",
  "title": [
    {
      "type": "text",
      "text": {
        "content": "Projects"
      }
    }
  ],
  "properties": {
    "Project Name": {
      "title": {}
    },
    "Project Lead": {
      "people": {}
    }
  }
}
```

**In this example:**

  * `database_id`: The ID of the existing database where you want to add the new data source.
  * `title`: The title of the new data source.
  * `properties`: The schema for this new "Projects" data source, including a "Project Name" and a "Project Lead".

By using these updated endpoints and request structures, you can effectively create and manage data sources in line with the latest version of the Notion API.

Of course. Here's the Python code to create a new Notion database with an initial data source using the `requests` library.

This script sends a `POST` request to the `/v1/databases` endpoint. It demonstrates the new structure required for API version `2025-09-03`, where the schema for the first data source is defined within the `initial_data_source` object.

-----

### Python Script to Create a Notion Database

First, make sure you have the `requests` library installed:

```bash
pip install requests
```

Now, you can use the following script. Remember to replace the placeholder values for `NOTION_TOKEN`, and `PARENT_PAGE_ID` with your actual integration token and the ID of the page where you want to create the database.

```python
import requests
import json

# --- Configuration ---
# Replace with your Notion integration token
NOTION_TOKEN = "YOUR_NOTION_INTEGRATION_TOKEN"
# Replace with the ID of the page that will contain your new database
PARENT_PAGE_ID = "YOUR_PARENT_PAGE_ID"

# API endpoint for creating a database
URL = "https://api.notion.com/v1/databases"

# --- Headers ---
# Set up the headers for the API request, including the API version
headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2025-09-03" # Use the new API version
}

# --- Request Body ---
# Define the structure and content of the new database and its initial data source
# The 'properties' for the data source are now nested under 'initial_data_source'
new_database_data = {
    "parent": {
        "type": "page_id",
        "page_id": PARENT_PAGE_ID
    },
    "title": [
        {
            "type": "text",
            "text": {
                "content": "My New Task Database" # Title for the database container
            }
        }
    ],
    "icon": {
        "type": "emoji",
        "emoji": "🚀"
    },
    "initial_data_source": {
        "title": [
            {
                "type": "text",
                "text": {
                    "content": "Tasks" # Title for the data source itself
                }
            }
        ],
        "properties": {
            "Task Name": { # This is the required 'title' property for the pages
                "title": {}
            },
            "Status": { # A 'select' property for tracking status
                "select": {
                    "options": [
                        {"name": "To Do", "color": "gray"},
                        {"name": "In Progress", "color": "blue"},
                        {"name": "Done", "color": "green"}
                    ]
                }
            },
            "Due Date": { # A 'date' property
                "date": {}
            },
            "Priority": { # A 'multi_select' property
                 "multi_select": {
                     "options": [
                         {"name": "High", "color": "red"},
                         {"name": "Medium", "color": "yellow"},
                         {"name": "Low", "color": "green"}
                     ]
                 }
            }
        }
    }
}


def create_notion_database():
    """
    Sends a POST request to the Notion API to create a new database.
    """
    # Convert the Python dictionary to a JSON string
    data_payload = json.dumps(new_database_data)

    print("Sending request to create database...")

    try:
        response = requests.post(URL, headers=headers, data=data_payload)

        # Raise an exception for bad status codes (4xx or 5xx)
        response.raise_for_status()

        print("\n✅ Success! Database created successfully.")
        print("Response JSON:")
        # Pretty-print the JSON response
        print(json.dumps(response.json(), indent=2))

    except requests.exceptions.HTTPError as http_err:
        print(f"\n❌ HTTP error occurred: {http_err}")
        print(f"Status Code: {response.status_code}")
        # Print the error details from the API response
        print(f"Response Body: {response.text}")
    except Exception as err:
        print(f"\n❌ An other error occurred: {err}")

if __name__ == "__main__":
    create_notion_database()
```

-----

### How to Run the Code

1.  **Get your Notion Token**: Go to your [integrations page](https://www.notion.so/my-integrations), create a new integration, and copy the "Internal Integration Secret".
2.  **Share the Parent Page**: The integration must have access to the parent page. Go to the page in Notion, click the "•••" menu, select "Add connections", and choose your integration.
3.  **Find the Parent Page ID**: The ID is the last part of the page's URL (e.g., for `https://www.notion.so/My-Page-_d1f8b4fa38e4_...`, the ID is `d1f8b4fa38e4...`).
4.  **Update the Script**: Paste your token and page ID into the `NOTION_TOKEN` and `PARENT_PAGE_ID` variables.
5.  **Execute**: Run the script from your terminal: `python your_script_name.py`.
6.

Certainly. To add a new page to the data source you just created, you'll use the `POST /v1/pages` endpoint. The key is to set the `parent` of the new page to the **ID of the data source**, which you can get from the response when you create the database.

The `properties` object in your request must match the names and types of the properties you defined in the data source's schema.

-----

### Combined Python Script

Here is a complete script that first creates the database (like before) and then immediately uses the new `data_source_id` to add a page to it.

```python
import requests
import json
import datetime

# --- Configuration ---
# Replace with your Notion integration token
NOTION_TOKEN = "YOUR_NOTION_INTEGRATION_TOKEN"
# Replace with the ID of the page that will contain your new database
PARENT_PAGE_ID = "YOUR_PARENT_PAGE_ID"

# --- API Endpoints and Headers ---
DATABASES_URL = "https://api.notion.com/v1/databases"
PAGES_URL = "https://api.notion.com/v1/pages"

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2025-09-03"
}

def create_notion_database():
    """
    Creates a new database and returns the ID of its initial data source.
    """
    print("Step 1: Creating the database...")

    db_create_data = {
        "parent": {"type": "page_id", "page_id": PARENT_PAGE_ID},
        "title": [{"type": "text", "text": {"content": "My New Task Database"}}],
        "icon": {"type": "emoji", "emoji": "🚀"},
        "initial_data_source": {
            "title": [{"type": "text", "text": {"content": "Tasks"}}],
            "properties": {
                "Task Name": {"title": {}},
                "Status": {
                    "select": {
                        "options": [
                            {"name": "To Do", "color": "gray"},
                            {"name": "In Progress", "color": "blue"},
                            {"name": "Done", "color": "green"}
                        ]
                    }
                },
                "Due Date": {"date": {}},
                "Priority": {
                    "multi_select": {
                        "options": [
                            {"name": "High", "color": "red"},
                            {"name": "Medium", "color": "yellow"},
                            {"name": "Low", "color": "green"}
                        ]
                    }
                }
            }
        }
    }

    try:
        response = requests.post(DATABASES_URL, headers=headers, data=json.dumps(db_create_data))
        response.raise_for_status()
        print("✅ Database created successfully.")

        # Extract the data source ID from the response
        database_response_json = response.json()
        data_source_id = database_response_json.get("data_sources", [{}])[0].get("id")

        if not data_source_id:
            print("❌ Error: Could not find data_source_id in the response.")
            return None

        print(f"Data Source ID: {data_source_id}")
        return data_source_id

    except requests.exceptions.HTTPError as http_err:
        print(f"\n❌ HTTP error occurred while creating database: {http_err}")
        print(f"Response Body: {response.text}")
        return None
    except Exception as err:
        print(f"\n❌ An other error occurred: {err}")
        return None


def add_page_to_datasource(data_source_id):
    """
    Adds a new page to the specified data source.
    """
    print("\nStep 2: Adding a new page to the data source...")

    # Get tomorrow's date in ISO format
    due_date = (datetime.date.today() + datetime.timedelta(days=1)).isoformat()

    new_page_data = {
        # The parent is now the data source
        "parent": { "data_source_id": data_source_id },
        "icon": { "type": "emoji", "emoji": "📝"},
        "properties": {
            # Match the property names and types from the database schema
            "Task Name": {
                "title": [
                    {
                        "text": {
                            "content": "My First Task Page"
                        }
                    }
                ]
            },
            "Status": {
                "select": {
                    "name": "In Progress"
                }
            },
            "Due Date": {
                "date": {
                    "start": due_date
                }
            },
            "Priority": {
                "multi_select": [
                    {"name": "High"}
                ]
            }
        }
    }

    try:
        response = requests.post(PAGES_URL, headers=headers, data=json.dumps(new_page_data))
        response.raise_for_status()
        print("✅ New page added successfully!")
        print(json.dumps(response.json(), indent=2))

    except requests.exceptions.HTTPError as http_err:
        print(f"\n❌ HTTP error occurred while adding page: {http_err}")
        print(f"Response Body: {response.text}")
    except Exception as err:
        print(f"\n❌ An other error occurred: {err}")


if __name__ == "__main__":
    # First, create the database and get the data source ID
    new_data_source_id = create_notion_database()

    # If the database was created successfully, add a page to it
    if new_data_source_id:
        add_page_to_datasource(new_data_source_id)

```

### How It Works

1.  **`create_notion_database()`**: This function is mostly the same as before, but with one key addition. After successfully creating the database, it parses the JSON response to find the ID of the initial data source (`response.json().get("data_sources", [{}])[0].get("id")`) and **returns** it.
2.  **`add_page_to_datasource(data_source_id)`**:
      * This new function takes the `data_source_id` as an argument.
      * It defines a `new_page_data` dictionary for the request body.
      * The **`parent`** object is set to `{"data_source_id": data_source_id}`. This tells Notion to create the page inside our new table.
      * The **`properties`** object contains the data for the new page. Each key (`"Task Name"`, `"Status"`, etc.) must exactly match a property in the data source schema. The value for each property must also be in the correct format (e.g., a `select` property needs an object with a `name` key).
3.  **`if __name__ == "__main__":`**: This main block controls the script's execution. It first calls `create_notion_database()`. If that function returns a valid ID, it then calls `add_page_to_datasource()` and passes that ID to it, linking the two operations together.
4.

To get the content of a page, you need to retrieve the list of block objects that make up the page's body. You can do this by using the `GET /v1/blocks/{page_id}/children` endpoint, which returns all the top-level blocks on that page.

It's important to distinguish between getting a page's **properties** (like its title, status, or due date) and its **content** (the paragraphs, headings, and other blocks on the page).

  * `GET /v1/pages/{page_id}` retrieves the page's properties.
  * `GET /v1/blocks/{page_id}/children` retrieves the page's content blocks.

-----

### Python Script to Get Page Content

This script defines a function that fetches all blocks from a given page, handling pagination automatically. It then includes a simple helper function to parse the raw block data into a more human-readable format.

Replace the placeholder values for `NOTION_TOKEN` and `PAGE_ID` with your information. The `PAGE_ID` should be the ID of the page you added in the previous step.

```python
import requests
import json

# --- Configuration ---
# Replace with your Notion integration token
NOTION_TOKEN = "YOUR_NOTION_INTEGRATION_TOKEN"
# Replace with the ID of the page whose content you want to fetch
PAGE_ID = "YOUR_PAGE_ID"

# --- API Headers ---
headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28" # This endpoint is stable, 2022-06-28 is fine
}

def get_page_content(page_id):
    """
    Fetches all content blocks from a page, handling pagination.
    """
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    all_blocks = []
    has_more = True
    next_cursor = None

    print(f"Fetching content for page: {page_id}...")

    try:
        while has_more:
            # Append start_cursor to URL if it exists
            request_url = url
            if next_cursor:
                request_url = f"{url}?start_cursor={next_cursor}"

            response = requests.get(request_url, headers=headers)
            response.raise_for_status()

            response_data = response.json()
            all_blocks.extend(response_data.get("results", []))

            # Check for more pages of content
            has_more = response_data.get("has_more", False)
            next_cursor = response_data.get("next_cursor", None)

        print("✅ Successfully fetched all content blocks.")
        return all_blocks

    except requests.exceptions.HTTPError as http_err:
        print(f"\n❌ HTTP error occurred: {http_err}")
        print(f"Response Body: {response.text}")
        return None
    except Exception as err:
        print(f"\n❌ An other error occurred: {err}")
        return None

def parse_and_print_content(blocks):
    """
    A simple parser to print the plain text from common block types.
    """
    if not blocks:
        print("No content blocks to parse.")
        return

    print("\n--- Page Content ---")
    for block in blocks:
        block_type = block.get("type")
        # The actual content is nested inside the block_type key
        content = block.get(block_type, {})

        # Extract rich_text which contains the actual text
        rich_text = content.get("rich_text", [])

        # Join the plain_text from all rich_text objects in the block
        plain_text = "".join([text.get("plain_text", "") for text in rich_text])

        if block_type == "heading_1":
            print(f"# {plain_text}")
        elif block_type == "heading_2":
            print(f"## {plain_text}")
        elif block_type == "heading_3":
            print(f"### {plain_text}")
        elif block_type == "paragraph":
            print(f"{plain_text}\n")
        elif block_type == "bulleted_list_item":
            print(f"- {plain_text}")
        elif block_type == "numbered_list_item":
             print(f"1. {plain_text}")
        elif block_type == "to_do":
            is_checked = content.get("checked", False)
            prefix = "[x]" if is_checked else "[ ]"
            print(f"{prefix} {plain_text}")
        elif block_type == "divider":
            print("---")

    print("--- End of Content ---\n")


if __name__ == "__main__":
    # Note: Before running, add some content (headings, paragraphs, etc.)
    # to your new page in the Notion UI so this script has something to fetch.
    content_blocks = get_page_content(PAGE_ID)

    if content_blocks:
        # Optionally, print the raw JSON to see the full structure
        # print("Raw JSON Response:")
        # print(json.dumps(content_blocks, indent=2))

        # Print the parsed, readable content
        parse_and_print_content(content_blocks)
```

-----

### How to Use the Script

1.  **Add Content to Your Page**: Go into Notion and add some content to the page you created with the previous script. Add a few headings, paragraphs, and a to-do list so you can see the parser in action.
2.  **Get the Page ID**: The page ID is the same one you used to add the page. You can also find it in your Notion URL.
3.  **Update and Run**: Paste your `NOTION_TOKEN` and the `PAGE_ID` into the script and run it from your terminal.

The script will first fetch the raw block data from the API and then print a clean, readable version of that content to your console.

Of course. I've updated the script to handle code blocks.

The Notion API returns a `code` block object that contains the programming language and an array of rich text objects for the code itself. The updated parsing function now specifically looks for this block type and formats it for clear display in your terminal.

-----

### Updated Python Script with Code Block Support

This is the complete, updated script. The only changes are within the `parse_and_print_content` function to add the logic for handling code blocks.

````python
import requests
import json

# --- Configuration ---
# Replace with your Notion integration token
NOTION_TOKEN = "YOUR_NOTION_INTEGRATION_TOKEN"
# Replace with the ID of the page whose content you want to fetch
PAGE_ID = "YOUR_PAGE_ID"

# --- API Headers ---
headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def get_page_content(page_id):
    """
    Fetches all content blocks from a page, handling pagination.
    """
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    all_blocks = []
    has_more = True
    next_cursor = None

    print(f"Fetching content for page: {page_id}...")

    try:
        while has_more:
            request_url = url
            if next_cursor:
                request_url = f"{url}?start_cursor={next_cursor}"

            response = requests.get(request_url, headers=headers)
            response.raise_for_status()

            response_data = response.json()
            all_blocks.extend(response_data.get("results", []))

            has_more = response_data.get("has_more", False)
            next_cursor = response_data.get("next_cursor", None)

        print("✅ Successfully fetched all content blocks.")
        return all_blocks

    except requests.exceptions.HTTPError as http_err:
        print(f"\n❌ HTTP error occurred: {http_err}")
        print(f"Response Body: {response.text}")
        return None
    except Exception as err:
        print(f"\n❌ An other error occurred: {err}")
        return None

def parse_and_print_content(blocks):
    """
    Parses and prints the plain text from common block types, now including code blocks.
    """
    if not blocks:
        print("No content blocks to parse.")
        return

    print("\n--- Page Content ---")
    for block in blocks:
        block_type = block.get("type")
        content = block.get(block_type, {})

        rich_text = content.get("rich_text", [])
        plain_text = "".join([text.get("plain_text", "") for text in rich_text])

        if block_type == "heading_1":
            print(f"# {plain_text}")
        elif block_type == "heading_2":
            print(f"## {plain_text}")
        elif block_type == "heading_3":
            print(f"### {plain_text}")
        elif block_type == "paragraph":
            print(f"{plain_text}\n")
        elif block_type == "bulleted_list_item":
            print(f"- {plain_text}")
        elif block_type == "numbered_list_item":
             print(f"1. {plain_text}")
        elif block_type == "to_do":
            is_checked = content.get("checked", False)
            prefix = "[x]" if is_checked else "[ ]"
            print(f"{prefix} {plain_text}")

        # --- NEW: Added logic for code blocks ---
        elif block_type == "code":
            language = content.get("language", "text")
            code_text = plain_text # The plain_text variable already holds the code

            # A code block can also have a caption
            caption_rich_text = content.get("caption", [])
            caption_text = "".join([text.get("plain_text", "") for text in caption_rich_text])

            print(f"``` {language}")
            print(code_text)
            print("```")
            if caption_text:
                print(f"Caption: {caption_text}\n")
            else:
                print() # Add a newline for spacing

        elif block_type == "divider":
            print("---")

    print("--- End of Content ---\n")


if __name__ == "__main__":
    # Note: Before running, add a code block to your page in the Notion UI
    # to test this new functionality.
    content_blocks = get_page_content(PAGE_ID)

    if content_blocks:
        parse_and_print_content(content_blocks)
````

-----

### How to Test the Changes

1.  **Add a Code Block in Notion**: Go to the Notion page you're testing with and add a new code block. You can do this by typing `/code` and pressing enter. Paste some code into it and select a language from the dropdown (e.g., Python). You can also add an optional caption.
2.  **Update Your Script**: Replace the existing `parse_and_print_content` function with the new version above.
3.  **Run the Script**: Execute the Python file. The output in your terminal will now format and display the code block you added, including its language.


# Here is some specific information about ENDPOINTS

# Create a database

Create a database and its initial data source.

Creates a database as a subpage in the specified parent page, or as a private page at the workspace level, with the specified `properties` schema set on its `initial_data_source`. Currently, the `parent` of a new database must be a Notion page (`page_id` type) or a [wiki database](https://www.notion.so/help/wikis-and-verified-pages).

Use this endpoint to create a database, its first [data source](ref:data-source), and its first table view, all in one API call. Then, if you want to add a second data source, use the [Create a data source](ref:create-a-data-source) API with a version of at least `2025-09-03`, and provide the `database_id` as the `id` returned by the database create response.

For a complete reference on what properties are available, see [Data source properties](ref:property-object). After creating the database, to update one of its child data sources' properties, use the [Update a data source](ref:update-a-data-source) API.

> 📘 Integration capabilities
>
> This endpoint requires an integration to have insert content capabilities. Attempting to call this API without insert content capabilities will return an HTTP response with a 403 status code. For more information on integration capabilities, see the [capabilities guide](ref:capabilities).

> 🚧 Limitations
>
> Creating new `status` database properties is currently not supported.

### Errors

Returns a 404 if the specified parent page does not exist, or if the integration does not have access to the parent page.

Returns a 400 if the request is incorrectly formatted, or a 429 HTTP response if the request exceeds the [request limits](ref:request-limits).

_Note: Each Public API endpoint can return several possible error codes. See the [Error codes section](https://developers.notion.com/reference/status-codes#error-codes) of the Status codes documentation for more information._

# OpenAPI definition
```json
{
  "openapi": "3.1.0",
  "info": {
    "title": "Notion API",
    "version": "1"
  },
  "servers": [
    {
      "url": "https://api.notion.com"
    }
  ],
  "components": {
    "securitySchemes": {
      "sec0": {
        "type": "oauth2",
        "flows": {}
      }
    }
  },
  "security": [
    {
      "sec0": []
    }
  ],
  "paths": {
    "/v1/databases": {
      "post": {
        "summary": "Create a database",
        "description": "Create a database and its initial data source.",
        "operationId": "database-create",
        "parameters": [
          {
            "name": "Notion-Version",
            "in": "header",
            "description": "The [API version](/reference/versioning) to use for this request. The latest version is `2025-09-03`.",
            "required": true,
            "schema": {
              "type": "string"
            }
          }
        ],
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "required": [
                  "parent"
                ],
                "properties": {
                  "parent": {
                    "type": "object",
                    "description": "The parent page or workspace where the database will be created.",
                    "required": [
                      "type"
                    ],
                    "properties": {
                      "type": {
                        "type": "string",
                        "description": "The type of parent under which to create the database. Either \"page_id\" or \"workspace\".",
                        "enum": [
                          "\"page_id\"",
                          "\"workspace\""
                        ]
                      },
                      "page_id": {
                        "type": "string",
                        "description": "ID of the new database's parent page, when `type=page_id`. This is a UUIDv4, with or without dashes."
                      },
                      "workspace": {
                        "type": "string",
                        "description": "Always `true` when `type=workspace`.",
                        "enum": [
                          "true"
                        ]
                      }
                    }
                  },
                  "initial_data_source": {
                    "type": "object",
                    "description": "Initial data source configuration for the database.",
                    "properties": {
                      "properties": {
                        "type": "object",
                        "description": "The properties to apply to the database's initial data source.",
                        "properties": {
                          "<propertyIdentifier>": {
                            "type": "object",
                            "description": "Hash map of strings (property identifiers) corresponding to the configuration of each property. The `type` of each property can be omitted, but you must provide a sub-object whose parameter name matches the type, even if it's an empty object. For example, {\"type\": \"date\", \"date\": {}} and {\"date\": {}} are both valid values, but {\"type\": \"date\"}` is not.",
                            "properties": {
                              "description": {
                                "type": "string",
                                "description": "The property's description (optional)."
                              },
                              "type": {
                                "type": "string",
                                "description": "The type of property.",
                                "enum": [
                                  "\"number\"",
                                  "\"formula\"",
                                  "\"select\"",
                                  "\"multi_select\"",
                                  "\"status\"",
                                  "\"relation\"",
                                  "\"rollup\"",
                                  "\"unique_id\"",
                                  "\"title\"",
                                  "\"rich_text\"",
                                  "\"url\"",
                                  "\"people\"",
                                  "\"files\"",
                                  "\"email\"",
                                  "\"phone_number\"",
                                  "\"date\"",
                                  "\"checkbox\"",
                                  "\"created_by\"",
                                  "\"created_time\"",
                                  "\"last_edited_by\"",
                                  "\"last_edited_time\"",
                                  "\"button\"",
                                  "\"location\"",
                                  "\"verification\"",
                                  "\"last_visited_time\"",
                                  "\"place\""
                                ]
                              },
                              "number": {
                                "type": "object",
                                "properties": {
                                  "format": {
                                    "type": "string",
                                    "description": "The format of the number property.",
                                    "enum": [
                                      "\"number\"",
                                      "\"number_with_commas\"",
                                      "\"percent\"",
                                      "\"dollar\"",
                                      "\"australian_dollar\"",
                                      "\"canadian_dollar\"",
                                      "\"singapore_dollar\"",
                                      "\"euro\"",
                                      "\"pound\"",
                                      "\"yen\"",
                                      "\"ruble\"",
                                      "\"rupee\"",
                                      "\"won\"",
                                      "\"yuan\"",
                                      "\"real\"",
                                      "\"lira\"",
                                      "\"rupiah\"",
                                      "\"franc\"",
                                      "\"hong_kong_dollar\"",
                                      "\"new_zealand_dollar\"",
                                      "\"krona\"",
                                      "\"norwegian_krone\"",
                                      "\"mexican_peso\"",
                                      "\"rand\"",
                                      "\"new_taiwan_dollar\"",
                                      "\"danish_krone\"",
                                      "\"zloty\"",
                                      "\"baht\"",
                                      "\"forint\"",
                                      "\"koruna\"",
                                      "\"shekel\"",
                                      "\"chilean_peso\"",
                                      "\"philippine_peso\"",
                                      "\"dirham\"",
                                      "\"colombian_peso\"",
                                      "\"riyal\"",
                                      "\"ringgit\"",
                                      "\"leu\"",
                                      "\"argentine_peso\"",
                                      "\"uruguayan_peso\"",
                                      "\"peruvian_sol\"",
                                      ""
                                    ]
                                  }
                                }
                              },
                              "formula": {
                                "type": "object",
                                "properties": {
                                  "expression": {
                                    "type": "string",
                                    "description": "A valid Notion formula expression."
                                  }
                                }
                              },
                              "select": {
                                "type": "object",
                                "properties": {
                                  "options": {
                                    "type": "array",
                                    "items": {
                                      "properties": {
                                        "color": {
                                          "type": "string",
                                          "enum": [
                                            "\"default\"",
                                            "\"gray\"",
                                            "\"brown\"",
                                            "\"orange\"",
                                            "\"yellow\"",
                                            "\"green\"",
                                            "\"blue\"",
                                            "\"purple\"",
                                            "\"pink\"",
                                            "\"red\"",
                                            ""
                                          ]
                                        },
                                        "description": {
                                          "type": "string"
                                        }
                                      },
                                      "type": "object"
                                    }
                                  }
                                }
                              },
                              "multi_select": {
                                "type": "object",
                                "properties": {
                                  "color": {
                                    "type": "string",
                                    "enum": [
                                      "\"default\"",
                                      "\"gray\"",
                                      "\"brown\"",
                                      "\"orange\"",
                                      "\"yellow\"",
                                      "\"green\"",
                                      "\"blue\"",
                                      "\"purple\"",
                                      "\"pink\"",
                                      "\"red\"",
                                      ""
                                    ]
                                  },
                                  "description": {
                                    "type": "string"
                                  }
                                }
                              },
                              "relation": {
                                "type": "object",
                                "properties": {
                                  "type": {
                                    "type": "string",
                                    "enum": [
                                      "\"single_property\"",
                                      "\"dual_property\""
                                    ]
                                  },
                                  "single_property": {
                                    "type": "object",
                                    "description": "An empty object `{}`.",
                                    "properties": {}
                                  },
                                  "dual_property": {
                                    "type": "object",
                                    "properties": {
                                      "synced_property_id": {
                                        "type": "string"
                                      },
                                      "synced_property_name": {
                                        "type": "string"
                                      }
                                    }
                                  }
                                }
                              },
                              "rollup": {
                                "type": "object",
                                "required": [
                                  "function"
                                ],
                                "properties": {
                                  "function": {
                                    "type": "string",
                                    "enum": [
                                      "\"count\"",
                                      "\"count_values\"",
                                      "\"empty\"",
                                      "\"not_empty\"",
                                      "\"unique\"",
                                      "\"show_unique\"",
                                      "\"percent_empty\"",
                                      "\"percent_not_empty\"",
                                      "\"sum\"",
                                      "\"average\"",
                                      "\"median\"",
                                      "\"min\"",
                                      "\"max\"",
                                      "\"range\"",
                                      "\"earliest_date\"",
                                      "\"latest_date\"",
                                      "\"date_range\"",
                                      "\"checked\"",
                                      "\"unchecked\"",
                                      "\"percent_checked\"",
                                      "\"percent_unchecked\"",
                                      "\"count_per_group\"",
                                      "\"percent_per_group\"",
                                      "\"show_original\""
                                    ]
                                  },
                                  "relation_property_name": {
                                    "type": "string"
                                  },
                                  "relation_property_id": {
                                    "type": "string"
                                  },
                                  "rollup_property_name": {
                                    "type": "string"
                                  },
                                  "rollup_property_id": {
                                    "type": "string"
                                  }
                                }
                              },
                              "unique_id": {
                                "type": "object",
                                "properties": {
                                  "prefix": {
                                    "type": "string"
                                  }
                                }
                              }
                            }
                          }
                        }
                      }
                    }
                  },
                  "title": {
                    "type": "array",
                    "description": "The title of the database.",
                    "items": {
                      "properties": {
                        "annotations": {
                          "type": "object",
                          "description": "The styling for the rich text.",
                          "properties": {
                            "bold": {
                              "type": "boolean",
                              "description": "Whether the text is formatted as bold.",
                              "default": false
                            },
                            "italic": {
                              "type": "boolean",
                              "description": "Whether the text is formatted as italic.",
                              "default": false
                            },
                            "strikethrough": {
                              "type": "boolean",
                              "description": "Whether the text is formatted with a strikethrough.",
                              "default": false
                            },
                            "underline": {
                              "type": "boolean",
                              "description": "Whether the text is formatted with an underline.",
                              "default": false
                            },
                            "code": {
                              "type": "boolean",
                              "description": "Whether the text is formatted as code.",
                              "default": false
                            },
                            "color": {
                              "type": "string",
                              "description": "The color of the text.",
                              "default": "\"default\"",
                              "enum": [
                                "\"default\"",
                                "\"gray\"",
                                "\"brown\"",
                                "\"orange\"",
                                "\"yellow\"",
                                "\"green\"",
                                "\"blue\"",
                                "\"purple\"",
                                "\"pink\"",
                                "\"red\"",
                                "\"default_background\"",
                                "\"gray_background\"",
                                "\"brown_background\"",
                                "\"orange_background\"",
                                "\"yellow_background\"",
                                "\"green_background\"",
                                "\"blue_background\"",
                                "\"purple_background\"",
                                "\"pink_background\"",
                                "\"red_background\""
                              ]
                            }
                          }
                        },
                        "plain_text": {
                          "type": "string",
                          "description": "The plain text content of the rich text object, without any styling."
                        },
                        "href": {
                          "type": "string",
                          "description": "A URL that the rich text object links to or mentions."
                        },
                        "type": {
                          "type": "string",
                          "enum": [
                            "\"text\"",
                            "\"mention\"",
                            "\"equation\""
                          ]
                        }
                      },
                      "type": "object"
                    }
                  },
                  "description": {
                    "type": "array",
                    "description": "The description of the database.",
                    "items": {
                      "properties": {
                        "annotations": {
                          "type": "object",
                          "description": "The styling for the rich text.",
                          "properties": {
                            "bold": {
                              "type": "boolean",
                              "description": "Whether the text is formatted as bold.",
                              "default": false
                            },
                            "italic": {
                              "type": "boolean",
                              "description": "Whether the text is formatted as italic.",
                              "default": false
                            },
                            "strikethrough": {
                              "type": "boolean",
                              "description": "Whether the text is formatted with a strikethrough.",
                              "default": false
                            },
                            "underline": {
                              "type": "boolean",
                              "description": "Whether the text is formatted with an underline.",
                              "default": false
                            },
                            "code": {
                              "type": "boolean",
                              "description": "Whether the text is formatted as code.",
                              "default": false
                            },
                            "color": {
                              "type": "string",
                              "description": "The color of the text.",
                              "default": "\"default\"",
                              "enum": [
                                "\"default\"",
                                "\"gray\"",
                                "\"brown\"",
                                "\"orange\"",
                                "\"yellow\"",
                                "\"green\"",
                                "\"blue\"",
                                "\"purple\"",
                                "\"pink\"",
                                "\"red\"",
                                "\"default_background\"",
                                "\"gray_background\"",
                                "\"brown_background\"",
                                "\"orange_background\"",
                                "\"yellow_background\"",
                                "\"green_background\"",
                                "\"blue_background\"",
                                "\"purple_background\"",
                                "\"pink_background\"",
                                "\"red_background\""
                              ]
                            }
                          }
                        },
                        "plain_text": {
                          "type": "string",
                          "description": "The plain text content of the rich text object, without any styling."
                        },
                        "href": {
                          "type": "string",
                          "description": "A URL that the rich text object links to or mentions."
                        },
                        "type": {
                          "type": "string",
                          "enum": [
                            "\"text\"",
                            "\"mention\"",
                            "\"equation\""
                          ]
                        }
                      },
                      "type": "object"
                    }
                  },
                  "icon": {
                    "type": "object",
                    "description": "The icon for the database.",
                    "properties": {
                      "type": {
                        "type": "string",
                        "description": "The type of icon parameter being provided.",
                        "enum": [
                          "\"file_upload\"",
                          "\"emoji\"",
                          "\"external\"",
                          "\"custom_emoji\""
                        ]
                      },
                      "emoji": {
                        "type": "string",
                        "description": "When `type=emoji`, an emoji character."
                      },
                      "file_upload": {
                        "type": "object",
                        "description": "When `type=file_upload`, an object containing the `id` of the File Upload.",
                        "required": [
                          "id"
                        ],
                        "properties": {
                          "id": {
                            "type": "string",
                            "description": "ID of a FileUpload object that has the status `uploaded`."
                          }
                        }
                      },
                      "external": {
                        "type": "object",
                        "description": "When `type=external`, an object containing the external URL.",
                        "required": [
                          "url"
                        ],
                        "properties": {
                          "url": {
                            "type": "string",
                            "description": "The URL of the external file."
                          }
                        }
                      },
                      "custom_emoji": {
                        "type": "object",
                        "description": "When `type=custom_emoji`, an object containing the custom emoji.",
                        "required": [
                          "id"
                        ],
                        "properties": {
                          "id": {
                            "type": "string",
                            "description": "The ID of the custom emoji."
                          },
                          "name": {
                            "type": "string",
                            "description": "The name of the custom emoji."
                          },
                          "url": {
                            "type": "string",
                            "description": "The URL of the custom emoji."
                          }
                        }
                      }
                    }
                  },
                  "cover": {
                    "type": "object",
                    "description": "The cover image for the database.",
                    "properties": {
                      "type": {
                        "type": "string",
                        "description": "The type of cover being provided.",
                        "enum": [
                          "\"file_upload\"",
                          "\"external\""
                        ]
                      },
                      "file_upload": {
                        "type": "object",
                        "description": "When `type=file_upload`, this is an object containing the ID of the File Upload.",
                        "required": [
                          "id"
                        ],
                        "properties": {
                          "id": {
                            "type": "string",
                            "description": "ID of a FileUpload object that has the status `uploaded`."
                          }
                        }
                      },
                      "external": {
                        "type": "object",
                        "description": "When `type=external`, this is an object containing the external URL for the cover.",
                        "required": [
                          "url"
                        ],
                        "properties": {
                          "url": {
                            "type": "string",
                            "description": "The URL of the external file."
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "200",
            "content": {
              "application/json": {
                "examples": {
                  "Result": {
                    "value": "{\n\t\"object\": \"database\",\n\t\"id\": \"248104cd-477e-80fd-b757-e945d38000bd\",\n\t\"title\": [\n\t\t{\n\t\t\t\"type\": \"text\",\n\t\t\t\"text\": {\n\t\t\t\t\"content\": \"My Task Tracker\",\n\t\t\t\t\"link\": null\n\t\t\t},\n\t\t\t\"annotations\": {\n\t\t\t\t\"bold\": false,\n\t\t\t\t\"italic\": false,\n\t\t\t\t\"strikethrough\": false,\n\t\t\t\t\"underline\": false,\n\t\t\t\t\"code\": false,\n\t\t\t\t\"color\": \"default\"\n\t\t\t},\n\t\t\t\"plain_text\": \"My Task Tracker\",\n\t\t\t\"href\": null\n\t\t}\n\t],\n\t\"parent\": {\n\t\t\"type\": \"page_id\",\n\t\t\"page_id\": \"255104cd-477e-808c-b279-d39ab803a7d2\"\n\t},\n\t\"is_inline\": false,\n\t\"in_trash\": false,\n\t\"created_time\": \"2025-08-07T10:11:07.504-07:00\",\n\t\"last_edited_time\": \"2025-08-10T15:53:11.386-07:00\",\n\t\"data_sources\": [\n\t\t{\n\t\t\t\"id\": \"248104cd-477e-80af-bc30-000bd28de8f9\",\n\t\t\t\"name\": \"My Task Tracker\"\n\t\t}\n\t],\n\t\"icon\": null,\n\t\"cover\": null,\n\t\"developer_survey\": \"https://example.com/xyz\",\n\t\"request_id\": \"2f788b44-abf3-4809-aa4c-dd40734fed0b\"\n}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "object": {
                      "type": "string",
                      "example": "database"
                    },
                    "id": {
                      "type": "string",
                      "example": "248104cd-477e-80fd-b757-e945d38000bd"
                    },
                    "title": {
                      "type": "array",
                      "items": {
                        "type": "object",
                        "properties": {
                          "type": {
                            "type": "string",
                            "example": "text"
                          },
                          "text": {
                            "type": "object",
                            "properties": {
                              "content": {
                                "type": "string",
                                "example": "My Task Tracker"
                              },
                              "link": {}
                            }
                          },
                          "annotations": {
                            "type": "object",
                            "properties": {
                              "bold": {
                                "type": "boolean",
                                "example": false,
                                "default": true
                              },
                              "italic": {
                                "type": "boolean",
                                "example": false,
                                "default": true
                              },
                              "strikethrough": {
                                "type": "boolean",
                                "example": false,
                                "default": true
                              },
                              "underline": {
                                "type": "boolean",
                                "example": false,
                                "default": true
                              },
                              "code": {
                                "type": "boolean",
                                "example": false,
                                "default": true
                              },
                              "color": {
                                "type": "string",
                                "example": "default"
                              }
                            }
                          },
                          "plain_text": {
                            "type": "string",
                            "example": "My Task Tracker"
                          },
                          "href": {}
                        }
                      }
                    },
                    "parent": {
                      "type": "object",
                      "properties": {
                        "type": {
                          "type": "string",
                          "example": "page_id"
                        },
                        "page_id": {
                          "type": "string",
                          "example": "255104cd-477e-808c-b279-d39ab803a7d2"
                        }
                      }
                    },
                    "is_inline": {
                      "type": "boolean",
                      "example": false,
                      "default": true
                    },
                    "in_trash": {
                      "type": "boolean",
                      "example": false,
                      "default": true
                    },
                    "created_time": {
                      "type": "string",
                      "example": "2025-08-07T10:11:07.504-07:00"
                    },
                    "last_edited_time": {
                      "type": "string",
                      "example": "2025-08-10T15:53:11.386-07:00"
                    },
                    "data_sources": {
                      "type": "array",
                      "items": {
                        "type": "object",
                        "properties": {
                          "id": {
                            "type": "string",
                            "example": "248104cd-477e-80af-bc30-000bd28de8f9"
                          },
                          "name": {
                            "type": "string",
                            "example": "My Task Tracker"
                          }
                        }
                      }
                    },
                    "icon": {},
                    "cover": {},
                    "developer_survey": {
                      "type": "string",
                      "example": "https://example.com/xyz"
                    },
                    "request_id": {
                      "type": "string",
                      "example": "2f788b44-abf3-4809-aa4c-dd40734fed0b"
                    }
                  }
                }
              }
            }
          },
          "400": {
            "description": "400",
            "content": {
              "application/json": {
                "examples": {
                  "Result": {
                    "value": "{}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {}
                }
              }
            }
          }
        },
        "deprecated": false,
        "security": []
      }
    }
  },
  "x-readme": {
    "headers": [],
    "explorer-enabled": false,
    "proxy-enabled": true
  },
  "x-readme-fauxas": true,
  "_id": "606ecc2cd9e93b0044cf6e47:68b0cf40c22c6762073b47da"
}
```

# Update a database

Updates the attributes — the title, description, icon, or cover, etc. — of a specified database.

Returns the updated [database object](ref:database).

To update the `properties` of the [data sources](ref:data-source) under a database, use the [Update a data source](ref:update-a-data-source) API starting from API version `2025-09-03`.

For an overview of how to use the REST API with databases, refer to the [Working with databases](https://developers.notion.com/docs/working-with-databases) guide.

Each Public API endpoint can return several possible error codes. See the [Error codes section](https://developers.notion.com/reference/status-codes#error-codes) of the Status codes documentation for more information.

# OpenAPI definition
```json
{
  "openapi": "3.1.0",
  "info": {
    "title": "Notion API",
    "version": "1"
  },
  "servers": [
    {
      "url": "https://api.notion.com"
    }
  ],
  "components": {
    "securitySchemes": {
      "sec0": {
        "type": "oauth2",
        "flows": {}
      }
    }
  },
  "security": [
    {
      "sec0": []
    }
  ],
  "paths": {
    "/v1/databases/{database_id}": {
      "patch": {
        "summary": "Update a database",
        "description": "",
        "operationId": "database-update",
        "parameters": [
          {
            "name": "Notion-Version",
            "in": "header",
            "description": "The [API version](/reference/versioning) to use for this request. The latest version is `<<internalLatestNotionVersion>>`.",
            "required": true,
            "schema": {
              "type": "string"
            }
          },
          {
            "name": "database_id",
            "in": "path",
            "description": "ID of a Notion database, a container for one or more data sources. This is a UUIDv4, with or without dashes.",
            "schema": {
              "type": "string"
            },
            "required": true
          }
        ],
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "parent": {
                    "type": "object",
                    "description": "The parent page or workspace to move the database to. If not provided, the database will not be moved.",
                    "required": [
                      "type"
                    ],
                    "properties": {
                      "type": {
                        "type": "string",
                        "description": "The type of parent under which to create the database. Either \"page_id\" or \"workspace\".",
                        "enum": [
                          "\"page_id\"",
                          "\"workspace\""
                        ]
                      },
                      "page_id": {
                        "type": "string",
                        "description": "ID of the new database's parent page, when `type=page_id`. This is a UUIDv4, with or without dashes."
                      },
                      "workspace": {
                        "type": "string",
                        "description": "Always `true` when `type=workspace`.",
                        "enum": [
                          "true"
                        ]
                      }
                    }
                  },
                  "title": {
                    "type": "array",
                    "description": "The updated title of the database, if any. If not provided, the title will not be updated.",
                    "items": {
                      "properties": {
                        "annotations": {
                          "type": "object",
                          "description": "The styling for the rich text.",
                          "properties": {
                            "bold": {
                              "type": "boolean",
                              "description": "Whether the text is formatted as bold.",
                              "default": false
                            },
                            "italic": {
                              "type": "boolean",
                              "description": "Whether the text is formatted as italic.",
                              "default": false
                            },
                            "strikethrough": {
                              "type": "boolean",
                              "description": "Whether the text is formatted with a strikethrough.",
                              "default": false
                            },
                            "underline": {
                              "type": "boolean",
                              "description": "Whether the text is formatted with an underline.",
                              "default": false
                            },
                            "code": {
                              "type": "boolean",
                              "description": "Whether the text is formatted as code.",
                              "default": false
                            },
                            "color": {
                              "type": "string",
                              "description": "The color of the text.",
                              "default": "\"default\"",
                              "enum": [
                                "\"default\"",
                                "\"gray\"",
                                "\"brown\"",
                                "\"orange\"",
                                "\"yellow\"",
                                "\"green\"",
                                "\"blue\"",
                                "\"purple\"",
                                "\"pink\"",
                                "\"red\"",
                                "\"default_background\"",
                                "\"gray_background\"",
                                "\"brown_background\"",
                                "\"orange_background\"",
                                "\"yellow_background\"",
                                "\"green_background\"",
                                "\"blue_background\"",
                                "\"purple_background\"",
                                "\"pink_background\"",
                                "\"red_background\""
                              ]
                            }
                          }
                        },
                        "plain_text": {
                          "type": "string",
                          "description": "The plain text content of the rich text object, without any styling."
                        },
                        "href": {
                          "type": "string",
                          "description": "A URL that the rich text object links to or mentions."
                        },
                        "type": {
                          "type": "string",
                          "enum": [
                            "\"text\"",
                            "\"mention\"",
                            "\"equation\""
                          ]
                        }
                      },
                      "type": "object"
                    }
                  },
                  "is_inline": {
                    "type": "boolean",
                    "description": "Whether the database should be displayed inline in the parent page. If not provided, the inline status will not be updated."
                  },
                  "icon": {
                    "type": "object",
                    "description": "The updated icon for the database, if any. If not provided, the icon will not be updated.",
                    "properties": {
                      "type": {
                        "type": "string",
                        "description": "The type of icon parameter being provided.",
                        "enum": [
                          "\"file_upload\"",
                          "\"emoji\"",
                          "\"external\"",
                          "\"custom_emoji\""
                        ]
                      },
                      "emoji": {
                        "type": "string",
                        "description": "When `type=emoji`, an emoji character."
                      },
                      "file_upload": {
                        "type": "object",
                        "description": "When `type=file_upload`, an object containing the `id` of the File Upload.",
                        "required": [
                          "id"
                        ],
                        "properties": {
                          "id": {
                            "type": "string",
                            "description": "ID of a FileUpload object that has the status `uploaded`."
                          }
                        }
                      },
                      "external": {
                        "type": "object",
                        "description": "When `type=external`, an object containing the external URL.",
                        "required": [
                          "url"
                        ],
                        "properties": {
                          "url": {
                            "type": "string",
                            "description": "The URL of the external file."
                          }
                        }
                      },
                      "custom_emoji": {
                        "type": "object",
                        "description": "When `type=custom_emoji`, an object containing the custom emoji.",
                        "required": [
                          "id"
                        ],
                        "properties": {
                          "id": {
                            "type": "string",
                            "description": "The ID of the custom emoji."
                          },
                          "name": {
                            "type": "string",
                            "description": "The name of the custom emoji."
                          },
                          "url": {
                            "type": "string",
                            "description": "The URL of the custom emoji."
                          }
                        }
                      }
                    }
                  },
                  "cover": {
                    "type": "object",
                    "description": "The updated cover image for the database, if any. If not provided, the cover will not be updated.",
                    "properties": {
                      "type": {
                        "type": "string",
                        "description": "The type of cover being provided.",
                        "enum": [
                          "\"file_upload\"",
                          "\"external\""
                        ]
                      },
                      "file_upload": {
                        "type": "object",
                        "description": "When `type=file_upload`, this is an object containing the ID of the File Upload.",
                        "required": [
                          "id"
                        ],
                        "properties": {
                          "id": {
                            "type": "string",
                            "description": "ID of a FileUpload object that has the status `uploaded`."
                          }
                        }
                      },
                      "external": {
                        "type": "object",
                        "description": "When `type=external`, this is an object containing the external URL for the cover.",
                        "required": [
                          "url"
                        ],
                        "properties": {
                          "url": {
                            "type": "string",
                            "description": "The URL of the external file."
                          }
                        }
                      }
                    }
                  },
                  "in_trash": {
                    "type": "boolean",
                    "description": "Whether the database should be moved to or from the trash. If not provided, the trash status will not be updated."
                  },
                  "is_locked": {
                    "type": "boolean",
                    "description": "Whether the database should be locked from editing in the Notion app UI. If not provided, the locked state will not be updated."
                  }
                }
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "200",
            "content": {
              "application/json": {
                "examples": {
                  "Result": {
                    "value": "{\n\t\"object\": \"database\",\n\t\"id\": \"248104cd-477e-80fd-b757-e945d38000bd\",\n\t\"title\": [\n\t\t{\n\t\t\t\"type\": \"text\",\n\t\t\t\"text\": {\n\t\t\t\t\"content\": \"My Task Tracker\",\n\t\t\t\t\"link\": null\n\t\t\t},\n\t\t\t\"annotations\": {\n\t\t\t\t\"bold\": false,\n\t\t\t\t\"italic\": false,\n\t\t\t\t\"strikethrough\": false,\n\t\t\t\t\"underline\": false,\n\t\t\t\t\"code\": false,\n\t\t\t\t\"color\": \"default\"\n\t\t\t},\n\t\t\t\"plain_text\": \"My Task Tracker\",\n\t\t\t\"href\": null\n\t\t}\n\t],\n\t\"parent\": {\n\t\t\"type\": \"page_id\",\n\t\t\"page_id\": \"255104cd-477e-808c-b279-d39ab803a7d2\"\n\t},\n\t\"is_inline\": false,\n  \"in_trash\": false,\n  \"is_locked\": false,\n\t\"created_time\": \"2025-08-07T10:11:07.504-07:00\",\n\t\"last_edited_time\": \"2025-08-10T15:53:11.386-07:00\",\n\t\"data_sources\": [\n\t\t{\n\t\t\t\"id\": \"248104cd-477e-80af-bc30-000bd28de8f9\",\n\t\t\t\"name\": \"My Task Tracker\"\n\t\t}\n\t],\n\t\"icon\": null,\n\t\"cover\": null,\n\t\"developer_survey\": \"https://example.com/xyz\",\n\t\"request_id\": \"2f788b44-abf3-4809-aa4c-dd40734fed0b\"\n}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "object": {
                      "type": "string",
                      "example": "database"
                    },
                    "id": {
                      "type": "string",
                      "example": "248104cd-477e-80fd-b757-e945d38000bd"
                    },
                    "title": {
                      "type": "array",
                      "items": {
                        "type": "object",
                        "properties": {
                          "type": {
                            "type": "string",
                            "example": "text"
                          },
                          "text": {
                            "type": "object",
                            "properties": {
                              "content": {
                                "type": "string",
                                "example": "My Task Tracker"
                              },
                              "link": {}
                            }
                          },
                          "annotations": {
                            "type": "object",
                            "properties": {
                              "bold": {
                                "type": "boolean",
                                "example": false,
                                "default": true
                              },
                              "italic": {
                                "type": "boolean",
                                "example": false,
                                "default": true
                              },
                              "strikethrough": {
                                "type": "boolean",
                                "example": false,
                                "default": true
                              },
                              "underline": {
                                "type": "boolean",
                                "example": false,
                                "default": true
                              },
                              "code": {
                                "type": "boolean",
                                "example": false,
                                "default": true
                              },
                              "color": {
                                "type": "string",
                                "example": "default"
                              }
                            }
                          },
                          "plain_text": {
                            "type": "string",
                            "example": "My Task Tracker"
                          },
                          "href": {}
                        }
                      }
                    },
                    "parent": {
                      "type": "object",
                      "properties": {
                        "type": {
                          "type": "string",
                          "example": "page_id"
                        },
                        "page_id": {
                          "type": "string",
                          "example": "255104cd-477e-808c-b279-d39ab803a7d2"
                        }
                      }
                    },
                    "is_inline": {
                      "type": "boolean",
                      "example": false,
                      "default": true
                    },
                    "in_trash": {
                      "type": "boolean",
                      "example": false,
                      "default": true
                    },
                    "is_locked": {
                      "type": "boolean",
                      "example": false,
                      "default": true
                    },
                    "created_time": {
                      "type": "string",
                      "example": "2025-08-07T10:11:07.504-07:00"
                    },
                    "last_edited_time": {
                      "type": "string",
                      "example": "2025-08-10T15:53:11.386-07:00"
                    },
                    "data_sources": {
                      "type": "array",
                      "items": {
                        "type": "object",
                        "properties": {
                          "id": {
                            "type": "string",
                            "example": "248104cd-477e-80af-bc30-000bd28de8f9"
                          },
                          "name": {
                            "type": "string",
                            "example": "My Task Tracker"
                          }
                        }
                      }
                    },
                    "icon": {},
                    "cover": {},
                    "developer_survey": {
                      "type": "string",
                      "example": "https://example.com/xyz"
                    },
                    "request_id": {
                      "type": "string",
                      "example": "2f788b44-abf3-4809-aa4c-dd40734fed0b"
                    }
                  }
                }
              }
            }
          },
          "400": {
            "description": "400",
            "content": {
              "application/json": {
                "examples": {
                  "Result": {
                    "value": "{}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {}
                }
              }
            }
          }
        },
        "deprecated": false,
        "security": []
      }
    }
  },
  "x-readme": {
    "headers": [],
    "explorer-enabled": false,
    "proxy-enabled": true
  },
  "x-readme-fauxas": true,
  "_id": "606ecc2cd9e93b0044cf6e47:68b1ec171f568af9d48cf70c"
}
```

# Retrieve a database

Retrieves a [database object](ref:database) — a container for one or more [data sources](ref:data-source) — for a provided database ID. The response adheres to any limits to an integration’s capabilities.

The most important fields in the database object response to highlight:

- `data_sources`: An array of JSON objects with the `id` and `name` of every data source under the database
  - These data source IDs can be used with the [Retrieve a data source](ref:retrieve-a-data-source), [Update a data source](ref:update-a-data-source), and [Query a data source](ref:query-a-data-source) APIs
- `parent`: The direct parent of the database; generally a `page_id` or `workspace: true`

To find a database ID, navigate to the database URL in your Notion workspace. The ID is the string of characters in the URL that is between the slash following the workspace name (if applicable) and the question mark. The ID is a 32 characters alphanumeric string.

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/64967fd-small-62e5027-notion_database_id.png",
        null,
        "Notion database ID"
      ],
      "align": "center",
      "caption": "Notion database ID"
    }
  ]
}
[/block]


Refer to the [Build your first integration guide](https://developers.notion.com/docs/create-a-notion-integration#step-3-save-the-database-id) for more details.

### Errors

Each Public API endpoint can return several possible error codes. See the [Error codes section](https://developers.notion.com/reference/status-codes#error-codes) of the Status codes documentation for more information.

### Additional resources

- [How to share a database with your integration](https://developers.notion.com/docs/create-a-notion-integration#give-your-integration-page-permissions)
- [Working with databases guide](https://developers.notion.com/docs/working-with-databases)

# OpenAPI definition
```json
{
  "openapi": "3.1.0",
  "info": {
    "title": "Notion API",
    "version": "1"
  },
  "servers": [
    {
      "url": "https://api.notion.com"
    }
  ],
  "components": {
    "securitySchemes": {
      "sec0": {
        "type": "oauth2",
        "flows": {}
      }
    }
  },
  "security": [
    {
      "sec0": []
    }
  ],
  "paths": {
    "/v1/databases/{database_id}": {
      "get": {
        "summary": "Retrieve a database",
        "description": "",
        "operationId": "database-retrieve",
        "parameters": [
          {
            "name": "database_id",
            "in": "path",
            "description": "ID of a Notion database, a container for one or more data sources. This is a UUIDv4, with or without dashes.",
            "schema": {
              "type": "string"
            },
            "required": true
          }
        ],
        "responses": {
          "200": {
            "description": "200",
            "content": {
              "application/json": {
                "examples": {
                  "Result": {
                    "value": "{\n\t\"object\": \"database\",\n\t\"id\": \"248104cd-477e-80fd-b757-e945d38000bd\",\n\t\"title\": [\n\t\t{\n\t\t\t\"type\": \"text\",\n\t\t\t\"text\": {\n\t\t\t\t\"content\": \"My Task Tracker\",\n\t\t\t\t\"link\": null\n\t\t\t},\n\t\t\t\"annotations\": {\n\t\t\t\t\"bold\": false,\n\t\t\t\t\"italic\": false,\n\t\t\t\t\"strikethrough\": false,\n\t\t\t\t\"underline\": false,\n\t\t\t\t\"code\": false,\n\t\t\t\t\"color\": \"default\"\n\t\t\t},\n\t\t\t\"plain_text\": \"My Task Tracker\",\n\t\t\t\"href\": null\n\t\t}\n\t],\n\t\"parent\": {\n\t\t\"type\": \"page_id\",\n\t\t\"page_id\": \"255104cd-477e-808c-b279-d39ab803a7d2\"\n\t},\n\t\"is_inline\": false,\n\t\"in_trash\": false,\n\t\"created_time\": \"2025-08-07T10:11:07.504-07:00\",\n\t\"last_edited_time\": \"2025-08-10T15:53:11.386-07:00\",\n\t\"data_sources\": [\n\t\t{\n\t\t\t\"id\": \"248104cd-477e-80af-bc30-000bd28de8f9\",\n\t\t\t\"name\": \"My Task Tracker\"\n\t\t}\n\t],\n\t\"icon\": null,\n\t\"cover\": null,\n\t\"developer_survey\": \"https://example.com/xyz\",\n\t\"request_id\": \"2f788b44-abf3-4809-aa4c-dd40734fed0b\"\n}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "object": {
                      "type": "string",
                      "example": "database"
                    },
                    "id": {
                      "type": "string",
                      "example": "248104cd-477e-80fd-b757-e945d38000bd"
                    },
                    "title": {
                      "type": "array",
                      "items": {
                        "type": "object",
                        "properties": {
                          "type": {
                            "type": "string",
                            "example": "text"
                          },
                          "text": {
                            "type": "object",
                            "properties": {
                              "content": {
                                "type": "string",
                                "example": "My Task Tracker"
                              },
                              "link": {}
                            }
                          },
                          "annotations": {
                            "type": "object",
                            "properties": {
                              "bold": {
                                "type": "boolean",
                                "example": false,
                                "default": true
                              },
                              "italic": {
                                "type": "boolean",
                                "example": false,
                                "default": true
                              },
                              "strikethrough": {
                                "type": "boolean",
                                "example": false,
                                "default": true
                              },
                              "underline": {
                                "type": "boolean",
                                "example": false,
                                "default": true
                              },
                              "code": {
                                "type": "boolean",
                                "example": false,
                                "default": true
                              },
                              "color": {
                                "type": "string",
                                "example": "default"
                              }
                            }
                          },
                          "plain_text": {
                            "type": "string",
                            "example": "My Task Tracker"
                          },
                          "href": {}
                        }
                      }
                    },
                    "parent": {
                      "type": "object",
                      "properties": {
                        "type": {
                          "type": "string",
                          "example": "page_id"
                        },
                        "page_id": {
                          "type": "string",
                          "example": "255104cd-477e-808c-b279-d39ab803a7d2"
                        }
                      }
                    },
                    "is_inline": {
                      "type": "boolean",
                      "example": false,
                      "default": true
                    },
                    "in_trash": {
                      "type": "boolean",
                      "example": false,
                      "default": true
                    },
                    "created_time": {
                      "type": "string",
                      "example": "2025-08-07T10:11:07.504-07:00"
                    },
                    "last_edited_time": {
                      "type": "string",
                      "example": "2025-08-10T15:53:11.386-07:00"
                    },
                    "data_sources": {
                      "type": "array",
                      "items": {
                        "type": "object",
                        "properties": {
                          "id": {
                            "type": "string",
                            "example": "248104cd-477e-80af-bc30-000bd28de8f9"
                          },
                          "name": {
                            "type": "string",
                            "example": "My Task Tracker"
                          }
                        }
                      }
                    },
                    "icon": {},
                    "cover": {},
                    "developer_survey": {
                      "type": "string",
                      "example": "https://example.com/xyz"
                    },
                    "request_id": {
                      "type": "string",
                      "example": "2f788b44-abf3-4809-aa4c-dd40734fed0b"
                    }
                  }
                }
              }
            }
          },
          "400": {
            "description": "400",
            "content": {
              "application/json": {
                "examples": {
                  "Result": {
                    "value": "{}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {}
                }
              }
            }
          }
        },
        "deprecated": false,
        "security": []
      }
    }
  },
  "x-readme": {
    "headers": [],
    "explorer-enabled": false,
    "proxy-enabled": true
  },
  "x-readme-fauxas": true,
  "_id": "606ecc2cd9e93b0044cf6e47:68b1ec3c9b52dcbb8a539f3f"
}
```

# Create a data source

Use this API to add an additional [data source](ref:data-source)  to an existing [database](ref:database). The `properties` follow the [same structure](ref:property-object)  as the initial schema passed to `initial_data_source[properties]` in the [Create a database](ref:database-create6ee911d9) API, but can be managed independently of the `properties` of any sibling data sources.

A standard "table" view is created alongside the new data source. To customize database views, use the Notion app. Managing views is not currently supported in the API.

# OpenAPI definition
```json
{
  "openapi": "3.1.0",
  "info": {
    "title": "Notion API",
    "version": "1"
  },
  "servers": [
    {
      "url": "https://api.notion.com"
    }
  ],
  "components": {
    "securitySchemes": {
      "sec0": {
        "type": "oauth2",
        "flows": {}
      }
    }
  },
  "security": [
    {
      "sec0": []
    }
  ],
  "paths": {
    "/v1/data_sources": {
      "post": {
        "summary": "Create a data source",
        "description": "",
        "operationId": "create-a-data-source",
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "required": [
                  "parent",
                  "properties"
                ],
                "properties": {
                  "parent": {
                    "type": "object",
                    "description": "An object specifying the parent of the new data source to be created.",
                    "required": [
                      "database_id"
                    ],
                    "properties": {
                      "type": {
                        "type": "string",
                        "description": "Always `database_id`.",
                        "enum": [
                          "\"database_id\""
                        ]
                      },
                      "database_id": {
                        "type": "string",
                        "description": "The ID of the parent database (with or without dashes), for example, 195de9221179449fab8075a27c979105"
                      }
                    }
                  },
                  "properties": {
                    "type": "object",
                    "description": "Property schema of the new data source.",
                    "properties": {
                      "<propertyIdentifier>": {
                        "type": "object",
                        "description": "Hash map of strings (property identifiers) corresponding to the configuration of each property. The `type` of each property can be omitted, but you must provide a sub-object whose parameter name matches the type, even if it's an empty object. For example, {\"type\": \"date\", \"date\": {}} and {\"date\": {}} are both valid values, but {\"type\": \"date\"}` is not.",
                        "properties": {
                          "description": {
                            "type": "string",
                            "description": "The property's description (optional)."
                          },
                          "type": {
                            "type": "string",
                            "description": "The type of property.",
                            "enum": [
                              "\"number\"",
                              "\"formula\"",
                              "\"select\"",
                              "\"multi_select\"",
                              "\"status\"",
                              "\"relation\"",
                              "\"rollup\"",
                              "\"unique_id\"",
                              "\"title\"",
                              "\"rich_text\"",
                              "\"url\"",
                              "\"people\"",
                              "\"files\"",
                              "\"email\"",
                              "\"phone_number\"",
                              "\"date\"",
                              "\"checkbox\"",
                              "\"created_by\"",
                              "\"created_time\"",
                              "\"last_edited_by\"",
                              "\"last_edited_time\"",
                              "\"button\"",
                              "\"location\"",
                              "\"verification\"",
                              "\"last_visited_time\"",
                              "\"place\""
                            ]
                          },
                          "number": {
                            "type": "object",
                            "properties": {
                              "format": {
                                "type": "string",
                                "description": "The format of the number property.",
                                "enum": [
                                  "\"number\"",
                                  "\"number_with_commas\"",
                                  "\"percent\"",
                                  "\"dollar\"",
                                  "\"australian_dollar\"",
                                  "\"canadian_dollar\"",
                                  "\"singapore_dollar\"",
                                  "\"euro\"",
                                  "\"pound\"",
                                  "\"yen\"",
                                  "\"ruble\"",
                                  "\"rupee\"",
                                  "\"won\"",
                                  "\"yuan\"",
                                  "\"real\"",
                                  "\"lira\"",
                                  "\"rupiah\"",
                                  "\"franc\"",
                                  "\"hong_kong_dollar\"",
                                  "\"new_zealand_dollar\"",
                                  "\"krona\"",
                                  "\"norwegian_krone\"",
                                  "\"mexican_peso\"",
                                  "\"rand\"",
                                  "\"new_taiwan_dollar\"",
                                  "\"danish_krone\"",
                                  "\"zloty\"",
                                  "\"baht\"",
                                  "\"forint\"",
                                  "\"koruna\"",
                                  "\"shekel\"",
                                  "\"chilean_peso\"",
                                  "\"philippine_peso\"",
                                  "\"dirham\"",
                                  "\"colombian_peso\"",
                                  "\"riyal\"",
                                  "\"ringgit\"",
                                  "\"leu\"",
                                  "\"argentine_peso\"",
                                  "\"uruguayan_peso\"",
                                  "\"peruvian_sol\"",
                                  ""
                                ]
                              }
                            }
                          },
                          "formula": {
                            "type": "object",
                            "properties": {
                              "expression": {
                                "type": "string",
                                "description": "A valid Notion formula expression."
                              }
                            }
                          },
                          "select": {
                            "type": "object",
                            "properties": {
                              "options": {
                                "type": "array",
                                "items": {
                                  "properties": {
                                    "color": {
                                      "type": "string",
                                      "enum": [
                                        "\"default\"",
                                        "\"gray\"",
                                        "\"brown\"",
                                        "\"orange\"",
                                        "\"yellow\"",
                                        "\"green\"",
                                        "\"blue\"",
                                        "\"purple\"",
                                        "\"pink\"",
                                        "\"red\"",
                                        ""
                                      ]
                                    },
                                    "description": {
                                      "type": "string"
                                    }
                                  },
                                  "type": "object"
                                }
                              }
                            }
                          },
                          "multi_select": {
                            "type": "object",
                            "properties": {
                              "color": {
                                "type": "string",
                                "enum": [
                                  "\"default\"",
                                  "\"gray\"",
                                  "\"brown\"",
                                  "\"orange\"",
                                  "\"yellow\"",
                                  "\"green\"",
                                  "\"blue\"",
                                  "\"purple\"",
                                  "\"pink\"",
                                  "\"red\"",
                                  ""
                                ]
                              },
                              "description": {
                                "type": "string"
                              }
                            }
                          },
                          "relation": {
                            "type": "object",
                            "properties": {
                              "type": {
                                "type": "string",
                                "enum": [
                                  "\"single_property\"",
                                  "\"dual_property\""
                                ]
                              },
                              "single_property": {
                                "type": "object",
                                "description": "An empty object `{}`.",
                                "properties": {}
                              },
                              "dual_property": {
                                "type": "object",
                                "properties": {
                                  "synced_property_id": {
                                    "type": "string"
                                  },
                                  "synced_property_name": {
                                    "type": "string"
                                  }
                                }
                              }
                            }
                          },
                          "rollup": {
                            "type": "object",
                            "required": [
                              "function"
                            ],
                            "properties": {
                              "function": {
                                "type": "string",
                                "enum": [
                                  "\"count\"",
                                  "\"count_values\"",
                                  "\"empty\"",
                                  "\"not_empty\"",
                                  "\"unique\"",
                                  "\"show_unique\"",
                                  "\"percent_empty\"",
                                  "\"percent_not_empty\"",
                                  "\"sum\"",
                                  "\"average\"",
                                  "\"median\"",
                                  "\"min\"",
                                  "\"max\"",
                                  "\"range\"",
                                  "\"earliest_date\"",
                                  "\"latest_date\"",
                                  "\"date_range\"",
                                  "\"checked\"",
                                  "\"unchecked\"",
                                  "\"percent_checked\"",
                                  "\"percent_unchecked\"",
                                  "\"count_per_group\"",
                                  "\"percent_per_group\"",
                                  "\"show_original\""
                                ]
                              },
                              "relation_property_name": {
                                "type": "string"
                              },
                              "relation_property_id": {
                                "type": "string"
                              },
                              "rollup_property_name": {
                                "type": "string"
                              },
                              "rollup_property_id": {
                                "type": "string"
                              }
                            }
                          },
                          "unique_id": {
                            "type": "object",
                            "properties": {
                              "prefix": {
                                "type": "string"
                              }
                            }
                          }
                        }
                      }
                    }
                  },
                  "title": {
                    "type": "array",
                    "description": "Title of data source as it appears in Notion.",
                    "items": {
                      "properties": {
                        "annotations": {
                          "type": "object",
                          "description": "The styling for the rich text.",
                          "properties": {
                            "bold": {
                              "type": "boolean",
                              "description": "Whether the text is formatted as bold.",
                              "default": false
                            },
                            "italic": {
                              "type": "boolean",
                              "description": "Whether the text is formatted as italic.",
                              "default": false
                            },
                            "strikethrough": {
                              "type": "boolean",
                              "description": "Whether the text is formatted with a strikethrough.",
                              "default": false
                            },
                            "underline": {
                              "type": "boolean",
                              "description": "Whether the text is formatted with an underline.",
                              "default": false
                            },
                            "code": {
                              "type": "boolean",
                              "description": "Whether the text is formatted as code.",
                              "default": false
                            },
                            "color": {
                              "type": "string",
                              "description": "The color of the text.",
                              "default": "\"default\"",
                              "enum": [
                                "\"default\"",
                                "\"gray\"",
                                "\"brown\"",
                                "\"orange\"",
                                "\"yellow\"",
                                "\"green\"",
                                "\"blue\"",
                                "\"purple\"",
                                "\"pink\"",
                                "\"red\"",
                                "\"default_background\"",
                                "\"gray_background\"",
                                "\"brown_background\"",
                                "\"orange_background\"",
                                "\"yellow_background\"",
                                "\"green_background\"",
                                "\"blue_background\"",
                                "\"purple_background\"",
                                "\"pink_background\"",
                                "\"red_background\""
                              ]
                            }
                          }
                        },
                        "plain_text": {
                          "type": "string",
                          "description": "The plain text content of the rich text object, without any styling."
                        },
                        "href": {
                          "type": "string",
                          "description": "A URL that the rich text object links to or mentions."
                        },
                        "type": {
                          "type": "string",
                          "enum": [
                            "\"text\"",
                            "\"mention\"",
                            "\"equation\""
                          ]
                        }
                      },
                      "type": "object"
                    }
                  },
                  "icon": {
                    "type": "object",
                    "description": "Icon to apply to the data source.",
                    "properties": {
                      "type": {
                        "type": "string",
                        "description": "The type of icon parameter being provided.",
                        "enum": [
                          "\"file_upload\"",
                          "\"emoji\"",
                          "\"external\"",
                          "\"custom_emoji\""
                        ]
                      },
                      "emoji": {
                        "type": "string",
                        "description": "When `type=emoji`, an emoji character."
                      },
                      "file_upload": {
                        "type": "object",
                        "description": "When `type=file_upload`, an object containing the `id` of the File Upload.",
                        "required": [
                          "id"
                        ],
                        "properties": {
                          "id": {
                            "type": "string",
                            "description": "ID of a FileUpload object that has the status `uploaded`."
                          }
                        }
                      },
                      "external": {
                        "type": "object",
                        "description": "When `type=external`, an object containing the external URL.",
                        "required": [
                          "url"
                        ],
                        "properties": {
                          "url": {
                            "type": "string",
                            "description": "The URL of the external file."
                          }
                        }
                      },
                      "custom_emoji": {
                        "type": "object",
                        "description": "When `type=custom_emoji`, an object containing the custom emoji.",
                        "required": [
                          "id"
                        ],
                        "properties": {
                          "id": {
                            "type": "string",
                            "description": "The ID of the custom emoji."
                          },
                          "name": {
                            "type": "string",
                            "description": "The name of the custom emoji."
                          },
                          "url": {
                            "type": "string",
                            "description": "The URL of the custom emoji."
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "200",
            "content": {
              "application/json": {
                "examples": {
                  "Result": {
                    "value": "{\n\t\"object\": \"data_source\",\n\t\"id\": \"bc1211ca-e3f1-4939-ae34-5260b16f627c\",\n\t\"created_time\": \"2021-07-08T23:50:00.000Z\",\n\t\"last_edited_time\": \"2021-07-08T23:50:00.000Z\",\n\t\"properties\": {\n\t\t\"+1\": {\n\t\t\t\"id\": \"Wp%3DC\",\n\t\t\t\"name\": \"+1\",\n\t\t\t\"type\": \"people\",\n\t\t\t\"people\": {}\n\t\t},\n\t\t\"In stock\": {\n\t\t\t\"id\": \"fk%5EY\",\n\t\t\t\"name\": \"In stock\",\n\t\t\t\"type\": \"checkbox\",\n\t\t\t\"checkbox\": {}\n\t\t},\n\t\t\"Price\": {\n\t\t\t\"id\": \"evWq\",\n\t\t\t\"name\": \"Price\",\n\t\t\t\"type\": \"number\",\n\t\t\t\"number\": {\n\t\t\t\t\"format\": \"dollar\"\n\t\t\t}\n\t\t},\n\t\t\"Description\": {\n\t\t\t\"id\": \"V}lX\",\n\t\t\t\"name\": \"Description\",\n\t\t\t\"type\": \"rich_text\",\n\t\t\t\"rich_text\": {}\n\t\t},\n\t\t\"Last ordered\": {\n\t\t\t\"id\": \"eVnV\",\n\t\t\t\"name\": \"Last ordered\",\n\t\t\t\"type\": \"date\",\n\t\t\t\"date\": {}\n\t\t},\n\t\t\"Meals\": {\n\t\t\t\"id\": \"%7DWA~\",\n\t\t\t\"name\": \"Meals\",\n\t\t\t\"type\": \"relation\",\n\t\t\t\"relation\": {\n\t\t\t\t\"database_id\": \"668d797c-76fa-4934-9b05-ad288df2d136\",\n\t\t\t\t\"synced_property_name\": \"Related to Grocery List (Meals)\"\n\t\t\t}\n\t\t},\n\t\t\"Number of meals\": {\n\t\t\t\"id\": \"Z\\\\Eh\",\n\t\t\t\"name\": \"Number of meals\",\n\t\t\t\"type\": \"rollup\",\n\t\t\t\"rollup\": {\n\t\t\t\t\"rollup_property_name\": \"Name\",\n\t\t\t\t\"relation_property_name\": \"Meals\",\n\t\t\t\t\"rollup_property_id\": \"title\",\n\t\t\t\t\"relation_property_id\": \"mxp^\",\n\t\t\t\t\"function\": \"count\"\n\t\t\t}\n\t\t},\n\t\t\"Store availability\": {\n\t\t\t\"id\": \"s}Kq\",\n\t\t\t\"name\": \"Store availability\",\n\t\t\t\"type\": \"multi_select\",\n\t\t\t\"multi_select\": {\n\t\t\t\t\"options\": [\n\t\t\t\t\t{\n\t\t\t\t\t\t\"id\": \"cb79b393-d1c1-4528-b517-c450859de766\",\n\t\t\t\t\t\t\"name\": \"Duc Loi Market\",\n\t\t\t\t\t\t\"color\": \"blue\"\n\t\t\t\t\t},\n\t\t\t\t\t{\n\t\t\t\t\t\t\"id\": \"58aae162-75d4-403b-a793-3bc7308e4cd2\",\n\t\t\t\t\t\t\"name\": \"Rainbow Grocery\",\n\t\t\t\t\t\t\"color\": \"gray\"\n\t\t\t\t\t},\n\t\t\t\t\t{\n\t\t\t\t\t\t\"id\": \"22d0f199-babc-44ff-bd80-a9eae3e3fcbf\",\n\t\t\t\t\t\t\"name\": \"Nijiya Market\",\n\t\t\t\t\t\t\"color\": \"purple\"\n\t\t\t\t\t},\n\t\t\t\t\t{\n\t\t\t\t\t\t\"id\": \"0d069987-ffb0-4347-bde2-8e4068003dbc\",\n\t\t\t\t\t\t\"name\": \"Gus's Community Market\",\n\t\t\t\t\t\t\"color\": \"yellow\"\n\t\t\t\t\t}\n\t\t\t\t]\n\t\t\t}\n\t\t},\n\t\t\"Photo\": {\n\t\t\t\"id\": \"yfiK\",\n\t\t\t\"name\": \"Photo\",\n\t\t\t\"type\": \"files\",\n\t\t\t\"files\": {}\n\t\t},\n\t\t\"Food group\": {\n\t\t\t\"id\": \"CM%3EH\",\n\t\t\t\"name\": \"Food group\",\n\t\t\t\"type\": \"select\",\n\t\t\t\"select\": {\n\t\t\t\t\"options\": [\n\t\t\t\t\t{\n\t\t\t\t\t\t\"id\": \"6d4523fa-88cb-4ffd-9364-1e39d0f4e566\",\n\t\t\t\t\t\t\"name\": \"🥦Vegetable\",\n\t\t\t\t\t\t\"color\": \"green\"\n\t\t\t\t\t},\n\t\t\t\t\t{\n\t\t\t\t\t\t\"id\": \"268d7e75-de8f-4c4b-8b9d-de0f97021833\",\n\t\t\t\t\t\t\"name\": \"🍎Fruit\",\n\t\t\t\t\t\t\"color\": \"red\"\n\t\t\t\t\t},\n\t\t\t\t\t{\n\t\t\t\t\t\t\"id\": \"1b234a00-dc97-489c-b987-829264cfdfef\",\n\t\t\t\t\t\t\"name\": \"💪Protein\",\n\t\t\t\t\t\t\"color\": \"yellow\"\n\t\t\t\t\t}\n\t\t\t\t]\n\t\t\t}\n\t\t},\n\t\t\"Name\": {\n\t\t\t\"id\": \"title\",\n\t\t\t\"name\": \"Name\",\n\t\t\t\"type\": \"title\",\n\t\t\t\"title\": {}\n\t\t}\n\t},\n\t\"parent\": {\n\t\t\"type\": \"database_id\",\n\t\t\"database_id\": \"6ee911d9-189c-4844-93e8-260c1438b6e4\"\n\t},\n\t\"database_parent\": {\n\t\t\"type\": \"page_id\",\n\t\t\"page_id\": \"98ad959b-2b6a-4774-80ee-00246fb0ea9b\"\n\t},\n\t\"archived\": false,\n\t\"is_inline\": false,\n\t\"icon\": {\n\t\t\"type\": \"emoji\",\n\t\t\"emoji\": \"🎉\"\n\t},\n\t\"cover\": {\n\t\t\"type\": \"external\",\n\t\t\"external\": {\n\t\t\t\"url\": \"https://website.domain/images/image.png\"\n\t\t}\n\t},\n\t\"url\": \"https://www.notion.so/bc1211cae3f14939ae34260b16f627c\",\n\t\"title\": [\n\t\t{\n\t\t\t\"type\": \"text\",\n\t\t\t\"text\": {\n\t\t\t\t\"content\": \"Grocery List\",\n\t\t\t\t\"link\": null\n\t\t\t},\n\t\t\t\"annotations\": {\n\t\t\t\t\"bold\": false,\n\t\t\t\t\"italic\": false,\n\t\t\t\t\"strikethrough\": false,\n\t\t\t\t\"underline\": false,\n\t\t\t\t\"code\": false,\n\t\t\t\t\"color\": \"default\"\n\t\t\t},\n\t\t\t\"plain_text\": \"Grocery List\",\n\t\t\t\"href\": null\n\t\t}\n\t]\n}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "object": {
                      "type": "string",
                      "example": "data_source"
                    },
                    "id": {
                      "type": "string",
                      "example": "bc1211ca-e3f1-4939-ae34-5260b16f627c"
                    },
                    "created_time": {
                      "type": "string",
                      "example": "2021-07-08T23:50:00.000Z"
                    },
                    "last_edited_time": {
                      "type": "string",
                      "example": "2021-07-08T23:50:00.000Z"
                    },
                    "properties": {
                      "type": "object",
                      "properties": {
                        "+1": {
                          "type": "object",
                          "properties": {
                            "id": {
                              "type": "string",
                              "example": "Wp%3DC"
                            },
                            "name": {
                              "type": "string",
                              "example": "+1"
                            },
                            "type": {
                              "type": "string",
                              "example": "people"
                            },
                            "people": {
                              "type": "object",
                              "properties": {}
                            }
                          }
                        },
                        "In stock": {
                          "type": "object",
                          "properties": {
                            "id": {
                              "type": "string",
                              "example": "fk%5EY"
                            },
                            "name": {
                              "type": "string",
                              "example": "In stock"
                            },
                            "type": {
                              "type": "string",
                              "example": "checkbox"
                            },
                            "checkbox": {
                              "type": "object",
                              "properties": {}
                            }
                          }
                        },
                        "Price": {
                          "type": "object",
                          "properties": {
                            "id": {
                              "type": "string",
                              "example": "evWq"
                            },
                            "name": {
                              "type": "string",
                              "example": "Price"
                            },
                            "type": {
                              "type": "string",
                              "example": "number"
                            },
                            "number": {
                              "type": "object",
                              "properties": {
                                "format": {
                                  "type": "string",
                                  "example": "dollar"
                                }
                              }
                            }
                          }
                        },
                        "Description": {
                          "type": "object",
                          "properties": {
                            "id": {
                              "type": "string",
                              "example": "V}lX"
                            },
                            "name": {
                              "type": "string",
                              "example": "Description"
                            },
                            "type": {
                              "type": "string",
                              "example": "rich_text"
                            },
                            "rich_text": {
                              "type": "object",
                              "properties": {}
                            }
                          }
                        },
                        "Last ordered": {
                          "type": "object",
                          "properties": {
                            "id": {
                              "type": "string",
                              "example": "eVnV"
                            },
                            "name": {
                              "type": "string",
                              "example": "Last ordered"
                            },
                            "type": {
                              "type": "string",
                              "example": "date"
                            },
                            "date": {
                              "type": "object",
                              "properties": {}
                            }
                          }
                        },
                        "Meals": {
                          "type": "object",
                          "properties": {
                            "id": {
                              "type": "string",
                              "example": "%7DWA~"
                            },
                            "name": {
                              "type": "string",
                              "example": "Meals"
                            },
                            "type": {
                              "type": "string",
                              "example": "relation"
                            },
                            "relation": {
                              "type": "object",
                              "properties": {
                                "database_id": {
                                  "type": "string",
                                  "example": "668d797c-76fa-4934-9b05-ad288df2d136"
                                },
                                "synced_property_name": {
                                  "type": "string",
                                  "example": "Related to Grocery List (Meals)"
                                }
                              }
                            }
                          }
                        },
                        "Number of meals": {
                          "type": "object",
                          "properties": {
                            "id": {
                              "type": "string",
                              "example": "Z\\Eh"
                            },
                            "name": {
                              "type": "string",
                              "example": "Number of meals"
                            },
                            "type": {
                              "type": "string",
                              "example": "rollup"
                            },
                            "rollup": {
                              "type": "object",
                              "properties": {
                                "rollup_property_name": {
                                  "type": "string",
                                  "example": "Name"
                                },
                                "relation_property_name": {
                                  "type": "string",
                                  "example": "Meals"
                                },
                                "rollup_property_id": {
                                  "type": "string",
                                  "example": "title"
                                },
                                "relation_property_id": {
                                  "type": "string",
                                  "example": "mxp^"
                                },
                                "function": {
                                  "type": "string",
                                  "example": "count"
                                }
                              }
                            }
                          }
                        },
                        "Store availability": {
                          "type": "object",
                          "properties": {
                            "id": {
                              "type": "string",
                              "example": "s}Kq"
                            },
                            "name": {
                              "type": "string",
                              "example": "Store availability"
                            },
                            "type": {
                              "type": "string",
                              "example": "multi_select"
                            },
                            "multi_select": {
                              "type": "object",
                              "properties": {
                                "options": {
                                  "type": "array",
                                  "items": {
                                    "type": "object",
                                    "properties": {
                                      "id": {
                                        "type": "string",
                                        "example": "cb79b393-d1c1-4528-b517-c450859de766"
                                      },
                                      "name": {
                                        "type": "string",
                                        "example": "Duc Loi Market"
                                      },
                                      "color": {
                                        "type": "string",
                                        "example": "blue"
                                      }
                                    }
                                  }
                                }
                              }
                            }
                          }
                        },
                        "Photo": {
                          "type": "object",
                          "properties": {
                            "id": {
                              "type": "string",
                              "example": "yfiK"
                            },
                            "name": {
                              "type": "string",
                              "example": "Photo"
                            },
                            "type": {
                              "type": "string",
                              "example": "files"
                            },
                            "files": {
                              "type": "object",
                              "properties": {}
                            }
                          }
                        },
                        "Food group": {
                          "type": "object",
                          "properties": {
                            "id": {
                              "type": "string",
                              "example": "CM%3EH"
                            },
                            "name": {
                              "type": "string",
                              "example": "Food group"
                            },
                            "type": {
                              "type": "string",
                              "example": "select"
                            },
                            "select": {
                              "type": "object",
                              "properties": {
                                "options": {
                                  "type": "array",
                                  "items": {
                                    "type": "object",
                                    "properties": {
                                      "id": {
                                        "type": "string",
                                        "example": "6d4523fa-88cb-4ffd-9364-1e39d0f4e566"
                                      },
                                      "name": {
                                        "type": "string",
                                        "example": "🥦Vegetable"
                                      },
                                      "color": {
                                        "type": "string",
                                        "example": "green"
                                      }
                                    }
                                  }
                                }
                              }
                            }
                          }
                        },
                        "Name": {
                          "type": "object",
                          "properties": {
                            "id": {
                              "type": "string",
                              "example": "title"
                            },
                            "name": {
                              "type": "string",
                              "example": "Name"
                            },
                            "type": {
                              "type": "string",
                              "example": "title"
                            },
                            "title": {
                              "type": "object",
                              "properties": {}
                            }
                          }
                        }
                      }
                    },
                    "parent": {
                      "type": "object",
                      "properties": {
                        "type": {
                          "type": "string",
                          "example": "database_id"
                        },
                        "database_id": {
                          "type": "string",
                          "example": "6ee911d9-189c-4844-93e8-260c1438b6e4"
                        }
                      }
                    },
                    "database_parent": {
                      "type": "object",
                      "properties": {
                        "type": {
                          "type": "string",
                          "example": "page_id"
                        },
                        "page_id": {
                          "type": "string",
                          "example": "98ad959b-2b6a-4774-80ee-00246fb0ea9b"
                        }
                      }
                    },
                    "archived": {
                      "type": "boolean",
                      "example": false,
                      "default": true
                    },
                    "is_inline": {
                      "type": "boolean",
                      "example": false,
                      "default": true
                    },
                    "icon": {
                      "type": "object",
                      "properties": {
                        "type": {
                          "type": "string",
                          "example": "emoji"
                        },
                        "emoji": {
                          "type": "string",
                          "example": "🎉"
                        }
                      }
                    },
                    "cover": {
                      "type": "object",
                      "properties": {
                        "type": {
                          "type": "string",
                          "example": "external"
                        },
                        "external": {
                          "type": "object",
                          "properties": {
                            "url": {
                              "type": "string",
                              "example": "https://website.domain/images/image.png"
                            }
                          }
                        }
                      }
                    },
                    "url": {
                      "type": "string",
                      "example": "https://www.notion.so/bc1211cae3f14939ae34260b16f627c"
                    },
                    "title": {
                      "type": "array",
                      "items": {
                        "type": "object",
                        "properties": {
                          "type": {
                            "type": "string",
                            "example": "text"
                          },
                          "text": {
                            "type": "object",
                            "properties": {
                              "content": {
                                "type": "string",
                                "example": "Grocery List"
                              },
                              "link": {}
                            }
                          },
                          "annotations": {
                            "type": "object",
                            "properties": {
                              "bold": {
                                "type": "boolean",
                                "example": false,
                                "default": true
                              },
                              "italic": {
                                "type": "boolean",
                                "example": false,
                                "default": true
                              },
                              "strikethrough": {
                                "type": "boolean",
                                "example": false,
                                "default": true
                              },
                              "underline": {
                                "type": "boolean",
                                "example": false,
                                "default": true
                              },
                              "code": {
                                "type": "boolean",
                                "example": false,
                                "default": true
                              },
                              "color": {
                                "type": "string",
                                "example": "default"
                              }
                            }
                          },
                          "plain_text": {
                            "type": "string",
                            "example": "Grocery List"
                          },
                          "href": {}
                        }
                      }
                    }
                  }
                }
              }
            }
          },
          "404": {
            "description": "404",
            "content": {
              "application/json": {
                "examples": {
                  "Result": {
                    "value": "{\n  code: \"object_not_found\",\n  message: \"Could not find database with ID: 6ee911d9-189c-4844-93e8-260c1438b6e4. Make sure the relevant pages and databases are shared with your integration.\",\n  object: \"error\",\n  status: 404,\n  request_id: \"db2ed4f6-3415-4f04-9a58-85e10df0a67c\"\n}"
                  }
                }
              }
            }
          }
        },
        "deprecated": false,
        "security": [],
        "x-readme": {
          "code-samples": [
            {
              "language": "curl",
              "code": "curl --request POST \\\n     --url https://api.notion.com/v1/data_sources \\\n     --header 'accept: application/json' \\\n     --header 'content-type: application/json' \\\n     --data '\n{\n\t\"parent\": {\n\t\t\"type\": \"database_id\",\n\t\t\"database_id\": \"6ee911d9-189c-4844-93e8-260c1438b6e4\"\n\t},\n\t\"properties\": {\n\t\t\"Title\": {\n\t\t\t\"type\": \"title\",\n\t\t\t\"title\": {}\n\t\t},\n\t\t\"Count\": {\n\t\t\t\"type\": \"number\",\n\t\t\t\"number\": {}\n\t\t}\n\t},\n\t\"title\": [\n\t\t{\n\t\t\t\"type\": \"text\",\n\t\t\t\"text\": {\"content\": \"New child data source\"}\n\t\t}\n\t]\n}\n'"
            },
            {
              "language": "node",
              "code": "import { Client } from \"@notionhq/client\"\n\nconst notion = new Client({\n  auth: \"{ACCESS_TOKEN}\",\n  notionVersion: \"2025-09-03\",\n})\n\ntry {\n  const response = await notion.dataSources.create({\n    parent: {\n      type: \"database_id\",\n      database_id: \"6ee911d9-189c-4844-93e8-260c1438b6e4\",\n    },\n    properties: {\n      Title: {\n        type: \"title\",\n        title: {}\n      },\n      Count: {\n        type: \"number\",\n        number: {}\n      }\n    },\n    title: [\n      {\n        type: \"text\",\n        text: {content: \"New child data source\"}\n      }\n    ]\n  })\n\n  const dataSourceId = response.id\n  console.log(\"Successfully created data source with ID:\", dataSourceId)\n\n} catch (error) {\n  // Handle `APIResponseError`\n  console.error(error)\n}"
            }
          ],
          "samples-languages": [
            "curl",
            "node"
          ]
        }
      }
    }
  },
  "x-readme": {
    "headers": [],
    "explorer-enabled": false,
    "proxy-enabled": true
  },
  "x-readme-fauxas": true,
  "_id": "606ecc2cd9e93b0044cf6e47:68b1eb79130b4cab6ed4fede"
}
```

# Update a data source

Updates the [data source](ref:data-source)  object — the properties, title, description, or whether it's in the trash — of a specified data source under a database.

Returns the updated data source object.

Use the `parent` parameter to move the data source to a different `database_id`. If you do so, any existing views that refer to the data source in the current database continue to exist, but become _linked_ views. A new standard "table" view for the moved data source is created under the new (destination) database. Use the Notion app to make any further changes to the views; managing views using the API is not currently supported.

Data source properties represent the columns (or schema) of a data source. To update the properties of a data source, use the `properties` [body param](ref:update-data-source-properties) with this endpoint. Learn more about data source properties in the [data source properties](ref:property-object) and [Update data source properties](ref:update-data-source-properties) docs.

To update a `relation` data source property, share the related database with the integration. Learn more about relations in the [data source properties](ref:property-object#relation) page.

For an overview of how to use the REST API with databases, refer to the [Working with databases](https://developers.notion.com/docs/working-with-databases) guide.

### How data sources property type changes work

All properties in pages are stored as rich text. Notion will convert that rich text based on the types defined in a data source's schema. When a type is changed using the API, the data will continue to be available, it is just presented differently.

For example, a multi select property value is represented as a comma-separated list of strings (eg. "1, 2, 3") and a people property value is represented as a comma-separated list of IDs. These are compatible and the type can be converted.

Note: Not all type changes work. In some cases data will no longer be returned, such as people type → file type.

### Interacting with data source rows

This endpoint cannot be used to update data source rows.

To update the properties of a data source row — rather than a column — use the [Update page properties](https://developers.notion.com/reference/patch-page) endpoint. To add a new row to a database, use the [Create a page](https://developers.notion.com/reference/post-page) endpoint.

### Recommended data source schema size limit

Developers are encouraged to keep their data source schema size to a maximum of **50KB**. To stay within this schema size limit, the number of properties (or columns) added to a data source should be managed.

Data source schema updates that are too large will be blocked by the REST API to help developers keep their data source queries performant.

### Errors

Each Public API endpoint can return several possible error codes. See the [Error codes section](https://developers.notion.com/reference/status-codes#error-codes) of the Status codes documentation for more information.

> 🚧 The following data source properties cannot be updated via the API:
>
> - `formula`
> - `status`
> - [Synced content](https://www.notion.so/help/guides/synced-databases-bridge-different-tools)
> - `place`

> 📘 Data source relations must be shared with your integration
>
> To update a data source [relation](https://www.notion.so/help/relations-and-rollups#what-is-a-database-relation) property, the related database must also be shared with your integration.

# OpenAPI definition
```json
{
  "openapi": "3.1.0",
  "info": {
    "title": "Notion API",
    "version": "1"
  },
  "servers": [
    {
      "url": "https://api.notion.com"
    }
  ],
  "components": {
    "securitySchemes": {
      "sec0": {
        "type": "oauth2",
        "flows": {}
      }
    }
  },
  "security": [
    {
      "sec0": []
    }
  ],
  "paths": {
    "/v1/data_sources/{data_source_id}": {
      "patch": {
        "summary": "Update a data source",
        "description": "",
        "operationId": "update-a-data-source",
        "parameters": [
          {
            "name": "Notion-Version",
            "in": "header",
            "description": "The [API version](/reference/versioning) to use for this request. The latest version is `<<internalLatestNotionVersion>>`.",
            "required": true,
            "schema": {
              "type": "string"
            }
          },
          {
            "name": "data_source_id",
            "in": "path",
            "description": "ID of a Notion data source. This is a UUIDv4, with or without dashes.",
            "schema": {
              "type": "string"
            },
            "required": true
          }
        ],
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "properties": {
                    "type": "object",
                    "properties": {
                      "<propertyIdentifier>": {
                        "type": "object",
                        "description": "Map from property identifier strings to `null` (to remove an existing property) or an an object with a property configuration update.",
                        "properties": {
                          "name": {
                            "type": "string",
                            "description": "Updated name of the property. Must be provided when renaming an existing parameter. Otherwise, optional."
                          },
                          "description": {
                            "type": "string",
                            "description": "Description of the property."
                          },
                          "type": {
                            "type": "string",
                            "description": "Type of property being updated, added, or renamed. (Optional)",
                            "enum": [
                              "\"number\"",
                              "\"formula\"",
                              "\"select\"",
                              "\"multi_select\"",
                              "\"status\"",
                              "\"relation\"",
                              "\"rollup\"",
                              "\"unique_id\"",
                              "\"title\"",
                              "\"rich_text\"",
                              "\"url\"",
                              "\"people\"",
                              "\"files\"",
                              "\"email\"",
                              "\"phone_number\"",
                              "\"date\"",
                              "\"checkbox\"",
                              "\"created_by\"",
                              "\"created_time\"",
                              "\"last_edited_by\"",
                              "\"last_edited_time\"",
                              "\"button\"",
                              "\"location\"",
                              "\"verification\"",
                              "\"last_visited_time\"",
                              "\"place\""
                            ]
                          },
                          "number": {
                            "type": "object",
                            "properties": {
                              "format": {
                                "type": "string",
                                "description": "The format of the number property.",
                                "enum": [
                                  "\"number\"",
                                  "\"number_with_commas\"",
                                  "\"percent\"",
                                  "\"dollar\"",
                                  "\"australian_dollar\"",
                                  "\"canadian_dollar\"",
                                  "\"singapore_dollar\"",
                                  "\"euro\"",
                                  "\"pound\"",
                                  "\"yen\"",
                                  "\"ruble\"",
                                  "\"rupee\"",
                                  "\"won\"",
                                  "\"yuan\"",
                                  "\"real\"",
                                  "\"lira\"",
                                  "\"rupiah\"",
                                  "\"franc\"",
                                  "\"hong_kong_dollar\"",
                                  "\"new_zealand_dollar\"",
                                  "\"krona\"",
                                  "\"norwegian_krone\"",
                                  "\"mexican_peso\"",
                                  "\"rand\"",
                                  "\"new_taiwan_dollar\"",
                                  "\"danish_krone\"",
                                  "\"zloty\"",
                                  "\"baht\"",
                                  "\"forint\"",
                                  "\"koruna\"",
                                  "\"shekel\"",
                                  "\"chilean_peso\"",
                                  "\"philippine_peso\"",
                                  "\"dirham\"",
                                  "\"colombian_peso\"",
                                  "\"riyal\"",
                                  "\"ringgit\"",
                                  "\"leu\"",
                                  "\"argentine_peso\"",
                                  "\"uruguayan_peso\"",
                                  "\"peruvian_sol\"",
                                  ""
                                ]
                              }
                            }
                          },
                          "formula": {
                            "type": "object",
                            "properties": {
                              "expression": {
                                "type": "string",
                                "description": "A valid Notion formula expression."
                              }
                            }
                          },
                          "select": {
                            "type": "object",
                            "properties": {
                              "options": {
                                "type": "array",
                                "description": "Array of added or updated options for a `select` or `multi_select` property. One of `id` or `name` must be included in each array entry.",
                                "items": {
                                  "properties": {
                                    "color": {
                                      "type": "string",
                                      "enum": [
                                        "\"default\"",
                                        "\"gray\"",
                                        "\"brown\"",
                                        "\"orange\"",
                                        "\"yellow\"",
                                        "\"green\"",
                                        "\"blue\"",
                                        "\"purple\"",
                                        "\"pink\"",
                                        "\"red\"",
                                        ""
                                      ]
                                    },
                                    "description": {
                                      "type": "string"
                                    },
                                    "name": {
                                      "type": "string"
                                    },
                                    "id": {
                                      "type": "string"
                                    }
                                  },
                                  "type": "object"
                                }
                              }
                            }
                          },
                          "multi_select": {
                            "type": "object",
                            "properties": {
                              "options": {
                                "type": "array",
                                "description": "Array of added or updated options for a `select` or `multi_select` property. One of `id` or `name` must be included in each array entry.",
                                "items": {
                                  "properties": {
                                    "color": {
                                      "type": "string",
                                      "enum": [
                                        "\"default\"",
                                        "\"gray\"",
                                        "\"brown\"",
                                        "\"orange\"",
                                        "\"yellow\"",
                                        "\"green\"",
                                        "\"blue\"",
                                        "\"purple\"",
                                        "\"pink\"",
                                        "\"red\"",
                                        ""
                                      ]
                                    },
                                    "description": {
                                      "type": "string"
                                    },
                                    "name": {
                                      "type": "string"
                                    },
                                    "id": {
                                      "type": "string"
                                    }
                                  },
                                  "type": "object"
                                }
                              }
                            }
                          },
                          "relation": {
                            "type": "object",
                            "properties": {
                              "type": {
                                "type": "string",
                                "enum": [
                                  "\"single_property\"",
                                  "\"dual_property\""
                                ]
                              },
                              "single_property": {
                                "type": "object",
                                "description": "An empty object `{}`.",
                                "properties": {}
                              },
                              "dual_property": {
                                "type": "object",
                                "properties": {
                                  "synced_property_id": {
                                    "type": "string"
                                  },
                                  "synced_property_name": {
                                    "type": "string"
                                  }
                                }
                              }
                            }
                          },
                          "rollup": {
                            "type": "object",
                            "required": [
                              "function"
                            ],
                            "properties": {
                              "function": {
                                "type": "string",
                                "enum": [
                                  "\"count\"",
                                  "\"count_values\"",
                                  "\"empty\"",
                                  "\"not_empty\"",
                                  "\"unique\"",
                                  "\"show_unique\"",
                                  "\"percent_empty\"",
                                  "\"percent_not_empty\"",
                                  "\"sum\"",
                                  "\"average\"",
                                  "\"median\"",
                                  "\"min\"",
                                  "\"max\"",
                                  "\"range\"",
                                  "\"earliest_date\"",
                                  "\"latest_date\"",
                                  "\"date_range\"",
                                  "\"checked\"",
                                  "\"unchecked\"",
                                  "\"percent_checked\"",
                                  "\"percent_unchecked\"",
                                  "\"count_per_group\"",
                                  "\"percent_per_group\"",
                                  "\"show_original\""
                                ]
                              },
                              "relation_property_name": {
                                "type": "string"
                              },
                              "relation_property_id": {
                                "type": "string"
                              },
                              "rollup_property_name": {
                                "type": "string"
                              },
                              "rollup_property_id": {
                                "type": "string"
                              }
                            }
                          },
                          "unique_id": {
                            "type": "object",
                            "properties": {
                              "prefix": {
                                "type": "string"
                              }
                            }
                          }
                        }
                      }
                    }
                  },
                  "title": {
                    "type": "array",
                    "items": {
                      "properties": {
                        "annotations": {
                          "type": "object",
                          "description": "The styling for the rich text.",
                          "properties": {
                            "bold": {
                              "type": "boolean",
                              "description": "Whether the text is formatted as bold.",
                              "default": false
                            },
                            "italic": {
                              "type": "boolean",
                              "description": "Whether the text is formatted as italic.",
                              "default": false
                            },
                            "strikethrough": {
                              "type": "boolean",
                              "description": "Whether the text is formatted with a strikethrough.",
                              "default": false
                            },
                            "underline": {
                              "type": "boolean",
                              "description": "Whether the text is formatted with an underline.",
                              "default": false
                            },
                            "code": {
                              "type": "boolean",
                              "description": "Whether the text is formatted as code.",
                              "default": false
                            },
                            "color": {
                              "type": "string",
                              "description": "The color of the text.",
                              "default": "\"default\"",
                              "enum": [
                                "\"default\"",
                                "\"gray\"",
                                "\"brown\"",
                                "\"orange\"",
                                "\"yellow\"",
                                "\"green\"",
                                "\"blue\"",
                                "\"purple\"",
                                "\"pink\"",
                                "\"red\"",
                                "\"default_background\"",
                                "\"gray_background\"",
                                "\"brown_background\"",
                                "\"orange_background\"",
                                "\"yellow_background\"",
                                "\"green_background\"",
                                "\"blue_background\"",
                                "\"purple_background\"",
                                "\"pink_background\"",
                                "\"red_background\""
                              ]
                            }
                          }
                        },
                        "plain_text": {
                          "type": "string",
                          "description": "The plain text content of the rich text object, without any styling."
                        },
                        "href": {
                          "type": "string",
                          "description": "A URL that the rich text object links to or mentions."
                        },
                        "type": {
                          "type": "string",
                          "enum": [
                            "\"text\"",
                            "\"mention\"",
                            "\"equation\""
                          ]
                        }
                      },
                      "type": "object"
                    }
                  },
                  "icon": {
                    "type": "object",
                    "description": "Optionally provide a new icon object to update the data source's icon, or provide `null` to remove the existing icon.",
                    "properties": {
                      "type": {
                        "type": "string",
                        "description": "The type of icon parameter being provided.",
                        "enum": [
                          "\"file_upload\"",
                          "\"emoji\"",
                          "\"external\"",
                          "\"custom_emoji\""
                        ]
                      },
                      "emoji": {
                        "type": "string",
                        "description": "When `type=emoji`, an emoji character."
                      },
                      "file_upload": {
                        "type": "object",
                        "description": "When `type=file_upload`, an object containing the `id` of the File Upload.",
                        "required": [
                          "id"
                        ],
                        "properties": {
                          "id": {
                            "type": "string",
                            "description": "ID of a FileUpload object that has the status `uploaded`."
                          }
                        }
                      },
                      "external": {
                        "type": "object",
                        "description": "When `type=external`, an object containing the external URL.",
                        "required": [
                          "url"
                        ],
                        "properties": {
                          "url": {
                            "type": "string",
                            "description": "The URL of the external file."
                          }
                        }
                      },
                      "custom_emoji": {
                        "type": "object",
                        "description": "When `type=custom_emoji`, an object containing the custom emoji.",
                        "required": [
                          "id"
                        ],
                        "properties": {
                          "id": {
                            "type": "string",
                            "description": "The ID of the custom emoji."
                          },
                          "name": {
                            "type": "string",
                            "description": "The name of the custom emoji."
                          },
                          "url": {
                            "type": "string",
                            "description": "The URL of the custom emoji."
                          }
                        }
                      }
                    }
                  },
                  "in_trash": {
                    "type": "boolean",
                    "description": "Pass `true` to move a data source to the trash, or `false` to restore it from the trash."
                  },
                  "parent": {
                    "type": "object",
                    "description": "The parent of the data source, when moving it to a different database. If not provided, the parent will not be updated.",
                    "required": [
                      "database_id"
                    ],
                    "properties": {
                      "type": {
                        "type": "string",
                        "description": "Always `database_id`.",
                        "enum": [
                          "\"database_id\""
                        ]
                      },
                      "database_id": {
                        "type": "string",
                        "description": "The ID of the parent database (with or without dashes), for example, 195de9221179449fab8075a27c979105"
                      }
                    }
                  }
                }
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "200",
            "content": {
              "application/json": {
                "examples": {
                  "Result": {
                    "value": "{\n\t\"object\": \"data_source\",\n\t\"id\": \"bc1211ca-e3f1-4939-ae34-5260b16f627c\",\n\t\"created_time\": \"2021-07-08T23:50:00.000Z\",\n\t\"last_edited_time\": \"2021-07-08T23:50:00.000Z\",\n\t\"properties\": {\n\t\t\"+1\": {\n\t\t\t\"id\": \"Wp%3DC\",\n\t\t\t\"name\": \"+1\",\n\t\t\t\"type\": \"people\",\n\t\t\t\"people\": {}\n\t\t},\n\t\t\"In stock\": {\n\t\t\t\"id\": \"fk%5EY\",\n\t\t\t\"name\": \"In stock\",\n\t\t\t\"type\": \"checkbox\",\n\t\t\t\"checkbox\": {}\n\t\t},\n\t\t\"Price\": {\n\t\t\t\"id\": \"evWq\",\n\t\t\t\"name\": \"Price\",\n\t\t\t\"type\": \"number\",\n\t\t\t\"number\": {\n\t\t\t\t\"format\": \"dollar\"\n\t\t\t}\n\t\t},\n\t\t\"Description\": {\n\t\t\t\"id\": \"V}lX\",\n\t\t\t\"name\": \"Description\",\n\t\t\t\"type\": \"rich_text\",\n\t\t\t\"rich_text\": {}\n\t\t},\n\t\t\"Last ordered\": {\n\t\t\t\"id\": \"eVnV\",\n\t\t\t\"name\": \"Last ordered\",\n\t\t\t\"type\": \"date\",\n\t\t\t\"date\": {}\n\t\t},\n\t\t\"Meals\": {\n\t\t\t\"id\": \"%7DWA~\",\n\t\t\t\"name\": \"Meals\",\n\t\t\t\"type\": \"relation\",\n\t\t\t\"relation\": {\n\t\t\t\t\"database_id\": \"668d797c-76fa-4934-9b05-ad288df2d136\",\n\t\t\t\t\"synced_property_name\": \"Related to Grocery List (Meals)\"\n\t\t\t}\n\t\t},\n\t\t\"Number of meals\": {\n\t\t\t\"id\": \"Z\\\\Eh\",\n\t\t\t\"name\": \"Number of meals\",\n\t\t\t\"type\": \"rollup\",\n\t\t\t\"rollup\": {\n\t\t\t\t\"rollup_property_name\": \"Name\",\n\t\t\t\t\"relation_property_name\": \"Meals\",\n\t\t\t\t\"rollup_property_id\": \"title\",\n\t\t\t\t\"relation_property_id\": \"mxp^\",\n\t\t\t\t\"function\": \"count\"\n\t\t\t}\n\t\t},\n\t\t\"Store availability\": {\n\t\t\t\"id\": \"s}Kq\",\n\t\t\t\"name\": \"Store availability\",\n\t\t\t\"type\": \"multi_select\",\n\t\t\t\"multi_select\": {\n\t\t\t\t\"options\": [\n\t\t\t\t\t{\n\t\t\t\t\t\t\"id\": \"cb79b393-d1c1-4528-b517-c450859de766\",\n\t\t\t\t\t\t\"name\": \"Duc Loi Market\",\n\t\t\t\t\t\t\"color\": \"blue\"\n\t\t\t\t\t},\n\t\t\t\t\t{\n\t\t\t\t\t\t\"id\": \"58aae162-75d4-403b-a793-3bc7308e4cd2\",\n\t\t\t\t\t\t\"name\": \"Rainbow Grocery\",\n\t\t\t\t\t\t\"color\": \"gray\"\n\t\t\t\t\t},\n\t\t\t\t\t{\n\t\t\t\t\t\t\"id\": \"22d0f199-babc-44ff-bd80-a9eae3e3fcbf\",\n\t\t\t\t\t\t\"name\": \"Nijiya Market\",\n\t\t\t\t\t\t\"color\": \"purple\"\n\t\t\t\t\t},\n\t\t\t\t\t{\n\t\t\t\t\t\t\"id\": \"0d069987-ffb0-4347-bde2-8e4068003dbc\",\n\t\t\t\t\t\t\"name\": \"Gus's Community Market\",\n\t\t\t\t\t\t\"color\": \"yellow\"\n\t\t\t\t\t}\n\t\t\t\t]\n\t\t\t}\n\t\t},\n\t\t\"Photo\": {\n\t\t\t\"id\": \"yfiK\",\n\t\t\t\"name\": \"Photo\",\n\t\t\t\"type\": \"files\",\n\t\t\t\"files\": {}\n\t\t},\n\t\t\"Food group\": {\n\t\t\t\"id\": \"CM%3EH\",\n\t\t\t\"name\": \"Food group\",\n\t\t\t\"type\": \"select\",\n\t\t\t\"select\": {\n\t\t\t\t\"options\": [\n\t\t\t\t\t{\n\t\t\t\t\t\t\"id\": \"6d4523fa-88cb-4ffd-9364-1e39d0f4e566\",\n\t\t\t\t\t\t\"name\": \"🥦Vegetable\",\n\t\t\t\t\t\t\"color\": \"green\"\n\t\t\t\t\t},\n\t\t\t\t\t{\n\t\t\t\t\t\t\"id\": \"268d7e75-de8f-4c4b-8b9d-de0f97021833\",\n\t\t\t\t\t\t\"name\": \"🍎Fruit\",\n\t\t\t\t\t\t\"color\": \"red\"\n\t\t\t\t\t},\n\t\t\t\t\t{\n\t\t\t\t\t\t\"id\": \"1b234a00-dc97-489c-b987-829264cfdfef\",\n\t\t\t\t\t\t\"name\": \"💪Protein\",\n\t\t\t\t\t\t\"color\": \"yellow\"\n\t\t\t\t\t}\n\t\t\t\t]\n\t\t\t}\n\t\t},\n\t\t\"Name\": {\n\t\t\t\"id\": \"title\",\n\t\t\t\"name\": \"Name\",\n\t\t\t\"type\": \"title\",\n\t\t\t\"title\": {}\n\t\t}\n\t},\n\t\"parent\": {\n\t\t\"type\": \"database_id\",\n\t\t\"database_id\": \"6ee911d9-189c-4844-93e8-260c1438b6e4\"\n\t},\n\t\"database_parent\": {\n\t\t\"type\": \"page_id\",\n\t\t\"page_id\": \"98ad959b-2b6a-4774-80ee-00246fb0ea9b\"\n\t},\n\t\"archived\": false,\n\t\"is_inline\": false,\n\t\"icon\": {\n\t\t\"type\": \"emoji\",\n\t\t\"emoji\": \"🎉\"\n\t},\n\t\"cover\": {\n\t\t\"type\": \"external\",\n\t\t\"external\": {\n\t\t\t\"url\": \"https://website.domain/images/image.png\"\n\t\t}\n\t},\n\t\"url\": \"https://www.notion.so/bc1211cae3f14939ae34260b16f627c\",\n\t\"title\": [\n\t\t{\n\t\t\t\"type\": \"text\",\n\t\t\t\"text\": {\n\t\t\t\t\"content\": \"Grocery List\",\n\t\t\t\t\"link\": null\n\t\t\t},\n\t\t\t\"annotations\": {\n\t\t\t\t\"bold\": false,\n\t\t\t\t\"italic\": false,\n\t\t\t\t\"strikethrough\": false,\n\t\t\t\t\"underline\": false,\n\t\t\t\t\"code\": false,\n\t\t\t\t\"color\": \"default\"\n\t\t\t},\n\t\t\t\"plain_text\": \"Grocery List\",\n\t\t\t\"href\": null\n\t\t}\n\t]\n}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "object": {
                      "type": "string",
                      "example": "data_source"
                    },
                    "id": {
                      "type": "string",
                      "example": "bc1211ca-e3f1-4939-ae34-5260b16f627c"
                    },
                    "created_time": {
                      "type": "string",
                      "example": "2021-07-08T23:50:00.000Z"
                    },
                    "last_edited_time": {
                      "type": "string",
                      "example": "2021-07-08T23:50:00.000Z"
                    },
                    "properties": {
                      "type": "object",
                      "properties": {
                        "+1": {
                          "type": "object",
                          "properties": {
                            "id": {
                              "type": "string",
                              "example": "Wp%3DC"
                            },
                            "name": {
                              "type": "string",
                              "example": "+1"
                            },
                            "type": {
                              "type": "string",
                              "example": "people"
                            },
                            "people": {
                              "type": "object",
                              "properties": {}
                            }
                          }
                        },
                        "In stock": {
                          "type": "object",
                          "properties": {
                            "id": {
                              "type": "string",
                              "example": "fk%5EY"
                            },
                            "name": {
                              "type": "string",
                              "example": "In stock"
                            },
                            "type": {
                              "type": "string",
                              "example": "checkbox"
                            },
                            "checkbox": {
                              "type": "object",
                              "properties": {}
                            }
                          }
                        },
                        "Price": {
                          "type": "object",
                          "properties": {
                            "id": {
                              "type": "string",
                              "example": "evWq"
                            },
                            "name": {
                              "type": "string",
                              "example": "Price"
                            },
                            "type": {
                              "type": "string",
                              "example": "number"
                            },
                            "number": {
                              "type": "object",
                              "properties": {
                                "format": {
                                  "type": "string",
                                  "example": "dollar"
                                }
                              }
                            }
                          }
                        },
                        "Description": {
                          "type": "object",
                          "properties": {
                            "id": {
                              "type": "string",
                              "example": "V}lX"
                            },
                            "name": {
                              "type": "string",
                              "example": "Description"
                            },
                            "type": {
                              "type": "string",
                              "example": "rich_text"
                            },
                            "rich_text": {
                              "type": "object",
                              "properties": {}
                            }
                          }
                        },
                        "Last ordered": {
                          "type": "object",
                          "properties": {
                            "id": {
                              "type": "string",
                              "example": "eVnV"
                            },
                            "name": {
                              "type": "string",
                              "example": "Last ordered"
                            },
                            "type": {
                              "type": "string",
                              "example": "date"
                            },
                            "date": {
                              "type": "object",
                              "properties": {}
                            }
                          }
                        },
                        "Meals": {
                          "type": "object",
                          "properties": {
                            "id": {
                              "type": "string",
                              "example": "%7DWA~"
                            },
                            "name": {
                              "type": "string",
                              "example": "Meals"
                            },
                            "type": {
                              "type": "string",
                              "example": "relation"
                            },
                            "relation": {
                              "type": "object",
                              "properties": {
                                "database_id": {
                                  "type": "string",
                                  "example": "668d797c-76fa-4934-9b05-ad288df2d136"
                                },
                                "synced_property_name": {
                                  "type": "string",
                                  "example": "Related to Grocery List (Meals)"
                                }
                              }
                            }
                          }
                        },
                        "Number of meals": {
                          "type": "object",
                          "properties": {
                            "id": {
                              "type": "string",
                              "example": "Z\\Eh"
                            },
                            "name": {
                              "type": "string",
                              "example": "Number of meals"
                            },
                            "type": {
                              "type": "string",
                              "example": "rollup"
                            },
                            "rollup": {
                              "type": "object",
                              "properties": {
                                "rollup_property_name": {
                                  "type": "string",
                                  "example": "Name"
                                },
                                "relation_property_name": {
                                  "type": "string",
                                  "example": "Meals"
                                },
                                "rollup_property_id": {
                                  "type": "string",
                                  "example": "title"
                                },
                                "relation_property_id": {
                                  "type": "string",
                                  "example": "mxp^"
                                },
                                "function": {
                                  "type": "string",
                                  "example": "count"
                                }
                              }
                            }
                          }
                        },
                        "Store availability": {
                          "type": "object",
                          "properties": {
                            "id": {
                              "type": "string",
                              "example": "s}Kq"
                            },
                            "name": {
                              "type": "string",
                              "example": "Store availability"
                            },
                            "type": {
                              "type": "string",
                              "example": "multi_select"
                            },
                            "multi_select": {
                              "type": "object",
                              "properties": {
                                "options": {
                                  "type": "array",
                                  "items": {
                                    "type": "object",
                                    "properties": {
                                      "id": {
                                        "type": "string",
                                        "example": "cb79b393-d1c1-4528-b517-c450859de766"
                                      },
                                      "name": {
                                        "type": "string",
                                        "example": "Duc Loi Market"
                                      },
                                      "color": {
                                        "type": "string",
                                        "example": "blue"
                                      }
                                    }
                                  }
                                }
                              }
                            }
                          }
                        },
                        "Photo": {
                          "type": "object",
                          "properties": {
                            "id": {
                              "type": "string",
                              "example": "yfiK"
                            },
                            "name": {
                              "type": "string",
                              "example": "Photo"
                            },
                            "type": {
                              "type": "string",
                              "example": "files"
                            },
                            "files": {
                              "type": "object",
                              "properties": {}
                            }
                          }
                        },
                        "Food group": {
                          "type": "object",
                          "properties": {
                            "id": {
                              "type": "string",
                              "example": "CM%3EH"
                            },
                            "name": {
                              "type": "string",
                              "example": "Food group"
                            },
                            "type": {
                              "type": "string",
                              "example": "select"
                            },
                            "select": {
                              "type": "object",
                              "properties": {
                                "options": {
                                  "type": "array",
                                  "items": {
                                    "type": "object",
                                    "properties": {
                                      "id": {
                                        "type": "string",
                                        "example": "6d4523fa-88cb-4ffd-9364-1e39d0f4e566"
                                      },
                                      "name": {
                                        "type": "string",
                                        "example": "🥦Vegetable"
                                      },
                                      "color": {
                                        "type": "string",
                                        "example": "green"
                                      }
                                    }
                                  }
                                }
                              }
                            }
                          }
                        },
                        "Name": {
                          "type": "object",
                          "properties": {
                            "id": {
                              "type": "string",
                              "example": "title"
                            },
                            "name": {
                              "type": "string",
                              "example": "Name"
                            },
                            "type": {
                              "type": "string",
                              "example": "title"
                            },
                            "title": {
                              "type": "object",
                              "properties": {}
                            }
                          }
                        }
                      }
                    },
                    "parent": {
                      "type": "object",
                      "properties": {
                        "type": {
                          "type": "string",
                          "example": "database_id"
                        },
                        "database_id": {
                          "type": "string",
                          "example": "6ee911d9-189c-4844-93e8-260c1438b6e4"
                        }
                      }
                    },
                    "database_parent": {
                      "type": "object",
                      "properties": {
                        "type": {
                          "type": "string",
                          "example": "page_id"
                        },
                        "page_id": {
                          "type": "string",
                          "example": "98ad959b-2b6a-4774-80ee-00246fb0ea9b"
                        }
                      }
                    },
                    "archived": {
                      "type": "boolean",
                      "example": false,
                      "default": true
                    },
                    "is_inline": {
                      "type": "boolean",
                      "example": false,
                      "default": true
                    },
                    "icon": {
                      "type": "object",
                      "properties": {
                        "type": {
                          "type": "string",
                          "example": "emoji"
                        },
                        "emoji": {
                          "type": "string",
                          "example": "🎉"
                        }
                      }
                    },
                    "cover": {
                      "type": "object",
                      "properties": {
                        "type": {
                          "type": "string",
                          "example": "external"
                        },
                        "external": {
                          "type": "object",
                          "properties": {
                            "url": {
                              "type": "string",
                              "example": "https://website.domain/images/image.png"
                            }
                          }
                        }
                      }
                    },
                    "url": {
                      "type": "string",
                      "example": "https://www.notion.so/bc1211cae3f14939ae34260b16f627c"
                    },
                    "title": {
                      "type": "array",
                      "items": {
                        "type": "object",
                        "properties": {
                          "type": {
                            "type": "string",
                            "example": "text"
                          },
                          "text": {
                            "type": "object",
                            "properties": {
                              "content": {
                                "type": "string",
                                "example": "Grocery List"
                              },
                              "link": {}
                            }
                          },
                          "annotations": {
                            "type": "object",
                            "properties": {
                              "bold": {
                                "type": "boolean",
                                "example": false,
                                "default": true
                              },
                              "italic": {
                                "type": "boolean",
                                "example": false,
                                "default": true
                              },
                              "strikethrough": {
                                "type": "boolean",
                                "example": false,
                                "default": true
                              },
                              "underline": {
                                "type": "boolean",
                                "example": false,
                                "default": true
                              },
                              "code": {
                                "type": "boolean",
                                "example": false,
                                "default": true
                              },
                              "color": {
                                "type": "string",
                                "example": "default"
                              }
                            }
                          },
                          "plain_text": {
                            "type": "string",
                            "example": "Grocery List"
                          },
                          "href": {}
                        }
                      }
                    }
                  }
                }
              }
            }
          },
          "400": {
            "description": "400",
            "content": {
              "application/json": {
                "examples": {
                  "Result": {
                    "value": "{}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {}
                }
              }
            }
          }
        },
        "deprecated": false,
        "security": [],
        "x-readme": {
          "code-samples": [
            {
              "language": "curl",
              "code": "curl --request POST \\\n     --url 'https://api.notion.com/v1/data_sources/b55c9c91-384d-452b-81db-d1ef79372b75' \\\n     --header 'accept: application/json' \\\n     --header 'content-type: application/json' \\\n     --data '\n{\n\t\"properties\": {\n    \"Count\": null,\n    \"Website\": {\n      \"type\": \"url\",\n      \"url\": {}\n    }\n\t},\n\t\"title\": [\n\t\t{\n\t\t\t\"type\": \"text\",\n\t\t\t\"text\": {\"content\": \"New data source title\"}\n\t\t}\n\t]\n}\n'"
            },
            {
              "language": "node",
              "code": "import { Client } from \"@notionhq/client\"\n\nconst notion = new Client({\n  auth: \"{ACCESS_TOKEN}\",\n  notionVersion: \"2025-09-03\",\n})\n\ntry {\n  const response = await notion.dataSources.update({\n    data_source_id: \"6ee911d9-189c-4844-93e8-260c1438b6e4\",\n    properties: {\n      Count: null,\n      Website: {\n        type: \"url\",\n        url: {}\n      }\n    },\n    title: [\n      {\n        type: \"text\",\n        text: {content: \"New child data source\"}\n      }\n    ]\n  })\n\n  const dataSourceId = response.id\n  console.log(\"Successfully updated data source with ID:\", dataSourceId)\n\n} catch (error) {\n  // Handle `APIResponseError`\n  console.error(error)\n}"
            }
          ],
          "samples-languages": [
            "curl",
            "node"
          ]
        }
      }
    }
  },
  "x-readme": {
    "headers": [],
    "explorer-enabled": false,
    "proxy-enabled": true
  },
  "x-readme-fauxas": true,
  "_id": "606ecc2cd9e93b0044cf6e47:68b1eb94294f81a52a785591"
}
```

# Update data source properties

The API represents columns of a data source in the Notion app UI as data source **properties**.

To use the API to update a data source's properties, send a [PATCH request](ref:update-a-data-source) with a `properties` body param.

## Remove a property

To remove a data source property, set the property object to null.

```json removing properties by ID
"properties": {
  "J@cT": null,
}
```

```json removing properties by name
"properties": {
  "propertyToDelete": null
}
```

## Rename a property

To change the name of a data source property, indicate the new name in the `name` property object value.

```json renaming properties by ID
"properties": {
	"J@cT": {
		"name": "New Property Name"
  }
}
```

```json renaming properties by name
"properties": {
  "Old Property Name": {
    "name": "New Property Name
  }
}
```

| Property | Type     | Description                                       |
| :------- | :------- | :------------------------------------------------ |
| `name`   | `string` | The name of the property as it appears in Notion. |

## Update property type

To update the property type, the property schema object should contain the key of the type. This type contains behavior of this property. Possible values of this key are `"title"`, `"rich_text"`, `"number"`, `"select"`, `"multi_select"`, `"date"`, `"people"`, `"files"`, `"checkbox"`, `"url"`, `"email"`, `"phone_number"`, `"formula"`, `"relation"`, `"rollup"`, `"created_time"`, `"created_by"`, `"last_edited_time"`, `"last_edited_by"`. Within this property, the configuration is a [property schema object](https://developers.notion.com/reference/property-schema-object).

> ❗️ Limitations
>
> Note that the property type of the `title` cannot be changed.
>
> It's not possible to update the `name` or `options` values of a `status` property via the API.

### Select configuration updates

To update an existing select configuration, the property schema object optionally contains the following configuration within the `select` property:

| Property  | Type                                                                                                                                    | Description                                                                                                                                                                | Example value |
| :-------- | :-------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------ |
| `options` | optional array of [existing select options](#existing-select-options) and [select option objects](ref:create-a-database#select-options) | Settings for select properties. If an existing option is omitted, it will be removed from the data source property. New options will be added to the data source property. |               |

#### Existing select options

Note that the name and color of an existing option cannot be updated.

| Property | Type              | Description         | Example value                             |
| :------- | :---------------- | :------------------ | :---------------------------------------- |
| `name`   | optional `string` | Name of the option. | `"Fruit"`                                 |
| `id`     | optional `string` | ID of the option.   | `"ff8e9269-9579-47f7-8f6e-83a84716863c" ` |

### Multi-select configuration updates

To update an existing select configuration, the property schema object optionally contains the following configuration within the `multi_select` property:

| Property  | Type                                                                                                                                                      | Description                                                                                                                                                                      | Example value |
| :-------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------ |
| `options` | optional array of [existing select options](#existing-multi-select-options) and [multi-select option objects](ref:create-a-database#multi-select-options) | Settings for multi select properties. If an existing option is omitted, it will be removed from the data source property. New options will be added to the data source property. |               |

#### Existing multi-select options

Note that the name and color of an existing option cannot be updated.

| Property | Type              | Description                                 | Example value                             |
| :------- | :---------------- | :------------------------------------------ | :---------------------------------------- |
| `name`   | `string`          | Name of the option as it appears in Notion. | `"Fruit"`                                 |
| `id`     | optional `string` | ID of the option.                           | `"ff8e9269-9579-47f7-8f6e-83a84716863c" ` |

## Limitations

### Formula maximum depth

Formulas in Notion can have high levels of complexity beyond what the API can compute in a single request. For `formula` property values that exceed _have or exceed depth of 10_  referenced tables, the API will return a "Formula depth" error as a [`"validation_error"`](https://developers.notion.com/reference/errors)

As a workaround, you can retrieve the `formula` property object from the [Retrieve a data source](ref:retrieve-a-data-source) endpoint and use the formula expression to compute the value of more complex formulas.

### Unsupported Rollup Aggregations

Due to the encoded cursor nature of computing rollup values, a subset of aggregation types are not supported. Instead the endpoint returns a list of _all_ property_item objects for the following rollup aggregations:

- `show_unique` (Show unique values)
- `unique` (Count unique values)
- `median` (Median)

### "Could not find page/data source" Error

A page property of type `rollup` and `formula` can involve computing a value based on the properties in another `relation` page. As such the integration needs permissions to the other `relation` page. If the integration doesn't have permissions page needed to compute the property value, the API will return a [`"object_not_found"`](https://developers.notion.com/reference/errors) error specifying the page the integration lacks permissions to.

### Property value doesn't match UI after pagination

If a property value involves [pagination](https://developers.notion.com/reference/pagination) and the underlying properties or pages used to compute the property value change whilst the integration is paginating through results, the final value will impacted and is not guaranteed to be accurate.

# Retrieve a data source

Retrieves a [data source](ref:data-source) object — information that describes the structure and columns of a data source — for a provided data source ID. The response adheres to any limits to an integration’s capabilities and the permissions of the `parent` database.

To fetch data source _rows_ (i.e. the child pages of a data source) rather than columns, use the [Query a data source](ref:query-a-data-source) endpoint.

### Finding a data source ID

Navigate to the database URL in your Notion workspace. The ID is the string of characters in the URL that is between the slash following the workspace name (if applicable) and the question mark. The ID is a 32 characters alphanumeric string.

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/64967fd-small-62e5027-notion_database_id.png",
        null,
        "Notion database ID"
      ],
      "align": "center",
      "caption": "Notion database ID"
    }
  ]
}
[/block]


Then, use the [Retrieve a database](ref:retrieve-a-database-1-6ee911d9) API to get a list of `data_sources` for that database. There is often only one data source, but when there are multiple, you may have the ID or name of the one you want to retrieve in mind (or you can retrieve each of them). Use that data source ID with this endpoint to get its `properties`.

To get a data source ID from the Notion app directly, the settings menu for a database includes a "Copy data source ID" button under "Manage data sources":

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/30ed6ac31d8c25eb2ff653dd3b11bfd2e30e8af4df6a6d5e0670b4ad7a96cf73-image.png",
        null,
        "Screenshot of the \"Manage data sources\" menu for a database in Notion, with \"Copy data source ID\" button."
      ],
      "align": "center",
      "sizing": "300px",
      "border": true,
      "caption": "Screenshot of the \"Manage data sources\" menu for a database in Notion, with \"Copy data source ID\" button."
    }
  ]
}
[/block]


Refer to the [Build your first integration guide](https://developers.notion.com/docs/create-a-notion-integration#step-3-save-the-database-id) for more details.

### Errors

Each Public API endpoint can return several possible error codes. See the [Error codes section](https://developers.notion.com/reference/status-codes#error-codes) of the Status codes documentation for more information.

### Additional resources

- [How to share a database with your integration](https://developers.notion.com/docs/create-a-notion-integration#give-your-integration-page-permissions)
- [Working with databases guide](https://developers.notion.com/docs/working-with-databases)

> 📘 Data source relations must be shared with your integration
>
> To retrieve data source properties from [database relations](https://www.notion.so/help/relations-and-rollups#what-is-a-database-relation), the related database must be shared with your integration in addition to the database being retrieved. If the related database is not shared, properties based on relations will not be included in the API response.

> 🚧 The Notion API does not support retrieving linked data sources
>
> To fetch the information in a [linked data source](https://www.notion.so/help/guides/using-linked-databases), share the original source database with your Notion integration.

# OpenAPI definition
```json
{
  "openapi": "3.1.0",
  "info": {
    "title": "Notion API",
    "version": "1"
  },
  "servers": [
    {
      "url": "https://api.notion.com"
    }
  ],
  "components": {
    "securitySchemes": {
      "sec0": {
        "type": "oauth2",
        "flows": {}
      }
    }
  },
  "security": [
    {
      "sec0": []
    }
  ],
  "paths": {
    "/v1/data_sources/{data_source_id}": {
      "get": {
        "summary": "Retrieve a data source",
        "description": "",
        "operationId": "retrieve-a-data-source",
        "parameters": [
          {
            "name": "data_source_id",
            "in": "path",
            "description": "ID of a Notion data source. This is a UUIDv4, with or without dashes.",
            "schema": {
              "type": "string"
            },
            "required": true
          }
        ],
        "responses": {
          "200": {
            "description": "200",
            "content": {
              "application/json": {
                "examples": {
                  "Result": {
                    "value": "{\n\t\"object\": \"data_source\",\n\t\"id\": \"bc1211ca-e3f1-4939-ae34-5260b16f627c\",\n\t\"created_time\": \"2021-07-08T23:50:00.000Z\",\n\t\"last_edited_time\": \"2021-07-08T23:50:00.000Z\",\n\t\"properties\": {\n\t\t\"+1\": {\n\t\t\t\"id\": \"Wp%3DC\",\n\t\t\t\"name\": \"+1\",\n\t\t\t\"type\": \"people\",\n\t\t\t\"people\": {}\n\t\t},\n\t\t\"In stock\": {\n\t\t\t\"id\": \"fk%5EY\",\n\t\t\t\"name\": \"In stock\",\n\t\t\t\"type\": \"checkbox\",\n\t\t\t\"checkbox\": {}\n\t\t},\n\t\t\"Price\": {\n\t\t\t\"id\": \"evWq\",\n\t\t\t\"name\": \"Price\",\n\t\t\t\"type\": \"number\",\n\t\t\t\"number\": {\n\t\t\t\t\"format\": \"dollar\"\n\t\t\t}\n\t\t},\n\t\t\"Description\": {\n\t\t\t\"id\": \"V}lX\",\n\t\t\t\"name\": \"Description\",\n\t\t\t\"type\": \"rich_text\",\n\t\t\t\"rich_text\": {}\n\t\t},\n\t\t\"Last ordered\": {\n\t\t\t\"id\": \"eVnV\",\n\t\t\t\"name\": \"Last ordered\",\n\t\t\t\"type\": \"date\",\n\t\t\t\"date\": {}\n\t\t},\n\t\t\"Meals\": {\n\t\t\t\"id\": \"%7DWA~\",\n\t\t\t\"name\": \"Meals\",\n\t\t\t\"type\": \"relation\",\n\t\t\t\"relation\": {\n\t\t\t\t\"database_id\": \"668d797c-76fa-4934-9b05-ad288df2d136\",\n\t\t\t\t\"synced_property_name\": \"Related to Grocery List (Meals)\"\n\t\t\t}\n\t\t},\n\t\t\"Number of meals\": {\n\t\t\t\"id\": \"Z\\\\Eh\",\n\t\t\t\"name\": \"Number of meals\",\n\t\t\t\"type\": \"rollup\",\n\t\t\t\"rollup\": {\n\t\t\t\t\"rollup_property_name\": \"Name\",\n\t\t\t\t\"relation_property_name\": \"Meals\",\n\t\t\t\t\"rollup_property_id\": \"title\",\n\t\t\t\t\"relation_property_id\": \"mxp^\",\n\t\t\t\t\"function\": \"count\"\n\t\t\t}\n\t\t},\n\t\t\"Store availability\": {\n\t\t\t\"id\": \"s}Kq\",\n\t\t\t\"name\": \"Store availability\",\n\t\t\t\"type\": \"multi_select\",\n\t\t\t\"multi_select\": {\n\t\t\t\t\"options\": [\n\t\t\t\t\t{\n\t\t\t\t\t\t\"id\": \"cb79b393-d1c1-4528-b517-c450859de766\",\n\t\t\t\t\t\t\"name\": \"Duc Loi Market\",\n\t\t\t\t\t\t\"color\": \"blue\"\n\t\t\t\t\t},\n\t\t\t\t\t{\n\t\t\t\t\t\t\"id\": \"58aae162-75d4-403b-a793-3bc7308e4cd2\",\n\t\t\t\t\t\t\"name\": \"Rainbow Grocery\",\n\t\t\t\t\t\t\"color\": \"gray\"\n\t\t\t\t\t},\n\t\t\t\t\t{\n\t\t\t\t\t\t\"id\": \"22d0f199-babc-44ff-bd80-a9eae3e3fcbf\",\n\t\t\t\t\t\t\"name\": \"Nijiya Market\",\n\t\t\t\t\t\t\"color\": \"purple\"\n\t\t\t\t\t},\n\t\t\t\t\t{\n\t\t\t\t\t\t\"id\": \"0d069987-ffb0-4347-bde2-8e4068003dbc\",\n\t\t\t\t\t\t\"name\": \"Gus's Community Market\",\n\t\t\t\t\t\t\"color\": \"yellow\"\n\t\t\t\t\t}\n\t\t\t\t]\n\t\t\t}\n\t\t},\n\t\t\"Photo\": {\n\t\t\t\"id\": \"yfiK\",\n\t\t\t\"name\": \"Photo\",\n\t\t\t\"type\": \"files\",\n\t\t\t\"files\": {}\n\t\t},\n\t\t\"Food group\": {\n\t\t\t\"id\": \"CM%3EH\",\n\t\t\t\"name\": \"Food group\",\n\t\t\t\"type\": \"select\",\n\t\t\t\"select\": {\n\t\t\t\t\"options\": [\n\t\t\t\t\t{\n\t\t\t\t\t\t\"id\": \"6d4523fa-88cb-4ffd-9364-1e39d0f4e566\",\n\t\t\t\t\t\t\"name\": \"🥦Vegetable\",\n\t\t\t\t\t\t\"color\": \"green\"\n\t\t\t\t\t},\n\t\t\t\t\t{\n\t\t\t\t\t\t\"id\": \"268d7e75-de8f-4c4b-8b9d-de0f97021833\",\n\t\t\t\t\t\t\"name\": \"🍎Fruit\",\n\t\t\t\t\t\t\"color\": \"red\"\n\t\t\t\t\t},\n\t\t\t\t\t{\n\t\t\t\t\t\t\"id\": \"1b234a00-dc97-489c-b987-829264cfdfef\",\n\t\t\t\t\t\t\"name\": \"💪Protein\",\n\t\t\t\t\t\t\"color\": \"yellow\"\n\t\t\t\t\t}\n\t\t\t\t]\n\t\t\t}\n\t\t},\n\t\t\"Name\": {\n\t\t\t\"id\": \"title\",\n\t\t\t\"name\": \"Name\",\n\t\t\t\"type\": \"title\",\n\t\t\t\"title\": {}\n\t\t}\n\t},\n\t\"parent\": {\n\t\t\"type\": \"database_id\",\n\t\t\"database_id\": \"6ee911d9-189c-4844-93e8-260c1438b6e4\"\n\t},\n\t\"database_parent\": {\n\t\t\"type\": \"page_id\",\n\t\t\"page_id\": \"98ad959b-2b6a-4774-80ee-00246fb0ea9b\"\n\t},\n\t\"archived\": false,\n\t\"is_inline\": false,\n\t\"icon\": {\n\t\t\"type\": \"emoji\",\n\t\t\"emoji\": \"🎉\"\n\t},\n\t\"cover\": {\n\t\t\"type\": \"external\",\n\t\t\"external\": {\n\t\t\t\"url\": \"https://website.domain/images/image.png\"\n\t\t}\n\t},\n\t\"url\": \"https://www.notion.so/bc1211cae3f14939ae34260b16f627c\",\n\t\"title\": [\n\t\t{\n\t\t\t\"type\": \"text\",\n\t\t\t\"text\": {\n\t\t\t\t\"content\": \"Grocery List\",\n\t\t\t\t\"link\": null\n\t\t\t},\n\t\t\t\"annotations\": {\n\t\t\t\t\"bold\": false,\n\t\t\t\t\"italic\": false,\n\t\t\t\t\"strikethrough\": false,\n\t\t\t\t\"underline\": false,\n\t\t\t\t\"code\": false,\n\t\t\t\t\"color\": \"default\"\n\t\t\t},\n\t\t\t\"plain_text\": \"Grocery List\",\n\t\t\t\"href\": null\n\t\t}\n\t]\n}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "object": {
                      "type": "string",
                      "example": "data_source"
                    },
                    "id": {
                      "type": "string",
                      "example": "bc1211ca-e3f1-4939-ae34-5260b16f627c"
                    },
                    "created_time": {
                      "type": "string",
                      "example": "2021-07-08T23:50:00.000Z"
                    },
                    "last_edited_time": {
                      "type": "string",
                      "example": "2021-07-08T23:50:00.000Z"
                    },
                    "properties": {
                      "type": "object",
                      "properties": {
                        "+1": {
                          "type": "object",
                          "properties": {
                            "id": {
                              "type": "string",
                              "example": "Wp%3DC"
                            },
                            "name": {
                              "type": "string",
                              "example": "+1"
                            },
                            "type": {
                              "type": "string",
                              "example": "people"
                            },
                            "people": {
                              "type": "object",
                              "properties": {}
                            }
                          }
                        },
                        "In stock": {
                          "type": "object",
                          "properties": {
                            "id": {
                              "type": "string",
                              "example": "fk%5EY"
                            },
                            "name": {
                              "type": "string",
                              "example": "In stock"
                            },
                            "type": {
                              "type": "string",
                              "example": "checkbox"
                            },
                            "checkbox": {
                              "type": "object",
                              "properties": {}
                            }
                          }
                        },
                        "Price": {
                          "type": "object",
                          "properties": {
                            "id": {
                              "type": "string",
                              "example": "evWq"
                            },
                            "name": {
                              "type": "string",
                              "example": "Price"
                            },
                            "type": {
                              "type": "string",
                              "example": "number"
                            },
                            "number": {
                              "type": "object",
                              "properties": {
                                "format": {
                                  "type": "string",
                                  "example": "dollar"
                                }
                              }
                            }
                          }
                        },
                        "Description": {
                          "type": "object",
                          "properties": {
                            "id": {
                              "type": "string",
                              "example": "V}lX"
                            },
                            "name": {
                              "type": "string",
                              "example": "Description"
                            },
                            "type": {
                              "type": "string",
                              "example": "rich_text"
                            },
                            "rich_text": {
                              "type": "object",
                              "properties": {}
                            }
                          }
                        },
                        "Last ordered": {
                          "type": "object",
                          "properties": {
                            "id": {
                              "type": "string",
                              "example": "eVnV"
                            },
                            "name": {
                              "type": "string",
                              "example": "Last ordered"
                            },
                            "type": {
                              "type": "string",
                              "example": "date"
                            },
                            "date": {
                              "type": "object",
                              "properties": {}
                            }
                          }
                        },
                        "Meals": {
                          "type": "object",
                          "properties": {
                            "id": {
                              "type": "string",
                              "example": "%7DWA~"
                            },
                            "name": {
                              "type": "string",
                              "example": "Meals"
                            },
                            "type": {
                              "type": "string",
                              "example": "relation"
                            },
                            "relation": {
                              "type": "object",
                              "properties": {
                                "database_id": {
                                  "type": "string",
                                  "example": "668d797c-76fa-4934-9b05-ad288df2d136"
                                },
                                "synced_property_name": {
                                  "type": "string",
                                  "example": "Related to Grocery List (Meals)"
                                }
                              }
                            }
                          }
                        },
                        "Number of meals": {
                          "type": "object",
                          "properties": {
                            "id": {
                              "type": "string",
                              "example": "Z\\Eh"
                            },
                            "name": {
                              "type": "string",
                              "example": "Number of meals"
                            },
                            "type": {
                              "type": "string",
                              "example": "rollup"
                            },
                            "rollup": {
                              "type": "object",
                              "properties": {
                                "rollup_property_name": {
                                  "type": "string",
                                  "example": "Name"
                                },
                                "relation_property_name": {
                                  "type": "string",
                                  "example": "Meals"
                                },
                                "rollup_property_id": {
                                  "type": "string",
                                  "example": "title"
                                },
                                "relation_property_id": {
                                  "type": "string",
                                  "example": "mxp^"
                                },
                                "function": {
                                  "type": "string",
                                  "example": "count"
                                }
                              }
                            }
                          }
                        },
                        "Store availability": {
                          "type": "object",
                          "properties": {
                            "id": {
                              "type": "string",
                              "example": "s}Kq"
                            },
                            "name": {
                              "type": "string",
                              "example": "Store availability"
                            },
                            "type": {
                              "type": "string",
                              "example": "multi_select"
                            },
                            "multi_select": {
                              "type": "object",
                              "properties": {
                                "options": {
                                  "type": "array",
                                  "items": {
                                    "type": "object",
                                    "properties": {
                                      "id": {
                                        "type": "string",
                                        "example": "cb79b393-d1c1-4528-b517-c450859de766"
                                      },
                                      "name": {
                                        "type": "string",
                                        "example": "Duc Loi Market"
                                      },
                                      "color": {
                                        "type": "string",
                                        "example": "blue"
                                      }
                                    }
                                  }
                                }
                              }
                            }
                          }
                        },
                        "Photo": {
                          "type": "object",
                          "properties": {
                            "id": {
                              "type": "string",
                              "example": "yfiK"
                            },
                            "name": {
                              "type": "string",
                              "example": "Photo"
                            },
                            "type": {
                              "type": "string",
                              "example": "files"
                            },
                            "files": {
                              "type": "object",
                              "properties": {}
                            }
                          }
                        },
                        "Food group": {
                          "type": "object",
                          "properties": {
                            "id": {
                              "type": "string",
                              "example": "CM%3EH"
                            },
                            "name": {
                              "type": "string",
                              "example": "Food group"
                            },
                            "type": {
                              "type": "string",
                              "example": "select"
                            },
                            "select": {
                              "type": "object",
                              "properties": {
                                "options": {
                                  "type": "array",
                                  "items": {
                                    "type": "object",
                                    "properties": {
                                      "id": {
                                        "type": "string",
                                        "example": "6d4523fa-88cb-4ffd-9364-1e39d0f4e566"
                                      },
                                      "name": {
                                        "type": "string",
                                        "example": "🥦Vegetable"
                                      },
                                      "color": {
                                        "type": "string",
                                        "example": "green"
                                      }
                                    }
                                  }
                                }
                              }
                            }
                          }
                        },
                        "Name": {
                          "type": "object",
                          "properties": {
                            "id": {
                              "type": "string",
                              "example": "title"
                            },
                            "name": {
                              "type": "string",
                              "example": "Name"
                            },
                            "type": {
                              "type": "string",
                              "example": "title"
                            },
                            "title": {
                              "type": "object",
                              "properties": {}
                            }
                          }
                        }
                      }
                    },
                    "parent": {
                      "type": "object",
                      "properties": {
                        "type": {
                          "type": "string",
                          "example": "database_id"
                        },
                        "database_id": {
                          "type": "string",
                          "example": "6ee911d9-189c-4844-93e8-260c1438b6e4"
                        }
                      }
                    },
                    "database_parent": {
                      "type": "object",
                      "properties": {
                        "type": {
                          "type": "string",
                          "example": "page_id"
                        },
                        "page_id": {
                          "type": "string",
                          "example": "98ad959b-2b6a-4774-80ee-00246fb0ea9b"
                        }
                      }
                    },
                    "archived": {
                      "type": "boolean",
                      "example": false,
                      "default": true
                    },
                    "is_inline": {
                      "type": "boolean",
                      "example": false,
                      "default": true
                    },
                    "icon": {
                      "type": "object",
                      "properties": {
                        "type": {
                          "type": "string",
                          "example": "emoji"
                        },
                        "emoji": {
                          "type": "string",
                          "example": "🎉"
                        }
                      }
                    },
                    "cover": {
                      "type": "object",
                      "properties": {
                        "type": {
                          "type": "string",
                          "example": "external"
                        },
                        "external": {
                          "type": "object",
                          "properties": {
                            "url": {
                              "type": "string",
                              "example": "https://website.domain/images/image.png"
                            }
                          }
                        }
                      }
                    },
                    "url": {
                      "type": "string",
                      "example": "https://www.notion.so/bc1211cae3f14939ae34260b16f627c"
                    },
                    "title": {
                      "type": "array",
                      "items": {
                        "type": "object",
                        "properties": {
                          "type": {
                            "type": "string",
                            "example": "text"
                          },
                          "text": {
                            "type": "object",
                            "properties": {
                              "content": {
                                "type": "string",
                                "example": "Grocery List"
                              },
                              "link": {}
                            }
                          },
                          "annotations": {
                            "type": "object",
                            "properties": {
                              "bold": {
                                "type": "boolean",
                                "example": false,
                                "default": true
                              },
                              "italic": {
                                "type": "boolean",
                                "example": false,
                                "default": true
                              },
                              "strikethrough": {
                                "type": "boolean",
                                "example": false,
                                "default": true
                              },
                              "underline": {
                                "type": "boolean",
                                "example": false,
                                "default": true
                              },
                              "code": {
                                "type": "boolean",
                                "example": false,
                                "default": true
                              },
                              "color": {
                                "type": "string",
                                "example": "default"
                              }
                            }
                          },
                          "plain_text": {
                            "type": "string",
                            "example": "Grocery List"
                          },
                          "href": {}
                        }
                      }
                    }
                  }
                }
              }
            }
          },
          "400": {
            "description": "400",
            "content": {
              "application/json": {
                "examples": {
                  "Result": {
                    "value": "{}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {}
                }
              }
            }
          }
        },
        "deprecated": false,
        "security": [],
        "x-readme": {
          "code-samples": [
            {
              "language": "curl",
              "code": "curl --request GET \\\n     --url 'https://api.notion.com/v1/data_sources/b55c9c91-384d-452b-81db-d1ef79372b75' \\\n     -H 'Notion-Version: 2025-09-03' \\\n     -H 'Authorization: Bearer '\"$NOTION_API_KEY\"''"
            },
            {
              "language": "node",
              "code": "const { Client } = require('@notionhq/client');\n\nconst notion = new Client({ auth: process.env.NOTION_API_KEY });\n\n(async () => {\n  const dataSourceId = '59833787-2cf9-4fdf-8782-e53db20768a5';\n  const response = await notion.dataSources.retrieve({ data_source_id: dataSourceId });\n  console.log(response);\n})();"
            }
          ],
          "samples-languages": [
            "curl",
            "node"
          ]
        }
      }
    }
  },
  "x-readme": {
    "headers": [],
    "explorer-enabled": false,
    "proxy-enabled": true
  },
  "x-readme-fauxas": true,
  "_id": "606ecc2cd9e93b0044cf6e47:68b1eba8c6fd9e0ed5b78608"
}
```

# Query a data source

Gets a list of [Pages](ref:page) and/or [Data Sources](ref:data-source)  contained in the data source, filtered and ordered according to the filter conditions and sort criteria provided in the request. The response may contain fewer than `page_size` of results. If the response includes a `next_cursor` value, refer to the [pagination reference](https://developers.notion.com/reference/intro#pagination) for details about how to use a cursor to iterate through the list.

> 📘 Databases, data sources, and wikis
>
> [Wiki](https://www.notion.so/help/wikis-and-verified-pages) data sources can contain both pages and databases as children. In all other cases, the children can only be pages.
>
> When there's a [database](ref:database) result, this API returns all data sources that are children of _that_ database, instead of surfacing the database directly. Surfacing the data source instead of the direct database child helps make it easier to craft your next API request (for example, retrieving the data source).

[**Filters**](ref:filter-data-source-entries) are similar to the [filters provided in the Notion UI](https://www.notion.so/help/views-filters-and-sorts) where the set of filters and filter groups chained by "And" in the UI is equivalent to having each filter in the array of the compound `"and"` filter. Similar a set of filters chained by "Or" in the UI would be represented as filters in the array of the `"or"` compound filter.
Filters operate on data source properties and can be combined. If no filter is provided, all the pages in the data source will be returned with pagination.

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/6fe4a44-Screen_Shot_2021-12-23_at_11.46.21_AM.png",
        "Screen Shot 2021-12-23 at 11.46.21 AM.png",
        1340
      ],
      "align": "center",
      "caption": "The above filters in the UI can be represented as the following filter object"
    }
  ]
}
[/block]


```json Filter Object
{
  "and": [
    {
      "property": "Done",
      "checkbox": {
        "equals": true
      }
    },
    {
      "or": [
        {
          "property": "Tags",
          "contains": "A"
        },
        {
          "property": "Tags",
          "contains": "B"
        }
      ]
  	}
  ]
}
```

In addition to chained filters, data sources can be queried with single filters.

```json
{
    "property": "Done",
    "checkbox": {
        "equals": true
   }
 }
```

[**Sorts**](ref:sort-data-source-entries) are similar to the [sorts provided in the Notion UI](https://notion.so/notion/Intro-to-databases-fd8cd2d212f74c50954c11086d85997e#0eb303043b1742468e5aff2f3f670505). Sorts operate on database properties or page timestamps and can be combined. The order of the sorts in the request matter, with earlier sorts taking precedence over later ones.

The properties of the data source schema returned in the response body can be filtered with the `filter_properties` query parameter.

```
https://api.notion.com/v1/data_sources/[data_source_id]/query?filter_properties=[property_id_1]
```

Multiple filter properties can be provided by chaining the `filter_properties` query param.

```
https://api.notion.com/v1/data_sources/[data_source_id]/query?filter_properties=[property_id_1]&filter_properties=[property_id_2]
```

Property IDs can be determined with the [Retrieve a data source](ref:retrieve-a-data-source) endpoint.

If you are using the [Notion JavaScript SDK](https://github.com/makenotion/notion-sdk-js), the `filter_properties` endpoint expects an array of property ID strings.

```javascript
notion.dataSources.query({
	data_source_id: id,
	filter_properties: ["propertyID1", "propertyID2"]
})
```

> 📘 Permissions
>
> Before an integration can query a data source, its parent database must be shared with the integration. Attempting to query a database that has not been shared will return an HTTP response with a 404 status code.
>
> To share a database with an integration, click the ••• menu at the top right of a database page, scroll to `Add connections`, and use the search bar to find and select the integration from the dropdown list.

> 📘 Integration capabilities
>
> This endpoint requires an integration to have read content capabilities. Attempting to call this API without read content capabilities will return an HTTP response with a 403 status code. For more information on integration capabilities, see the [capabilities guide](ref:capabilities).

> 📘 To display the page titles of related pages rather than just the ID:
>
> 1. Add a rollup property to the data source which uses a formula to get the related page's title. This works well if you have access to [update](ref:update-a-data-source) the data source's schema.
>
> 2. Otherwise, [retrieve the individual related pages](ref:retrieve-a-page) using each page ID.

> 🚧 Formula and rollup limitations
>
> - If a formula depends on a page property that is a relation, and that relation has more than 25 references, only 25 will be evaluated as part of the formula.
> - Rollups and formulas that depend on multiple layers of relations may not return correct results.
> - Notion recommends individually [retrieving each page property item](ref:retrieve-a-page-property) to get the most accurate result.

### Errors

Returns a 404 HTTP response if the data source doesn't exist, or if the integration doesn't have access to the data source.

Returns a 400 or a 429 HTTP response if the request exceeds the [request limits](ref:request-limits).

_Note: Each Public API endpoint can return several possible error codes. See the [Error codes section](https://developers.notion.com/reference/status-codes#error-codes) of the Status codes documentation for more information._

# OpenAPI definition
```json
{
  "openapi": "3.1.0",
  "info": {
    "title": "Notion API",
    "version": "1"
  },
  "servers": [
    {
      "url": "https://api.notion.com"
    }
  ],
  "components": {
    "securitySchemes": {
      "sec0": {
        "type": "oauth2",
        "flows": {}
      }
    }
  },
  "security": [
    {
      "sec0": []
    }
  ],
  "paths": {
    "/v1/data_sources/{data_source_id}/query": {
      "post": {
        "summary": "Query a data source",
        "description": "",
        "operationId": "query-a-data-source",
        "parameters": [
          {
            "name": "Notion-Version",
            "in": "header",
            "description": "The [API version](/reference/versioning) to use for this request. The latest version is `<<internalLatestNotionVersion>>`.",
            "required": true,
            "schema": {
              "type": "string"
            }
          },
          {
            "name": "data_source_id",
            "in": "path",
            "description": "ID of a Notion data source. This is a UUIDv4, with or without dashes.",
            "schema": {
              "type": "string"
            },
            "required": true
          }
        ],
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "sorts": {
                    "type": "array",
                    "description": "An array of property or timestamp sort objects.",
                    "items": {
                      "properties": {
                        "property": {
                          "type": "string"
                        },
                        "timestamp": {
                          "type": "string",
                          "enum": [
                            "\"created_time\"",
                            "\"last_edited_time\""
                          ]
                        },
                        "direction": {
                          "type": "string",
                          "enum": [
                            "\"ascending\"",
                            "\"descending\""
                          ]
                        }
                      },
                      "required": [
                        "direction"
                      ],
                      "type": "object"
                    }
                  },
                  "filter": {
                    "type": "object",
                    "properties": {
                      "timestamp": {
                        "type": "string",
                        "enum": [
                          "\"created_time\"",
                          "\"last_edited_time\""
                        ]
                      },
                      "created_time": {
                        "type": "object",
                        "properties": {
                          "equals": {
                            "type": "string",
                            "format": "date"
                          },
                          "before": {
                            "type": "string",
                            "format": "date"
                          },
                          "after": {
                            "type": "string",
                            "format": "date"
                          },
                          "on_or_before": {
                            "type": "string",
                            "format": "date"
                          },
                          "on_or_after": {
                            "type": "string",
                            "format": "date"
                          },
                          "this_week": {
                            "type": "object",
                            "description": "Empty object `{}`",
                            "properties": {}
                          },
                          "past_week": {
                            "type": "object",
                            "description": "Empty object `{}`",
                            "properties": {}
                          },
                          "past_month": {
                            "type": "object",
                            "description": "Empty object `{}`",
                            "properties": {}
                          },
                          "past_year": {
                            "type": "object",
                            "description": "Empty object `{}`",
                            "properties": {}
                          },
                          "next_week": {
                            "type": "object",
                            "description": "Empty object `{}`",
                            "properties": {}
                          },
                          "next_month": {
                            "type": "object",
                            "description": "Empty object `{}`",
                            "properties": {}
                          },
                          "next_year": {
                            "type": "object",
                            "description": "Empty object `{}`",
                            "properties": {}
                          },
                          "is_empty": {
                            "type": "string",
                            "enum": [
                              "true"
                            ]
                          },
                          "is_not_empty": {
                            "type": "boolean",
                            "description": "true"
                          }
                        }
                      },
                      "last_edited_time": {
                        "type": "object",
                        "properties": {
                          "equals": {
                            "type": "string",
                            "format": "date"
                          },
                          "before": {
                            "type": "string",
                            "format": "date"
                          },
                          "after": {
                            "type": "string",
                            "format": "date"
                          },
                          "on_or_before": {
                            "type": "string",
                            "format": "date"
                          },
                          "on_or_after": {
                            "type": "string",
                            "format": "date"
                          },
                          "this_week": {
                            "type": "object",
                            "description": "Empty object `{}`",
                            "properties": {}
                          },
                          "past_week": {
                            "type": "object",
                            "description": "Empty object `{}`",
                            "properties": {}
                          },
                          "past_month": {
                            "type": "object",
                            "description": "Empty object `{}`",
                            "properties": {}
                          },
                          "past_year": {
                            "type": "object",
                            "description": "Empty object `{}`",
                            "properties": {}
                          },
                          "next_week": {
                            "type": "object",
                            "description": "Empty object `{}`",
                            "properties": {}
                          },
                          "next_month": {
                            "type": "object",
                            "description": "Empty object `{}`",
                            "properties": {}
                          },
                          "next_year": {
                            "type": "object",
                            "description": "Empty object `{}`",
                            "properties": {}
                          },
                          "is_empty": {
                            "type": "string",
                            "enum": [
                              "true"
                            ]
                          },
                          "is_not_empty": {
                            "type": "boolean",
                            "description": "true"
                          }
                        }
                      },
                      "property": {
                        "type": "string"
                      },
                      "title": {
                        "type": "object",
                        "properties": {
                          "equals": {
                            "type": "string"
                          },
                          "does_not_equal": {
                            "type": "string"
                          },
                          "contains": {
                            "type": "string"
                          },
                          "does_not_contain": {
                            "type": "string"
                          },
                          "starts_with": {
                            "type": "string"
                          },
                          "ends_with": {
                            "type": "string"
                          },
                          "is_empty": {
                            "type": "string"
                          },
                          "is_not_empty": {
                            "type": "string"
                          }
                        }
                      },
                      "rich_text": {
                        "type": "object",
                        "properties": {
                          "equals": {
                            "type": "string"
                          },
                          "does_not_equal": {
                            "type": "string"
                          },
                          "contains": {
                            "type": "string"
                          },
                          "does_not_contain": {
                            "type": "string"
                          },
                          "starts_with": {
                            "type": "string"
                          },
                          "ends_with": {
                            "type": "string"
                          },
                          "is_empty": {
                            "type": "string"
                          },
                          "is_not_empty": {
                            "type": "string"
                          }
                        }
                      },
                      "number": {
                        "type": "object",
                        "properties": {
                          "equals": {
                            "type": "number",
                            "format": "float"
                          },
                          "does_not_equal": {
                            "type": "number",
                            "format": "float"
                          },
                          "greater_than": {
                            "type": "number",
                            "format": "float"
                          },
                          "less_than": {
                            "type": "number",
                            "format": "float"
                          },
                          "greater_than_or_equal_to": {
                            "type": "number",
                            "format": "float"
                          },
                          "less_than_or_equal_to": {
                            "type": "number",
                            "format": "float"
                          },
                          "is_empty": {
                            "type": "number",
                            "format": "float"
                          },
                          "is_not_empty": {
                            "type": "number",
                            "format": "float"
                          }
                        }
                      },
                      "checkbox": {
                        "type": "object",
                        "properties": {
                          "equals": {
                            "type": "boolean"
                          },
                          "does_not_equal": {
                            "type": "boolean"
                          }
                        }
                      },
                      "select": {
                        "type": "object",
                        "properties": {
                          "equals": {
                            "type": "string"
                          },
                          "does_not_equal": {
                            "type": "string"
                          },
                          "is_empty": {
                            "type": "string",
                            "enum": [
                              "true"
                            ]
                          },
                          "is_not_empty": {
                            "type": "string",
                            "enum": [
                              "true"
                            ]
                          }
                        }
                      },
                      "multi_select": {
                        "type": "object",
                        "properties": {
                          "equals": {
                            "type": "string"
                          },
                          "does_not_equal": {
                            "type": "string"
                          },
                          "is_empty": {
                            "type": "string",
                            "enum": [
                              "true"
                            ]
                          },
                          "is_not_empty": {
                            "type": "string",
                            "enum": [
                              "true"
                            ]
                          }
                        }
                      },
                      "status": {
                        "type": "object",
                        "properties": {
                          "equals": {
                            "type": "string"
                          },
                          "does_not_equal": {
                            "type": "string"
                          },
                          "is_empty": {
                            "type": "string",
                            "enum": [
                              "true"
                            ]
                          },
                          "is_not_empty": {
                            "type": "string",
                            "enum": [
                              "true"
                            ]
                          }
                        }
                      },
                      "date": {
                        "type": "object",
                        "properties": {
                          "equals": {
                            "type": "string",
                            "format": "date"
                          },
                          "before": {
                            "type": "string",
                            "format": "date"
                          },
                          "after": {
                            "type": "string",
                            "format": "date"
                          },
                          "on_or_before": {
                            "type": "string",
                            "format": "date"
                          },
                          "on_or_after": {
                            "type": "string",
                            "format": "date"
                          },
                          "this_week": {
                            "type": "object",
                            "description": "Empty object `{}`",
                            "properties": {}
                          },
                          "past_week": {
                            "type": "object",
                            "description": "Empty object `{}`",
                            "properties": {}
                          },
                          "past_month": {
                            "type": "object",
                            "description": "Empty object `{}`",
                            "properties": {}
                          },
                          "past_year": {
                            "type": "object",
                            "description": "Empty object `{}`",
                            "properties": {}
                          },
                          "next_week": {
                            "type": "object",
                            "description": "Empty object `{}`",
                            "properties": {}
                          },
                          "next_month": {
                            "type": "object",
                            "description": "Empty object `{}`",
                            "properties": {}
                          },
                          "next_year": {
                            "type": "object",
                            "description": "Empty object `{}`",
                            "properties": {}
                          },
                          "is_empty": {
                            "type": "string",
                            "enum": [
                              "true"
                            ]
                          },
                          "is_not_empty": {
                            "type": "boolean",
                            "description": "true"
                          }
                        }
                      },
                      "people": {
                        "type": "object",
                        "properties": {
                          "contains": {
                            "type": "string"
                          },
                          "does_not_contain": {
                            "type": "string"
                          },
                          "is_empty": {
                            "type": "string",
                            "enum": [
                              "true"
                            ]
                          },
                          "is_not_empty": {
                            "type": "string",
                            "enum": [
                              "true"
                            ]
                          }
                        }
                      },
                      "files": {
                        "type": "object",
                        "properties": {
                          "is_empty": {
                            "type": "string",
                            "enum": [
                              "true"
                            ]
                          },
                          "is_not_empty": {
                            "type": "string",
                            "enum": [
                              "true"
                            ]
                          }
                        }
                      },
                      "url": {
                        "type": "object",
                        "properties": {
                          "equals": {
                            "type": "string"
                          },
                          "does_not_equal": {
                            "type": "string"
                          },
                          "contains": {
                            "type": "string"
                          },
                          "does_not_contain": {
                            "type": "string"
                          },
                          "starts_with": {
                            "type": "string"
                          },
                          "ends_with": {
                            "type": "string"
                          },
                          "is_empty": {
                            "type": "string"
                          },
                          "is_not_empty": {
                            "type": "string"
                          }
                        }
                      },
                      "email": {
                        "type": "object",
                        "properties": {
                          "equals": {
                            "type": "string"
                          },
                          "does_not_equal": {
                            "type": "string"
                          },
                          "contains": {
                            "type": "string"
                          },
                          "does_not_contain": {
                            "type": "string"
                          },
                          "starts_with": {
                            "type": "string"
                          },
                          "ends_with": {
                            "type": "string"
                          },
                          "is_empty": {
                            "type": "string"
                          },
                          "is_not_empty": {
                            "type": "string"
                          }
                        }
                      },
                      "phone_number": {
                        "type": "object",
                        "properties": {
                          "equals": {
                            "type": "string"
                          },
                          "does_not_equal": {
                            "type": "string"
                          },
                          "contains": {
                            "type": "string"
                          },
                          "does_not_contain": {
                            "type": "string"
                          },
                          "starts_with": {
                            "type": "string"
                          },
                          "ends_with": {
                            "type": "string"
                          },
                          "is_empty": {
                            "type": "string"
                          },
                          "is_not_empty": {
                            "type": "string"
                          }
                        }
                      },
                      "relation": {
                        "type": "object",
                        "properties": {
                          "contains": {
                            "type": "string"
                          },
                          "does_not_contain": {
                            "type": "string"
                          },
                          "is_empty": {
                            "type": "string",
                            "enum": [
                              "true"
                            ]
                          },
                          "is_not_empty": {
                            "type": "string",
                            "enum": [
                              "true"
                            ]
                          }
                        }
                      },
                      "created_by": {
                        "type": "object",
                        "properties": {
                          "contains": {
                            "type": "string"
                          },
                          "does_not_contain": {
                            "type": "string"
                          },
                          "is_empty": {
                            "type": "string",
                            "enum": [
                              "true"
                            ]
                          },
                          "is_not_empty": {
                            "type": "string",
                            "enum": [
                              "true"
                            ]
                          }
                        }
                      },
                      "last_edited_by": {
                        "type": "object",
                        "properties": {
                          "contains": {
                            "type": "string"
                          },
                          "does_not_contain": {
                            "type": "string"
                          },
                          "is_empty": {
                            "type": "string",
                            "enum": [
                              "true"
                            ]
                          },
                          "is_not_empty": {
                            "type": "string",
                            "enum": [
                              "true"
                            ]
                          }
                        }
                      },
                      "formula": {
                        "type": "object",
                        "properties": {
                          "string": {
                            "type": "object",
                            "properties": {
                              "equals": {
                                "type": "string"
                              },
                              "does_not_equal": {
                                "type": "string"
                              },
                              "contains": {
                                "type": "string"
                              },
                              "does_not_contain": {
                                "type": "string"
                              },
                              "starts_with": {
                                "type": "string"
                              },
                              "ends_with": {
                                "type": "string"
                              },
                              "is_empty": {
                                "type": "string"
                              },
                              "is_not_empty": {
                                "type": "string"
                              }
                            }
                          },
                          "checkbox": {
                            "type": "object",
                            "properties": {
                              "equals": {
                                "type": "boolean"
                              },
                              "does_not_equal": {
                                "type": "boolean"
                              }
                            }
                          },
                          "number": {
                            "type": "object",
                            "properties": {
                              "equals": {
                                "type": "number",
                                "format": "float"
                              },
                              "does_not_equal": {
                                "type": "number",
                                "format": "float"
                              },
                              "greater_than": {
                                "type": "number",
                                "format": "float"
                              },
                              "less_than": {
                                "type": "number",
                                "format": "float"
                              },
                              "greater_than_or_equal_to": {
                                "type": "number",
                                "format": "float"
                              },
                              "less_than_or_equal_to": {
                                "type": "number",
                                "format": "float"
                              },
                              "is_empty": {
                                "type": "number",
                                "format": "float"
                              },
                              "is_not_empty": {
                                "type": "number",
                                "format": "float"
                              }
                            }
                          },
                          "date": {
                            "type": "object",
                            "properties": {
                              "equals": {
                                "type": "string",
                                "format": "date"
                              },
                              "before": {
                                "type": "string",
                                "format": "date"
                              },
                              "after": {
                                "type": "string",
                                "format": "date"
                              },
                              "on_or_before": {
                                "type": "string",
                                "format": "date"
                              },
                              "on_or_after": {
                                "type": "string",
                                "format": "date"
                              },
                              "this_week": {
                                "type": "object",
                                "description": "Empty object `{}`",
                                "properties": {}
                              },
                              "past_week": {
                                "type": "object",
                                "description": "Empty object `{}`",
                                "properties": {}
                              },
                              "past_month": {
                                "type": "object",
                                "description": "Empty object `{}`",
                                "properties": {}
                              },
                              "past_year": {
                                "type": "object",
                                "description": "Empty object `{}`",
                                "properties": {}
                              },
                              "next_week": {
                                "type": "object",
                                "description": "Empty object `{}`",
                                "properties": {}
                              },
                              "next_month": {
                                "type": "object",
                                "description": "Empty object `{}`",
                                "properties": {}
                              },
                              "next_year": {
                                "type": "object",
                                "description": "Empty object `{}`",
                                "properties": {}
                              },
                              "is_empty": {
                                "type": "string",
                                "enum": [
                                  "true"
                                ]
                              },
                              "is_not_empty": {
                                "type": "boolean",
                                "description": "true"
                              }
                            }
                          }
                        }
                      },
                      "unique_id": {
                        "type": "object",
                        "properties": {
                          "equals": {
                            "type": "number",
                            "format": "float"
                          },
                          "does_not_equal": {
                            "type": "number",
                            "format": "float"
                          },
                          "greater_than": {
                            "type": "number",
                            "format": "float"
                          },
                          "less_than": {
                            "type": "number",
                            "format": "float"
                          },
                          "greater_than_or_equal_to": {
                            "type": "number",
                            "format": "float"
                          },
                          "less_than_or_equal_to": {
                            "type": "number",
                            "format": "float"
                          },
                          "is_empty": {
                            "type": "number",
                            "format": "float"
                          },
                          "is_not_empty": {
                            "type": "number",
                            "format": "float"
                          }
                        }
                      },
                      "verification": {
                        "type": "object",
                        "required": [
                          "status"
                        ],
                        "properties": {
                          "status": {
                            "type": "string",
                            "enum": [
                              "\"verified\"",
                              "\"expired\"",
                              "\"none\"",
                              ""
                            ]
                          }
                        }
                      }
                    }
                  },
                  "start_cursor": {
                    "type": "string"
                  },
                  "page_size": {
                    "type": "integer",
                    "format": "int32"
                  }
                }
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "200",
            "content": {
              "application/json": {
                "examples": {
                  "Result": {
                    "value": "{\n  \"object\": \"list\",\n  \"results\": [\n    {\n      \"object\": \"page\",\n      \"id\": \"59833787-2cf9-4fdf-8782-e53db20768a5\",\n      \"created_time\": \"2022-03-01T19:05:00.000Z\",\n      \"last_edited_time\": \"2022-07-06T20:25:00.000Z\",\n      \"created_by\": {\n        \"object\": \"user\",\n        \"id\": \"ee5f0f84-409a-440f-983a-a5315961c6e4\"\n      },\n      \"last_edited_by\": {\n        \"object\": \"user\",\n        \"id\": \"0c3e9826-b8f7-4f73-927d-2caaf86f1103\"\n      },\n      \"cover\": {\n        \"type\": \"external\",\n        \"external\": {\n          \"url\": \"https://upload.wikimedia.org/wikipedia/commons/6/62/Tuscankale.jpg\"\n        }\n      },\n      \"icon\": {\n        \"type\": \"emoji\",\n        \"emoji\": \"🥬\"\n      },\n      \"parent\": {\n        \"type\": \"data_source_id\",\n        \"database_id\": \"d9824bdc-8445-4327-be8b-5b47500af6ce\"\n        \"data_source_id\": \"27a2eeb5-b4f6-4dbe-b3b5-609a7ab26620\"\n      },\n      \"archived\": false,\n      \"properties\": {\n        \"Store availability\": {\n          \"id\": \"%3AUPp\",\n          \"type\": \"multi_select\",\n          \"multi_select\": [\n            {\n              \"id\": \"t|O@\",\n              \"name\": \"Gus's Community Market\",\n              \"color\": \"yellow\"\n            },\n            {\n              \"id\": \"{Ml\\\\\",\n              \"name\": \"Rainbow Grocery\",\n              \"color\": \"gray\"\n            }\n          ]\n        },\n        \"Food group\": {\n          \"id\": \"A%40Hk\",\n          \"type\": \"select\",\n          \"select\": {\n            \"id\": \"5e8e7e8f-432e-4d8a-8166-1821e10225fc\",\n            \"name\": \"🥬 Vegetable\",\n            \"color\": \"pink\"\n          }\n        },\n        \"Price\": {\n          \"id\": \"BJXS\",\n          \"type\": \"number\",\n          \"number\": 2.5\n        },\n        \"Responsible Person\": {\n          \"id\": \"Iowm\",\n          \"type\": \"people\",\n          \"people\": [\n            {\n              \"object\": \"user\",\n              \"id\": \"cbfe3c6e-71cf-4cd3-b6e7-02f38f371bcc\",\n              \"name\": \"Cristina Cordova\",\n              \"avatar_url\": \"https://lh6.googleusercontent.com/-rapvfCoTq5A/AAAAAAAAAAI/AAAAAAAAAAA/AKF05nDKmmUpkpFvWNBzvu9rnZEy7cbl8Q/photo.jpg\",\n              \"type\": \"person\",\n              \"person\": {\n                \"email\": \"cristina@makenotion.com\"\n              }\n            }\n          ]\n        },\n        \"Last ordered\": {\n          \"id\": \"Jsfb\",\n          \"type\": \"date\",\n          \"date\": {\n            \"start\": \"2022-02-22\",\n            \"end\": null,\n            \"time_zone\": null\n          }\n        },\n        \"Cost of next trip\": {\n          \"id\": \"WOd%3B\",\n          \"type\": \"formula\",\n          \"formula\": {\n            \"type\": \"number\",\n            \"number\": 0\n          }\n        },\n        \"Recipes\": {\n          \"id\": \"YfIu\",\n          \"type\": \"relation\",\n          \"relation\": [\n            {\n              \"id\": \"90eeeed8-2cdd-4af4-9cc1-3d24aff5f63c\"\n            },\n            {\n              \"id\": \"a2da43ee-d43c-4285-8ae2-6d811f12629a\"\n            }\n          ],\n\t\t\t\t\t\"has_more\": false\n        },\n        \"Description\": {\n          \"id\": \"_Tc_\",\n          \"type\": \"rich_text\",\n          \"rich_text\": [\n            {\n              \"type\": \"text\",\n              \"text\": {\n                \"content\": \"A dark \",\n                \"link\": null\n              },\n              \"annotations\": {\n                \"bold\": false,\n                \"italic\": false,\n                \"strikethrough\": false,\n                \"underline\": false,\n                \"code\": false,\n                \"color\": \"default\"\n              },\n              \"plain_text\": \"A dark \",\n              \"href\": null\n            },\n            {\n              \"type\": \"text\",\n              \"text\": {\n                \"content\": \"green\",\n                \"link\": null\n              },\n              \"annotations\": {\n                \"bold\": false,\n                \"italic\": false,\n                \"strikethrough\": false,\n                \"underline\": false,\n                \"code\": false,\n                \"color\": \"green\"\n              },\n              \"plain_text\": \"green\",\n              \"href\": null\n            },\n            {\n              \"type\": \"text\",\n              \"text\": {\n                \"content\": \" leafy vegetable\",\n                \"link\": null\n              },\n              \"annotations\": {\n                \"bold\": false,\n                \"italic\": false,\n                \"strikethrough\": false,\n                \"underline\": false,\n                \"code\": false,\n                \"color\": \"default\"\n              },\n              \"plain_text\": \" leafy vegetable\",\n              \"href\": null\n            }\n          ]\n        },\n        \"In stock\": {\n          \"id\": \"%60%5Bq%3F\",\n          \"type\": \"checkbox\",\n          \"checkbox\": true\n        },\n        \"Number of meals\": {\n          \"id\": \"zag~\",\n          \"type\": \"rollup\",\n          \"rollup\": {\n            \"type\": \"number\",\n            \"number\": 2,\n            \"function\": \"count\"\n          }\n        },\n        \"Photo\": {\n          \"id\": \"%7DF_L\",\n          \"type\": \"url\",\n          \"url\": \"https://i.insider.com/612fb23c9ef1e50018f93198?width=1136&format=jpeg\"\n        },\n        \"Name\": {\n          \"id\": \"title\",\n          \"type\": \"title\",\n          \"title\": [\n            {\n              \"type\": \"text\",\n              \"text\": {\n                \"content\": \"Tuscan kale\",\n                \"link\": null\n              },\n              \"annotations\": {\n                \"bold\": false,\n                \"italic\": false,\n                \"strikethrough\": false,\n                \"underline\": false,\n                \"code\": false,\n                \"color\": \"default\"\n              },\n              \"plain_text\": \"Tuscan kale\",\n              \"href\": null\n            }\n          ]\n        }\n      },\n      \"url\": \"https://www.notion.so/Tuscan-kale-598337872cf94fdf8782e53db20768a5\"\n    }\n  ],\n  \"next_cursor\": null,\n  \"has_more\": false,\n  \"type\": \"page_or_data_source\",\n\t\"page_or_data_source\": {}\n}"
                  }
                }
              }
            }
          },
          "400": {
            "description": "400",
            "content": {
              "application/json": {
                "examples": {
                  "Result": {
                    "value": "{}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {}
                }
              }
            }
          }
        },
        "deprecated": false,
        "security": [],
        "x-readme": {
          "code-samples": [
            {
              "language": "curl",
              "code": "curl -X POST 'https://api.notion.com/v1/data_sources/897e5a76ae524b489fdfe71f5945d1af/query' \\\n  -H 'Authorization: Bearer '\"$NOTION_API_KEY\"'' \\\n  -H 'Notion-Version: 2022-06-28' \\\n  -H \"Content-Type: application/json\" \\\n--data '{\n  \"filter\": {\n    \"or\": [\n      {\n        \"property\": \"In stock\",\n        \"checkbox\": {\n          \"equals\": true\n        }\n      },\n      {\n        \"property\": \"Cost of next trip\",\n        \"number\": {\n          \"greater_than_or_equal_to\": 2\n        }\n      }\n    ]\n  },\n  \"sorts\": [\n    {\n      \"property\": \"Last ordered\",\n      \"direction\": \"ascending\"\n    }\n  ]\n}'"
            },
            {
              "language": "node",
              "code": "const { Client } = require('@notionhq/client');\n\nconst notion = new Client({ auth: process.env.NOTION_API_KEY });\n\n(async () => {\n  const dataSourceId = 'd9824bdc-8445-4327-be8b-5b47500af6ce';\n  const response = await notion.dataSources.query({\n    data_source_id: dataSourceId,\n    filter: {\n      or: [\n        {\n          property: 'In stock',\n          checkbox: {\n            equals: true,\n          },\n        },\n        {\n          property: 'Cost of next trip',\n          number: {\n            greater_than_or_equal_to: 2,\n          },\n        },\n      ],\n    },\n    sorts: [\n      {\n        property: 'Last ordered',\n        direction: 'ascending',\n      },\n    ],\n  });\n  console.log(response);\n})();"
            }
          ],
          "samples-languages": [
            "curl",
            "node"
          ]
        }
      }
    }
  },
  "x-readme": {
    "headers": [],
    "explorer-enabled": false,
    "proxy-enabled": true
  },
  "x-readme-fauxas": true,
  "_id": "606ecc2cd9e93b0044cf6e47:68b1ebd3866ea01713ccb69a"
}
```

# Filter data source entries

When you [query a data source](ref:query-a-data-source), you can send a `filter` object in the body of the request that limits the returned entries based on the specified criteria.

For example, the below query limits the response to entries where the `"Task completed"`  `checkbox` property value is `true`:

```curl
curl -X POST 'https://api.notion.com/v1/data_sources/897e5a76ae524b489fdfe71f5945d1af/query' \
  -H 'Authorization: Bearer '"$NOTION_API_KEY"'' \
  -H 'Notion-Version: 2022-06-28' \
  -H "Content-Type: application/json" \
--data '{
  "filter": {
    "property": "Task completed",
    "checkbox": {
        "equals": true
   }
  }
}'
```

Here is the same query using the [Notion SDK for JavaScript](https://github.com/makenotion/notion-sdk-js):

```javascript
const { Client } = require('@notionhq/client');

const notion = new Client({ auth: process.env.NOTION_API_KEY });
// replace with your own data source ID
const dataSourceId = 'd9824bdc-8445-4327-be8b-5b47500af6ce';

const filteredRows = async () => {
	const response = await notion.databases.query({
	  data_source_id: dataSourceId,
	  filter: {
	    property: "Task completed",
	    checkbox: {
	      equals: true
	    }
	  },
	});
  return response;
}

```

Filters can be chained with the `and` and `or` keys so that multiple filters are applied at the same time. (See [Query a data source](ref:query-a-data-source) for additional examples.)

```json
{
  "and": [
    {
      "property": "Done",
      "checkbox": {
        "equals": true
      }
    },
    {
      "or": [
        {
          "property": "Tags",
          "contains": "A"
        },
        {
          "property": "Tags",
          "contains": "B"
        }
      ]
    }
  ]
}
```

If no filter is provided, all the pages in the data source will be returned with pagination.

## The filter object

Each `filter` object contains the following fields:

[block:parameters]
{
  "data": {
    "h-0": "Field",
    "h-1": "Type",
    "h-2": "Description",
    "h-3": "Example value",
    "0-0": "`property`",
    "0-1": "`string`",
    "0-2": "The name of the property as it appears in the data source, or the property ID.",
    "0-3": "`\"Task completed\"`",
    "1-0": "`checkbox`  \n`date`  \n`files`  \n`formula`  \n`multi_select`  \n`number`  \n`people`  \n`phone_number`  \n`relation`  \n`rich_text`  \n`select`  \n`status`  \n`timestamp`  \n`verification`  \n`ID`",
    "1-1": "`object`",
    "1-2": "The type-specific filter condition for the query. Only types listed in the Field column of this table are supported.  \n  \nRefer to [type-specific filter conditions](#type-specific-filter-conditions) for details on corresponding object values.",
    "1-3": "`\"checkbox\": {\n  \"equals\": true\n}`"
  },
  "cols": 4,
  "rows": 2,
  "align": [
    "left",
    "left",
    "left",
    "left"
  ]
}
[/block]


```json Example checkbox filter object
{
  "filter": {
    "property": "Task completed",
    "checkbox": {
      "equals": true
    }
  }
}
```

> 👍
>
> The filter object mimics the data source [filter option in the Notion UI](https://www.notion.so/help/views-filters-and-sorts).

## Type-specific filter conditions

### Checkbox

[block:parameters]
{
  "data": {
    "h-0": "Field",
    "h-1": "Type",
    "h-2": "Description",
    "h-3": "Example value",
    "0-0": "`equals`",
    "0-1": "`boolean`",
    "0-2": "Whether a `checkbox` property value matches the provided value exactly.  \n  \nReturns or excludes all data source entries with an exact value match.",
    "0-3": "`false`",
    "1-0": "`does_not_equal`",
    "1-1": "`boolean`",
    "1-2": "Whether a `checkbox` property value differs from the provided value.  \n  \nReturns or excludes all data source entries with a difference in values.",
    "1-3": "`true`"
  },
  "cols": 4,
  "rows": 2,
  "align": [
    "left",
    "left",
    "left",
    "left"
  ]
}
[/block]


```json Example checkbox filter condition
{
  "filter": {
    "property": "Task completed",
    "checkbox": {
      "does_not_equal": true
    }
  }
}
```

### Date

> 📘
>
> For the `after`, `before`, `equals, on_or_before`, and `on_or_after` fields, if a date string with a time is provided, then the comparison is done with millisecond precision.
>
> If no timezone is provided, then the timezone defaults to UTC.

A date filter condition can be used to limit `date` property value types and the [timestamp](#timestamp) property types `created_time` and `last_edited_time`.

The condition contains the below fields:

[block:parameters]
{
  "data": {
    "h-0": "Field",
    "h-1": "Type",
    "h-2": "Description",
    "h-3": "Example value",
    "0-0": "`after`",
    "0-1": "`string` ([ISO 8601 date](https://en.wikipedia.org/wiki/ISO_8601))",
    "0-2": "The value to compare the date property value against.  \n  \nReturns data source entries where the date property value is after the provided date.",
    "0-3": "`\"2021-05-10\"`  \n  \n`\"2021-05-10T12:00:00\"`  \n  \n`\"2021-10-15T12:00:00-07:00\"`",
    "1-0": "`before`",
    "1-1": "`string` ([ISO 8601 date](https://en.wikipedia.org/wiki/ISO_8601))",
    "1-2": "The value to compare the date property value against.  \n  \nReturns data source entries where the date property value is before the provided date.",
    "1-3": "`\"2021-05-10\"`  \n  \n`\"2021-05-10T12:00:00\"`  \n  \n`\"2021-10-15T12:00:00-07:00\"`",
    "2-0": "`equals`",
    "2-1": "`string` ([ISO 8601 date](https://en.wikipedia.org/wiki/ISO_8601))",
    "2-2": "The value to compare the date property value against.  \n  \nReturns data source entries where the date property value is the provided date.",
    "2-3": "`\"2021-05-10\"`  \n  \n`\"2021-05-10T12:00:00\"`  \n  \n`\"2021-10-15T12:00:00-07:00\"`",
    "3-0": "`is_empty`",
    "3-1": "`true`",
    "3-2": "The value to compare the date property value against.  \n  \nReturns data source entries where the date property value contains no data.",
    "3-3": "`true`",
    "4-0": "`is_not_empty`",
    "4-1": "`true`",
    "4-2": "The value to compare the date property value against.  \n  \nReturns data source entries where the date property value is not empty.",
    "4-3": "`true`",
    "5-0": "`next_month`",
    "5-1": "`object` (empty)",
    "5-2": "A filter that limits the results to data source entries where the date property value is within the next month.",
    "5-3": "`{}`",
    "6-0": "`next_week`",
    "6-1": "`object` (empty)",
    "6-2": "A filter that limits the results to data source entries where the date property value is within the next week.",
    "6-3": "`{}`",
    "7-0": "`next_year`",
    "7-1": "`object` (empty)",
    "7-2": "A filter that limits the results to data source entries where the date property value is within the next year.",
    "7-3": "`{}`",
    "8-0": "`on_or_after`",
    "8-1": "`string` ([ISO 8601 date](https://en.wikipedia.org/wiki/ISO_8601))",
    "8-2": "The value to compare the date property value against.  \n  \nReturns data source entries where the date property value is on or after the provided date.",
    "8-3": "`\"2021-05-10\"`  \n  \n`\"2021-05-10T12:00:00\"`  \n  \n`\"2021-10-15T12:00:00-07:00\"`",
    "9-0": "`on_or_before`",
    "9-1": "`string` ([ISO 8601 date](https://en.wikipedia.org/wiki/ISO_8601))",
    "9-2": "The value to compare the date property value against.  \n  \nReturns data source entries where the date property value is on or before the provided date.",
    "9-3": "`\"2021-05-10\"`  \n  \n`\"2021-05-10T12:00:00\"`  \n  \n`\"2021-10-15T12:00:00-07:00\"`",
    "10-0": "`past_month`",
    "10-1": "`object` (empty)",
    "10-2": "A filter that limits the results to data source entries where the `date` property value is within the past month.",
    "10-3": "`{}`",
    "11-0": "`past_week`",
    "11-1": "`object` (empty)",
    "11-2": "A filter that limits the results to data source entries where the `date` property value is within the past week.",
    "11-3": "`{}`",
    "12-0": "`past_year`",
    "12-1": "`object` (empty)",
    "12-2": "A filter that limits the results to data source entries where the `date` property value is within the past year.",
    "12-3": "`{}`",
    "13-0": "`this_week`",
    "13-1": "`object` (empty)",
    "13-2": "A filter that limits the results to data source entries where the `date` property value is this week.",
    "13-3": "`{}`"
  },
  "cols": 4,
  "rows": 14,
  "align": [
    "left",
    "left",
    "left",
    "left"
  ]
}
[/block]


```json Example date filter condition
{
  "filter": {
    "property": "Due date",
    "date": {
      "on_or_after": "2023-02-08"
    }
  }
}
```

### Files

[block:parameters]
{
  "data": {
    "h-0": "Field",
    "h-1": "Type",
    "h-2": "Description",
    "h-3": "Example value",
    "0-0": "`is_empty`",
    "0-1": "`true`",
    "0-2": "Whether the files property value does not contain any data.  \n  \nReturns all data source entries with an empty `files` property value.",
    "0-3": "`true`",
    "1-0": "`is_not_empty`",
    "1-1": "`true`",
    "1-2": "Whether the `files` property value contains data.  \n  \nReturns all entries with a populated `files` property value.",
    "1-3": "`true`"
  },
  "cols": 4,
  "rows": 2,
  "align": [
    "left",
    "left",
    "left",
    "left"
  ]
}
[/block]


```json Example files filter condition
{
  "filter": {
    "property": "Blueprint",
    "files": {
      "is_not_empty": true
    }
  }
}
```

### Formula

The primary field of the `formula` filter condition object matches the type of the formula’s result. For example, to filter a formula property that computes a `checkbox`, use a `formula` filter condition object with a `checkbox` field containing a checkbox filter condition as its value.

[block:parameters]
{
  "data": {
    "h-0": "Field",
    "h-1": "Type",
    "h-2": "Description",
    "h-3": "Example value",
    "0-0": "`checkbox`",
    "0-1": "`object`",
    "0-2": "A [checkbox](#checkbox) filter condition to compare the formula result against.  \n  \nReturns data source entries where the formula result matches the provided condition.",
    "0-3": "Refer to the [checkbox](#checkbox) filter condition.",
    "1-0": "`date`",
    "1-1": "`object`",
    "1-2": "A [date](#date) filter condition to compare the formula result against.  \n  \nReturns data source entries where the formula result matches the provided condition.",
    "1-3": "Refer to the [date](#date) filter condition.",
    "2-0": "`number`",
    "2-1": "`object`",
    "2-2": "A [number](#number) filter condition to compare the formula result against.  \n  \nReturns data source entries where the formula result matches the provided condition.",
    "2-3": "Refer to the [number](#number) filter condition.",
    "3-0": "`string`",
    "3-1": "`object`",
    "3-2": "A [rich text](#rich-text) filter condition to compare the formula result against.  \n  \nReturns data source entries where the formula result matches the provided condition.",
    "3-3": "Refer to the [rich text](#rich-text) filter condition."
  },
  "cols": 4,
  "rows": 4,
  "align": [
    "left",
    "left",
    "left",
    "left"
  ]
}
[/block]


```json Example formula filter condition
{
  "filter": {
    "property": "One month deadline",
    "formula": {
      "date":{
          "after": "2021-05-10"
      }
    }
  }
}
```

### Multi-select

[block:parameters]
{
  "data": {
    "h-0": "Field",
    "h-1": "Type",
    "h-2": "Description",
    "h-3": "Example value",
    "0-0": "`contains`",
    "0-1": "`string`",
    "0-2": "The value to compare the multi-select property value against.  \n  \nReturns data source entries where the multi-select value matches the provided string.",
    "0-3": "`\"Marketing\"`",
    "1-0": "`does_not_contain`",
    "1-1": "`string`",
    "1-2": "The value to compare the multi-select property value against.  \n  \nReturns data source entries where the multi-select value does not match the provided string.",
    "1-3": "`\"Engineering\"`",
    "2-0": "`is_empty`",
    "2-1": "`true`",
    "2-2": "Whether the multi-select property value is empty.  \n  \nReturns data source entries where the multi-select value does not contain any data.",
    "2-3": "`true`",
    "3-0": "`is_not_empty`",
    "3-1": "`true`",
    "3-2": "Whether the multi-select property value is not empty.  \n  \nReturns data source entries where the multi-select value does contains data.",
    "3-3": "`true`"
  },
  "cols": 4,
  "rows": 4,
  "align": [
    "left",
    "left",
    "left",
    "left"
  ]
}
[/block]


```json Example multi-select filter condition
{
  "filter": {
    "property": "Programming language",
    "multi_select": {
      "contains": "TypeScript"
    }
  }
}
```

### Number

[block:parameters]
{
  "data": {
    "h-0": "Field",
    "h-1": "Type",
    "h-2": "Description",
    "h-3": "Example value",
    "0-0": "`does_not_equal`",
    "0-1": "`number`",
    "0-2": "The `number` to compare the number property value against.  \n  \nReturns data source entries where the number property value differs from the provided `number`.",
    "0-3": "`42`",
    "1-0": "`equals`",
    "1-1": "`number`",
    "1-2": "The `number` to compare the number property value against.  \n  \nReturns data source entries where the number property value is the same as the provided number.",
    "1-3": "`42`",
    "2-0": "`greater_than`",
    "2-1": "`number`",
    "2-2": "The `number` to compare the number property value against.  \n  \nReturns data source entries where the number property value exceeds the provided `number`.",
    "2-3": "`42`",
    "3-0": "`greater_than_or_equal_to`",
    "3-1": "`number`",
    "3-2": "The `number` to compare the number property value against.  \n  \nReturns data source entries where the number property value is equal to or exceeds the provided `number`.",
    "3-3": "`42`",
    "4-0": "`is_empty`",
    "4-1": "`true`",
    "4-2": "Whether the `number` property value is empty.  \n  \nReturns data source entries where the number property value does not contain any data.",
    "4-3": "`true`",
    "5-0": "`is_not_empty`",
    "5-1": "`true`",
    "5-2": "Whether the number property value is not empty.  \n  \nReturns data source entries where the number property value contains data.",
    "5-3": "`true`",
    "6-0": "`less_than`",
    "6-1": "`number`",
    "6-2": "The `number` to compare the number property value against.  \n  \nReturns data source entries where the number property value is less than the provided `number`.",
    "6-3": "`42`",
    "7-0": "`less_than_or_equal_to`",
    "7-1": "`number`",
    "7-2": "The `number` to compare the number property value against.  \n  \nReturns data source entries where the number property value is equal to or is less than the provided `number`.",
    "7-3": "`42`"
  },
  "cols": 4,
  "rows": 8,
  "align": [
    "left",
    "left",
    "left",
    "left"
  ]
}
[/block]


```json Example number filter condition
{
  "filter": {
    "property": "Estimated working days",
    "number": {
      "less_than_or_equal_to": 5
    }
  }
}
```

### People

You can apply a people filter condition to `people`, `created_by`, and `last_edited_by` data source property types.

The people filter condition contains the following fields:

[block:parameters]
{
  "data": {
    "h-0": "Field",
    "h-1": "Type",
    "h-2": "Description",
    "h-3": "Example value",
    "0-0": "`contains`",
    "0-1": "`string` (UUIDv4)",
    "0-2": "The value to compare the people property value against.  \n  \nReturns data source entries where the people property value contains the provided `string`.",
    "0-3": "`\"6c574cee-ca68-41c8-86e0-1b9e992689fb\"`",
    "1-0": "`does_not_contain`",
    "1-1": "`string` (UUIDv4)",
    "1-2": "The value to compare the people property value against.  \n  \nReturns data source entries where the people property value does not contain the provided `string`.",
    "1-3": "`\"6c574cee-ca68-41c8-86e0-1b9e992689fb\"`",
    "2-0": "`is_empty`",
    "2-1": "`true`",
    "2-2": "Whether the people property value does not contain any data.  \n  \nReturns data source entries where the people property value does not contain any data.",
    "2-3": "`true`",
    "3-0": "`is_not_empty`",
    "3-1": "`true`",
    "3-2": "Whether the people property value contains data.  \n  \nReturns data source entries where the people property value is not empty.",
    "3-3": "`true`"
  },
  "cols": 4,
  "rows": 4,
  "align": [
    "left",
    "left",
    "left",
    "left"
  ]
}
[/block]


```json Example people filter condition
{
  "filter": {
    "property": "Last edited by",
    "people": {
      "contains": "c2f20311-9e54-4d11-8c79-7398424ae41e"
    }
  }
}
```

### Relation

[block:parameters]
{
  "data": {
    "h-0": "Field",
    "h-1": "Type",
    "h-2": "Description",
    "h-3": "Example value",
    "0-0": "`contains`",
    "0-1": "`string` (UUIDv4)",
    "0-2": "The value to compare the relation property value against.  \n  \nReturns data source entries where the relation property value contains the provided `string`.",
    "0-3": "`\"6c574cee-ca68-41c8-86e0-1b9e992689fb\"`",
    "1-0": "`does_not_contain`",
    "1-1": "`string` (UUIDv4)",
    "1-2": "The value to compare the relation property value against.  \n  \nReturns entries where the relation property value does not contain the provided `string`.",
    "1-3": "`\"6c574cee-ca68-41c8-86e0-1b9e992689fb\"`",
    "2-0": "`is_empty`",
    "2-1": "`true`",
    "2-2": "Whether the relation property value does not contain data.  \n  \nReturns data source entries where the relation property value does not contain any data.",
    "2-3": "`true`",
    "3-0": "`is_not_empty`",
    "3-1": "`true`",
    "3-2": "Whether the relation property value contains data.  \n  \nReturns data source entries where the property value is not empty.",
    "3-3": "`true`"
  },
  "cols": 4,
  "rows": 4,
  "align": [
    "left",
    "left",
    "left",
    "left"
  ]
}
[/block]


```json Example relation filter condition
{
  "filter": {
    "property": "✔️ Task List",
    "relation": {
      "contains": "0c1f7cb280904f18924ed92965055e32"
    }
  }
}
```

### Rich text

[block:parameters]
{
  "data": {
    "h-0": "Field",
    "h-1": "Type",
    "h-2": "Description",
    "h-3": "Example value",
    "0-0": "`contains`",
    "0-1": "`string`",
    "0-2": "The `string` to compare the text property value against.  \n  \nReturns data source entries with a text property value that includes the provided `string`.",
    "0-3": "`\"Moved to Q2\"`",
    "1-0": "`does_not_contain`",
    "1-1": "`string`",
    "1-2": "The `string` to compare the text property value against.  \n  \nReturns data source entries with a text property value that does not include the provided `string`.",
    "1-3": "`\"Moved to Q2\"`",
    "2-0": "`does_not_equal`",
    "2-1": "`string`",
    "2-2": "The `string` to compare the text property value against.  \n  \nReturns data source entries with a text property value that does not match the provided `string`.",
    "2-3": "`\"Moved to Q2\"`",
    "3-0": "`ends_with`",
    "3-1": "`string`",
    "3-2": "The `string` to compare the text property value against.  \n  \nReturns data source entries with a text property value that ends with the provided `string`.",
    "3-3": "`\"Q2\"`",
    "4-0": "`equals`",
    "4-1": "`string`",
    "4-2": "The `string` to compare the text property value against.  \n  \nReturns data source entries with a text property value that matches the provided `string`.",
    "4-3": "`\"Moved to Q2\"`",
    "5-0": "`is_empty`",
    "5-1": "`true`",
    "5-2": "Whether the text property value does not contain any data.  \n  \nReturns data source entries with a text property value that is empty.",
    "5-3": "`true`",
    "6-0": "`is_not_empty`",
    "6-1": "`true`",
    "6-2": "Whether the text property value contains any data.  \n  \nReturns data source entries with a text property value that contains data.",
    "6-3": "`true`",
    "7-0": "`starts_with`",
    "7-1": "`string`",
    "7-2": "The `string` to compare the text property value against.  \n  \nReturns data source entries with a text property value that starts with the provided `string`.",
    "7-3": "\"Moved\""
  },
  "cols": 4,
  "rows": 8,
  "align": [
    "left",
    "left",
    "left",
    "left"
  ]
}
[/block]


```json Example rich text filter condition
{
  "filter": {
    "property": "Description",
    "rich_text": {
      "contains": "cross-team"
    }
  }
}
```

### Rollup

A rollup data source property can evaluate to an array, date, or number value. The filter condition for the rollup property contains a `rollup` key and a corresponding object value that depends on the computed value type.

#### Filter conditions for `array` rollup values

[block:parameters]
{
  "data": {
    "h-0": "Field",
    "h-1": "Type",
    "h-2": "Description",
    "h-3": "Example value",
    "0-0": "`any`",
    "0-1": "`object`",
    "0-2": "The value to compare each rollup property value against. Can be a [filter condition](#type-specific-filter-conditions) for any other type.  \n  \nReturns data source entries where the rollup property value matches the provided criteria.",
    "0-3": "`\"rich_text\": {\n\"contains\": \"Take Fig on a walk\"\n}`",
    "1-0": "`every`",
    "1-1": "`object`",
    "1-2": "The value to compare each rollup property value against. Can be a [filter condition](#type-specific-filter-conditions) for any other type.  \n  \nReturns data source entries where every rollup property value matches the provided criteria.",
    "1-3": "`\"rich_text\": {\n\"contains\": \"Take Fig on a walk\"\n}`",
    "2-0": "`none`",
    "2-1": "`object`",
    "2-2": "The value to compare each rollup property value against. Can be a [filter condition](#type-specific-filter-conditions) for any other type.  \n  \nReturns data source entries where no rollup property value matches the provided criteria.",
    "2-3": "`\"rich_text\": {\n\"contains\": \"Take Fig on a walk\"\n}`"
  },
  "cols": 4,
  "rows": 3,
  "align": [
    "left",
    "left",
    "left",
    "left"
  ]
}
[/block]


```json Example array rollup filter condition
{
  "filter": {
    "property": "Related tasks",
    "rollup": {
      "any": {
        "rich_text": {
          "contains": "Migrate data source"
        }
      }
    }
  }
}
```

#### Filter conditions for `date` rollup values

A rollup value is stored as a `date` only if the "Earliest date", "Latest date", or "Date range" computation is selected for the property in the Notion UI.

[block:parameters]
{
  "data": {
    "h-0": "Field",
    "h-1": "Type",
    "h-2": "Description",
    "h-3": "Example value",
    "0-0": "`date`",
    "0-1": "`object`",
    "0-2": "A [date](#date) filter condition to compare the rollup value against.  \n  \nReturns data source entries where the rollup value matches the provided condition.",
    "0-3": "Refer to the [date](#date) filter condition."
  },
  "cols": 4,
  "rows": 1,
  "align": [
    "left",
    "left",
    "left",
    "left"
  ]
}
[/block]


```json Example date rollup filter condition
{
  "filter": {
    "property": "Parent project due date",
    "rollup": {
      "date": {
        "on_or_before": "2023-02-08"
      }
    }
  }
}
```

#### Filter conditions for `number` rollup values

[block:parameters]
{
  "data": {
    "h-0": "Field",
    "h-1": "Type",
    "h-2": "Description",
    "h-3": "Example value",
    "0-0": "`number`",
    "0-1": "`object`",
    "0-2": "A [number](#number) filter condition to compare the rollup value against.  \n  \nReturns data source entries where the rollup value matches the provided condition.",
    "0-3": "Refer to the [number](#number) filter condition."
  },
  "cols": 4,
  "rows": 1,
  "align": [
    "left",
    "left",
    "left",
    "left"
  ]
}
[/block]


```json Example number rollup filter condition
{
  "filter": {
    "property": "Total estimated working days",
    "rollup": {
      "number": {
        "does_not_equal": 42
      }
    }
  }
}
```

### Select

[block:parameters]
{
  "data": {
    "h-0": "Field",
    "h-1": "Type",
    "h-2": "Description",
    "h-3": "Example value",
    "0-0": "`equals`",
    "0-1": "`string`",
    "0-2": "The `string` to compare the select property value against.  \n  \nReturns data source entries where the select property value matches the provided string.",
    "0-3": "`\"This week\"`",
    "1-0": "`does_not_equal`",
    "1-1": "`string`",
    "1-2": "The `string` to compare the select property value against.  \n  \nReturns data source entries where the select property value does not match the provided `string`.",
    "1-3": "`\"Backlog\"`",
    "2-0": "`is_empty`",
    "2-1": "`true`",
    "2-2": "Whether the select property value does not contain data.  \n  \nReturns data source entries where the select property value is empty.",
    "2-3": "`true`",
    "3-0": "`is_not_empty`",
    "3-1": "`true`",
    "3-2": "Whether the select property value contains data.  \n  \nReturns data source entries where the select property value is not empty.",
    "3-3": "`true`"
  },
  "cols": 4,
  "rows": 4,
  "align": [
    "left",
    "left",
    "left",
    "left"
  ]
}
[/block]


```json Example select filter condition
{
  "filter": {
    "property": "Frontend framework",
    "select": {
      "equals": "React"
    }
  }
}
```

### Status

[block:parameters]
{
  "data": {
    "h-0": "Field",
    "h-1": "Type",
    "h-2": "Description",
    "h-3": "Example value",
    "0-0": "equals",
    "0-1": "string",
    "0-2": "The string to compare the status property value against.  \n  \nReturns data source entries where the status property value matches the provided string.",
    "0-3": "\"This week\"",
    "1-0": "does_not_equal",
    "1-1": "string",
    "1-2": "The string to compare the status property value against.  \n  \nReturns data source entries where the status property value does not match the provided string.",
    "1-3": "\"Backlog\"",
    "2-0": "is_empty",
    "2-1": "true",
    "2-2": "Whether the status property value does not contain data.  \n  \nReturns data source entries where the status property value is empty.",
    "2-3": "true",
    "3-0": "is_not_empty",
    "3-1": "true",
    "3-2": "Whether the status property value contains data.  \n  \nReturns data source entries where the status property value is not empty.",
    "3-3": "true"
  },
  "cols": 4,
  "rows": 4,
  "align": [
    "left",
    "left",
    "left",
    "left"
  ]
}
[/block]


```json Example status filter condition
{
  "filter": {
    "property": "Project status",
    "status": {
      "equals": "Not started"
    }
  }
}
```

### Timestamp

Use a timestamp filter condition to filter results based on `created_time` or `last_edited_time` values.

[block:parameters]
{
  "data": {
    "h-0": "Field",
    "h-1": "Type",
    "h-2": "Description",
    "h-3": "Example value",
    "0-0": "timestamp",
    "0-1": "created_time last_edited_time",
    "0-2": "A constant string representing the type of timestamp to use as a filter.",
    "0-3": "\"created_time\"",
    "1-0": "created_time  \nlast_edited_time",
    "1-1": "object",
    "1-2": "A date filter condition used to filter the specified timestamp.",
    "1-3": "Refer to the [date](#date) filter condition."
  },
  "cols": 4,
  "rows": 2,
  "align": [
    "left",
    "left",
    "left",
    "left"
  ]
}
[/block]


```json Example timestamp filter condition for created_time
{
  "filter": {
    "timestamp": "created_time",
    "created_time": {
      "on_or_before": "2022-10-13"
    }
  }
}
```

> 🚧
>
> The `timestamp` filter condition does not require a property name. The API throws an error if you provide one.

### Verification

[block:parameters]
{
  "data": {
    "h-0": "Field",
    "h-1": "Type",
    "h-2": "Description",
    "h-3": "Example value",
    "0-0": "status",
    "0-1": "string",
    "0-2": "The verification status being queried. Valid options are: `verified`, `expired`, `none`  \n  \nReturns data source entries where the current verification status matches the queried status.",
    "0-3": "\"verified\""
  },
  "cols": 4,
  "rows": 1,
  "align": [
    "left",
    "left",
    "left",
    "left"
  ]
}
[/block]


```json Example verification filter condition for getting verified pages
{
  "filter": {
    "property": "verification",
    "verification": {
      "status": "verified"
    }
  }
}
```

### ID

Use a timestamp filter condition to filter results based on the `unique_id` value.

[block:parameters]
{
  "data": {
    "h-0": "Field",
    "h-1": "Type",
    "h-2": "Description",
    "h-3": "Example value",
    "0-0": "`does_not_equal`",
    "0-1": "`number`",
    "0-2": "The value to compare the unique_id property value against.  \n  \nReturns data source entries where the unique_id property value differs from the provided value.",
    "0-3": "`42`",
    "1-0": "`equals`",
    "1-1": "`number`",
    "1-2": "The value to compare the unique_id property value against.  \n  \nReturns data source entries where the unique_id property value is the same as the provided value.",
    "1-3": "`42`",
    "2-0": "`greater_than`",
    "2-1": "`number`",
    "2-2": "The value to compare the unique_id property value against.  \n  \nReturns data source entries where the unique_id property value exceeds the provided value.",
    "2-3": "`42`",
    "3-0": "`greater_than_or_equal_to`",
    "3-1": "`number`",
    "3-2": "The value to compare the unique_id property value against.  \n  \nReturns data source entries where the unique_id property value is equal to or exceeds the provided value.",
    "3-3": "`42`",
    "4-0": "`less_than`",
    "4-1": "`number`",
    "4-2": "The value to compare the unique_id property value against.  \n  \nReturns data source entries where the unique_id property value is less than the provided value.",
    "4-3": "`42`",
    "5-0": "`less_than_or_equal_to`",
    "5-1": "`number`",
    "5-2": "The value to compare the unique_id property value against.  \n  \nReturns data source entries where the unique_id property value is equal to or is less than the provided value.",
    "5-3": "`42`"
  },
  "cols": 4,
  "rows": 6,
  "align": [
    "left",
    "left",
    "left",
    "left"
  ]
}
[/block]


```json Example ID filter condition
{
  "filter": {
    "and": [
      {
        "property": "ID",
        "unique_id": {
          "greater_than": 1
        }
      },
      {
        "property": "ID",
        "unique_id": {
          "less_than": 3
        }
      }
    ]
  }
}
```

## Compound filter conditions

You can use a compound filter condition to limit the results of a data source query based on multiple conditions. This mimics filter chaining in the Notion UI.

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/14ec7e8-Untitled.png",
        "Untitled.png",
        1340
      ],
      "align": "center",
      "caption": "An example filter chain in the Notion UI"
    }
  ]
}
[/block]


The above filters in the Notion UI are equivalent to the following compound filter condition via the API:

```json
{
  "and": [
    {
      "property": "Done",
      "checkbox": {
        "equals": true
      }
    },
    {
      "or": [
        {
          "property": "Tags",
          "contains": "A"
        },
        {
          "property": "Tags",
          "contains": "B"
        }
      ]
    }
  ]
}
```

A compound filter condition contains an `and` or `or` key with a value that is an array of filter objects or nested compound filter objects. Nesting is supported up to two levels deep.

[block:parameters]
{
  "data": {
    "h-0": "Field",
    "h-1": "Type",
    "h-2": "Description",
    "h-3": "Example value",
    "0-0": "`and`",
    "0-1": "`array`",
    "0-2": "An array of [filter](#type-specific-filter-conditions) objects or compound filter conditions.  \n  \nReturns data source entries that match **all** of the provided filter conditions.",
    "0-3": "Refer to the examples below.",
    "1-0": "or",
    "1-1": "array",
    "1-2": "An array of [filter](#type-specific-filter-conditions) objects or compound filter conditions.  \n  \nReturns data source entries that match **any** of the provided filter conditions",
    "1-3": "Refer to the examples below."
  },
  "cols": 4,
  "rows": 2,
  "align": [
    "left",
    "left",
    "left",
    "left"
  ]
}
[/block]


### Example compound filter conditions

```json Example compound filter condition for a checkbox and number property value
{
  "filter": {
    "and": [
      {
        "property": "Complete",
        "checkbox": {
          "equals": true
        }
      },
      {
        "property": "Working days",
        "number": {
          "greater_than": 10
        }
      }
    ]
  }
}
```

```json Example nested filter condition
{
  "filter": {
    "or": [
      {
        "property": "Description",
        "rich_text": {
          "contains": "2023"
        }
      },
      {
        "and": [
          {
            "property": "Department",
            "select": {
              "equals": "Engineering"
            }
          },
          {
            "property": "Priority goal",
            "checkbox": {
              "equals": true
            }
          }
        ]
      }
    ]
  }
}
```

# Sort data source entries

A sort is a condition used to order the entries returned from a data source query.

A [data source query](ref:query-a-data-source) can be sorted by a property and/or timestamp and in a given direction. For example, a library data source can be sorted by the "Name of a book" (i.e. property) and in `ascending` (i.e. direction).

Here is an example of a sort on a data source property.

```json Sorting by "Name" property in ascending direction
{
  "sorts": [
    {
      "property": "created_time",
      "direction": "ascending"
    },
  ]
}
```

If you’re using the [Notion SDK for JavaScript](https://github.com/makenotion/notion-sdk-js), you can apply this sorting property to your query like so:

```javascript
const { Client } = require('@notionhq/client');

const notion = new Client({ auth: process.env.NOTION_API_KEY });
// replace with your own data source ID
const dataSourceId = 'd9824bdc-8445-4327-be8b-5b47500af6ce';

const sortedRows = async () => {
  const response = await notion.dataSources.query({
    database_id: databaseId,
    sorts: [
      {
        property: "Name",
        direction: "ascending"
      }
    ],
  });
  return response;
}
```

Data source queries can also be sorted by two or more properties, which is formally called a nested sort. The sort object listed first in the nested sort list takes precedence.

Here is an example of a nested sort.

```json
{
  "sorts": [
        {
      "property": "Food group",
      "direction": "descending"
    },
    {
      "property": "Name",
      "direction": "ascending"
    }
  ]
}
```

In this example, the data source query will first be sorted by "Food group" and the set with the same food group is then sorted by "Name".

## Sort object

### Property value sort

This sort orders the data source query by a particular property.

The sort object must contain the following properties:

| Property    | Type            | Description                                                                      | Example value   |
| :---------- | :-------------- | :------------------------------------------------------------------------------- | :-------------- |
| `property`  | `string`        | The name of the property to sort against.                                        | `"Ingredients"` |
| `direction` | `string` (enum) | The direction to sort. Possible values include `"ascending"` and `"descending"`. | `"descending"`  |

### Entry timestamp sort

This sort orders the data source query by the timestamp associated with a data source entry.

The sort object must contain the following properties:

| Property    | Type            | Description                                                                                                   | Example value        |
| :---------- | :-------------- | :------------------------------------------------------------------------------------------------------------ | :------------------- |
| `timestamp` | `string` (enum) | The name of the timestamp to sort against. Possible values include `"created_time"` and `"last_edited_time"`. | `"last_edited_time"` |
| `direction` | `string` (enum) | The direction to sort. Possible values include `"ascending"` and `"descending"`.                              | `"descending"`       |
