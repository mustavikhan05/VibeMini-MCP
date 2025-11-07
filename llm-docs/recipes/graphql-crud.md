# Recipe: GraphQL CRUD Operations

## 🚨 CRITICAL: This is the ONLY Source for Data Operations

**NEVER look at inventory feature for data operations - it uses different patterns!**
**This recipe is based on actual working Selise Cloud GraphQL patterns.**

## GraphQL Naming Patterns You MUST Know

### 1. Correct Schema Name Pattern (Updated 2025-11-08 - VERIFIED WORKING)
```typescript
// 🚨 ACTUAL NAMING CONVENTION - Based on real working implementation:
// Schema: "Category" → Query field: "getCategorys" (get + schema name + 's')
// Schema: "MenuItem" → Query field: "getMenuItems" (get + schema name + 's')
// Schema: "MenuType" → Query field: "getMenuTypes" (get + schema name + 's')

// ⚠️ CRITICAL: Note the lowercase 'g' and sometimes unconventional pluralization!
// - Category → getCategorys (not getCategories!)
// - MenuItem → getMenuItems
// - MenuType → getMenuTypes

// QUERIES use "get" + schema name + 's' (lowercase 'g', direct pluralization):
query { getCategorys(input: ...) }      // get + "Category" + 's' = getCategorys
query { getMenuItems(input: ...) }      // get + "MenuItem" + 's' = getMenuItems
query { getMenuTypes(input: ...) }      // get + "MenuType" + 's' = getMenuTypes

// MUTATIONS use operation + original schema name (singular):
mutation { insertCategory(...) }       // insert + "Category"
mutation { updateCategory(...) }       // update + "Category"
mutation { deleteCategory(...) }       // delete + "Category"

// INPUT TYPES use schema name + operation + Input:
// CategoryInsertInput, CategoryUpdateInput
// (Selise Cloud UI shows exact type names)

// 🚨 CRITICAL WARNING: The Selise Cloud UI may SHOW "getCategories" in samples,
// but the ACTUAL working query field is "getCategorys" (with lowercase 'g' and 'ys').
// ALWAYS test with curl or GraphQL playground to verify the exact field name!
```

### 2. Schema Discovery with MCP (MANDATORY FIRST STEP!)
```typescript
// 🚨 CRITICAL: ALWAYS use MCP to get exact schema names BEFORE implementing!
// The Selise Cloud UI can show INCORRECT query field names in samples!

// Step 1: List all schemas
list_schemas()
// Returns: ["Category", "MenuItem", "MenuType"]

// Step 2: Get schema details to see fields
get_schema_details("Category")
// Returns: schema structure with fields like Name, Description, etc.

// Step 3: Apply naming pattern (lowercase 'get' + SchemaName + 's'):
// Schema: "Category" → Query: "getCategorys" (NOT "getCategories"!)
// Schema: "MenuItem" → Query: "getMenuItems"
// Schema: "MenuType" → Query: "getMenuTypes"

// Step 4: VERIFY with curl or GraphQL playground before coding!
// Don't trust the Selise Cloud UI samples - they may show wrong names!

// 🚨 DEBUGGING WORKFLOW when query field name is wrong:
// 1. MCP: list_schemas() to confirm schema name
// 2. Try: get + schemaName + s (lowercase 'g')
// 3. Test with curl or GraphQL playground
// 4. Look for GraphQL autocomplete suggestions
// 5. Check error message - "variables not used" = wrong field name
```

### 3. MongoDB Filter Syntax (CRITICAL - _id vs ItemId)
```typescript
// 🚨 CRITICAL: Use _id for mutation filters, even though you can't query it!
// - Queries CANNOT return _id or id fields (they don't exist in GraphQL schema)
// - Mutations MUST use _id in MongoDB filter (it's the actual MongoDB _id field)
// - ItemId is returned by queries but is NOT the same as MongoDB's _id
// - HOWEVER: ItemId VALUE equals MongoDB's _id VALUE, so use ItemId's value in _id filter!

// ✅ CORRECT PATTERN:
// 1. Query returns ItemId: "18d87139-4d59-4d45-9e9b-afc81db8a620"
// 2. Pass ItemId VALUE to mutation
// 3. Use it in filter as _id: { _id: "18d87139-4d59-4d45-9e9b-afc81db8a620" }

// For mutations (update/delete):
const filter = JSON.stringify({ _id: itemId });  // itemId is the VALUE from ItemId field

// ❌ WRONG - This will NOT find records:
const filter = JSON.stringify({ ItemId: itemId });  // totalImpactedData will be 0

// Complex filters:
const filter = JSON.stringify({
  $and: [
    { IsDeleted: false },
    { Status: "active" }
  ]
});
```

