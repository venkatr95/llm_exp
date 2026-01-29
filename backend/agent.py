from openai import OpenAI
from typing import Dict, Any
import json


class UUIDAgent:
    """OpenAI-powered agent for mapping UUIDs to form objects"""
    
    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        self.client = OpenAI(api_key=api_key)
        self.model = model
    
    def map_uuid_to_form(self, uuid: str, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Use OpenAI to intelligently map and enhance UUID data to form fields
        
        Args:
            uuid: The UUID identifier
            raw_data: Raw data from database
            
        Returns:
            Dict with mapped form fields
        """
        
        system_prompt = """You are an intelligent form-filling assistant. 
        Given a UUID and associated raw data, you need to:
        1. Validate and format the data appropriately
        2. Ensure all fields are properly filled
        3. Add helpful context or formatting where needed
        4. Return a JSON object with these exact fields: uuid, name, email, phone, address, company, position, notes
        
        Always maintain data accuracy and format it professionally."""
        
        user_prompt = f"""
        UUID: {uuid}
        Raw Data: {json.dumps(raw_data, indent=2)}
        
        Please process this data and return a properly formatted JSON object for form filling.
        Ensure all fields are present and formatted correctly.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.3
            )
            
            result = json.loads(response.choices[0].message.content)
            
            # Ensure UUID is included
            result["uuid"] = uuid
            
            # Ensure all required fields exist
            required_fields = ["uuid", "name", "email", "phone", "address", "company", "position", "notes"]
            for field in required_fields:
                if field not in result:
                    result[field] = raw_data.get(field, "")
            
            return result
            
        except Exception as e:
            print(f"Agent error: {str(e)}")
            # Fallback to raw data if agent fails
            return {
                "uuid": uuid,
                "name": raw_data.get("name", ""),
                "email": raw_data.get("email", ""),
                "phone": raw_data.get("phone", ""),
                "address": raw_data.get("address", ""),
                "company": raw_data.get("company", ""),
                "position": raw_data.get("position", ""),
                "notes": raw_data.get("notes", "")
            }
