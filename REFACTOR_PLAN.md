# Refactor Plan: Convert CLI Tools to Command Generators

## Overview
Convert tools that execute shell commands on the server to return formatted command strings for users to run locally on their machines.

---

## Task List

### Task 1: Update `check_blocks_cli()`
**Location:** `src/selise_mcp_server.py:1108`

**Changes needed:**
- [ ] Remove `run_command("blocks --version")` call
- [ ] Return instructions on how to check CLI installation
- [ ] Include verification command: `blocks --version`
- [ ] Update docstring to reflect new behavior
- [ ] Return format:
  ```json
  {
    "status": "info",
    "message": "To check if Blocks CLI is installed, run this command:",
    "command": "blocks --version",
    "instructions": "If installed, you'll see the version number. If not, install it using npm."
  }
  ```

**Docstring update:**
```python
"""
Get instructions for checking if Blocks CLI is installed locally.

Returns:
    JSON string with command to check CLI installation status
"""
```

---

### Task 2: Update `install_blocks_cli()`
**Location:** `src/selise_mcp_server.py:1133`

**Changes needed:**
- [ ] Remove `run_command("npm install -g @seliseblocks/cli")` call
- [ ] Remove verification step
- [ ] Return installation command and verification steps
- [ ] Update docstring to reflect new behavior
- [ ] Return format:
  ```json
  {
    "status": "ready",
    "message": "To install Blocks CLI, run these commands:",
    "commands": [
      "npm install -g @seliseblocks/cli",
      "blocks --version"
    ],
    "instructions": "1. Run the installation command\n2. Verify installation with version check\n3. You should see the CLI version number"
  }
  ```

**Docstring update:**
```python
"""
Get instructions for installing Blocks CLI locally using npm.

Returns:
    JSON string with installation commands and verification steps
"""
```

---

### Task 3: Update `create_local_repository()`
**Location:** `src/selise_mcp_server.py:1162`

**Changes needed:**
- [ ] Remove CLI availability check (`run_command("blocks --version")`)
- [ ] Remove repository creation (`run_command(blocks new ...)`)
- [ ] Build the command string with all parameters
- [ ] Return formatted command for user to run
- [ ] Update docstring to reflect new behavior
- [ ] Return format:
  ```json
  {
    "status": "ready",
    "message": "To create your local repository, run this command in your terminal:",
    "command": "blocks new web {repository_name} --cli --blocks-key {tenant_id} --app-domain {domain}",
    "working_directory": "Navigate to your projects folder first",
    "next_steps": "After running the command, the repository will be created in a new folder named '{repository_name}'",
    "note": "Make sure Blocks CLI is installed. If not, use the install_blocks_cli tool first."
  }
  ```

**Docstring update:**
```python
"""
Get the command to create a local Selise repository using Blocks CLI.

This tool generates the complete blocks CLI command with your project's
configuration (tenant ID and application domain) pre-filled.

Args:
    repository_name: Name for the local repository (uses project name if empty)
    template: Template to use for the repository (default: "web")
    use_cli: Whether to use CLI mode (default: True)

Returns:
    JSON string with the command to run locally and instructions
"""
```

---

### Task 4: Update `init_git_repository()`
**Location:** `src/selise_mcp_server.py:1234`

**Changes needed:**
- [ ] Remove all `run_command()` calls for git operations
- [ ] Remove `os.chdir()` call (no longer needed)
- [ ] Build array of git commands
- [ ] Return formatted commands for user to run
- [ ] Update docstring to reflect new behavior
- [ ] Return format:
  ```json
  {
    "status": "ready",
    "message": "To initialize git repository and push to GitHub, run these commands:",
    "working_directory": "{directory_path}",
    "commands": [
      "cd {directory_path}",
      "git init",
      "git remote add origin https://github.com/{github_name}/{repo_name}",
      "git branch -M dev",
      "git add .",
      "git commit -m 'feat: initiate project'",
      "git push -u origin dev"
    ],
    "instructions": "Run these commands in order. Make sure you're in the correct directory.",
    "prerequisites": [
      "Git must be installed",
      "You must have push access to the GitHub repository",
      "Repository should exist on GitHub"
    ]
  }
  ```

