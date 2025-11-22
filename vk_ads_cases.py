import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def parse_vk_cases(page_number=1):
    base_url = 'https://ads.vk.com'
    all_cases = []
    
    url = f"{base_url}/cases?p={page_number}"

    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        all_links = soup.find_all('a')
        cases_list = []
        
        for link in all_links:
            href = link.get('href')
            if href and '/cases/' in href:
                cases_list.append(link)
        
        
        for case in cases_list:
            try:
                name = "Название не найдено"
                
                for tag_name in ['h1', 'h2', 'h3', 'h4']:
                    title_element = case.find(tag_name)
                    if title_element and title_element.get_text(strip=True):
                        name = title_element.get_text(strip=True)
                        break
                
                if name == "Название не найдено":
                    all_text_elements = case.find_all(string=True)
                    for text_element in all_text_elements:
                        text = text_element.strip()
                        if text and len(text) > 10 and len(text) < 200:
                            name = text
                            break
                
                relative_link = case.get('href')
                absolute_link = urljoin(base_url, relative_link)
                
                date = "Дата не указана"
                all_text_elements = case.find_all(string=True)
                for text_element in all_text_elements:
                    text = text_element.strip()
                    if any(char.isdigit() for char in text):
                        if any(year in text for year in ['2023', '2024', '2025']):
                            date = text
                            break
                        months = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 
                                 'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
                        if any(month in text.lower() for month in months):
                            date = text
                            break
                
                case_data = {
                    'name': name,
                    'url': absolute_link,
                    'date': date
                }
                
                all_cases.append(case_data)
                    
            except Exception as e:
                continue
        
    except Exception as e:
        pass
    
    return all_cases


def parse_multiple_pages(start_page=1, end_page=1):
    
    all_cases = []
    
    for page in range(start_page, end_page + 1):
        page_cases = parse_vk_cases(page)
        all_cases.extend(page_cases)
    
    return all_cases


def save_to_json(data, filename='vk_cases.json'):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Данные сохранены в файл: {filename}")


def main():

    try:
        print("Аналитика кейсов VK ADS")
        print("Доступные режимы:")
        print("1 - Одна страница")
        print("2 - Несколько страниц")
        print("3 - Все страницы (1-18)")
        
        choice = input("\nВыберите режим (1-3): ").strip()
        
        if choice == "1":
            page = int(input("Введите номер страницы (1-18): ").strip())
            cases = parse_vk_cases(page)
            filename = f'vk_cases_page_{page}.json'
            
        elif choice == "2":
            start_page = int(input("Введите начальную страницу (1-18): ").strip())
            end_page = int(input("Введите конечную страницу (1-18): ").strip())
            cases = parse_multiple_pages(start_page, end_page)
            filename = f'vk_cases_pages_{start_page}_{end_page}.json'
            
        elif choice == "3":
            cases = parse_multiple_pages(1, 18)
            filename = 'vk_cases_all_pages.json'
            
        else:
            print("Неверный выбор. Используется режим по умолчанию (страница 1)")
            cases = parse_vk_cases(1)
            filename = 'vk_cases_page_1.json'
        
        save_to_json(cases, filename)
        
        print(f"\nВсе собранные кейсы")
        print(f"Всего собрано кейсов: {len(cases)}")
        
        if cases:
            for i, case in enumerate(cases, 1):
                print(f"\nКейс {i} ")
                print(f"Название: {case['name']}")
                print(f"Ссылка: {case['url']}")
                print(f"Дата: {case['date']}")
                
        else:
            print("Кейсы не найдены.")
            
    except ValueError:
        print("Ошибка: введите корректный номер страницы")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()
