import serial
import pygame
import time

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("EEPROM Interface")

font = pygame.font.Font(None, 36)
input_box = pygame.Rect(100, 100, 200, 32)
output_box = pygame.Rect(100, 150, 200, 32)
write_button = pygame.Rect(100, 200, 140, 32)
read_button = pygame.Rect(100, 250, 140, 32)
reset_button = pygame.Rect(100, 300, 140, 32)

color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
color = color_inactive
text = ''
output_text = ''
clock = pygame.time.Clock()
input_active = False

# Set up serial connection (Update COM port as needed)
ser = serial.Serial('COM3', 9600, timeout=1)

def send_to_arduino(command, address, data=None):
    ser.write(bytes([address]))
    ser.write(bytes([data]) if data is not None else bytes([0]))
    ser.write(bytes([command]))

def read_from_arduino():
    if ser.in_waiting > 0:
        return ser.read()
    return None

def reset_eeprom():
    # Send reset command to Arduino
    send_to_arduino(2, 0)

def write_to_eeprom():
    try:
        address = int(text[:2], 16)
        data = int(text[2:], 16)  # Convert hex string to integer
        send_to_arduino(0, address, data)
    except ValueError:
        print("Invalid address or data")

def read_from_eeprom():
    try:
        address = int(text[:2], 16)
        send_to_arduino(1, address)
        time.sleep(0.1)  # Give Arduino time to process
        data = read_from_arduino()
        if data is not None:
            return format(ord(data), '02X')  # Format the byte to hex
    except ValueError:
        print("Invalid address")

def draw_text(surf, text, pos):
    text_surface = font.render(text, True, pygame.Color('white'))
    text_rect = text_surface.get_rect(center=pos)
    surf.blit(text_surface, text_rect)

def main():
    global input_active, text, output_text, color
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    input_active = not input_active
                    color = color_active if input_active else color_inactive
                elif write_button.collidepoint(event.pos):
                    write_to_eeprom()
                elif read_button.collidepoint(event.pos):
                    read_data = read_from_eeprom()
                    if read_data:
                        output_text = read_data
                    else:
                        output_text = "0"
                elif reset_button.collidepoint(event.pos):
                    reset_eeprom()
            if event.type == pygame.KEYDOWN:
                if input_active:
                    if event.key == pygame.K_RETURN:
                        write_to_eeprom()
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
                if event.key == pygame.K_r and not input_active:
                    read_data = read_from_eeprom()
                    if read_data:
                        output_text = read_data
                if event.key == pygame.K_d and not input_active:
                    reset_eeprom()

        screen.fill((0, 0, 0))

        # Draw input box
        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(screen, color, input_box, 2)

        # Draw output box
        output_surface = font.render(output_text, True, pygame.Color('white'))
        output_box.w = max(200, output_surface.get_width()+10)
        screen.blit(output_surface, (output_box.x+5, output_box.y+5))
        pygame.draw.rect(screen, pygame.Color('white'), output_box, 2)

        # Draw buttons
        pygame.draw.rect(screen, pygame.Color('green'), write_button)
        draw_text(screen, 'Write', (write_button.x + write_button.w // 2, write_button.y + write_button.h // 2))
        
        pygame.draw.rect(screen, pygame.Color('blue'), read_button)
        draw_text(screen, 'Read', (read_button.x + read_button.w // 2, read_button.y + read_button.h // 2))

        pygame.draw.rect(screen, pygame.Color('red'), reset_button)
        draw_text(screen, 'Reset', (reset_button.x + reset_button.w // 2, reset_button.y + reset_button.h // 2))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    ser.close()

if __name__ == "__main__":
    main()
