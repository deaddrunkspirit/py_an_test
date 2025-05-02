import pytest
import asyncio
from phone_extractor import PhoneExtractor

@pytest.fixture
def extractor():
    return PhoneExtractor()

@pytest.mark.asyncio
async def test_normalize_phone(extractor):
    test_cases = [
        ("+7 912-345-67-89", "+7(912)345-67-89"),
        ("8 (495) 123 45 67", "+7(495)123-45-67"),
        ("+7(903) 456 78 90", "+7(903)456-78-90"),
        ("8-900-111-22-33", "+7(900)111-22-33"),
        ("+7-900-123-45-67", "+7(900)123-45-67"),
        ("+7 (999) 888.77.66", "+7(999)888-77-66"),
        ("1234567890", None),
        ("+7(123)456-78-9", None),
        ("8(123)456-78", None),
        ("+7(123)456-78-901", None),
    ]

    for input_phone, expected in test_cases:
        assert extractor.normalize_phone(input_phone) == expected

@pytest.mark.asyncio
async def test_extract_phones_from_text(extractor):
    test_text = """
    Phone numbers: +7 912-345-67-89, 8 (495) 123 45 67,
    +7(903) 456 78 90, 8-900-111-22-33
    """
    
    expected = [
        "+7(912)345-67-89",
        "+7(495)123-45-67",
        "+7(903)456-78-90",
        "+7(900)111-22-33"
    ]
    
    result = await extractor.extract_phones_from_text(test_text)
    assert result == expected

@pytest.mark.asyncio
async def test_extract_phones_from_file(extractor):
    expected = [
        "+7(912)345-67-89",
        "+7(495)123-45-67",
        "+7(903)456-78-90",
        "+7(900)123-45-67",
        "+7(999)888-77-66"
    ]
    
    result = await extractor.extract_phones_from_file("test_data.txt")
    assert result == expected

@pytest.mark.asyncio
async def test_duplicate_phones(extractor):
    test_text = "+7 912-345-67-89 +7(912)345-67-89"
    expected = ["+7(912)345-67-89"]
    
    result = await extractor.extract_phones_from_text(test_text)
    assert result == expected

@pytest.mark.asyncio
async def test_invalid_input(extractor):
    result = await extractor.extract_phones_from_text(123)
    assert result == [] 