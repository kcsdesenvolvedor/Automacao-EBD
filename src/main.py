from scraper import fetch_lesson_data
from image_gen import generate_card
import sys

def main():
    print("--- EBD Automation Tool ---")
    print("1. Fetching lesson data...")
    data = fetch_lesson_data()
    
    if not data:
        print("Error: Could not fetch lesson data.")
        sys.exit(1)
        
    print(f"\nFound Lesson: {data['lesson_number']}")
    print(f"Theme: {data['theme']}")
    print(f"Hymns: {data['hymns']}")
    
    confirm = input("\nIs this correct? (Y/n): ").strip().lower()
    if confirm == 'n':
        print("Operation cancelled.")
        sys.exit(0)
        
    print("\n--- Additional Info ---")
    professor = input("Professor Name (e.g. Pr. Kleber): ").strip()
    if not professor:
        professor = "Pr. Kleber" # Default
        
    santa_ceia = input("Is this Sunday Holy Supper (Santa Ceia)? (y/N): ").strip().lower()
    has_breakfast = True
    if santa_ceia == 'y':
        has_breakfast = False
        
    print("\nGenerating image...")
    success = generate_card(data, professor, has_breakfast)
    
    if success:
        print("\nSuccess! Image saved in 'output' folder.")
    else:
        print("\nFailed to generate image.")

if __name__ == "__main__":
    main()
