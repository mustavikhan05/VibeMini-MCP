# MCP Tools Reference

Complete reference of all available MCP tools in the SELISE MCP Server.

## Authentication Tools

### login
Authenticate with Selise Blocks API and retrieve access tokens.

**Args:**
- username: Email address for login
- password: Password for login

**Returns:** JSON string with authentication status and token info

---

### get_auth_status
Check current authentication status and token validity.

**Returns:** JSON string with authentication status

---

### get_global_state
Get the current global state including authentication and application domain.

**Returns:** JSON string with current global state

---

## Project Management Tools

### get_projects
Get projects from Selise Blocks API and extract application domains.

**Args:**
- tenant_group_id: Tenant Group ID to filter projects (optional)
- page: Page number for pagination (default: 0)
- page_size: Number of items per page (default: 100)

**Returns:** JSON string with projects data and extracted application domains

---

### create_project
Create a new project in Selise Cloud.

**Args:**
- project_name: Name of the project to create
- repo_name: Repository name (e.g., 'username/repo')
- repo_link: Full GitHub repository URL
- repo_id: Repository ID from GitHub or Git provider
- is_production: Whether this is a production environment (default: False)

**Returns:** JSON string with project creation results

---

### set_application_domain
Manually set the application domain and tenant ID for repository creation.

**Args:**
- domain: Application domain URL
- tenant_id: Tenant ID for the project
- project_name: Project name (optional)
- tenant_group_id: Tenant Group ID (optional)

**Returns:** JSON string with confirmation

---

## Schema Management Tools

### create_schema
Create a new schema in Selise Blocks GraphQL API.

**Args:**
- schema_name: Name of the schema to create
- project_key: Project key (tenant ID). Uses global tenant_id if not provided

**Returns:** JSON string with schema creation result

---

### list_schemas
List schemas from Selise Blocks GraphQL API.

**Args:**
- project_key: Project key (tenant ID). Uses global tenant_id if not provided
- keyword: Search keyword for filtering schemas
- page_size: Number of items per page (default: 100)
- page_number: Page number for pagination (default: 1)
- sort_descending: Sort in descending order (default: True)
- sort_by: Field to sort by (default: "CreatedDate")

**Returns:** JSON string with schemas listing result

---

### get_schema
Get a schema's current fields using its ID (step 1 of schema field management).

**Args:**
- schema_id: The ID of the schema to retrieve
- project_key: Project key (tenant ID). Uses global tenant_id if not provided

**Returns:** JSON string with schema fields and metadata

---

### update_schema_fields
Update schema fields (step 2 of schema field management).

**Args:**
- schema_id: The ID of the schema to update
- fields: Complete list of fields for the schema (existing + new)
- project_key: Project key (tenant ID). Uses global tenant_id if not provided

**Returns:** JSON string with update result

---

### finalize_schema
Finalize schema changes by retrieving updated schema (step 3 of schema field management).

**Args:**
- schema_id: The ID of the schema to finalize
- project_key: Project key (tenant ID). Uses global tenant_id if not provided

**Returns:** JSON string with finalized schema data

---

## Blocks CLI Tools

### check_blocks_cli
Get instructions for checking if Blocks CLI is installed locally.

**Returns:** JSON string with command to verify CLI installation on your local machine

**Note:** This tool provides the command to run locally. The server does not check your local installation.

---

### install_blocks_cli
Get instructions and commands for installing Blocks CLI using npm.

**Returns:** JSON string with installation commands and verification steps to run locally

**Note:** This tool provides commands to run on your local machine. Installation happens locally, not on the server.

---

### create_local_repository
Generate the command to create a local repository using Blocks CLI.

This tool generates the complete blocks CLI command with your project's configuration (tenant ID and application domain) pre-filled.

**Args:**
- repository_name: Name of the repository to create (uses project name if empty)
- template: Template to use for the repository (default: "web")
- use_cli: Whether to use CLI mode (default: True)

**Returns:** JSON string with the complete blocks CLI command pre-configured with your project settings

**Note:** Run the returned command in your terminal to create the repository locally.

---

### init_git_repository
Generate commands to initialize a git repository and push to GitHub.

This tool generates the complete git initialization workflow including remote setup and initial push to the dev branch.

**Args:**
- github_name: GitHub username or organization name
- repo_name: Repository name on GitHub
- directory_path: Path to the directory to initialize (default: current directory)

**Returns:** JSON string with step-by-step git commands to run locally

**Note:** Run the returned commands in your terminal. Ensure the GitHub repository exists and you have push access.

---

### list_github_repos
Get all GitHub repositories for a project.

**Args:**
- project_key: Project key (tenant ID). Uses global tenant_id if not provided

**Returns:** JSON string with GitHub repositories list

---

## Authentication Configuration Tools

