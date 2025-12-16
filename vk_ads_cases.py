import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_cases():
    url = 'https://ads.vk.com/cases'
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        cases = [] #создаем список
        
        all_links = soup.find_all('a') #тут ищем все ссылки на странице
        
        case_links = []
        for link in all_links:
            address = link.get('href')
            if address and "/cases/" in address:
                case_links.append(link)
        
        for link in case_links:
            text = link.get_text(strip=True) #берем текст ссылки и убираем лишние пробелы с помощью strip=True
            if len(text) > 10:
                
                relative_link = link['href']
                true_link = urljoin(url, relative_link)
                cases.append({
                    'name': text,
                    'url': true_link
                })
        return cases
    except:
        return []

def main():
    cases = get_cases()
    
    print(f"Найдено: {len(cases)} кейсов\n")
    
    for i, case in enumerate(cases, 1):
        name = case['name']
        if len(name) > 10:
            date = name[:10]  
            title = name[10:]  
        else:
            date = ""
            title = name
        
        print(f"{i}. {date}")
        if title:
            print(f"{title}")
        print(f"Ссылка: {case['url']}")
        print()

if __name__ == "__main__":
    main()
