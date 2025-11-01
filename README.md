# VibeMini-MCP: Complete Selise Cloud Development System

A comprehensive development system combining:
1. **MCP Server** - 35 tools for Selise Cloud platform automation and frontend development documentation
2. **LLM Documentation** - Complete development workflows, recipes, and patterns hosted on GitHub

The MCP server now handles both **Selise Cloud backend operations** (33 tools) and **frontend development guidance** (2 documentation tools), providing a complete end-to-end development experience.

Designed for AI agents (Claude Code, Cursor, etc.) to build production-ready applications with proper multi-user authentication, data isolation, and enterprise security.

## Features

### 🔐 **Authentication & Security**
- **Multi-Factor Authentication (MFA)**: Email and authenticator app support
- **Single Sign-On (SSO)**: OAuth integration for Google, Facebook, GitHub, and other providers  
- **CAPTCHA Management**: Google reCAPTCHA and hCaptcha configuration
- **Token Management**: Automatic access token handling with expiration tracking

### 🏗️ **Project & Infrastructure**
- **Project Management**: Create, list, and configure Selise Cloud projects
- **Repository Integration**: GitHub/Git repository linking and local repository creation
- **Application Domains**: Automatic domain extraction and configuration
- **Blocks CLI Integration**: Automated CLI installation and repository scaffolding

### 📊 **GraphQL Schema Management**
- **Schema Operations**: Create, list, update, and finalize GraphQL schemas
- **Field Management**: Dynamic schema field addition and modification
- **Data Gateway**: Configure GraphQL data gateway for real-time operations

### 👥 **Identity & Access Management (IAM)**
- **Role Management**: Create and list user roles with descriptions and slugs
- **Permission System**: Comprehensive CRUD operations for permissions with resource groups
- **Role-Permission Assignment**: Assign/remove permissions from roles dynamically
- **Resource Groups**: Organize permissions into logical resource groupings

### 🔧 **Configuration & State**
- **Global State Management**: Track authentication, domains, and project context
- **Authentication Configuration**: Social login activation and settings management
- **Security Headers**: Enterprise-grade API security with proper CORS handling

### 📚 **Documentation Tools (NEW)**
- **list_sections**: Discover all 16 available documentation topics from GitHub
- **get_documentation**: Fetch specific workflows, recipes, and patterns on-demand
- **GitHub Integration**: Always up-to-date documentation fetched directly from repository
- **Covers**: Project setup, GraphQL CRUD, React patterns, IAM mapping, architecture, and more

## 📚 **LLM Documentation System**

### **Complete Development Workflows**
- **User Interaction Patterns**: How to gather requirements and detect multi-user apps
- **Feature Planning**: Break down tasks with real-time tracking (TASKS.md, SCRATCHPAD.md)
- **Schema Design**: NoSQL patterns with automatic business record bridging
- **Implementation Recipes**: Production-ready patterns for GraphQL, forms, permissions

### **Multi-User Application Support**
- **IAM-to-Business Data Mapping**: Bridge Selise Cloud authentication to business entities
- **Role-Based Access Control**: Complete RBAC implementation with MCP role management  
- **Data Isolation**: Ensure users only see their own data with security patterns
- **Auto-Provisioning**: Automatic user onboarding with business record creation

### **5 Production-Ready Recipes**
- **graphql-crud.md** - MongoDB/NoSQL GraphQL operations (CRITICAL)
- **react-hook-form-integration.md** - Form patterns with Zod validation
- **confirmation-modal-patterns.md** - Standardized confirmation dialogs
- **iam-to-business-data-mapping.md** - Multi-user data isolation patterns
- **permissions-and-roles.md** - Complete RBAC implementation guide

### **Component Hierarchy System**
- **3-Layer Architecture**: Feature → Block → UI component structure
- **Component Catalog**: Quick reference for all Selise components
- **Usage Patterns**: When to use AdvanceDataTable, ConfirmationModal, etc.

## Quick Start (Complete Setup)

### 1. Clone Repository
```bash
git clone https://github.com/milab-nsu/VibeMini-MCP.git
cd VibeMini-MCP
```

### 2. Setup MCP Server
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Add MCP server to Claude Code
claude mcp add selise-cloud python /absolute/path/to/selise_mcp_server.py
```

### 3. Access Documentation (via MCP Tools)
**Documentation is now accessed directly via MCP tools - no local files needed:**

```python
# Use MCP tools in your AI agent (Claude Code, Cursor, etc.):

