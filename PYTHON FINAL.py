import tkinter as tk
from tkinter import messagebox
import pygame
from PIL import Image, ImageTk
import random

WIDTH, HEIGHT = 800, 600  # Define WIDTH and HEIGHT as global variables
screen = None  # Initialize screen as global variable
pause_rect = None  # Initialize pause_rect as global variable
music_playing = False  # Flag to indicate if music is playing

def display_winner(winner):
    global WIDTH, HEIGHT, screen, music_playing  # Access global WIDTH, HEIGHT, and screen
    pygame.mixer.music.stop()  # Stop previous music
    if music_playing:
        pygame.mixer.music.stop()  # Stop previous music if playing
    screen.fill((0, 0, 0))  # Fill the screen with black color
    
    # Firework animation combined with player name
    fireworks = []
    for _ in range(30):
        x = random.randint(50, WIDTH - 50)
        y = random.randint(50, HEIGHT - 50)
        speed_x = random.randint(-5, 5)
        speed_y = random.randint(-20, -5)
        fireworks.append([x, y, speed_x, speed_y])
    
    font = pygame.font.SysFont(None, 60)
    text = font.render(f"{winner} You won the Game!", True, (255, 255, 255))  # Render the text
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))  # Center the text
    
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill((0, 0, 0))  # Fill the screen with black color
        
        # Draw fireworks
        for firework in fireworks:
            firework[1] += firework[3]
            firework[0] += firework[2]
            pygame.draw.circle(screen, (255, 255, 255), (int(firework[0]), int(firework[1])), 3)
            firework[3] += 0.5
            if firework[1] > HEIGHT:
                fireworks.remove(firework)
        
        screen.blit(text, text_rect)  # Draw the text on the screen
        
        pygame.display.flip()
        clock.tick(30)
        
        if not fireworks:
            running = False  # Exit the loop once fireworks are finished
    
    pygame.display.update()  # Update the display
    pygame.time.delay(3000)  # Pause for 3 seconds
    # Play win sound effect
    win_sound = pygame.mixer.Sound(r"C:\Users\benja\OneDrive\Documents\winner.mp3")
    win_sound.play()
    pygame.time.delay(3000)  # Pause for 3 seconds after playing the winner audio
    # Resume music
    pygame.mixer.music.load(r"C:\users\benja\OneDrive\Documents\pong audio.mp3")
    pygame.mixer.music.play(-1)  # Play the music on loop
    music_playing = True  # Set flag to indicate music is playing

