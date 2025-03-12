from tkinter import *
from tkinter import messagebox
import time

root = Tk()
w=460
h=370
ws=root.winfo_screenwidth()
hs=root.winfo_screenheight()
x=(ws/2)-(w/2)
y=(hs/2)-(h/2)
root.geometry('%dx%d+%d+%d'%(w,h,x,y))

# Sudoku solver class
class SudokuSolver():
    start_time = 0
    def __init__(self):
        self.setZero()
        for i in range(9):
            for j in range(9):
                s[i][j] = int(Sudo_Board[i][j].get())
        if self.isvalid():  
            self.start_time=time.time()      
            self.start_sol(s)
            for line in s:
                if 0 in line:
                    self.solve_sudoku(s, 0, 0)
                    break
            
            for i in range(9):
                for j in range(9):
                   Sudo_Board[i][j].set(s[i][j])
            end_time = time.time()
            run_time = end_time - self.start_time
            Time = round(run_time * 1000) / 1000
            flag = True
            for line in s:
                if 0 in line:
                    flag = False
                    break
            if not flag:
                for row in range(9):
                    for col in range(9):
                        if Sudo_Board[row][col].get() == '0':
                            Sudo_Board[row][col].set('')
                messagebox.showinfo("Error","Invalid Sudoku, Retry")
            else:
                messagebox.showinfo("Success",f"Team CGS, Solved it in {Time} seconds ")
                

        else:
            for row in range(9):
                for col in range(9):
                    if Sudo_Board[row][col].get() == '0':
                        Sudo_Board[row][col].set('')
            messagebox.showinfo("Error","Invalid Sudoku, Retry")

    def setZero(self):
        for i in range(9):
            for j in range(9):
                if Sudo_Board[i][j].get() not in ['1','2','3','4','5','6','7','8','9']:
                    Sudo_Board[i][j].set(0)
                
    def isvalid(self):
        for i in range(9):
            for j in range(9):
                if s[i][j]!=0:
                    if not self.isValid(s[i][j],(i,j)):
                        return False
        return True

    # Check row, column and subgrid(3x3 square) to see if number can be placed in cell          
    def isValid (self, num, pos):
        # Check Row
        for i in range(9):
            if s[pos[0]][i] == num and i!=pos[1]:
                return False
        # Check Column 
        for i in range(9):
            if s[i][pos[1]] == num and i!=pos[0]:
                return False

        #Check Sub Grid
        row = pos[0] // 3 
        column = pos[1] // 3 

        for i in range(row * 3, (row * 3) + 3):
            for j in range(column * 3, (column * 3) + 3):
                if s[i][j] == num and (i,j) != pos:
                    return False 
        return True


    def test_cell(self,s, row, col):
        used = [0]*10
        used[0] = 1
        block_row = row // 3
        block_col = col // 3

        # Row and Column
        for m in range(9):
            used[s[m][col]] = 1;
            used[s[row][m]] = 1;

        # Square
        for m in range(3):
            for n in range(3):
                used[s[m + block_row*3][n + block_col*3]] = 1

        return used

    def start_sol(self,s):
        stuck = False

        while not stuck:
            stuck = True
            # Iterate through the Sudoku puzzle
            for row in range(9):
                for col in range(9):
                    used = self.test_cell(s, row, col)
                    # More than one possibility
                    if used.count(0) != 1:
                        continue

                    for m in range(1, 10):
                        # If current cell is empty and there is only one possibility
                        # then fill in the current cell
                        if s[row][col] == 0 and used[m] == 0:
                            s[row][col] = m
                            stuck = False
                            break

    def solve_sudoku(self,s, row, col):
        
        if row == 8 and col == 8:
            used = self.test_cell(s, row, col)
            if 0 in used:
                s[row][col] = used.index(0)
            return True

        if col == 9:
            row = row+1
            col = 0

        if s[row][col] == 0:
            used = self.test_cell(s, row, col)
            for i in range(1, 10):
                if used[i] == 0:
                    s[row][col] = i
                    if self.solve_sudoku(s, row, col+1):
                        status = True
                        return True

            
            s[row][col] = 0
            status = False
            return False

        return self.solve_sudoku(s, row, col+1)

   
# GUI class
class Interface():
    def __init__(self, window):
        self.window = window
        window.title("Sudoku Solver-Team CGS")
        font = ('Arial', 20)
        color = 'white'

        # Create solve and clear button and link them to Solve and Clear methods
        solve = Button(window, text = 'Solve', command = self.Solve)
        solve.grid(column=3,row=20)
        clear = Button(window, text = 'Clear', command = self.Clear)
        clear.grid(column = 5,row=20)

        # Initialise empty 2D list
        self.board  = []
        for row in range(9):
            self.board += [["","","","","","","","",""]]

        for row in range(9):
            for col in range(9):
                # Change color of cells based on position in grid
                if (row < 3 or row > 5) and (col < 3 or col > 5):
                    color = 'white' 
                elif (row >= 3 and row < 6) and (col >=3 and col < 6):
                    color = 'white'
                else:
                    color = 'yellow'
                
                # Make each cell of grid a entry box 
                self.board[row][col] = Entry(window, width = 3, font = font, bg = color, cursor = 'arrow', borderwidth = 2,justify="center",
                                          highlightcolor = 'yellow', highlightthickness = 0, highlightbackground = 'black', 
                                          textvariable = Sudo_Board[row][col]) 
                self.board[row][col].bind('<FocusOut>', self.gridChecker)
                self.board[row][col].bind('<Motion>', self.BasicgridChecker)                        
                self.board[row][col].grid(row = row, column = col)


    def BasicgridChecker(self, event):
        for row in range(9):
            for col in range(9):
                if Sudo_Board[row][col].get() not in ['1','2','3','4','5','6','7','8','9']:
                    Sudo_Board[row][col].set('')
    
    def gridChecker(self,event):
        loc = self.ExtractNumber(str(event.widget))
        i = (loc-1)%9
        j = (loc-1)//9
        num = Sudo_Board[j][i].get()
        if num == '':
            num='0'
        
        if not self.isValid(num,(j,i)):
            Sudo_Board[j][i].set('')
            messagebox.showinfo("Error","Invalid Sudoku, Retry")

    def ExtractNumber(self,s):
        if len(s)==9:
            return int(s[-2::])
        if len(s)==8:
            return int(s[-1])
        if len(s)==7:
            return 1


    # Check row, column and subgrid(3x3 square) to see if number can be placed in cell          
    def isValid(self,num,pos):
        # Check Row
        for i in range(9):
            if Sudo_Board[pos[0]][i].get() == num and i!=pos[1]:
                return False
        # Check Column 
        for i in range(9):
            if Sudo_Board[i][pos[1]].get() == num and i!=pos[0]:
                return False

        #Check Sub Grid
        row = pos[0] // 3 
        column = pos[1] // 3 

        for i in range(row * 3, (row * 3) + 3):
            for j in range(column * 3, (column * 3) + 3):
                if Sudo_Board[i][j].get() == num and (i,j) != pos:
                    return False 
        return True

    # Call Sudoku solver class
    def Solve(self):
        SudokuSolver()

    # Function to clear board 
    def Clear(self):
        for row in range(9):
            for col in range(9):
                Sudo_Board[row][col].set('')

Sudo_Board = []
s = []
for row in range(9): 
    Sudo_Board += [["","","","","","","","",""]]
    s += [["","","","","","","","",""]]
for row in range(9):
    for col in range(9):
        Sudo_Board[row][col] = StringVar(root)    

# Main Loop
Interface(root)
root.mainloop()