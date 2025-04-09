import tkinter as tk
import random

class RPSGame:
    def __init__(self, root):
        self.root = root
        self.root.title("✨ Rock Paper Scissors ✨")
        self.root.geometry("550x500")
        self.root.config(bg="#FDF6F0")
        self.root.resizable(False, False)
        
        self.user_score = 0
        self.computer_score = 0
        
        self.header = tk.Frame(self.root, bg="#F9D5E5", bd=5, relief="groove")
        self.header.pack(pady=20, fill=tk.X)

        self.title_label = tk.Label(self.header, text="Rock ✊  Paper ✋  Scissors ✌️", font=("Verdana", 20, "bold"), bg="#F9D5E5", fg="#4B3F72")
        self.title_label.pack(pady=10)

        
        self.button_frame = tk.Frame(self.root, bg="#FDF6F0")
        self.button_frame.pack(pady=30)

        self.rock_btn = tk.Button(self.button_frame, text="✊ Rock", font=("Helvetica", 14, "bold"), width=12,
                                  bg="#B5EAD7", fg="#2C2C2C", bd=0, relief="ridge", activebackground="#A1DAC8",
                                  cursor="hand2", command=lambda: self.play("rock"))
        self.rock_btn.grid(row=0, column=0, padx=15)

        self.paper_btn = tk.Button(self.button_frame, text="✋ Paper", font=("Helvetica", 14, "bold"), width=12,
                                   bg="#FFDAC1", fg="#2C2C2C", bd=0, relief="ridge", activebackground="#FEC8A9",
                                   cursor="hand2", command=lambda: self.play("paper"))
        self.paper_btn.grid(row=0, column=1, padx=15)

        self.scissors_btn = tk.Button(self.button_frame, text="✌️ Scissors", font=("Helvetica", 14, "bold"), width=12,
                                      bg="#C7CEEA", fg="#2C2C2C", bd=0, relief="ridge", activebackground="#B8C1E4",
                                      cursor="hand2", command=lambda: self.play("scissors"))
        self.scissors_btn.grid(row=0, column=2, padx=15)

        self.result_label = tk.Label(self.root, text="", font=("Verdana", 14), bg="#FDF6F0", fg="#444")
        self.result_label.pack(pady=20)
        
        self.score_label = tk.Label(self.root, text="Score ➤  You: 0 | Computer: 0", font=("Verdana", 12, "bold"),
                                    bg="#FDF6F0", fg="#4B3F72")
        self.score_label.pack(pady=10)
        
        self.play_again_btn = tk.Button(self.root, text="🔄 Play Again", font=("Verdana", 12, "bold"),
                                        bg="#FFB7B2", fg="black", activebackground="#FF9A96", bd=0, cursor="hand2",
                                        command=self.reset_result)
        self.play_again_btn.pack(pady=15)

    def play(self, user_choice):
        options = ["rock", "paper", "scissors"]
        computer_choice = random.choice(options)

        result_msg = f"You chose: {user_choice.capitalize()} \nComputer chose: {computer_choice.capitalize()}"

        if user_choice == computer_choice:
            result = "It's a Tie! 😐"
        elif (user_choice == "rock" and computer_choice == "scissors") or \
             (user_choice == "paper" and computer_choice == "rock") or \
             (user_choice == "scissors" and computer_choice == "paper"):
            result = "You Win! 🎉"
            self.user_score += 1
        else:
            result = "Computer Wins! 😢"
            self.computer_score += 1

        self.result_label.config(text=f"{result_msg}\n\n{result}")
        self.score_label.config(text=f"Score ➤  You: {self.user_score} | Computer: {self.computer_score}")

    def reset_result(self):
        self.result_label.config(text="Let's go another round! Choose your move 👇")

if __name__ == "__main__":
    root = tk.Tk()
    game = RPSGame(root)
    root.mainloop()
