# Tools Requiring Client-Side Execution

## Summary
These tools execute shell commands using `run_command()` which runs `asyncio.create_subprocess_shell()` on the **server's filesystem**. With HTTP transport, this means they execute on the remote server, NOT the client's local machine.

## Status: ❌ BROKEN WITH HTTP TRANSPORT

---

## Affected Tools

### 1. `check_blocks_cli()`
**Location:** `src/selise_mcp_server.py:1108`

**What it does:**
- Checks if Blocks CLI is installed by running `blocks --version`

**Problem:**
- Checks for CLI on the **server**, not the client's machine
- Will always fail unless CLI is installed on the server

**Fix needed:**
- Remove this tool (users should check locally)
- OR document that it checks server-side installation only

---

### 2. `install_blocks_cli()`
**Location:** `src/selise_mcp_server.py:1133`

**What it does:**
- Installs Blocks CLI using `npm install -g @seliseblocks/cli`

**Problem:**
- Installs on the **server's system**, not client's machine
- Requires npm and proper permissions on server
- Pointless for client's local development

**Fix needed:**
- **REMOVE** this tool entirely
- Replace with documentation instructing users to install locally

---

### 3. `create_local_repository()`
**Location:** `src/selise_mcp_server.py:1162`

**What it does:**
- Runs `blocks new {template} {repository_name} --cli --blocks-key {tenant_id} --app-domain {domain}`
- Creates a repository using Blocks CLI

**Problem:**
- Creates repository on **server's filesystem**, not client's workspace
- Files are inaccessible to the client
- Completely broken for remote HTTP use

**Fix needed:**
- **REMOVE** or redesign to:
  - Return CLI command as a string for user to run locally
  - Document manual setup steps

---

### 4. `init_git_repository()`
**Location:** `src/selise_mcp_server.py:1234`

**What it does:**
- Initializes git repository with multiple commands:
  - `git init`
  - `git remote add origin https://github.com/{github_name}/{repo_name}`
  - `git branch -M dev`
  - `git add .`
  - `git commit -m 'feat: initiate project'`
  - `git push -u origin dev`

**Problems:**
- **Uses `os.chdir(directory_path)`** - Changes server's working directory
- Initializes git on **server's filesystem**, not client's
- `git add .` adds server's files, not client's project
- Completely broken for HTTP transport

**Fix needed:**
- **REMOVE** this tool entirely
- Replace with:
  - Return git commands as a string for user to execute
  - Or create a guide/documentation

---

## Root Cause: `run_command()` Function
**Location:** `src/selise_mcp_server.py:115`

```python
async def run_command(command: str) -> Dict[str, Any]:
    """Run a shell command asynchronously and return the result."""
    process = await asyncio.create_subprocess_shell(
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
```

This function executes on the **MCP server**, not the client.

---

## MCP Protocol Limitation

According to FastMCP documentation:
- **STDIO transport**: Client launches server as subprocess on local machine (commands would work)
- **HTTP transport**: Server runs remotely, completely separate from client (commands broken)

**There is NO mechanism in MCP protocol to execute commands on the client side from an HTTP server.**

---

## Recommended Actions

### Immediate (Required for HTTP Transport):

1. ✅ **Remove these tools:**
   - `install_blocks_cli()`
   - `create_local_repository()`
   - `init_git_repository()`

2. ⚠️ **Modify this tool:**
   - `check_blocks_cli()` - Document that it checks server-side only (likely not useful)

3. 📝 **Create documentation:**
   - Add setup guide for local project initialization
   - Provide commands users should run locally
   - Update `get_project_setup()` to include local setup instructions

### Alternative Solutions:

**Option A: Instruction-Based Approach**
- Tools return formatted instructions/commands
- User copies and runs commands locally
- MCP tools focus on cloud/API operations only

**Option B: Hybrid Approach**
- Keep API-based tools (login, create_project, schemas, etc.)
- Remove filesystem/CLI tools
- Provide rich documentation for local setup

**Option C: STDIO Fallback** (Not recommended)
- Offer STDIO transport for local use
- Keep HTTP for cloud operations
- Confusing for users, harder to maintain

---

## Safe Tools (API-Based - No Changes Needed)

All other tools are safe because they only make HTTP API calls to Selise Blocks:
- Authentication tools (login, get_auth_status, etc.)
- Project management (get_projects, create_project, set_application_domain)
- Schema tools (create_schema, list_schemas, get_schema, etc.)
- IAM tools (roles, permissions)
- CAPTCHA tools
- MFA tools
- Documentation tools
- All other API-based operations

---

## Conclusion

**For HTTP transport deployment, we MUST remove or redesign the 4 CLI/filesystem tools.** They fundamentally cannot work with remote server deployment and will confuse users or fail silently.
