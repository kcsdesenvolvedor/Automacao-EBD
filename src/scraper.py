import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

BLOG_URL = "https://marcosandreclubdateologia.blogspot.com"

def get_headers():
    return {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

def fetch_lesson_data():
    """
    Fetches the latest 'ESCOLA DOMINICAL BETEL SUBSÍDIO' lesson.
    Returns a dictionary with:
    - lesson_number (str)
    - theme (str)
    - hymns (str)
    - date (str)
    """
    print(f"Connecting to {BLOG_URL}...")
    try:
        response = requests.get(BLOG_URL, headers=get_headers())
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching blog main page: {e}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the link to the latest BETEL lesson
    # We look for links containing "ESCOLA DOMINICAL BETEL SUBSÍDIO"
    target_link = None
    for link in soup.find_all('a'):
        text = link.get_text()
        if "ESCOLA DOMINICAL BETEL SUBSÍDIO" in text:
            target_link = link.get('href')
            print(f"Found lesson link: {target_link}")
            break
            
    if not target_link:
        print("Could not find a link for 'ESCOLA DOMINICAL BETEL SUBSÍDIO' on the main page.")
        return None

    # Fetch the lesson page
    try:
        lesson_response = requests.get(target_link, headers=get_headers())
        lesson_response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching lesson page: {e}")
        return None

    lesson_soup = BeautifulSoup(lesson_response.text, 'html.parser')
    
    # Extract Lesson Number from Title
    # Title format usually: "ESCOLA DOMINICAL BETEL SUBSÍDIO - Lição X / 1º Trim YYYY"
    title_element = lesson_soup.find('h3', class_='post-title')
    if not title_element:
        # Fallback: try looking at the page title or headers
        title_element = lesson_soup.find('h1') or lesson_soup.find('title')
    
    title_text = title_element.get_text().strip() if title_element else ""
    print(f"Page Title: {title_text}")
    
    lesson_number = "Unknown"
    match = re.search(r'Lição\s+(\d+)', title_text, re.IGNORECASE)
    if match:
        lesson_number = match.group(1)
        
    # Extract Theme and Hymns from content
    # We need to look for specific keywords in the post content
    post_body = lesson_soup.find('div', class_='post-body')
    if not post_body:
        print("Could not find post body.")
        return None
        
    text_content = post_body.get_text("\n")
    
    # The structure varies, but usually "Tema:" or "TEMA:" follows
    # And "Hinos Sugeridos:"
    
    theme = "Tema não encontrado"
    hymns = "Hinos não encontrados"
    
    # Regex for Theme (capture line after "Tema:")
    # Attempt 1: Look for "Tema:" lines
    lines = text_content.split('\n')
    for i, line in enumerate(lines):
        cl = line.strip()
        if "TEMA" in cl.upper() and len(cl) < 50: # Avoid capturing long paragraphs if they just contain the word "Tema"
             # The theme might be on the same line or next line
             if ":" in cl:
                 parts = cl.split(":", 1)
                 if len(parts) > 1 and parts[1].strip():
                     theme = parts[1].strip()
                 elif i + 1 < len(lines):
                     theme = lines[i+1].strip()
             elif i + 1 < len(lines):
                 theme = lines[i+1].strip()
             break

    # Regex/Search for Hymns
    # "HINOS SUGERIDOS: 123, 456, 789"
    hymns_match = re.search(r'HINOS\s+SUGERIDOS:?\s*([\d,\s]+)', text_content, re.IGNORECASE)
    if hymns_match:
        hymns = hymns_match.group(1).strip()
    
    return {
        "lesson_number": lesson_number,
        "theme": theme,
        "hymns": hymns,
        "link": target_link,
        "fetched_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

if __name__ == "__main__":
    data = fetch_lesson_data()
    if data:
        print("\n--- DATA EXTRACTED ---")
        print(f"Lesson: {data['lesson_number']}")
        print(f"Theme: {data['theme']}")
        print(f"Hymns: {data['hymns']}")
        print(f"Link: {data['link']}")
    else:
        print("Failed to extract data.")
