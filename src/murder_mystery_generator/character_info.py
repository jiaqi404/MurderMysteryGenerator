from PIL import Image, ImageDraw, ImageFont

def generate_text_on_image(image_path, output_path, title, subtitle, small_text, color):
    # 打开图片
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    
    # 加载系统默认字体
    title_font = ImageFont.truetype("arial.ttf", 80)  # 设置标题字体大小为40
    subtitle_font = ImageFont.truetype("arial.ttf", 32)  # 设置副标题字体大小为30
    small_text_font = ImageFont.truetype("arial.ttf", 24)  # 设置小文字字体大小为20
    
    # 获取图片尺寸
    image_width, image_height = image.size
    
    # 绘制标题
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width, title_height = title_bbox[2] - title_bbox[0], title_bbox[3] - title_bbox[1]
    title_position = ((image_width - title_width) // 2, 220)
    draw.text(title_position, title, font=title_font, fill=color)
    
    # 绘制副标题
    subtitle_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
    subtitle_width, subtitle_height = subtitle_bbox[2] - subtitle_bbox[0], subtitle_bbox[3] - subtitle_bbox[1]
    subtitle_position = ((image_width - subtitle_width) // 2, 340)
    draw.text(subtitle_position, subtitle, font=subtitle_font, fill=color)
    
    # 绘制小文字，自动换行
    max_width = image_width - 240# 设置最大宽度，留出边距
    lines = []
    words = small_text.split()
    current_line = ""

    for word in words:
        test_line = f"{current_line} {word}".strip()
        test_bbox = draw.textbbox((0, 0), test_line, font=small_text_font)
        test_width = test_bbox[2] - test_bbox[0]
        if test_width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)

    # 绘制每一行文字
    y_text = 420  # 起始高度
    line_spacing = 10  # 行间距
    for line in lines:
        line_bbox = draw.textbbox((0, 0), line, font=small_text_font)
        line_width = line_bbox[2] - line_bbox[0]
        line_height = line_bbox[3] - line_bbox[1]
        line_bbox = draw.textbbox((0, 0), line, font=small_text_font)
        line_width, line_height = line_bbox[2] - line_bbox[0], line_bbox[3] - line_bbox[1]
        line_position = ((image_width - line_width) // 2, y_text)
        draw.text(line_position, line, font=small_text_font, fill=color)
        y_text += line_height + line_spacing
    
    # 保存图片
    image.save(output_path)

# 示例用法
generate_text_on_image(
    image_path="C:\\Users\\sdit\\Documents\\GitHub\\murder_mystery_generator\\ComfyUI Workflow\\Card Design\\2.png",
    output_path="output.png",
    title="Lyra",
    subtitle="Adventurer and Cartographer",
    small_text="Lyra was born into a family of nomadic explorers and developed exceptional skills in navigation, botany, and deciphering ancient symbols. She became a renowned adventurer, but her parents' disappearance on an expedition left her with a sense of abandonment.",
    color=(255, 255, 255)
)