# Attack YAML Schema

Each attack file must include:

- `id`: unique attack identifier
- `name`: human-readable name
- `category`: attack category
- `description`: reviewer-facing description
- `prompt`: prompt sent to the target
- `success_criteria.type`: currently `keyword_present`
- `success_criteria.keywords`: non-empty list of keywords
- `severity`: informational, low, medium, high, or critical
- `references`: list of references