### get_authentication_config
Get the current authentication configuration for the project.

**Args:**
- project_key: Project key (tenant ID). Uses global tenant_id if not provided

**Returns:** JSON string with current authentication configuration

---

### activate_social_login
Activate social login for the project by updating authentication configuration.

**Args:**
- item_id: Configuration item ID (default: "682c40c3872fab1bc2cc8988")
- project_key: Project key (tenant ID). Uses global tenant_id if not provided
- refresh_token_minutes: Refresh token validity in minutes (default: 300)
- access_token_minutes: Access token validity in minutes (default: 15)
- remember_me_minutes: Remember me token validity in minutes (default: 43200)
- allowed_grant_types: List of allowed grant types (default: ["password", "refresh_token", "social"])
- wrong_attempts_lock: Number of wrong attempts before lock (default: 5)
- lock_duration_minutes: Lock duration in minutes (default: 5)

**Returns:** JSON string with social login activation result

---

### add_sso_credential
Add SSO credentials for external authentication providers.

**Args:**
- provider_name: Name of the SSO provider
- client_id: Client ID from the provider
- client_secret: Client secret from the provider
- project_key: Project key (tenant ID). Uses global tenant_id if not provided

**Returns:** JSON string with SSO credential addition result

---

### enable_email_mfa
Enable Email Multi-Factor Authentication for a project.

**Args:**
- project_key: Project key (tenant ID). Uses global tenant_id if not provided

**Returns:** JSON string with Email MFA configuration result

---

### enable_authenticator_mfa
Enable Authenticator Multi-Factor Authentication for a project.

**Args:**
- project_key: Project key (tenant ID). Uses global tenant_id if not provided

**Returns:** JSON string with Authenticator MFA configuration result

---

## CAPTCHA Tools

### save_captcha_config
Save a new CAPTCHA configuration.

**Args:**
- captcha_type: Type of CAPTCHA (e.g., "recaptcha", "hcaptcha")
- site_key: Site key from CAPTCHA provider
- secret_key: Secret key from CAPTCHA provider
- project_key: Project key (tenant ID). Uses global tenant_id if not provided

**Returns:** JSON string with CAPTCHA configuration save result

---

### list_captcha_configs
List all CAPTCHA configurations for a project.

**Args:**
- project_key: Project key (tenant ID). Uses global tenant_id if not provided

**Returns:** JSON string with list of CAPTCHA configurations

---

### update_captcha_status
Enable or disable a CAPTCHA configuration.

**Args:**
- item_id: The ID of the CAPTCHA configuration to update
- is_enable: True to enable, False to disable the configuration
- project_key: Project key (tenant ID). Uses global tenant_id if not provided

**Returns:** JSON string with status update result

---

## IAM Tools (Roles & Permissions)

### list_roles
List all roles in the project.

**Args:**
- project_key: Project key (tenant ID). Uses global tenant_id if not provided
- page: Page number for pagination
- page_size: Number of items per page

**Returns:** JSON string with roles list

---

### create_role
Create a new role.

**Args:**
- name: Role name
- description: Role description
- slug: Role slug (URL-friendly identifier)
- project_key: Project key (tenant ID). Uses global tenant_id if not provided

**Returns:** JSON string with role creation result

---

### list_permissions
List all permissions in the project.

**Args:**
- project_key: Project key (tenant ID). Uses global tenant_id if not provided
- page: Page number for pagination
- page_size: Number of items per page

**Returns:** JSON string with permissions list

---

### create_permission
Create a new permission.

**Args:**
- name: Permission name
- description: Permission description
- resource_group_id: Resource group ID
- project_key: Project key (tenant ID). Uses global tenant_id if not provided

**Returns:** JSON string with permission creation result

---

### update_permission
Update an existing permission.

**Args:**
- permission_id: ID of the permission to update
- name: New permission name
- description: New permission description
- project_key: Project key (tenant ID). Uses global tenant_id if not provided

**Returns:** JSON string with permission update result

---

### get_resource_groups
Get available resource groups for a project.

**Args:**
- project_key: Project key (tenant ID). Uses global tenant_id if not provided

**Returns:** JSON string with resource groups result

---

### set_role_permissions
Assign or remove permissions from a role.

**Args:**
- role_slug: Role slug identifier
- add_permissions: List of permission IDs to add to the role (default: [])
- remove_permissions: List of permission IDs to remove from the role (default: [])
- project_key: Project key (tenant ID). Uses global tenant_id if not provided

**Returns:** JSON string with role permission assignment result

---

### get_role_permissions
Get all permissions assigned to a role.

**Args:**
- role_slug: Role slug identifier
- project_key: Project key (tenant ID). Uses global tenant_id if not provided

**Returns:** JSON string with role permissions

---

## Configuration Tools