### 4. Response Structure
```typescript
// graphqlClient returns data directly (no 'data' wrapper):
const result = await graphqlClient.query({...});

// Access: result.[queryFieldName].items
// Remember: query field = get + SchemaName + s (lowercase 'g')
// Examples:
// - result.getCategorys.items (NOT getCategories!)
// - result.getMenuItems.items
// - result.getMenuTypes.items

// ⚠️ The query field name matches what you used in the GraphQL query!
// If your query says "getCategorys", response has "getCategorys"
```

## Implementation Pattern

### Step 1: Import GraphQL Client (NO Apollo!)

```typescript
// services/[feature].service.ts
import { graphqlClient } from 'lib/graphql-client';  // NEVER use @apollo/client!
```

### Step 2: Define Queries (Using "get" prefix - lowercase 'g')

```typescript
// List query - "get" + schema name + 's' (lowercase 'g', direct +s pluralization)
// 🚨 CRITICAL: Check Selise Cloud GraphQL playground for EXACT field name!
// UI may show "getCategories" but actual field is "getCategorys"

export const GET_ITEMS_QUERY = `
  query GetItems($input: DynamicQueryInput) {
    getCategorys(input: $input) {  // VERIFIED WORKING: getCategorys (lowercase g, +ys)
      hasNextPage
      hasPreviousPage
      totalCount
      totalPages
      pageSize
      pageNo
      items {
        // ⚠️ CANNOT include _id or id fields - they don't exist in GraphQL schema!
        // Standard Selise fields:
        ItemId          // ← Use this for identifying records
        CreatedDate
        CreatedBy
        LastUpdatedDate
        LastUpdatedBy
        IsDeleted
        Language
        OrganizationIds
        Tags
        DeletedDate

        // Your custom fields from schema:
        Name
        Description
        DisplayOrder
        IsActive
        // ... other custom fields
      }
    }
  }
`;

// For other schemas, replace "getCategorys" with:
// - getMenuItems (for MenuItem schema)
// - getMenuTypes (for MenuType schema)
// - etc.
```

### Step 3: Define Mutations (Singular Schema Name)

```typescript
// Insert - uses insert + singular schema name
export const INSERT_ITEM_MUTATION = `
  mutation InsertItem($input: [SchemaName]InsertInput!) {
    insert[SchemaName](input: $input) {  // e.g., insertCategory, insertMenuItem
      itemId
      totalImpactedData
      acknowledged
    }
  }
`;

// Update - uses filter + input (note: filter is stringified MongoDB query)
export const UPDATE_ITEM_MUTATION = `
  mutation UpdateItem($filter: String!, $input: [SchemaName]UpdateInput!) {
    update[SchemaName](filter: $filter, input: $input) {
      itemId
      totalImpactedData
      acknowledged
    }
  }
`;

// Delete - uses filter (note: filter is stringified MongoDB query)
export const DELETE_ITEM_MUTATION = `
  mutation DeleteItem($filter: String!) {
    delete[SchemaName](filter: $filter) {
      acknowledged
      totalImpactedData
      itemId
    }
  }
`;
```

### Step 4: Service Functions