**Docstring update:**
```python
"""
Get commands to initialize a git repository and push to GitHub.

This tool generates the complete git initialization workflow including
remote setup and initial push to the dev branch.

Args:
    github_name: GitHub username or organization name
    repo_name: Repository name on GitHub
    directory_path: Path to the directory to initialize (default: current directory)

Returns:
    JSON string with git commands to run locally and instructions
"""
```

---

### Task 5: Handle `run_command()` Function
**Location:** `src/selise_mcp_server.py:115`

**Decision needed:**
- [ ] Option A: **Keep it** - Other parts of code might use it (check first)
- [ ] Option B: **Remove it** - If only these 4 tools use it
- [ ] First: Search codebase for other uses of `run_command()`

**Action:**
```bash
# Search for uses of run_command
grep -n "run_command" src/selise_mcp_server.py
```

If only used by the 4 tools we're refactoring:
- [ ] Delete `run_command()` function
- [ ] Remove `import subprocess` if no longer needed
- [ ] Remove `import asyncio` subprocess-related imports if no longer needed

---

### Task 6: Update `MCP_TOOLS_REFERENCE.md`
**Location:** `MCP_TOOLS_REFERENCE.md`

**Changes needed:**
- [ ] Update `check_blocks_cli` description (line 137-142)
- [ ] Update `install_blocks_cli` description (line 144-150)
- [ ] Update `create_local_repository` description (line 152-160)
- [ ] Update `init_git_repository` description (line 162-172)

**New descriptions:**

```markdown
### check_blocks_cli
Get instructions for checking if Blocks CLI is installed locally.

**Returns:** JSON string with command to verify CLI installation

---

### install_blocks_cli
Get instructions and commands for installing Blocks CLI using npm.

**Returns:** JSON string with installation commands and verification steps

---

### create_local_repository
Generate the command to create a local repository using Blocks CLI.

**Args:**
- repository_name: Name of the repository to create
- template: Template to use (default: "web")
- use_cli: Whether to use CLI mode (default: True)

**Returns:** JSON string with the complete blocks CLI command pre-configured with your project settings

---

### init_git_repository
Generate commands to initialize a git repository and push to GitHub.

**Args:**
- github_name: GitHub username or organization name
- repo_name: Repository name on GitHub
- directory_path: Path where repository is located (default: current directory)

**Returns:** JSON string with step-by-step git commands to run locally

---
```

---

### Task 7: Update Workflow Documentation (if needed)
**Location:** Check if `get_project_setup()` or other docs reference these tools

**Changes needed:**
- [ ] Search for references to these tools in documentation
- [ ] Update workflow guides to mention "run the provided commands"
- [ ] Add notes about running commands locally vs. server operations

---

### Task 8: Testing
**After all changes:**

- [ ] Test `check_blocks_cli()` - verify it returns proper instructions
- [ ] Test `install_blocks_cli()` - verify commands are correct
- [ ] Test `create_local_repository()` - verify command includes tenant_id, domain
- [ ] Test `init_git_repository()` - verify all git commands are properly formatted
- [ ] Test that global state (tenant_id, application_domain) is properly used
- [ ] Verify JSON formatting is valid
- [ ] Check that error handling still works (missing tenant_id, etc.)

---

## Implementation Order

1. ✅ Start with `check_blocks_cli()` (simplest, no dependencies)
2. ✅ Then `install_blocks_cli()` (simple, references check)
3. ✅ Then `create_local_repository()` (uses global state)
4. ✅ Then `init_git_repository()` (most complex)
5. ✅ Search and handle `run_command()` usage
6. ✅ Update `MCP_TOOLS_REFERENCE.md`
7. ✅ Review and test all changes
8. ✅ Update any related documentation

---

## Success Criteria

- ✅ All 4 tools return command strings instead of executing
- ✅ No more `run_command()` calls in these tools
- ✅ Docstrings accurately reflect new behavior
- ✅ JSON responses are well-formatted and helpful
- ✅ Commands include all necessary parameters from global state
- ✅ Reference documentation is updated
- ✅ Server doesn't need Blocks CLI, npm, or git installed
- ✅ Users get clear, copy-paste-ready commands

---

## Notes

- Keep error handling for missing tenant_id/application_domain
- Maintain the same tool names and parameters for backward compatibility
- Format commands for easy copy-paste
- Include helpful instructions and next steps
- Consider adding example output to documentation
