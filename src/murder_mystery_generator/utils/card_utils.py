from PIL import Image, ImageDraw, ImageFont
import yaml

# hex to rgb
def transfer_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

# get content from character markdown
def get_content(character_md, character_name, content_name):
    with open(character_md, 'r', encoding='utf-8') as file:
        character_md = file.read()
    lines = character_md.splitlines()
    content = ""
    found_character = False

    for line in lines:
        if character_name in line:
            found_character = True
        elif found_character and content_name in line:
            content = line.split(content_name, 1)[1].strip()
            content = content.replace('*', '').replace('-', '').replace(':', '').replace('#', '')
            break

    return content

# limit text width in pil draw
def limit_text_width(draw, text, font, color, image_width, spacing, start_height, line_spacing):
    if text is None:
        text = ""
    max_width = image_width - spacing
    lines = []
    words = text.split()
    current_line = ""

    for word in words:
        test_line = f"{current_line} {word}".strip()
        test_bbox = draw.textbbox((0, 0), test_line, font=font)
        test_width = test_bbox[2] - test_bbox[0]
        if test_width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)

    for line in lines:
        line_bbox = draw.textbbox((0, 0), line, font=font)
        line_width = line_bbox[2] - line_bbox[0]
        line_height = line_bbox[3] - line_bbox[1]
        line_bbox = draw.textbbox((0, 0), line, font=font)
        line_width, line_height = line_bbox[2] - line_bbox[0], line_bbox[3] - line_bbox[1]
        line_position = ((image_width - line_width) // 2, start_height)
        draw.text(line_position, line, font=font, fill=color)
        start_height += line_height + line_spacing

    return start_height

# generate card info with given parameters
def generate_card_info(
        image_path, 
        output_path, 
        title, 
        subtitle, 
        text, 
        title_font="arial.ttf", 
        subtitle_font="arial.ttf", 
        text_font="arial.ttf", 
        color=(255, 255, 255)
    ):
    
    start_height = 240

    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    
    title_font = ImageFont.truetype(title_font, 128)
    subtitle_font = ImageFont.truetype(subtitle_font, 32)
    small_text_font = ImageFont.truetype(text_font, 24)
    
    image_width, image_height = image.size
    
    # draw title, auto center
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width, title_height = title_bbox[2] - title_bbox[0], title_bbox[3] - title_bbox[1]
    title_position = ((image_width - title_width) // 2, start_height)
    draw.text(title_position, title, font=title_font, fill=color)
    
    # draw subtitle, auto center and limit width
    start_height_2 = limit_text_width(
        draw=draw,
        text=subtitle,
        font=subtitle_font,
        color=color,
        image_width=image_width,
        spacing=280,
        start_height=start_height + 140,
        line_spacing=12
    )
    
    # draw text, auto center and limit width
    limit_text_width(
        draw=draw, 
        text=text, 
        font=small_text_font, 
        color=color, 
        image_width=image_width, 
        spacing=320, 
        start_height=start_height_2 + 40, 
        line_spacing=12
    )
    
    image.save(output_path)