import tkinter as tk
from tkinter import messagebox
import random
import winsound
import time

class FullScreenTicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("🎮 SUPER TIC-TAC-TOE!")
        self.root.configure(bg="#FFD700")  # Bright yellow background
        
        # Make the game fullscreen (escape key exits fullscreen)
        self.root.attributes('-fullscreen', True)
        self.root.bind("<Escape>", lambda e: self.root.attributes("-fullscreen", False))
        
        # Game settings (customize emojis here!)
        self.players = ["🐶", "🐱"]  # Dog vs Cat (try 🦄 vs 🦖 too!)
        self.player_colors = ["#FF6B6B", "#4ECDC4"]  # Red & Teal
        self.current_player = random.choice([0, 1])  # Random starter
        self.game_active = True
        
        # Sound effects (simple beeps)
        self.sounds = {
            "click": (784, 100),  # High beep
            "win": [(659, 200), (784, 200), (988, 300)],  # Fanfare
            "tie": (392, 500),  # Low "aww" sound
        }
        
        # Create the game UI
        self.setup_ui()
        
    def setup_ui(self):
        # Title with emojis (bigger font for fullscreen)
        title = tk.Label(
            self.root, 
            text=f"TIC-TAC-TOE: {self.players[0]} vs {self.players[1]}", 
            font=("Comic Sans MS", 36, "bold"), 
            fg="#FF1493",  # Deep pink
            bg="#FFD700"
        )
        title.pack(pady=20)
        
        # Turn indicator (who's playing now?)
        self.turn_label = tk.Label(
            self.root, 
            text=f"{self.players[self.current_player]}'s Turn!", 
            font=("Comic Sans MS", 28, "bold"), 
            fg=self.player_colors[self.current_player], 
            bg="#FFD700"
        )
        self.turn_label.pack(pady=10)
        
        # Game board frame (centered)
        game_frame = tk.Frame(self.root, bg="#FFD700")
        game_frame.pack(expand=True)
        
        # Create BIG buttons (filling the screen)
        self.buttons = []
        button_font = ("Segoe UI Emoji", 60)  # Very large emojis
        
        for i in range(9):
            button = tk.Button ( 
                game_frame, 
                text="", 
                font=button_font,
                width=3, 
                height=1, 
                bg="#FFFFFF",  # White buttons
                relief="raised", 
                bd=8,
                command=lambda i=i: self.button_click(i)
            )
            button.grid(
                row=i//3, 
                column=i%3, 
                padx=10, 
                pady=10,
                sticky="nsew"  # Makes buttons expand
            )
            self.buttons.append(button)
        
        # Make buttons expand to fill space
        for i in range(3):
            game_frame.grid_rowconfigure(i, weight=1)
            game_frame.grid_columnconfigure(i, weight=1)
        
        # Reset button (big and colorful)
        reset_btn = tk.Button(
            self.root, 
            text="🔄 PLAY AGAIN!", 
            font=("Comic Sans MS", 24), 
            command=self.reset_game, 
            bg="#FFA07A",  # Light salmon
            fg="white",
            activebackground="#FF6347"  # Tomato
        )
        reset_btn.pack(pady=5)
    
    def button_click(self, index):
        if not self.game_active or self.buttons[index]["text"] != "":
            return
        
        # Play a fun click sound
        self.play_sound("click")
        
        # Set the emoji & color
        self.buttons[index]["text"] = self.players[self.current_player]
        self.buttons[index]["fg"] = self.player_colors[self.current_player]
        
        # Check for a winner
        if self.check_winner():
            self.game_active = False
            self.celebrate_win()
            return
        
        # Check for a tie
        if all(btn["text"] != "" for btn in self.buttons):
            self.game_active = False
            self.play_sound("tie")
            messagebox.showinfo("Game Over!", "It's a TIE! 🎭")
            return
        
        # Switch player
        self.current_player = 1 - self.current_player  # Toggle 0 ↔ 1
        self.turn_label.config(
            text=f"{self.players[self.current_player]}'s Turn!", 
            fg=self.player_colors[self.current_player]
        )
    
    def check_winner(self):
        winning_combos = [
            [0,1,2], [3,4,5], [6,7,8],  # Rows
            [0,3,6], [1,4,7], [2,5,8],  # Columns
            [0,4,8], [2,4,6]            # Diagonals
        ]
        
        for combo in winning_combos:
            a, b, c = combo
            if (self.buttons[a]["text"] == self.buttons[b]["text"] == 
                self.buttons[c]["text"] != ""):
                return True
        return False
    
    def celebrate_win(self):
        # Play victory fanfare
        for note in self.sounds["win"]:
            self.play_sound(note)
            time.sleep(0.2)
        
        # Find the winning combo
        winning_combos = [
            [0,1,2], [3,4,5], [6,7,8],  # Rows
            [0,3,6], [1,4,7], [2,5,8],  # Columns
            [0,4,8], [2,4,6]             # Diagonals
        ]
        
        winning_combo = None
        for combo in winning_combos:
            a, b, c = combo
            if (self.buttons[a]["text"] == self.buttons[b]["text"] == 
                self.buttons[c]["text"] != ""):
                winning_combo = combo
                break
        
        if winning_combo:
            # Make winning buttons "dance" (change colors)
            for _ in range(5):
                for index in winning_combo:
                    self.buttons[index].config(bg="#FF69B4")  # Hot pink
                self.root.update()
                time.sleep(0.2)
                
                for index in winning_combo:
                    self.buttons[index].config(bg="#7FFFD4")  # Aquamarine
                self.root.update()
                time.sleep(0.2)
            
            winner = self.buttons[winning_combo[0]]["text"]
            messagebox.showinfo(
                "🎊 WINNER! 🎊", 
                f"{winner} WINS! 🎉"
            )
    
    def play_sound(self, sound):
        try:
            if isinstance(sound, tuple):  # Single note
                winsound.Beep(*sound)
            else:  # Sound name (e.g., "click")
                winsound.Beep(*self.sounds[sound])
        except:
            pass  # Skip if sound fails
    
    def reset_game(self):
        # Play a reset sound
        self.play_sound("click")
        
        # Reset game state
        self.game_active = True
        self.current_player = random.choice([0, 1])  # Random starter
        
        # Update turn label
        self.turn_label.config(
            text=f"{self.players[self.current_player]}'s Turn!", 
            fg=self.player_colors[self.current_player]
        )
        
        # Clear all buttons
        for button in self.buttons:
            button.config(text="", bg="#FFFFFF")  # Reset to white

# Run the game in fullscreen!
root = tk.Tk()
game = FullScreenTicTacToe(root)
root.mainloop()