def start_game(left_player_name, right_player_name):
    global WIDTH, HEIGHT, screen, pause_rect, music_playing  # Access global variables
    
    pygame.init()
    pygame.mixer.init()
    
    # Play music indicating the game is about to start
    ready_music = pygame.mixer.Sound(r"C:\Users\benja\OneDrive\Documents\are you ready.opus")
    ready_music.play()
    
    messagebox.showinfo("Table Tennis Game", "Are You Ready😎...")
    
    pygame.mixer.music.load(r"C:\users\benja\OneDrive\Documents\pong audio.mp3")
    pygame.mixer.music.play(-1)  # Play the main music on loop
    music_playing = True  # Set flag to indicate music is playing
    
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pong")
    
    # Load background image
    background_image = pygame.image.load(r"C:\Users\benja\OneDrive\Documents\background5.jpg").convert()
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
    
    GRASS = (0, 154, 23)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
    PADDLE_SPEED = 10
    BALL_SIZE = 20
    BALL_SPEED_X, BALL_SPEED_Y = 5, 5
    FONT = pygame.font.Font(None, 74)
    
    left_paddle = pygame.Rect(30, (HEIGHT // 2) - (PADDLE_HEIGHT // 2), PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = pygame.Rect(WIDTH - 40, (HEIGHT // 2) - (PADDLE_HEIGHT // 2), PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
    
    left_score = 0
    right_score = 0
    
    running = True
    clock = pygame.time.Clock()
    
    def reset_ball():
        nonlocal BALL_SPEED_X, BALL_SPEED_Y
        ball.x = WIDTH // 2 - BALL_SIZE // 2
        ball.y = HEIGHT // 2 - BALL_SIZE // 2
        BALL_SPEED_X *= -1
    
    paused = False  # Flag to indicate if the game is paused
    
    # Initialize pause button rectangle
    pause_rect = pygame.Rect(WIDTH - 120, 20, 100, 40)
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pause_rect.collidepoint(event.pos):  # Check if pause button is clicked
                    paused = not paused  # Toggle pause state
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and left_paddle.top > 0:
            left_paddle.y -= PADDLE_SPEED
        if keys[pygame.K_s] and left_paddle.bottom < HEIGHT:
            left_paddle.y += PADDLE_SPEED
        if keys[pygame.K_UP] and right_paddle.top > 0:
            right_paddle.y -= PADDLE_SPEED
        if keys[pygame.K_DOWN] and right_paddle.bottom < HEIGHT:
            right_paddle.y += PADDLE_SPEED
    
        if not paused:  # If not paused, update ball position
            ball.x += BALL_SPEED_X
            ball.y += BALL_SPEED_Y
    
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            BALL_SPEED_Y *= -1
    
        if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
            BALL_SPEED_X *= -1
    
        if ball.left <= 0:
            right_score += 1
            reset_ball()
        if ball.right >= WIDTH:
            left_score += 1
            reset_ball()
    
        if left_score == 11:
            display_winner(left_player_name)
            running = False
        elif right_score == 11:
            display_winner(right_player_name)
            running = False
    
        # Draw background image
        screen.blit(background_image, (0, 0))
    
        pygame.draw.rect(screen, WHITE, left_paddle)
        pygame.draw.rect(screen, WHITE, right_paddle)
        pygame.draw.ellipse(screen, BLACK, ball)
        pygame.draw.aaline(screen, BLACK, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))
    
        left_text = FONT.render(str(left_score), True, WHITE)
        screen.blit(left_text, (WIDTH // 4 - left_text.get_width() // 2, 20))
    
        right_text = FONT.render(str(right_score), True, WHITE)
        screen.blit(right_text, (WIDTH * 3 // 4 - right_text.get_width() // 2, 20))
        
        # Draw pause button with increased width and color
        pygame.draw.rect(screen, (255, 0, 0), pause_rect)
        pause_font = pygame.font.Font(None, 30)
        pause_text = pause_font.render("Pause" if not paused else "Resume", True, (255, 255, 255))
        screen.blit(pause_text, (pause_rect.x + 15, pause_rect.y + 10))
    
        # Draw player names at the bottom
        player_font = pygame.font.Font(None, 36)
        left_player_text = player_font.render(left_player_name, True, WHITE)
        right_player_text = player_font.render(right_player_name, True, WHITE)
        screen.blit(left_player_text, (50, HEIGHT - 40))
        screen.blit(right_player_text, (WIDTH - 50 - right_player_text.get_width(), HEIGHT - 40))
    
        pygame.display.flip()
        clock.tick(60)

    pygame.mixer.music.stop()  # Stop music when game ends
    music_playing = False  # Reset flag for music playing
    pygame.quit()

def quit_game():
    root.destroy()

root = tk.Tk()
root.title("Table Tennis Game")

# Load background image for the front page
front_page_background_image = Image.open(r"C:\Users\benja\OneDrive\Pictures\pong8.png")
front_page_background_photo = ImageTk.PhotoImage(front_page_background_image)

front_page_background_label = tk.Label(root, image=front_page_background_photo)
front_page_background_label.place(relwidth=1, relheight=1)

frame = tk.Frame(root, padx=20, pady=20)
frame.pack(padx=10, pady=10)

# Center the label
welcome_label = tk.Label(frame, text="🏓Welcome to Table Tennis Game🏓", font=("Arial", 24))
welcome_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
welcome_label.pack(pady=10)

# Entry fields for player names
left_player_entry = tk.Entry(frame, font=("Arial", 14))
left_player_entry.insert(0, "Player 1")
left_player_entry.pack(pady=5)

right_player_entry = tk.Entry(frame, font=("Arial", 14))
right_player_entry.insert(0, "Player 2")
right_player_entry.pack(pady=5)

start_button = tk.Button(frame, text="Start", font=("Arial", 18), command=lambda: start_game(left_player_entry.get(), right_player_entry.get()), bg="green", fg="white")
start_button.pack(pady=10)

quit_button = tk.Button(frame, text="Quit", font=("Arial", 18), command=quit_game, bg="red", fg="white")
quit_button.pack(pady=10)

root.mainloop()