# 1. Discover all available documentation topics
list_sections()

# 2. Fetch specific documentation as needed
get_documentation("project-setup")
get_documentation(["graphql-crud", "architecture-patterns"])
```

**Documentation Repository:** https://github.com/mustavikhan05/selise-blocks-docs

### 4. Start Building
Open your project in Claude Code or Cursor and say:

```
"Use list_sections to discover available documentation, then help me build a [describe your app].
Fetch relevant workflows and recipes using get_documentation as needed."
```

**For multi-user apps, mention:** "This app will have multiple users with different access levels"

The MCP server will automatically fetch relevant documentation from GitHub as needed.

## What You Get

### 🤖 **AI Agent Optimized**
- **Decision Trees**: Clear guidance for single-user vs multi-user apps
- **Conditional Workflows**: Only read relevant recipes for your app type
- **Real-time Tracking**: TASKS.md, SCRATCHPAD.md, FEATURELIST.md stay current
- **Error Prevention**: NoSQL patterns, security best practices built-in

### 🏗️ **Complete Development Pipeline**
1. **Requirements Gathering** → Structured user interaction with multi-user detection
2. **Project Setup** → Automated MCP-based Selise Cloud project creation  
3. **Schema Design** → NoSQL patterns with user confirmation workflow
4. **Implementation** → Recipe-driven development with 3-layer architecture
5. **Testing & Deployment** → Quality checks and git workflow integration

## Available Tools (35 Total)

### 🔐 Authentication & Core (3 tools)
- `login(username, password)` - Authenticate with Selise Cloud API
- `get_auth_status()` - Check current authentication status and token validity
- `get_global_state()` - Get current global state including auth and app state

### 🏗️ Project Management (2 tools)
- `get_projects(tenant_group_id, page, page_size)` - List projects and extract application domains
- `create_project(project_name, repo_name, repo_link, repo_id, is_production)` - Create new Selise Cloud project

### 📊 GraphQL Schema Management (5 tools)
- `create_schema(schema_name, project_key)` - Create new GraphQL schema
- `list_schemas(project_key, keyword, page_size, page_number, sort_descending, sort_by)` - List existing schemas
- `get_schema(schema_id, project_key)` - Get schema details and fields by ID
- `update_schema_fields(schema_id, fields, project_key)` - Update schema field definitions
- `finalize_schema(schema_id, project_key)` - Finalize and commit schema changes

### 🔧 Repository & CLI Management (4 tools)
- `set_application_domain(domain, tenant_id, project_name)` - Set application domain and tenant ID
- `check_blocks_cli()` - Check if Blocks CLI is installed and available
- `install_blocks_cli()` - Install Blocks CLI using npm package manager
- `create_local_repository(repository_name, template, use_cli)` - Create local Selise repository

### 🔑 Authentication Configuration (2 tools)
- `activate_social_login(item_id, project_key, ...)` - Activate social login with token configurations
- `get_authentication_config(project_key)` - Get current authentication configuration

### 🛡️ CAPTCHA Management (3 tools)
- `save_captcha_config(provider, site_key, secret_key, project_key, is_enable)` - Configure Google reCAPTCHA or hCaptcha
- `list_captcha_configs(project_key)` - List all CAPTCHA configurations for project
- `update_captcha_status(item_id, is_enable, project_key)` - Enable/disable CAPTCHA configurations

### 👥 IAM Role Management (2 tools)
- `list_roles(project_key, page, page_size, search, sort_by, sort_descending)` - List all roles with pagination
- `create_role(name, description, slug, project_key)` - Create new role with slug identifier

### 🔐 IAM Permission Management (4 tools)
- `list_permissions(project_key, page, page_size, search, sort_by, sort_descending, is_built_in, resource_group)` - List permissions with filtering
- `create_permission(name, description, resource, resource_group, tags, project_key, type, dependent_permissions, is_built_in)` - Create new permission
- `update_permission(item_id, name, description, resource, resource_group, tags, project_key, type, dependent_permissions, is_built_in)` - Update existing permission
- `get_resource_groups(project_key)` - Get available resource groups for organizing permissions

### 🔗 Role-Permission Assignment (2 tools)
- `set_role_permissions(role_slug, add_permissions, remove_permissions, project_key)` - Assign/remove permissions from roles
- `get_role_permissions(role_slugs, project_key, page, page_size, search, is_built_in, resource_group)` - Get permissions assigned to specific roles

### 🔒 Multi-Factor Authentication (4 tools)
- `enable_mfa(project_key, mfa_types)` - Enable MFA with custom types (email, authenticator)
- `enable_email_mfa(project_key)` - Enable email-only MFA configuration
- `enable_authenticator_mfa(project_key)` - Enable authenticator app-only MFA
- `enable_both_mfa_types(project_key)` - Enable both email and authenticator MFA

### 🌐 Data Gateway (1 tool)
- `configure_blocks_data_gateway(project_key, gateway_config)` - Configure GraphQL data gateway with real-time subscriptions

### 🔑 Single Sign-On (1 tool)
- `add_sso_credential(provider, client_id, client_secret, project_key, is_enable, redirect_uri)` - Add OAuth SSO credentials for providers (Google, Facebook, GitHub, etc.)

### 📚 Documentation Access (2 tools)
- `list_sections()` - Discover all 16 available documentation topics from GitHub with metadata
- `get_documentation(topic)` - Fetch specific documentation by topic ID (single or multiple topics)

## Usage Examples

### Basic Authentication
```python
# Login to Selise Cloud
await login("your-email@example.com", "your-password")

