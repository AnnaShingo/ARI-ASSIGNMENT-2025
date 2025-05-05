import tkinter as tk
from tkinter import messagebox
from tictactoe import initial_state, player, actions, result, winner, terminal, utility, minimax

class TicTacToeGUI:
    def __init__(self, root):
        """Initialize the Tic-Tac-Toe game GUI"""
        self.root = root
        self.root.title("Tic-Tac-Toe AI")
        self.root.resizable(False, False)
        
        # Game state variables
        self.board = initial_state()
        self.human_player = None
        self.ai_player = None
        self.current_player = 'X'  # X always goes first
        
        # GUI styling constants
        self.BG_COLOR = "#f0f0f0"
        self.BUTTON_FONT = ('Arial', 32, 'bold')
        self.TITLE_FONT = ('Arial', 16, 'bold')
        self.BUTTON_SIZE = 5
        
        # Configure root window background
        self.root.configure(bg=self.BG_COLOR)
        
        self.setup_player_selection()
    
    def setup_player_selection(self):
        """Create player selection screen"""
        self.selection_frame = tk.Frame(self.root, bg=self.BG_COLOR)
        self.selection_frame.pack(pady=20, padx=20)
        
        # Title label
        tk.Label(
            self.selection_frame, 
            text="Choose Your Player", 
            font=self.TITLE_FONT,
            bg=self.BG_COLOR
        ).pack(pady=(0, 10))
        
        # Player selection radio buttons
        self.player_var = tk.StringVar(value="X")
        
        tk.Radiobutton(
            self.selection_frame, 
            text="X (Go First)", 
            variable=self.player_var, 
            value="X",
            font=('Arial', 12),
            bg=self.BG_COLOR,
            activebackground=self.BG_COLOR
        ).pack(anchor='w', padx=20)
        
        tk.Radiobutton(
            self.selection_frame, 
            text="O (Go Second)", 
            variable=self.player_var, 
            value="O",
            font=('Arial', 12),
            bg=self.BG_COLOR,
            activebackground=self.BG_COLOR
        ).pack(anchor='w', padx=20)
        
        # Start game button
        tk.Button(
            self.selection_frame, 
            text="Start Game", 
            command=self.start_game,
            font=('Arial', 12, 'bold'),
            bg="#4CAF50",
            fg="white",
            activebackground="#45a049",
            relief=tk.RAISED,
            padx=10,
            pady=5
        ).pack(pady=15)
    
    def start_game(self):
        """Start the game with selected player"""
        self.human_player = self.player_var.get()
        self.ai_player = 'O' if self.human_player == 'X' else 'X'
        
        # Remove selection screen
        self.selection_frame.destroy()
        
        # Create game board
        self.create_board()
        
        # If AI goes first, make its move
        if self.current_player == self.ai_player:
            self.ai_move()
    
    def create_board(self):
        """Create the 3x3 game board"""
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        
        # Create a frame for the board
        board_frame = tk.Frame(self.root, bg=self.BG_COLOR)
        board_frame.pack(pady=20)
        
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(
                    board_frame,
                    text="",
                    font=self.BUTTON_FONT,
                    width=self.BUTTON_SIZE,
                    height=self.BUTTON_SIZE//2,
                    bg="white",
                    activebackground="#e6e6e6",
                    relief=tk.RIDGE,
                    command=lambda row=i, col=j: self.human_move(row, col)
                )
                self.buttons[i][j].grid(
                    row=i, 
                    column=j, 
                    padx=5, 
                    pady=5,
                    ipadx=5,
                    ipady=5
                )
    
    def human_move(self, row, col):
        """Handle human player's move"""
        if self.current_player == self.human_player and (row, col) in actions(self.board):
            # Make the move
            self.board = result(self.board, (row, col))
            self.update_board()
            
            # Switch player
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            
            # Check if game continues
            if not terminal(self.board):
                self.ai_move()
            else:
                self.game_over()
    
    def ai_move(self):
        """Handle AI player's move"""
        if self.current_player == self.ai_player and not terminal(self.board):
            # Disable buttons while AI is "thinking"
            self.disable_buttons()
            self.root.update()
            
            # Get AI move
            move = minimax(self.board)
            
            if move:
                # Make the move
                self.board = result(self.board, move)
                self.update_board()
                
                # Switch player
                self.current_player = 'O' if self.current_player == 'X' else 'X'
            
            # Re-enable buttons
            self.enable_buttons()
            
            # Check if game is over
            if terminal(self.board):
                self.game_over()
    
    def update_board(self):
        """Update the visual representation of the board"""
        for i in range(3):
            for j in range(3):
                cell_value = self.board[i][j]
                button = self.buttons[i][j]
                
                if cell_value is not None:
                    button.config(
                        text=cell_value,
                        state=tk.DISABLED,
                        disabledforeground="red" if cell_value == 'X' else "blue"
                    )
    
    def disable_buttons(self):
        """Disable all board buttons"""
        for row in self.buttons:
            for button in row:
                button.config(state=tk.DISABLED)
    
    def enable_buttons(self):
        """Enable available board buttons"""
        for i in range(3):
            for j in range(3):
                if self.board[i][j] is None:
                    self.buttons[i][j].config(state=tk.NORMAL)
    
    def game_over(self):
        """Handle game over scenario"""
        game_winner = winner(self.board)
        
        # Show appropriate message
        if game_winner:
            if game_winner == self.human_player:
                message = "Congratulations! You won!"
            else:
                message = "AI wins!"
        else:
            message = "It's a tie!"
        
        # Show game over dialog
        messagebox.showinfo(
            "Game Over", 
            message,
            parent=self.root
        )
        
        # Close the game
        self.root.destroy()

def main():
    """Main function to start the application"""
    root = tk.Tk()
    game = TicTacToeGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()