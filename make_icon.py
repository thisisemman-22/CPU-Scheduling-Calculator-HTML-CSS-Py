from PIL import Image, ImageDraw

def create_cpu_icon():
    # Create a 256x256 image with transparent background
    img = Image.new('RGBA', (256, 256), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # Background gradient or solid color (Indigo)
    color = (99, 102, 241, 255) # #6366f1
    
    # Draw pins (the outer lines)
    pin_color = color
    pin_width = 16
    
    # Top and Bottom pins
    for x in [64, 128, 192]:
        # Top
        draw.rectangle([x-pin_width//2, 16, x+pin_width//2, 64], fill=pin_color)
        # Bottom
        draw.rectangle([x-pin_width//2, 192, x+pin_width//2, 240], fill=pin_color)
        
    # Left and Right pins
    for y in [64, 128, 192]:
        # Left
        draw.rectangle([16, y-pin_width//2, 64, y+pin_width//2], fill=pin_color)
        # Right
        draw.rectangle([192, y-pin_width//2, 240, y+pin_width//2], fill=pin_color)
    
    # Main body (rounded rectangle)
    draw.rounded_rectangle([40, 40, 216, 216], radius=24, fill=color)
    
    # Inner circuit/box
    draw.rounded_rectangle([90, 90, 166, 166], radius=12, outline=(255, 255, 255, 255), width=16)
    
    # Save as ICO (Pillow handles multiple sizes automatically if we just save as .ico, 
    # but we can just save a 256x256 which is fine for modern Windows)
    img.save('icon.ico', format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])

if __name__ == '__main__':
    create_cpu_icon()