```typescript
// Get paginated list
export const getItems = async (context: {
  queryKey: [string, { pageNo: number; pageSize: number; filter?: string; sort?: string }];
}) => {
  const [, { pageNo, pageSize, filter = '{}', sort = '{}' }] = context.queryKey;
  
  return graphqlClient.query({
    query: GET_ITEMS_QUERY,
    variables: {
      input: {
        filter,
        sort,
        pageNo,
        pageSize,
      },
    },
  });
};

// Get single item by ID (uses MongoDB filter)
export const getItemById = async (itemId: string) => {
  // MongoDB filter with _id field
  const mongoFilter = JSON.stringify({ _id: itemId });
  
  const result = await graphqlClient.query({
    query: GET_ITEMS_QUERY,
    variables: {
      input: {
        filter: mongoFilter,
        sort: '{}',
        pageNo: 1,
        pageSize: 1,
      },
    },
  }) as any;
  
  // Check if found (use "get" + schema name pluralized)
  const queryFieldName = `get${schemaName}s`; // e.g., "getCategories", "getMenuItems"
  if (result?.[queryFieldName]?.items?.length > 0) {
    return {
      data: {
        [queryFieldName]: result[queryFieldName]
      }
    };
  }

  // Return empty result if not found
  return {
    data: {
      [queryFieldName]: {
        items: [],
        totalCount: 0
      }
    }
  };
};

// Add new item
export const addItem = async (params: { input: any }) => {
  return graphqlClient.mutate({
    query: INSERT_ITEM_MUTATION,
    variables: params,
  });
};

// Update existing item
export const updateItem = async (params: { filter: string; input: any }) => {
  return graphqlClient.mutate({
    query: UPDATE_ITEM_MUTATION,
    variables: params,
  });
};

// Delete item (soft delete by default)
export const deleteItem = async (itemId: string, isHardDelete = false) => {
  const filter = JSON.stringify({ _id: itemId });
  return graphqlClient.mutate({
    query: DELETE_ITEM_MUTATION,
    variables: { 
      filter,
      input: { isHardDelete }
    },
  });
};
```

### Step 5: React Query Hooks

```typescript
// hooks/use-[feature].ts
import { useGlobalQuery, useGlobalMutation } from 'state/query-client/hooks';
import { useQueryClient } from '@tanstack/react-query';
import { useToast } from 'hooks/use-toast';

export const useGetItems = (params: {
  pageNo: number;
  pageSize: number;
  filter?: string;
}) => {
  return useGlobalQuery({
    queryKey: ['items', params],
    queryFn: getItems,
    staleTime: 5 * 60 * 1000,
  });
};

export const useGetItemById = (itemId: string) => {
  return useGlobalQuery({
    queryKey: ['item', itemId],
    queryFn: () => getItemById(itemId),
    enabled: !!itemId,
  });
};

export const useAddItem = () => {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useGlobalMutation({
    mutationFn: addItem,
    onSuccess: () => {
      queryClient.invalidateQueries(['items']);
      toast({ title: 'Item added successfully' });
    },
    onError: (error) => {
      toast({
        title: 'Error adding item',
        description: error.message,
        variant: 'destructive',
      });
    },
  });
};

export const useUpdateItem = () => {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useGlobalMutation({
    mutationFn: updateItem,
    onSuccess: () => {
      queryClient.invalidateQueries(['items']);
      toast({ title: 'Item updated successfully' });
    },
  });
};

export const useDeleteItem = () => {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useGlobalMutation({
    mutationFn: ({ itemId }: { itemId: string }) => {
      return deleteItem(itemId, false);
    },
    onSuccess: () => {
      queryClient.invalidateQueries(['items']);
      toast({ title: 'Item deleted successfully' });
    },
  });
};
```

## MongoDB Filter Examples

### Basic Filters
```typescript
// By ID
{ "_id": "item-123" }

// By field
{ "Status": "active" }

// Multiple conditions (AND)
{ "Status": "active", "Category": "premium" }

// Exclude deleted
{ "IsDeleted": false }
```

### Advanced Filters
```typescript
// OR condition
{ "$or": [{ "Category": "A" }, { "Category": "B" }] }

// Greater than
{ "Price": { "$gt": 100 } }

// Text search (case-insensitive)
{ "Name": { "$regex": "search", "$options": "i" } }

// Array contains
{ "Tags": { "$in": ["urgent"] } }

// Complex combination
{
  "$and": [
    { "IsDeleted": false },
    { "Price": { "$gt": 0 } },
    { "$or": [
      { "Category": "Electronics" },
      { "Category": "Software" }
    ]}
  ]
}
```

