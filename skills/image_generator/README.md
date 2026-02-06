# Skill: image_generator

## Service Description
The `image_generator` skill enables Worker agents to create visual assets using generative AI models such as DALL-E or Midjourney. It supports creative campaigns, meme generation, and branded content.

**Business Value:**
- Automates the creation of high-quality images for social posts and campaigns.
- Reduces turnaround time for visual content and supports A/B testing.

## Input Schema (JSON Schema)
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "ImageGeneratorInput",
  "type": "object",
  "properties": {
    "prompt": { "type": "string", "description": "Text prompt describing the desired image." },
    "model": { "type": "string", "enum": ["dalle", "midjourney"], "description": "Image generation model to use." },
    "aspect_ratio": { "type": "string", "enum": ["1:1", "16:9", "9:16", "4:5"], "description": "Aspect ratio for the output image." },
    "style": { "type": "string", "description": "Optional style or mood (e.g., 'cyberpunk', 'minimalist')." },
    "count": { "type": "integer", "minimum": 1, "maximum": 4, "default": 1, "description": "Number of images to generate." },
    "seed": { "type": "integer", "minimum": 0, "description": "Optional deterministic seed for reproducibility." },
    "format": { "type": "string", "enum": ["png", "jpg"], "default": "png", "description": "Output image format." }
  },
  "required": ["prompt", "model", "aspect_ratio"],
  "additionalProperties": false
}
```

## Output Schema (JSON Schema)
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "ImageGeneratorOutput",
  "type": "object",
  "properties": {
    "image_url": { "type": "string", "format": "uri" },
    "model": { "type": "string" },
    "created_at": { "type": "string", "format": "date-time" },
    "prompt": { "type": "string" },
    "aspect_ratio": { "type": "string" }
  },
  "required": ["image_url", "model", "created_at", "prompt", "aspect_ratio"],
  "additionalProperties": false
}
```

## Error Codes
| Code                  | Description                                 | Agent Handling                |
|-----------------------|---------------------------------------------|-------------------------------|
| RATE_LIMIT_EXCEEDED   | API rate limit hit                          | Retry with backoff            |
| SCHEMA_VIOLATION      | Input does not match schema                  | Halt, notify Planner          |
| UNSUPPORTED_STYLE     | Style or aspect ratio not supported          | Return error, suggest fallback|
| MODEL_UNAVAILABLE     | Model API is down                           | Retry or switch model         |

## Idempotency Policy
- Requests with identical `prompt`, `model`, and `aspect_ratio` within a 10-minute window are deduplicated.
- The skill returns the same image or a reference to the original request to prevent duplicate asset generation.
 - If `seed` and `format` are specified, exact outputs are expected; otherwise, dedup returns canonical first result.