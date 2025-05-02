import re
from typing import List, Set, Pattern
from loguru import logger
import asyncio
from six import string_types

class PhoneExtractor:
    def __init__(self):
        self.phone_pattern: Pattern = re.compile(r'^(?:\+7|8)[\s\-]?\(?(\d{3})\)?[\s\-\.]?(\d{3})[\s\-\.]?(\d{2})[\s\-\.]?(\d{2})$')
        self.extract_pattern: Pattern = re.compile(r'(?:^|\s|[^\d])(?:\+7|8)[\s\-]?\(?\d{3}\)?[\s\-\.]?\d{3}[\s\-\.]?\d{2}[\s\-\.]?\d{2}(?:\s|$|[^\d])')

    def normalize_phone(self, phone: str) -> str:
        cleaned = re.sub(r'[^\d+()]', '', phone)
        if len(cleaned.replace('+', '').replace('(', '').replace(')', '')) > 11:
            return None
            
        match = self.phone_pattern.search(cleaned)
        if not match:
            return None
        
        area_code, first_part, second_part, third_part = match.groups()
        return f"+7({area_code}){first_part}-{second_part}-{third_part}"

    async def extract_phones_from_text(self, text: str) -> List[str]:
        if not isinstance(text, string_types):
            logger.error("Input must be a string")
            return []

        potential_phones = self.extract_pattern.finditer(text)
        seen: Set[str] = set()
        result: List[str] = []

        for match in potential_phones:
            phone = match.group(0).strip()
            phone = re.sub(r'^[^\d+]+', '', phone)
            phone = re.sub(r'[^\d)]+$', '', phone)
            
            normalized = self.normalize_phone(phone)
            if normalized and normalized not in seen:
                seen.add(normalized)
                result.append(normalized)

        return result

    async def extract_phones_from_file(self, file_path: str) -> List[str]:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            return await self.extract_phones_from_text(text)
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {str(e)}")
            return [] 