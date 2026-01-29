from openai import OpenAI
from typing import Dict, Any
import json
import os
from functools import lru_cache
import hashlib


class UUIDAgent:
    """LLM-powered agent for mapping UUIDs to form objects (supports OpenAI and LM Studio)"""
    
    def __init__(self, api_key: str = None, model: str = None, provider: str = "openai"):
        """
        Initialize agent with specified LLM provider
        
        Args:
            api_key: API key for OpenAI (not needed for LM Studio)
            model: Model name (e.g., "gpt-4o-mini" for OpenAI, "gemma-3" for LM Studio)
            provider: "openai" or "lmstudio"
        """
        self.provider = provider.lower()
        self.cache = {}  # Simple in-memory cache
        
        if self.provider == "lmstudio":
            # LM Studio uses OpenAI-compatible API at localhost
            self.client = OpenAI(
                base_url="http://localhost:1234/v1",
                api_key="lm-studio",
                timeout=10.0  # 10 second timeout
            )
            self.model = model or "gemma-3"  # Default to gemma-3 for LM Studio
        else:
            # OpenAI
            self.client = OpenAI(
                api_key=api_key,
                timeout=10.0  # 10 second timeout
            )
            self.model = model or "gpt-4o-mini"
    
    def map_uuid_to_form(self, uuid: str, raw_data: Dict[str, Any], use_llm: bool = True) -> Dict[str, Any]:
        """
        Use LLM to intelligently map and enhance UUID data to form fields
        
        Args:
            uuid: The UUID identifier
            raw_data: Raw data from database
            use_llm: Whether to use LLM processing (default: True)
            
        Returns:
            Dict with mapped form fields
        """
        
        # Check cache first
        cache_key = f"{uuid}_{hashlib.md5(json.dumps(raw_data, sort_keys=True).encode()).hexdigest()}"
        if cache_key in self.cache:
            print(f"Cache hit for UUID: {uuid}")
            return self.cache[cache_key]
        
        # If LLM is disabled, return raw data immediately
        if not use_llm:
            return self._format_raw_data(uuid, raw_data)
        
        system_prompt = """You are a form-filling assistant. Format the data professionally and return JSON with these fields: uuid, name, email, phone, address, company, position, notes. Keep it concise."""
        
        user_prompt = f"""Format this data: {json.dumps(raw_data)}"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.1,  # Lower temperature for faster, more consistent results
                max_tokens=500  # Limit tokens for faster response
            )
            
            result = json.loads(response.choices[0].message.content)
            
            # Ensure UUID is included
            result["uuid"] = uuid
            
            # Ensure all required fields exist
            required_fields = ["uuid", "name", "email", "phone", "address", "company", "position", "notes"]
            for field in required_fields:
                if field not in result:
                    result[field] = raw_data.get(field, "")
            
            # Cache the result
            self.cache[cache_key] = result
            
            return result
            
        except Exception as e:
            print(f"Agent error (falling back to raw data): {str(e)}")
            # Fallback to raw data if agent fails
            return self._format_raw_data(uuid, raw_data)
    
    def _format_raw_data(self, uuid: str, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Format raw data without LLM processing"""
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