## Common Gotchas & Solutions

### 1. Wrong Schema Names in Queries (MOST COMMON ERROR!)
```typescript
// ❌ WRONG - Using schema name without "get" prefix
query { Categories(input: ...) }  // Missing "get" prefix
query { Category(input: ...) }    // Singular form
query { Categorys(input: ...) }   // Missing "get" prefix

// ❌ WRONG - Uppercase 'G' (from Selise Cloud UI samples)
query { getCategories(input: ...) }  // Shows in UI but doesn't work!

// ✅ CORRECT - lowercase "get" + schema name + 's'
query { getCategorys(input: ...) }   // VERIFIED WORKING!
query { getMenuItems(input: ...) }
query { getMenuTypes(input: ...) }

// 🚨 CRITICAL: The Selise Cloud UI GraphQL samples show "getCategories" (uppercase G)
// but the ACTUAL working field is "getCategorys" (lowercase g)!
// ALWAYS test the exact field name in GraphQL playground!

// ⚠️ DEBUGGING TIP: If you get "Field does not exist on type Query":
// 1. Try lowercase 'g': getCategorys instead of getCategories
// 2. Try direct +s pluralization: getCategorys instead of getCategories
// 3. Check GraphQL playground for autocomplete suggestions
// 4. The error "variables were not used: input" often means wrong field name

// ALWAYS verify exact schema names:
list_schemas()  // Shows: "Category", "MenuItem", "MenuType"
// Then apply pattern: get + schemaName + s (lowercase!)
```

### 2. Wrong Filter Field (CRITICAL FOR UPDATE/DELETE!)
```typescript
// ❌ WRONG - ItemId doesn't work for filtering in mutations
const filter = JSON.stringify({ ItemId: "18d87139-4d59-4d45-9e9b-afc81db8a620" });
// Result: totalImpactedData: 0 (no records found/updated/deleted)

// ❌ WRONG - Trying to use _id or id in queries
query {
  getCategorys(input: $input) {
    items {
      _id   // ❌ Error: Field `_id` does not exist on type `Category`
      id    // ❌ Error: Field `id` does not exist on type `Category`
    }
  }
}

// ✅ CORRECT - Use ItemId in queries (for display/identification)
query {
  getCategorys(input: $input) {
    items {
      ItemId  // ✅ This works and returns the record ID
      Name
      // ... other fields
    }
  }
}

// ✅ CORRECT - Use _id in mutation filters with ItemId's VALUE
// Step 1: Get ItemId from query result
const category = result.getCategorys.items[0];
const itemId = category.ItemId; // "18d87139-4d59-4d45-9e9b-afc81db8a620"

// Step 2: Use that VALUE in _id filter for mutations
const filter = JSON.stringify({ _id: itemId }); // ← Use _id key, ItemId value!

// Step 3: Execute mutation
await updateCategory({ filter, input: {...} });
// Result: totalImpactedData: 1 ✅ (record found and updated!)

// 🚨 KEY INSIGHT:
// - GraphQL schema doesn't expose _id field for queries
// - But MongoDB internally uses _id as primary key
// - ItemId VALUE = MongoDB _id VALUE
// - So: query with ItemId, filter mutations with _id using ItemId's value
```

### 3. Apollo Client Import
```typescript
// ❌ WRONG - Never use Apollo
import { gql } from '@apollo/client';
import { useQuery } from '@apollo/client';

// ✅ CORRECT - Use Selise's graphqlClient
import { graphqlClient } from 'lib/graphql-client';
```

### 4. Response Structure Confusion
```typescript
// ❌ WRONG - graphqlClient doesn't wrap in 'data'
const items = result.data.getCategories.items;

// ❌ WRONG - Missing "get" prefix
const items = result.Categories.items;

// ✅ CORRECT - Direct access with proper field name (get + pluralized schema name)
const items = result.getCategories.items;
const menuItems = result.getMenuItems.items;
const menuTypes = result.getMenuTypes.items;
```

### 5. Mutation Response Check
```typescript
// Always check totalImpactedData
const result = await updateItem({...});
if (result.totalImpactedData === 0) {
  // No records were updated - filter didn't match
  throw new Error('Item not found');
}
```

