from PIL import Image, ImageDraw, ImageFont
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_PATH = os.path.join(BASE_DIR, "assets", "template.png")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
FONT_PATH = os.path.join(BASE_DIR, "assets", "Arial.ttf")

def generate_card(lesson_data, professor_name, has_breakfast):
    """
    Generates the EBD card.
    lesson_data: dict with 'lesson_number', 'theme', 'hymns'
    professor_name: str
    has_breakfast: bool
    """
    print(f"DEBUG: Looking for template at {TEMPLATE_PATH}")
    if not os.path.exists(TEMPLATE_PATH):
        print(f"Error: Template not found at {TEMPLATE_PATH}")
        return f"Template not found at {TEMPLATE_PATH}"

    try:
        img = Image.open(TEMPLATE_PATH)
        draw = ImageDraw.Draw(img)
        
        # Dimensions for centering
        W, H = img.size
        
        # Colors
        TEXT_COLOR = (255, 255, 255) # White
        TEXT_COLOR_BLUE = (0, 50, 100)   # Dark Blue
        
        # --- CONFIGURATION (Adjust these coordinates) ---
        
        # --- FONT CONFIGURATION ---
        print(f"DEBUG: Loading font from {FONT_PATH}")
        try:
            # Drastically increasing sizes based on user feedback
            font_lesson = ImageFont.truetype(FONT_PATH, 40)
            font_theme = ImageFont.truetype(FONT_PATH, 30)
            font_hymns = ImageFont.truetype(FONT_PATH, 40)
            font_prof = ImageFont.truetype(FONT_PATH, 160)
            font_break = ImageFont.truetype(FONT_PATH, 30)
        except Exception as e:
            print(f"CRITICAL ERROR loading font {FONT_PATH}: {e}")
            print("Falling back to default font (will be small).")
            # Fallback
            font_lesson = ImageFont.load_default()
            font_theme = ImageFont.load_default()
            font_hymns = ImageFont.load_default()
            font_prof = ImageFont.load_default()
            font_break = ImageFont.load_default()

        # 1. Lesson Number
        lesson_number = str(lesson_data['lesson_number']).zfill(2)
        lesson_text = f"Lição {lesson_number}"
        length_lesson = draw.textlength(lesson_text, font=font_lesson)
        draw.text((W - length_lesson - 40, 90), lesson_text, font=font_lesson, fill=TEXT_COLOR)
        
        # 2. Theme (Central, Big)
        theme_text = lesson_data['theme']
        lines = []
        words = theme_text.split()
        current_line = []
        for word in words:
            current_line.append(word)
            w_test = draw.textlength(" ".join(current_line), font=font_theme)
            if w_test > W * 0.8: # 80% of width
                current_line.pop()
                lines.append(" ".join(current_line))
                current_line = [word]
        lines.append(" ".join(current_line))
        
        y_text = H * 0.34
        for line in lines:
            length = draw.textlength(line, font=font_theme)
            x_text = (W - length) / 2
            draw.text((x_text, y_text), line, font=font_theme, fill=TEXT_COLOR_BLUE)
            y_text += 70
            
        # 3. Hymns (Below Theme)
        y_hymns = y_text + 50
        hymns_text = f"Hinos Sugeridos: {lesson_data['hymns']}"
        length_hymns = draw.textlength(hymns_text, font=font_hymns)
        draw.text(((W - length_hymns)/2, y_hymns), hymns_text, font=font_hymns, fill=TEXT_COLOR)
        
        # 4. Professor (Bottom)
        y_prof = H * 0.60
        prof_text = f"{professor_name}"
        length_prof = draw.textlength(prof_text, font=font_prof)
        draw.text(((W - length_prof)/2, y_prof), prof_text, font=font_prof, fill=TEXT_COLOR)
        
        # 5. Breakfast (Bottom text)
        if has_breakfast:
            y_break = H * 0.85
            break_text = "Café da manhã às 8:30h"
            length_break = draw.textlength(break_text, font=font_break)
            draw.text(((W - length_break)/2, y_break), break_text, font=font_break, fill=TEXT_COLOR)

        # Output
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)
            
        filename = f"ebd_licao_{lesson_data['lesson_number']}.png"
        save_path = os.path.join(OUTPUT_DIR, filename)
        img.save(save_path)
        print(f"Image saved to {save_path}")
        return True

    except Exception as e:
        print(f"Error generating image: {e}")
        return str(e)

if __name__ == "__main__":
    # Test data
    data = {"lesson_number": "07", "theme": "A Soberania de Deus na História", "hymns": "124, 456, 789"}
    generate_card(data, "Pr. Kleber", True)
