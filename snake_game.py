import curses
from random import randint
import json

score = {
    "score": []
}

def read_score(filename):
    try:
        # Read the file if it exists
        with open(filename, "r") as score_text:
            score_json = json.loads(score_text)
        
        return score_json["score"]
    
    # Generate a blank score otherwise.
    except:
        return score['score']

def save_score(filename, score):
    '''Save the current game to a file.'''
    # Put file writing code here
    with open(filename, "w") as file:
        score_json = {}
        score_text = json.dumps(score_json)
        file.write(score_text)

# Get score board
read_score("final_Score.json")


# Set up window
curses.initscr()
# y, x
win = curses.newwin(20, 60, 0, 0) 
win.keypad(1)
curses.noecho()
curses.curs_set(0)
win.border(0)
win.nodelay(1)

# Snake and food
snake = [(4, 10), (4,9), (4,8)]
food = (10,20)

# class Snake:
#     def __init__(snake):
#         snake = [(4, 10), (4,9), (4,8)]
        
# class Food:
#     def __init__(food):        
#         food = (10,20)

win.addch(food[0], food[1], '#')

# Game logic
score = 0

ESC = 27
key = curses.KEY_RIGHT

while key != ESC:
    win.addstr(0, 2, "Score " + str(score) + " ")
    
    # Increase speed
    win.timeout(150 - len(snake) // 5 + len(snake) // 10 % 120) 

    prev_key = key
    event = win.getch()
    key = event if event != -1 else prev_key

    if key not in [curses.KEY_LEFT, curses.KEY_RIGHT, curses.KEY_DOWN, curses.KEY_UP, ESC]:
        key = prev_key

    # Calculate next coordinates
    y = snake[0][0]
    x = snake[0][1]
    if key == curses.KEY_DOWN:
        y += 1
    if key == curses.KEY_UP:
        y -= 1
    if key == curses.KEY_LEFT:
        x -= 1
    if key == curses.KEY_RIGHT:
        x += 1
    
    snake.insert(0, (y, x))

    # Check if we hit the borders
    if y == 0: break
    if y == 19: break
    if x == 0: break
    if x == 59: break

    # If snake runs over itself
    if snake[0] in snake[1:]: break

    if snake[0] == food:
        # eat the food
        score += 1
        food = ()
        while food == ():
            food = (randint(1, 18), randint(1, 58))
            if food in snake:
                food = ()
        win.addch(food[0], food[1], '#')
    else:
        # Move snake
        last = snake.pop()
        win.addch(last[0], last[1], " ")

    win.addch(snake[0][0], snake[0][1], '*')


curses.endwin()
print(f"Final score = {score}")

save_score("final_score.json", score)