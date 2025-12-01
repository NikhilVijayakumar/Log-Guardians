import re
import json
import logging

logger = logging.getLogger(__name__)

def clean_json_content(raw_content: str) -> str:
        """Extract valid JSON object from raw LLM output and return compact JSON string."""
        content = re.sub(r'```json', '', raw_content, flags=re.IGNORECASE)
        content = re.sub(r'```', '', content)

        # Find the first { ... } or [ ... ]
        match = re.search(r'(\{.*\}|\[.*\])', content, flags=re.DOTALL)
        if not match:
            logger.warning("No JSON block found in LLM output")
            return json.dumps({"Response": content.strip()})  # fallback

        json_str = match.group(0).strip()

        try:
            parsed_json = json.loads(json_str)
            # Return COMPACT JSON string (no indent!) → safe for json.loads()
            return json.dumps(parsed_json)
        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse JSON block: {e}\nBlock: {json_str[:200]}")
            return json.dumps({"Response": json_str})  # safe fallback