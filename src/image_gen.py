from PIL import Image, ImageDraw, ImageFont
import os

TEMPLATE_PATH = "assets/template.png"
OUTPUT_DIR = "output"
FONT_PATH = "assets/font.ttf"  # Local font file

def generate_card(lesson_data, professor_name, has_breakfast):
    """
    Generates the EBD card.
    lesson_data: dict with 'lesson_number', 'theme', 'hymns'
    professor_name: str
    has_breakfast: bool
    """
    if not os.path.exists(TEMPLATE_PATH):
        print(f"Error: Template not found at {TEMPLATE_PATH}")
        print(f"Current Working Directory: {os.getcwd()}")
        print(f"Files in assets: {os.listdir('assets') if os.path.exists('assets') else 'Assets folder not found'}")
        return f"Template not found at {TEMPLATE_PATH}. CWD: {os.getcwd()}"

    try:
        img = Image.open(TEMPLATE_PATH)
        draw = ImageDraw.Draw(img)
        
        # Dimensions for centering
        W, H = img.size
        
        # Colors
        TEXT_COLOR = (255, 255, 255) # White
        TEXT_COLOR_BLUE = (0, 50, 100)   # Dark Blue for Theme Box (if we were drawing it, but we assume it's part of the bg or we just draw text)
        THEME_COLOR = (0, 50, 100)   # Dark Blue for Theme Box (if we were drawing it, but we assume it's part of the bg or we just draw text)
        # Actually the user sent a "clean" image, so we just draw text over it.
        
        # --- CONFIGURATION (Adjust these coordinates) ---
        # Lesson Number (Top Right usually, or near title)
        # Assuming layout based on typical EBD cards
        
        # 1. Lesson Number
        # Font Loading Logic
        try:
            font_lesson = ImageFont.truetype(FONT_PATH, 40)
            font_theme = ImageFont.truetype(FONT_PATH, 30)
            font_hymns = ImageFont.truetype(FONT_PATH, 40)
            font_prof = ImageFont.truetype(FONT_PATH, 120)
            font_break = ImageFont.truetype(FONT_PATH, 30)
        except IOError:
            print(f"Warning: Font not found at {FONT_PATH}. Using default.")
            font_lesson = ImageFont.load_default()
            font_theme = ImageFont.load_default()
            font_hymns = ImageFont.load_default()
            font_prof = ImageFont.load_default()
            font_break = ImageFont.load_default()
        # Position: Let's assume top right or top center. 
        # User said: "numero da lição... tema... hinos... professor... café"
        # I will print "Lição X" 
        lesson_number = str(lesson_data['lesson_number']).zfill(2)
        lesson_text = f"Lição {lesson_number}"
        # Position: Top Right
        length_lesson = draw.textlength(lesson_text, font=font_lesson)
        draw.text((W - length_lesson - 40, 90), lesson_text, font=font_lesson, fill=TEXT_COLOR)
        
        # 2. Theme (Central, Big)
        # font_theme is already loaded above
        theme_text = lesson_data['theme']
        # Wrap text if too long
        lines = []
        words = theme_text.split()
        current_line = []
        for word in words:
            current_line.append(word)
            # test width
            w_test = draw.textlength(" ".join(current_line), font=font_theme)
            if w_test > W * 0.8: # 80% of width
                current_line.pop()
                lines.append(" ".join(current_line))
                current_line = [word]
        lines.append(" ".join(current_line))
        
        y_text = H * 0.34 # Start at 34% height
        for line in lines:
            length = draw.textlength(line, font=font_theme)
            x_text = (W - length) / 2
            draw.text((x_text, y_text), line, font=font_theme, fill=TEXT_COLOR_BLUE)
            y_text += 70 # Line height
            
        # 3. Hymns (Below Theme)
        y_hymns = y_text + 50
        # font_hymns is already loaded above
        hymns_text = f"Hinos Sugeridos: {lesson_data['hymns']}"
        length_hymns = draw.textlength(hymns_text, font=font_hymns)
        draw.text(((W - length_hymns)/2, y_hymns), hymns_text, font=font_hymns, fill=TEXT_COLOR)
        
        # 4. Professor (Bottom)
        y_prof = H * 0.60
        # font_prof is already loaded above
        prof_text = f"{professor_name}"
        length_prof = draw.textlength(prof_text, font=font_prof)
        draw.text(((W - length_prof)/2, y_prof), prof_text, font=font_prof, fill=TEXT_COLOR)
        
        # 5. Breakfast (Bottom text)
        if not has_breakfast: # If NOT Holy Supper (Santa Ceia) -> We have breakfast
            # Wait, "caso não seja culto de santa ceia colocamos a informação de que teremos café"
            # So if NOT Santa Ceia -> Print Breakfast
            # User input "Holy Supper sunday?" (True/False). If True -> No Breakfast.
            pass
        
        if has_breakfast:
            y_break = H * 0.85
            # font_break is already loaded above
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