# Check authentication status
await get_auth_status()
```

### Project Setup
```python
# Get list of projects
await get_projects()

# Create a new project
await create_project(
    project_name="my-new-project",
    repo_name="username/my-repo",
    repo_link="https://github.com/username/my-repo.git",
    repo_id="123456789"
)
```

### Schema Management
```python
# Create a new schema
await create_schema("User")

# List all schemas
await list_schemas()

# Get schema by ID
await get_schema("schema-id-here")
```

### Local Repository Creation
```python
# Check if Blocks CLI is installed
await check_blocks_cli()

# Install Blocks CLI if needed
await install_blocks_cli()

# Create a local repository
await create_local_repository("my-app", "web", use_cli=True)
```

### Security & Authentication
```python
# Configure CAPTCHA (Google reCAPTCHA)
await save_captcha_config("recaptcha", "site_key_here", "secret_key_here")

# Enable Multi-Factor Authentication
await enable_both_mfa_types()  # Enables both email and authenticator

# Add Google OAuth SSO
await add_sso_credential("google", "client_id", "client_secret")
```

### Identity & Access Management
```python
# Create roles
await create_role("admin", "Administrator role", "admin")
await create_role("editor", "Editor role", "editor")

# Create permissions
await create_permission("user_management", "Manage users", "Users", "Administration", ["create", "read", "update", "delete"])

# Assign permissions to roles
await set_role_permissions("admin", add_permissions=["permission_id_here"])

# List role permissions
await get_role_permissions(["admin", "editor"])
```

### Data Gateway Configuration
```python
# Configure GraphQL data gateway
await configure_blocks_data_gateway(gateway_config={
    "enableDataGateway": True,
    "enableRealTimeSubscriptions": True
})
```

## Configuration

The server maintains global state for:
- **Authentication**: Access tokens, refresh tokens, and expiration times
- **Application State**: Current application domain, tenant ID, and project name

This state is automatically managed and updated as you use the various tools.

## Error Handling

All tools return JSON responses with:
- `status`: "success" or "error"
- `message`: Descriptive message about the result
- Additional data specific to each tool

## Security Notes

- Access tokens are automatically managed and validated
- Tokens expire and need to be refreshed by re-authenticating
- The server includes security headers matching the Selise Cloud web interface
- Never commit credentials or tokens to version control

## Troubleshooting

### Authentication Issues
- You need to register an account in Selise Cloud first. 

### CLI Issues
- Ensure Node.js and npm are installed
- Check if the Blocks CLI installation was successful
- Verify global npm permissions

### Schema/Project Issues
- Selise cloud doesn't support the same schema names (to be fixed), even for different projects & accounts. If schema creation fails, try a different name. The agent should tell you when it fails due to naming conflicts.

## API Endpoints

The server communicates with the following Selise Cloud API endpoints:

### Core Services
- **Authentication**: `https://api.seliseblocks.com/authentication/v1/OAuth/Token`
- **Projects**: `https://api.seliseblocks.com/identifier/v1/Project/*`
- **GraphQL Schemas**: `https://api.seliseblocks.com/graphql/v1/schemas/*`
- **Configuration**: `https://api.seliseblocks.com/authentication/v1/Configuration/*`

