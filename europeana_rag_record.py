import json
from typing import Dict, List

class EuropeanaRagRecord:
    """
    Represents a RAG-friendly record as a JSON-compatible map of string arrays.
    """

    def __init__(self):
        """
        Initializes an empty map for fields.
        """
        self.fields: Dict[str, List[str]] = {}

    def add_field(self, field_name: str, value: str):
        """
        Adds a value to the specified field's list of strings.

        Args:
            field_name (str): The name of the field.
            value (str): The value to add.
        """
        if field_name not in self.fields:
            self.fields[field_name] = []
        
        # Avoid duplicates in the list if necessary, 
        # but the requirement just says array string values.
        if value not in self.fields[field_name]:
            self.fields[field_name].append(value)

    def to_json(self) -> str:
        """
        Returns the JSON representation of the field map.

        Returns:
            str: JSON string.
        """
        return json.dumps(self.fields, indent=2, ensure_ascii=False)

    def to_text(self) -> str:
        """
        Transforms the record into plain text with field names as labels.

        Returns:
            str: Formatted plain text.
        """
        lines = []
        for field, values in self.fields.items():
            if values:
                val_str = ", ".join(values)
                lines.append(f"{field}: {val_str}")
        return "\n".join(lines)

    def __str__(self):
        return self.to_text()
