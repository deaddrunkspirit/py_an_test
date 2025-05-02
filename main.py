import asyncio
import os
from phone_extractor import PhoneExtractor
from loguru import logger

async def process_file(file_path: str, output_file: str) -> None:
    try:
        extractor = PhoneExtractor()
        phones = await extractor.extract_phones_from_file(file_path)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            for phone in phones:
                f.write(f"{phone}\n")
        
        logger.info(f"Найдено {len(phones)} телефонных номеров. Результаты сохранены в {output_file}")
        for phone in phones:
            logger.info(f"Найден номер: {phone}")
            
    except Exception as e:
        logger.error(f"Ошибка при обработке файла: {str(e)}")

async def main():
    default_file = "test_data.txt"
    
    print("Извлечение телефонных номеров")
    print("============================")
    print(f"Тестовый файл по умолчанию: {default_file}")
    print("Введите путь к файлу или нажмите Enter для использования тестового файла:")
    
    file_path = input().strip()
    if not file_path:
        file_path = default_file
    
    if not os.path.exists(file_path):
        logger.error(f"Файл не найден: {file_path}")
        return
    
    output_file = os.path.join(os.path.dirname(file_path), "result.txt")
    
    await process_file(file_path, output_file)

if __name__ == "__main__":
    asyncio.run(main()) 