### configure_blocks_data_gateway
Configure Blocks Data Gateway for GraphQL operations.

**Args:**
- project_key: Project key (tenant ID). Uses global tenant_id if not provided
- gateway_config: Gateway configuration dictionary

**Returns:** JSON string with data gateway configuration result

---

## Documentation Tools

### list_sections
⚠️ **CALL THIS FIRST** - Discover all available Selise Blocks documentation topics.

Returns metadata for all documentation including:
- Workflows (project setup, feature planning, implementation checklist)
- Recipes (GraphQL CRUD, forms, permissions, modals)
- Component catalog and architecture patterns
- Use cases and triggers for when to read each topic

**Returns:** JSON string with complete topics catalog and metadata

---

### get_documentation
Fetch specific Selise Blocks documentation by topic ID or multiple topics.

Use this tool to retrieve full documentation content for:
- Workflows: 'project-setup', 'feature-planning', 'implementation-checklist'
- Recipes: 'graphql-crud', 'react-hook-form', 'permissions-and-roles'
- Architecture: 'patterns', 'pitfalls'
- Components: 'component-quick-reference', 'selise-component-hierarchy'

**Args:**
- topic: Single topic ID (string) or list of topic IDs (e.g., ['graphql-crud', 'patterns'])

**Returns:** JSON string with full markdown content for requested topics

**Note:** Token limit is ~20-25k per call. For large requests, split into multiple calls.

**Prerequisite:** Call list_sections first to discover all available topics and their IDs.

---

### get_project_setup
⚠️ **STEP 1: Call FIRST** when user wants to build a project.

Returns the complete Vibecoding workflow for project setup including:
- User interaction patterns
- Feature planning approach
- Tracking file setup (TASKS.md, SCRATCHPAD.md, etc.)
- MCP tool usage workflow
- CLAUDE.md template for the project

**After calling this tool:**
1. Read the project setup workflow documentation
2. Create CLAUDE.md in the project root using the provided template
3. Follow the Vibecoding workflow

**Returns:** JSON string with project setup workflow documentation and CLAUDE.md content

**NEXT:** Follow Vibecoding flow, then call get_implementation_checklist

---

### get_implementation_checklist
⚠️ **REQUIRED** - Call BEFORE writing implementation code.

Returns the implementation checklist to verify prerequisites before coding:
- Schema confirmation requirements
- User approval checkpoints
- MCP tool preparation steps
- Architecture planning verification

**When to call:** After project setup and BEFORE starting implementation.

**Returns:** JSON string with implementation checklist documentation

**NEXT:** Call get_dev_workflow and get_architecture_patterns

---

### get_dev_workflow
Call when starting implementation or when git workflow is unclear.

Returns the development workflow including:
- Git commit patterns
- Code review process
- Testing approach
- Deployment workflow

**When to use:** During active development to follow proper workflow.

**Returns:** JSON string with development workflow documentation

**NEXT:** Call get_documentation for specific patterns, get_common_pitfalls before commits

---

### get_architecture_patterns
Call when planning features or deciding component structure.

Returns the 3-layer architecture hierarchy guide:
- Feature → Block → UI component structure
- Component organization patterns
- When to use which components
- Proper separation of concerns

**When to use:** When designing new features or refactoring structure.

**Returns:** JSON string with architecture patterns documentation

**Remember:** Inventory is STRUCTURE only, use graphql-crud recipe for data operations

---

### get_common_pitfalls
⚠️ **Call BEFORE committing code.**

Returns anti-patterns and common mistakes to avoid:
- GraphQL operation mistakes
- Data handling errors
- Component usage anti-patterns
- Security pitfalls

**When to use:** As a final check before committing to catch common errors.

**Returns:** JSON string with common pitfalls documentation

---

## Tool Usage Workflow

### For New Projects:
1. `get_project_setup()` - Read the Vibecoding workflow FIRST
2. `login()` - Authenticate
3. `create_project()` - Create Selise Cloud project
4. Create tracking files (FEATURELIST.md, TASKS.md, SCRATCHPAD.md, CLOUD.md)
5. `create_schema()` - Create schemas after user confirmation
6. `get_implementation_checklist()` - Verify prerequisites before coding
7. `get_dev_workflow()` - Follow during implementation
8. `get_common_pitfalls()` - Check before commits

### For Schema Management:
1. `list_schemas()` - See existing schemas
2. `create_schema()` - Create new schema
3. `get_schema()` - Get current fields
4. `update_schema_fields()` - Update fields
5. `finalize_schema()` - Finalize changes

### For Documentation:
1. `list_sections()` - Discover all topics
2. `get_documentation(topic)` - Fetch specific topics
3. Or use convenience tools: `get_project_setup()`, `get_implementation_checklist()`, etc.
