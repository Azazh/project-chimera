# Skill: trend_hunter

## Service Description
The `trend_hunter` skill enables Worker agents to discover and analyze viral trends in the crypto and social media landscape. It leverages search APIs and social listening tools to surface high-impact topics, hashtags, and tokens. 

**Business Value:**
- Identifies emerging opportunities for campaign targeting and content creation.
- Informs strategic planning for influencer and trading agents.

## Input Schema (JSON Schema)
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "TrendHunterInput",
  "type": "object",
  "properties": {
    "query": { "type": "string", "description": "Search term or hashtag to focus the trend analysis." },
    "platforms": {
      "type": "array",
      "items": { "type": "string", "enum": ["twitter", "reddit", "coingecko", "dune", "tiktok"] },
      "description": "Platforms to search for trends."
    },
    "time_window": {
      "type": "string",
      "pattern": "^\\d+[hdw]$",
      "description": "Time window for trend search (e.g., '24h', '7d', '1w')."
    },
    "min_volume": { "type": "integer", "minimum": 0, "description": "Minimum mention or trading volume." }
  },
  "required": ["query", "platforms", "time_window"],
  "additionalProperties": false
}
```

## Output Schema (JSON Schema)
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "TrendHunterOutput",
  "type": "object",
  "properties": {
    "trends": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": { "type": "string" },
          "platform": { "type": "string" },
          "volume": { "type": "integer" },
          "sentiment": { "type": "string", "enum": ["positive", "neutral", "negative"] },
          "url": { "type": "string", "format": "uri" }
        },
        "required": ["name", "platform", "volume", "sentiment", "url"]
      }
    },
    "queried_at": { "type": "string", "format": "date-time" }
  },
  "required": ["trends", "queried_at"],
  "additionalProperties": false
}
```

## Error Codes
| Code                  | Description                                 | Agent Handling                |
|-----------------------|---------------------------------------------|-------------------------------|
| RATE_LIMIT_EXCEEDED   | API rate limit hit                          | Retry with backoff            |
| SCHEMA_VIOLATION      | Input does not match schema                  | Halt, notify Planner          |
| NO_RESULTS            | No trends found for query                    | Return empty trends array     |
| PLATFORM_UNAVAILABLE  | Platform API is down                        | Retry or skip platform        |

## Idempotency Policy
- Requests with identical `query`, `platforms`, and `time_window` within a 5-minute window are deduplicated.
- The skill returns the same result for duplicate requests to prevent redundant API calls and ensure consistency.