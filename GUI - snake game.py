#snake game
from tkinter import*
import random

#constants - although there are no constants in python, the values are likely to be changed less than usual
GAME_WIDTH = 500 #to create a perfect square
GAME_HEIGHT = 500 #to create a perfect square
SPEED = 120 #the snakes velocity, the lower the faster
SPACE_SIZE = 25 #how large the canvas items/icons are 
BODY_PARTS = 10 #number of body parts the snakes would have at the start
SNAKE_COLOR = "yellow"
FOOD_COLOR = "red"
BACKGROUND_COLOR = "black" #or #0000000

class Snake:
    def __init__(self): #creates a snake object 
        self.body_size = BODY_PARTS #snake has 3 body parts made of sqaures at the start
        self.coordinates = []  #coordinates define the snake's body placement on screen
        self.squares = []   #squares make up the snakes body

        #creating a list of coordinates for each snake body part
        for i in range(0, BODY_PARTS): 
            self.coordinates.append([0, 0]) #places each snake body part at the top left corner of the window at the start of the game
        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake") 
        #                                coordinates, width, height, color and tag (for easy reference to delete)
            self.squares.append(square) #appends more squares to the intial square created

class Food: #creates a food class object for the snake
    def __init__(self): 
        x = random.randint(0, (GAME_WIDTH/SPACE_SIZE)-1) * SPACE_SIZE #dervies 14 random coordinates on the x axis between (0 and the game_width/space_size = 14) for placing the snake food on the canavas
        #game_width/space_size helps us determine how many places (determining how many times) on the canvas we can randomly place the snake food on the x-axis and multiplying by
        #the spaces size converts the number of places (14) into pixels
        y = random.randint(0, (GAME_HEIGHT/SPACE_SIZE)-1) * SPACE_SIZE #dervies 14 random coordinates on the y axis between (0 and game_height/space_size) for placing the snake food on the canvas
        self.coordinates = [x, y] #sets the snake food coordinates to the randomly generated ones
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food") #creates an oval snake food according the coordinates, widith, height and color agruments

def next_turn(snake, food): 
    
    x, y = snake.coordinates[0] #takes the snake's head coordinates 
    if direction == 'up':
        y -= SPACE_SIZE #moves the snakes head one space up
    elif direction == 'down':
        y += SPACE_SIZE #moves the snakes head one space down
    elif direction == 'left':
        x -= SPACE_SIZE #moves snakes head one space to the left
    elif direction == 'right':
        x += SPACE_SIZE #moves snakes head one space to the right
    
    #updating coordinates for the head of the snake
    snake.coordinates.insert(0, (x, y)) #updates/places the head of the snake (index 0) on x and y coordinates after moving in either direction
    #                       index 0 is the head of the snake 
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR) #creates new squares for the snake's body
    snake.squares.insert(0, square) #updates list of squares (snake's body parts) by inserting at index 0, a new square
    
    #adding a score to be returned everytime time the snake swallows food
    if x == food.coordinates[0] and y == food.coordinates[1]: #if the x coordinates for the head of the snake equals the food objects x (index 0) coordinates and the y
        #coordinates for the head of the snake equals the food object's y coordinates at (index 1) - that is they are overlapping
        global score 
        score += 1 #increase the score by one everytime there is an overlap (that is the snake head swallows the food object)
        score_label.config(text= "Score : {}".format(score)) #set the score label to reflect the increase after each swallow

        canvas.delete("food") #delete the food from the canavas after each swallow
        food = Food() #and create a new one at random x and y coordinates on the canvas
    else:
    #delete the last square(tail) of the snake off the coordinates, canvas and snake when the snake swallows nothing
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]
    
    if check_collisions(snake): #stops the game by calling the game over function whenever the snake collides with anything except the food
        game_over()

    else:
        window.after(SPEED, next_turn, snake, food) #updates the window after each iteration by the speed (representing time), next_turn function, snake and food

def change_direction(new_direction):
    global direction  

    if new_direction == 'left': #if the new direction is left (as described by the event in the window bind function) and not right, then replace direction with the new direction
        if direction != 'right': #so the snake head doesn't do a 180 degree turn
            direction = new_direction

    elif new_direction == 'right': #if the new direction is right (as described by the event in the window bind function) and not right, then replace direction with the new direction
        if direction != 'left':
            direction = new_direction

    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction

    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction

def check_collisions(snake): #fuction to retain snake within the canvas borders 
    x, y = snake.coordinates[0] #assigns the snakes' head coordinates to variable x and y

    if x < 0 or x >= GAME_WIDTH: #if x is greater than or equal to the size of the game width or less than 0
        return True #returns True - yes there is a collision. you can print("game over") to test if it works
    
    elif y < 0 or y >= GAME_HEIGHT: #if y is greater than or equal to the size of game height or less than 0
        return True #returns True - yes there is a collision
    
    #checking collisions where the snake head touches either its tail or part of its body
    for body_parts in snake.coordinates[1:]: #[1:] devrives the coordinates of other squares after the snake's head (that is its other body parts)
       if x == body_parts[0] and y == body_parts[1]: #if the x axis coordinates of the snake's head is equal the x axis coordinates of a body part from the snake's head down
    #       #and if the y axis coordinates of the snake's head is equal to the y axis coordinates of every other body part from the snake's head down
           return True #there is a collision 
       
    return False #no collisions
               
def game_over():
    canvas.delete(ALL) #deletes all widgets on the canvas
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2, font=('Consolas', 40), text="GAME OVER!", fill="red", tag="gameover") #centers the "game over" text
    #by diving the canvas.winfo_width()/2 and canvas.winfo_height()/2 after a collision 

window = Tk() #instantiates the instance of a window
window.title('Snake Game')
window.resizable(False, False) #prevents the window from being adjusted

score = 0 
direction = 'right' 

score_label = Label(window, text="Score: {}".format(score), font=('Consolas', 20))
score_label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update() #updates the window so it renders

#to centralize the canvas on the window using dimension 
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

#binding buttons to keys to control snake direction
window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

#creating objects from the class
snake = Snake()
food = Food()

next_turn(snake, food)

window.mainloop() #keeps window display on screen