### 6. Form Validation with Null Values (React Hook Form + Zod)
```typescript
// ❌ PROBLEM: GraphQL returns null for optional fields, but Zod expects string or undefined
// Error: "Expected string, received null" when editing records with null optional fields

// ❌ WRONG - Passing null to form
const form = useForm({
  defaultValues: {
    Name: initialData?.Name || '',
    Description: initialData?.Description,  // ← Could be null!
  }
});

// ✅ CORRECT - Convert null to empty string
const form = useForm({
  defaultValues: {
    Name: initialData?.Name || '',
    Description: initialData?.Description || '',  // ← null becomes ''
    // This satisfies Zod's string.optional() validation
  }
});

// Zod schema for optional fields:
const schema = z.object({
  Name: z.string().min(2),
  Description: z.string().max(500).optional(),  // Accepts '' or undefined, NOT null
});

// 🚨 KEY INSIGHT:
// - GraphQL/MongoDB returns null for empty optional fields
// - React Hook Form passes these as null to Zod
// - Zod's .optional() accepts undefined or string, NOT null
// - Solution: Convert null to '' in defaultValues (|| '')
```

## Testing with curl Requests (MANDATORY Safety Check)

**🚨 CRITICAL: Always test your GraphQL operations with curl BEFORE implementing in code!**

### Building Your App-Specific curl Requests

**The curl examples in this section use "TodoTasks" as a sample schema name from a todo app. You MUST:**

1. **Replace "TodoTasks"** with YOUR actual schema names (e.g., Products, Users, Orders, etc.)
2. **Replace field names** (title, status, description) with YOUR actual schema fields  
3. **Get YOUR schema info** from MCP using `list_schemas()` and `get_schema_details("YourSchemaName")`
4. **Use YOUR bearer token** from MCP `get_global_state()` or `get_auth_status()`
5. **Use YOUR blocks key** from your project setup

**Example transformation:**
- If your app manages Products with fields: name, price, category
- Replace `TodoTasks` → `Products` 
- Replace `insertTodoTasks` → `insertProduct`
- Replace `{"title":"Test","status":"pending"}` → `{"name":"Test Product","price":29.99,"category":"electronics"}`

### Getting Your Bearer Token
```python
# Get bearer token from MCP global state
get_global_state()
# Look for "bearer_token" or "access_token" in the response
# OR check authentication status:
get_auth_status()
```

### Basic curl Request Template
```bash
curl 'https://api.seliseblocks.com/graphql/v1/graphql' \
-X 'POST' \
-H 'Content-Type: application/json' \
-H 'Accept: */*' \
-H 'Authorization: bearer YOUR_BEARER_TOKEN_HERE' \
-H 'x-blocks-key: YOUR_BLOCKS_KEY_HERE' \
--data-raw '{"query":"YOUR_GRAPHQL_QUERY_HERE","variables":{"input":{}}}'
```

### Test Each Operation Type

**⚠️ IMPORTANT: The examples below use "TodoTasks" as a sample schema name. Replace with YOUR actual schema names from your MCP-created schemas!**

#### 1. Test Schema Query (Verify Naming)
```bash
# EXAMPLE: Test if your schema query field name is correct
# Replace "TodoTasks" with YOUR schema name + 's' (e.g., Products, Users, etc.)
# Replace "title, status" with YOUR actual schema fields
curl 'https://api.seliseblocks.com/graphql/v1/graphql' \
-X 'POST' \
-H 'Content-Type: application/json' \
-H 'Authorization: bearer YOUR_TOKEN' \
-H 'x-blocks-key: YOUR_BLOCKS_KEY' \
--data-raw '{"query":"query TestSchema { YOUR_SCHEMA_NAMES(input: {filter: \"{}\", sort: \"{}\", pageNo: 1, pageSize: 10}) { totalCount items { ItemId YOUR_FIELDS_HERE } } }"}'

# Real example with TodoTasks schema:
# --data-raw '{"query":"query TestSchema { TodoTasks(input: {filter: \"{}\", sort: \"{}\", pageNo: 1, pageSize: 10}) { totalCount items { ItemId title status } } }"}'
```

