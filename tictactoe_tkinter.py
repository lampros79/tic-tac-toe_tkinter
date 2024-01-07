import random
import tkinter as tk
from tkinter import messagebox

class TicTacToe():
    # η κλάση που διαχειρίζεται τα μενού του προγράμματος καθώς και τη λειτουργία του παιχνιδιού
    def __init__(self, root):
        self.w = root
        self.w.title("TicTacToe")  # τίτλος του παιχνιδιού με όνομα TicTacToe
        self.w.geometry("700x750")  # μέγεθος του παραθύρου του παιχνιδιού
        self.w.resizable(0, 0)  # απαγόρευση δυνατότητας μεγέθυνσης ή σμίκρυνσης του παραθύρου από τον χρήστη
        self.w.configure(bg='brown')  # background του παραθύρου
        self.font_large = "Helvetica 40"  # γραμματοσειρά Helvetica με μέγεθος λέξεων 40 για το μενού
        self.font_small = "Helvetica 35"  # γραμματοσειρά Helvetica με μέγεθος λέξεων 35 για το αποτέλεσμα της παρτίδας
        self.button_style = {"font": self.font_large, "bg": "#FFD580", "activebackground": "#FFD580", "bd": 0, "relief": "flat"}
        # λεξικό με τις παραμέτρους του πως εμφανίζονται τα κουμπιά που πατάει ο χρήστης
        self.label_style = {"bg": "#800020", "fg": "white", "font": self.font_large}
        # λεξικό με τις παραμέτρους του πως εμφανίζεται ο τίτλος του παιχνιδιού πριν ανακοινωθεί ο νικητής
        self.win_label_initial = {"bg": "brown", "fg": "white", "font": self.font_small}
        # λεξικό με τις παραμέτρους του πως εμφανίζεται ο τίτλος του παιχνιδιού αφού ανακοινωθεί ο νικητής
        self.win_label_final = {"bg": "#800020"}
        # στην αρχή προσθέτουμε στο παράθυρο το στοιχείο το οποίο θα ανακοινώνει τον νικητή και στην αρχή πριν
        # ανακοινωθεί έχει το ίδιο χρώμα με το background προκειμένου να είναι αόρατο, έπειτα αλλάζουμε το χρώμα του
        # background ώστε να φανεί το κείμενο
        self.mainMenu() # ανοίγει το κυρίως μενού

    def mainMenu(self):
        # μέθοδος που ανοίγει το κύριο παράθυρο του προγράμματος
        # εμφανίζει τον τίτλο του παιχνιδιού και τις επιλογές να παίξει ο χρήστης είτε ενάντια ενός άλλου χρήστη είτε
        # ενάντια του υπολογιστή, είτε να κάνει έξοδο
        self.clearWindow()
        tk.Label(self.w, text="TicTacToe", **self.label_style).pack(expand=1, fill="both", padx=10, pady=10)
        tk.Button(self.w, text="1 player (AI)", command=self.onePlayer, **self.button_style).pack(expand=1, fill="both", padx=10, pady=10)
        tk.Button(self.w, text="2 players", command=self.twoPlayers, **self.button_style).pack(expand=1, fill="both", padx=10, pady=10)
        tk.Button(self.w, text="Exit", command=self.exit, **self.button_style).pack(expand=1, fill="both", padx=10, pady=10)

    # επιστρέφει τα παρακάτω νούμερα αναλόγως με το αποτέλεσμα του παιχνιδιού που εκτελείται την εκάστοτε στιγμή:
    #0 -> δεν υπάρχει νικητήρια παρτίδα άρα το παιχνίδι συνεχίζεται
    #1 -> κερδίζει ο παίκτης με τον χαρακτήρα X
    #2 -> κερδίζει ο παίκτης με τον χαρακτήρα O
    #3 -> ισοπαλία

    def checkWinner(self):
        # Ο gamePos είναι ένας πίνακας 3x3 που παίρνει τιμή 0 σε ένα κελί αν δεν υπάρχει καμία κίνηση σε αυτό
        # (ούτε Χ ούτε Ο). Έχει τιμή 1 αν υπάρχει Χ και τιμή 2 αν υπάρχει Ο.
        # Ελέγχει αν στην τρέχουσα παρτίδα υπάρχει νικητής στις οριζόντιες γραμμές
        for row in self.gamePos:
            if row[0] == row[1] == row[2] and row[0] != 0:
                return row[0]
        # Ελέγχει αν στην τρέχουσα παρτίδα υπάρχει νικητής στις κάθετες στήλες
        for i in range(3):
            if self.gamePos[0][i] == self.gamePos[1][i] == self.gamePos[2][i] and self.gamePos[0][i] != 0:
                return self.gamePos[0][i]
        # Ελέγχει τις 2 διαγώνιους για νικητή
        if self.gamePos[0][0] == self.gamePos[1][1] == self.gamePos[2][2] and self.gamePos[0][0] != 0:
            return self.gamePos[0][0]
        if self.gamePos[0][2] == self.gamePos[1][1] == self.gamePos[2][0] and self.gamePos[0][2] != 0:
            return self.gamePos[0][2]
        # Προκειμένου, έχουν εξαντληθεί όλες οι πιθανότητες για νικητή τα μόνα πιθανά αποτελέσματα είναι ή ισοπαλία ή
        # να συνεχιστεί το παιχνίδι (υπάρχει έστω ένα κελί που να μην έχει πατήσει ο παίκτης)
        # Ελέγχει αν υπάρχει έστω ένα κελί που να μην έχει κάποια κίνηση
        for i in range(3):
            for j in range(3):
                if self.gamePos[i][j] == 0:
                    return 0
        # Δεν υπάρχουν διαθέσιμα κελιά άρα το παιχνίδι λήγει με αποτέλεσμα ισοπαλίας
        return 3

    # Παίζει την κίνηση του παίκτη που έχει σειρά στο κελί με τις συντεταγμένες (posX, posY)
    def makeMove(self, posX, posY, isAI = False):
        # αν το παιχνίδι έχει ολοκληρωθεί να μην πραγματοποιηθεί καμία κίνηση
        if self.checkWinner() != 0:
            return
        if self.gamePos[posX][posY] == 0:  # Έλεγχος αν δεν υπάρχει ήδη κίνηση στο αντίστοιχο κελί
            # Αλλαγή της τιμής του κελιού στον πίνακα gamePos σε 1 ή 2 (Χ ή Ο αντίστοιχα)
            self.gamePos[posX][posY] = self.move
            if self.move == 1:
                new_text = "X"
            else:
                new_text = "O"
            # Αλλάζει το κείμενο του κουμπιού που αντιστοιχεί στο εκάστοτε κελί της παρτίδας (στην tkinter) σε X ή O
            self.buttons[posX][posY].config(text=new_text)
            winner = self.checkWinner()
            # Ελέγχουμε αν προκύπτει νίκη ή ισοπαλία μετά από την αντίστοιχη κίνηση
            if winner == 0:  # Αν όχι, αλλάζουμε τη σειρά στον άλλον παίκτη (από Ο να παίξει το Χ και αντίστροφα)
                if self.move == 1:
                    self.move = 2
                else:
                    self.move = 1
                # Αν ο χρήστης παίζει με τον υπολογιστή και ήταν προηγουμένως η σειρά του χρήστη, παίζει την κίνηση
                # του ο υπολογιστής
                if self.isOnePlayer and not isAI:
                    self.aiMove()
            else:  # ανακοινώνεται το αποτέλεσμα της παρτίδας: Νικητής (Χ ή Ο) ή ισοπαλία
                self.announceWinner(winner)


    # Εμφανίζει το μενού με τις επιλογές για την παρτίδα του χρήστη ενάντια του υπολογιστή καθώς και τον τίτλο:
    # Choose your side αντίστοιχα Play as X (first) ή Play as O (second) ή Return to main menu
    def onePlayer(self):
        self.clearWindow()
        tk.Label(self.w, text="Choose your side", **self.label_style).pack(expand=1, fill="both", padx=10, pady=10)
        tk.Button(self.w, text="Play as X (first)", command=lambda: self.startOnePlayerGame(True), **self.button_style).pack(expand=1, fill="both", padx=10, pady=10)
        tk.Button(self.w, text="Play as O (second)", command=lambda: self.startOnePlayerGame(False), **self.button_style).pack(expand=1, fill="both", padx=10, pady=10)
        tk.Button(self.w, text="Return to main menu", command=self.mainMenu, **self.button_style).pack(expand=1, fill="both", padx=10, pady=10)

    # Ξεκινάει την παρτίδα ενάντια του υπολογιστή
    def startOnePlayerGame(self, playerFirst):
        self.createGame()  # Αρχικοποιεί τις μεταβλητές του παιχνιδιού
        self.isOnePlayer = True
        self.playerSymbol = 1 if playerFirst else 2
        self.aiSymbol = 2 if playerFirst else 1
        # Αν παίζει πρώτος ο υπολογιστής τοποθετεί την πρώτη κίνηση αυτού σε ένα τυχαίο κουτί
        if not playerFirst:
            self.aiMove(True)

    # Παίζει τη βέλτιστη κίνηση του υπολογιστή στην παρτίδα ή μια τυχαία κίνηση αν randomMove = True
    def aiMove(self, randomMove = False):
        if randomMove:
            # τοποθετεί την κίνηση του σε ένα τυχαίο κελί
            self.makeMove(random.randint(0, 2), random.randint(0, 2), True)
            return

        # O αλγόριθμος δοκιμάζει όλες τις πιθανές κινήσεις στην τρέχουσα παρτίδα και εν τέλει παίζει την κίνηση
        # που έχει το μεγαλύτερο σκορ (Ο υπολογιστής κερδίζει την παρτίδα ή καταλήγει σε ισοπαλία)
        # Αρχικοποιεί τη μεταβλητή bestScore και bestMove
        bestScore = float('-inf')
        bestMove = None

        # Ο υπολογιστής παίζει προσωρινά την κίνηση του για καθένα από τα άδεια κελιά
        # Έπειτα, ο αλγόριθμος υπολογίζει το σκορ για κάθε μια από αυτές τις κινήσεις και αναιρεί την αντίστοιχη
        # κίνηση απο τον πίνακα gamePos
        # Εν τέλει, αν το σκορ σε αυτή τη βαριάντα (ακολουθία κινήσεων) είναι υψηλότερο από τα σκορ στις προηγούμενες,
        # ενημερώνονται οι μεταβλητές bestScore και bestMove
        for i in range(3):
            for j in range(3):
                if self.gamePos[i][j] == 0:
                    self.gamePos[i][j] = self.aiSymbol
                    score = self.minimax(False)
                    self.gamePos[i][j] = 0
                    if score > bestScore:
                        bestScore = score
                        bestMove = (i, j)

        # αν υπάρχει βέλτιστη κίνηση ο υπολογιστής επιλέγει αυτή χρησιμοποιώντας την ενάντια του χρήστη
        if bestMove:
            self.makeMove(*bestMove, True)

    # Αλγόριθμος για την υπολογισμό του σκορ από την οπτική του υπολογιστή ή του χρήστη (isMaximizing)
    # Θετικά σκορ σημαίνει ότι κερδίζει ο υπολογιστής ενώ αρνητικά σημαίνει ότι κερδίζει ο χρήστης
    def minimax(self, isMaximizing):
        winner = self.checkWinner()
        if winner != 0:
            # Επιστρέφει 1 αν ή βαριάντα (ακολουθία κινήσεων) κερδίζει υπέρ του υπολογιστή ή -1 αν κερδίζει υπέρ του
            # χρήστη αλλιώς, επιστρέφει 0 για αποτέλεσμα ισοπαλίας
            return self.scorePosition(winner)

        if isMaximizing:
            # Όμοια με την aiMove, δοκιμάζει όλα τα πιθανά άδεια κελιά ως την επόμενη κίνηση του υπολογιστή και
            # επιστρέφει το σκορ της καλύτερης κίνησης
            bestScore = float('-inf')
            for i in range(3):
                for j in range(3):
                    if self.gamePos[i][j] == 0:
                        self.gamePos[i][j] = self.aiSymbol
                        score = self.minimax(False)
                        self.gamePos[i][j] = 0
                        bestScore = max(score, bestScore)
            return bestScore
        else:
            # Όμοια με παραπάνω, επιστρέφει το σκορ της καλύτερης κίνησης για τον χρήστη
            bestScore = float('inf')
            for i in range(3):
                for j in range(3):
                    if self.gamePos[i][j] == 0:
                        self.gamePos[i][j] = self.playerSymbol
                        score = self.minimax(True)
                        self.gamePos[i][j] = 0
                        bestScore = min(score, bestScore)
            return bestScore

    # Κομμάτι του αλγορίθμου για την εύρεση της βέλτιστης κίνησης
    # Επιστρέφει 1 αν νικάει ο υπολογιστής και -1 αν νικάει ο χρήστης αλλιώς επιστρέφει 0
    def scorePosition(self, winner):
        if winner == self.aiSymbol:
            return 1
        elif winner == self.playerSymbol:
            return -1
        return 0

    # Κάνει εκκίνηση του παιχνιδιού εναντίων 2 παικτών
    def twoPlayers(self):
        self.createGame()
        self.isOnePlayer = False

    # Μέθοδος που αρχικοποιεί τις τιμές του παιχνιδιού
    def createGame(self):
        # Η σειρά του παίκτη που παίζει τώρα
        #1 -> X
        #2 -> O
        self.move = 1 # παίζει πάντα πρώτο το Χ
        # πίνακας 3x3 που αποθηκεύει τις κινήσεις της παρτίδας
        # 0 - καμία κίνηση
        # 1 - X
        # 2 - O
        self.gamePos = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]
        self.clearWindow()
        # Πίνακας 3x3 με τα κελιά της παρτίδας (της tkinter)
        self.buttons = [[None, None, None], [None, None, None], [None, None, None]]

        # Δημιουργεί τα άδεια κουμπιά από την tkinter
        for i in range(3):
            for j in range(3):
                button = tk.Button(self.w, text=" ", command=lambda i=i, j=j: self.makeMove(i, j), **self.button_style)
                button.grid(row=i, column=j, sticky="nsew", padx=5, pady=5)
                button.config(width=4, height=2)
                self.w.grid_rowconfigure(i, weight=1)
                self.w.grid_columnconfigure(j, weight=1)
                self.buttons[i][j] = button

        # Δημιουργεί μια αόρατη ετικέτα η οποία στην πορεία θα ανακοινώσει το αποτέλεσμα του παιχνιδιού

        self.winner_announcement = tk.Label(self.w, text="", **self.win_label_initial)
        self.winner_announcement.grid(row=3, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)

        # δημιουργεί το κουμπί για την επιστροφή στο κυρίως μενού
        self.return_button = tk.Button(self.w, text="Return to the main menu", command=self.mainMenu, **self.button_style)
        self.return_button.grid(row=4, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)

    # ανακοινώνει τον νικητή της παρτίδας στην ετικέτα που δημιουργήθηκε προηγουμένως
    def announceWinner(self, winner):
        if winner == 1:
            winner_text = "Player X wins!"
        elif winner == 2:
            winner_text = "Player O wins!"
        else:
            winner_text = "It's a draw!"

        # Κάνει την ετικέτα να μην είναι αόρατη
        self.winner_announcement.config(self.win_label_final)
        # Αλλάζει το κείμενο της ετικέτας
        self.winner_announcement.config(text=winner_text)

    # Διαγράφει όλα τα στοιχεία από το παράθυρο της tkinter
    def clearWindow(self):
        for widget in self.w.winfo_children():
            widget.destroy()

    # Κλείνει το πρόγραμμα
    def exit(self):
        self.w.destroy()

# Εκκινεί το παράθυρο της tkinter ώστε να ξεκινήσει το πρόγραμμα
def launchWindow():
    root = tk.Tk()
    TicTacToe(root)
    root.mainloop()

# Καλεί τη μέθοδο launchWindow ώστε να εκκινηθεί το πρόγραμμα
launchWindow()