### Security & IAM
- **CAPTCHA**: `https://api.seliseblocks.com/captcha/v1/Configuration/*`
- **IAM Roles**: `https://api.seliseblocks.com/iam/v1/Resource/GetRoles`, `CreateRole`
- **IAM Permissions**: `https://api.seliseblocks.com/iam/v1/Resource/GetPermissions`, `CreatePermission`, `UpdatePermission`
- **Role Assignment**: `https://api.seliseblocks.com/iam/v1/Resource/SetRoles`
- **Resource Groups**: `https://api.seliseblocks.com/iam/v1/Resource/GetResourceGroups`

### Advanced Features
- **Multi-Factor Authentication**: `https://api.seliseblocks.com/mfa/v1/Configuration/Save`
- **Data Gateway**: `https://api.seliseblocks.com/graphql/v1/configurations`
- **SSO Credentials**: `https://api.seliseblocks.com/authentication/v1/Social/SaveSsoCredential`

## Enterprise Features

This MCP server provides enterprise-grade capabilities:

### 🏢 **Complete Platform Control**
- **33 MCP Tools**: Comprehensive Selise Cloud management
- **Zero Manual Configuration**: Automated setup and deployment workflows
- **Enterprise Security**: MFA, SSO, CAPTCHA, and IAM management
- **Production Ready**: Token management, error handling, and state persistence

### 🔧 **Development Workflow Integration**
- **AI Agent Compatible**: Designed for Claude Code and other MCP clients
- **Automated Repository Setup**: GitHub integration with local development
- **Schema Management**: GraphQL schema lifecycle management
- **CLI Integration**: Blocks CLI automation for rapid development

### 📊 **Monitoring & Management**
- **Global State Tracking**: Authentication, projects, and configuration state
- **Comprehensive Error Handling**: Detailed error messages and status codes
- **Security Headers**: Enterprise CORS and security header management
- **Token Validation**: Automatic token refresh and expiration handling

## Example Workflow

Here's what happens when you ask Claude Code to "build me a task management app with admin and regular users":

### 1. **Auto-Detection** 🔍
```
Agent reads CLAUDE.md → Detects "admin and regular users" → 
Classifies as MULTI-USER APP → Reads additional recipes:
- iam-to-business-data-mapping.md
- permissions-and-roles.md
```

### 2. **Requirements Gathering** 📝
```
Agent follows user-interaction.md patterns:
- "Will multiple people use this with separate accounts?" ✅
- "Should each user only see their own tasks?" ✅ 
- "Do you need admin users who see all tasks?" ✅

Creates: FEATURELIST.md, TASKS.md, SCRATCHPAD.md, CLOUD.md
```

### 3. **Project Setup** 🚀
```
Agent uses MCP tools:
login() → create_project() → create_local_repository()
Documents everything in CLOUD.md
```

### 4. **Schema Design** 📊
```
Agent plans NoSQL schemas:
BusinessRecord (bridges IAM to business data)
Tasks (with BusinessRecordId for data isolation)
Asks user: "Does this schema look good?"
Uses MCP: create_schema() for each entity
```

### 5. **Implementation** 💻
```
Agent follows recipes systematically:
- GraphQL queries with user filtering (graphql-crud.md)
- Business record auto-provisioning (iam-to-business-data-mapping.md) 
- Role-based UI controls (permissions-and-roles.md)
- Updates TASKS.md: [ ] → [🔄] → [x] for each task
```

### 6. **Result** ✨
**Production-ready app with:**
- ✅ Secure user authentication via Selise Cloud
- ✅ Data isolation (users only see their own tasks)
- ✅ Admin panel (admins see all tasks)
- ✅ Auto-provisioning (new users get business records)
- ✅ Role-based permissions and UI
- ✅ NoSQL patterns with proper GraphQL operations

## Getting Started

1. **Clone this repo**
2. **Setup MCP server** (follow Quick Start above)
3. **Copy CLAUDE.md to your project**
4. **Ask your AI agent**: "Read CLAUDE.md and build me a [your app idea]"

The system handles everything from requirements to deployment! 🎉