#### 2. Test Insert Mutation
```bash
# EXAMPLE: Test creating new records  
# Replace "TodoTasks" with YOUR schema name
# Replace the input fields with YOUR actual schema fields
curl 'https://api.seliseblocks.com/graphql/v1/graphql' \
-X 'POST' \
-H 'Content-Type: application/json' \
-H 'Authorization: bearer YOUR_TOKEN' \
-H 'x-blocks-key: YOUR_BLOCKS_KEY' \
--data-raw '{"query":"mutation InsertTest($input: YOUR_SCHEMA_NAMEInsertInput!) { insertYOUR_SCHEMA_NAME(input: $input) { itemId totalImpactedData acknowledged } }","variables":{"input":{"YOUR_FIELD_1":"value","YOUR_FIELD_2":"value"}}}'

# Real example with TodoTasks schema:
# --data-raw '{"query":"mutation InsertTest($input: TodoTasksInsertInput!) { insertTodoTasks(input: $input) { itemId totalImpactedData acknowledged } }","variables":{"input":{"title":"Test Task","description":"Testing curl","status":"pending"}}}'
```

#### 3. Test Update Mutation  
```bash
# EXAMPLE: Test updating records (use _id from insert response)
# Replace "TodoTasks" with YOUR schema name and fields
curl 'https://api.seliseblocks.com/graphql/v1/graphql' \
-X 'POST' \
-H 'Content-Type: application/json' \
-H 'Authorization: bearer YOUR_TOKEN' \
-H 'x-blocks-key: YOUR_BLOCKS_KEY' \
--data-raw '{"query":"mutation UpdateTest($filter: String!, $input: YOUR_SCHEMA_NAMEUpdateInput!) { updateYOUR_SCHEMA_NAME(filter: $filter, input: $input) { totalImpactedData acknowledged } }","variables":{"filter":"{\"_id\":\"RECORD_ID_HERE\"}","input":{"YOUR_FIELD":"Updated Value"}}}'

# Real example with TodoTasks schema:
# --data-raw '{"query":"mutation UpdateTest($filter: String!, $input: TodoTasksUpdateInput!) { updateTodoTasks(filter: $filter, input: $input) { totalImpactedData acknowledged } }","variables":{"filter":"{\"_id\":\"RECORD_ID_HERE\"}","input":{"title":"Updated Task"}}}'
```

#### 4. Test Delete Mutation (SAFETY - Always Test Delete!)
```bash
# EXAMPLE: Test deleting records (IMPORTANT: Test this with test data first!)
# Replace "TodoTasks" with YOUR schema name
curl 'https://api.seliseblocks.com/graphql/v1/graphql' \
-X 'POST' \
-H 'Content-Type: application/json' \
-H 'Authorization: bearer YOUR_TOKEN' \
-H 'x-blocks-key: YOUR_BLOCKS_KEY' \
--data-raw '{"query":"mutation DeleteTest($filter: String!, $input: YOUR_SCHEMA_NAMEDeleteInput!) { deleteYOUR_SCHEMA_NAME(filter: $filter, input: $input) { acknowledged totalImpactedData } }","variables":{"filter":"{\"_id\":\"TEST_RECORD_ID\"}","input":{"isHardDelete":false}}}'

# Real example with TodoTasks schema:
# --data-raw '{"query":"mutation DeleteTest($filter: String!, $input: TodoTasksDeleteInput!) { deleteTodoTasks(filter: $filter, input: $input) { acknowledged totalImpactedData } }","variables":{"filter":"{\"_id\":\"TEST_RECORD_ID\"}","input":{"isHardDelete":false}}}'
```

### curl Testing Workflow

**For each schema you create:**
1. **First**: Test the query field name (TodoTasks, Products, etc.)
2. **Second**: Test insert with sample data  
3. **Third**: Test update using the inserted record's _id
4. **Fourth**: Test delete with a test record
5. **MANDATORY**: Delete ALL test records you created using delete curl requests

### 🚨 CRITICAL: Clean Up Test Data

**You MUST delete any records you create during curl testing!**

```bash
# After testing, delete ALL test records you created:
# 1. Save the _id from each insert response
# 2. Use delete curl for each test record

curl 'https://api.seliseblocks.com/graphql/v1/graphql' \
-X 'POST' \
-H 'Content-Type: application/json' \
-H 'Authorization: bearer YOUR_TOKEN' \
-H 'x-blocks-key: YOUR_BLOCKS_KEY' \
--data-raw '{"query":"mutation CleanupTest($filter: String!, $input: YOUR_SCHEMA_NAMEDeleteInput!) { deleteYOUR_SCHEMA_NAME(filter: $filter, input: $input) { acknowledged totalImpactedData } }","variables":{"filter":"{\"_id\":\"INSERT_RESPONSE_ID_HERE\"}","input":{"isHardDelete":true}}}'

# This serves dual purpose:
# 1. Tests your delete functionality 
# 2. Cleans up test data from your database
```

### Common curl Errors & Solutions

```bash
# Error: Field 'TodoTask' not found
# ✅ Fix: Use TodoTasks (schema name + 's')

# Error: Unknown argument 'filter' 
# ✅ Fix: Check input structure matches DynamicQueryInput

# Error: 401 Unauthorized
# ✅ Fix: Check bearer token is valid, refresh from MCP if needed

# Error: Variable '$input' not defined
# ✅ Fix: Ensure variables object matches query parameters
```

## Testing Schema Names with MCP

**MANDATORY: Always verify schema names with MCP before implementing:**

```python
# List all schemas first
list_schemas()

# Get schema details for the exact name
get_schema_details(schema_name="TodoTask")
```

This will show:
- Exact schema name: "TodoTask"
- Query field will be: "TodoTasks" (schema name + 's')
- Mutations will use: "insertTodoTask", "updateTodoTask", "deleteTodoTask"
- Input types: "TodoTaskInsertInput", "TodoTaskUpdateInput", "TodoTaskDeleteInput"

## File Structure Pattern

```
src/features/[feature]/
├── components/         # UI components
├── graphql/           # Queries and mutations
│   ├── queries.ts
│   └── mutations.ts
├── hooks/             # React Query hooks
│   └── use-[feature].ts
├── services/          # Service functions
│   └── [feature].service.ts
├── types/             # TypeScript types
│   └── [feature].types.ts
└── index.ts           # Public exports
```

## Summary - Complete Workflow for ANY Schema

### Before You Code (MANDATORY):
1. **Use MCP to discover schemas**: `list_schemas()` and `get_schema_details("SchemaName")`
2. **Verify query field name**: Test with curl or GraphQL playground (UI samples can be WRONG!)
3. **Expected pattern**: lowercase "get" + SchemaName + "s" (e.g., getCategorys, getMenuItems)

### Critical Patterns (VERIFIED WORKING):
1. **Query fields**: `getCategorys`, `getMenuItems`, `getMenuTypes` (lowercase 'g', direct +s)
   - ⚠️ NOT getCategories (uppercase G) - UI shows this but it's WRONG!
2. **Mutations**: `insertCategory`, `updateCategory`, `deleteCategory` (singular schema name)
3. **Query field access**: `result.getCategorys.items` (NO _id or id fields in queries!)
4. **Mutation filters**: Use `{ _id: itemIdValue }` where itemIdValue comes from ItemId field
5. **ItemId vs _id**:
   - Queries return: `ItemId` field
   - Mutations filter by: `_id` field (using ItemId's VALUE)
   - ItemId VALUE = MongoDB _id VALUE
6. **Form validation**: Convert null to `''` for optional fields in React Hook Form defaultValues
7. **Import**: `graphqlClient` from 'lib/graphql-client' (NEVER Apollo Client!)
8. **Check mutations**: `totalImpactedData > 0` means success, `= 0` means filter didn't match

### This Document is Now Complete For:
- ✅ Any schema created via MCP
- ✅ Any CRUD operation (Create, Read, Update, Delete)
- ✅ Handling query field name variations
- ✅ Proper _id vs ItemId usage
- ✅ Form validation with null values
- ✅ All common errors and their solutions

**Just follow the MCP → Verify → Implement pattern and you're good!**