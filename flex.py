import random
import numpy as np
from PIL import ImageGrab
from pynput.keyboard import Key, Controller
import time

num_runs = 3000

def enter_word(word):
  keyboard = Controller()
  keyboard.type(word)
  keyboard.press(Key.enter)
  keyboard.release(Key.enter)

def get_screenshot():
  # To capture the screen
  time.sleep(0.03)
  image = ImageGrab.grab(bbox = (783, 226, 1065, 507))
    
  # To save the screenshot
  image.save("img.png")

  # img = Image.open("img.png")
  pixels = np.array(image)

  found = False
  
  last = []

  for i in range(5):
    l = []
    if pixels[i * 70][0][0] == 255:
      if len(last) == 0:
        return "REDO"
      return last

    for j in range(5):
      l.append(pixels[i * 70][j * 70])
    
    last = l
  return last

def determine_result(arr):
  l = ""
  
  for i in range(5):
    if arr[i][0] == 121:
      l += "c"
    elif arr[i][0] == 243:
      l += "h"
    elif arr[i][0] == 164:
      l += "w"
    else:
      l += "?"
      time.sleep(100)

  return l

word_size = 5
    

d = {
  "e": 12.49,
  "t": 9.28,
  "a": 8.04,
  "o": 7.64,
  "i": 7.57,
  "n": 7.23,
  "s": 6.51,
  "r": 6.28,
  "h": 5.05,
  "l": 4.07,
  "d": 3.82,
  "c": 3.37,
  "u": 2.73,
  "m": 2.51,
  "f": 2.40,
  "p": 2.14,
  "g": 1.87,
  "w": 1.68,
  "y": 1.66,
  "b": 1.48,
  "v": 1.05,
  "k": 0.54,
  "x": 0.23,
  "j": 0.16,
  "q": 0.12,
  "z": 0.09
}

f = open("word_list", "r")
f_common = open("common_words", "r")
f_commoner = open("commoner_words", "r")
word_to_value2 = dict()
common = []
for line in f_common:
  w = line.strip()
  if len(w) == 5:
    common.append(w)
commoner = []
for line in f_commoner:
  w = line.strip()
  if len(w) == 5:
    commoner.append(w)

# put all words in a list
raw_potential_words = []
for line in f:
  w = line.strip().lower()
  pts = 0
  if w in common:
    pts += 300
  if w in commoner:
    pts += 1000
  dup = dict()
  for letter in range(len(w)):
    
    pts += d[w[letter]]
    if w[letter] in dup:  
      pts -= 10 ** (dup[w[letter]] + 1)
      dup[w[letter]] += 1
    else:
      dup[w[letter]] = 1
  
  word_to_value2[w] = pts
  if len(w) == word_size:
    raw_potential_words.append(w)

word_to_value = dict(sorted(word_to_value2.items(), key=lambda x: x[1], reverse=True))


final_results = dict()
for i in range(1, 7):
  final_results[i] = 0

final_results[-1] = 0

for i in range(num_runs):

  potential_words = word_to_value.copy()

  correct_letters = []

  guess_num = 1

  hints = dict()
  confirmed = []


  while len(potential_words) > 1:
    # pick a random word from the list

    if guess_num == 1:
      word = "raise"
    else:
      word = next(iter(potential_words))

    print(str(len(potential_words)) + " optimal guess: " + word)

    enter_word(word)
    
    data = get_screenshot()
    if data == "REDO":
      break
    
    result = determine_result(data)
    guess = word

    for i in range(len(result)):
      d2 = potential_words.copy()
      if result[i] == 'c':
        confirmed.append(i)
        correct_letters.append(guess[i])
        for key in potential_words:
          if key[i] != guess[i]:
            del d2[key]
    
      elif result[i] == 'h':
        for key in potential_words:
          if guess[i] not in key or guess[i] == key[i]:
            del d2[key]
        if guess in d2:
          del d2[guess]


      elif result[i] == 'w':
        for key in potential_words:
      
          if guess[i] in key:
            bk = False
            for k in range(5):
              if (result[k] == 'c' or result[k] == 'h') and guess[k] == guess[i]:
                bk = True
                break
            
            if not bk:
              del d2[key]
        
        if guess in d2:
          del d2[guess]

      potential_words = d2

    
    if (len(potential_words) == 1):
      print("it's " + next(iter(potential_words)) + "!")
      print("\n")
      final_results[guess_num] += 1
  
    guess_num += 1

  if (len(potential_words) == 1):
    enter_word(next(iter(potential_words)))

  time.sleep(0.03)
  keyboard = Controller()
  keyboard.press(Key.enter)
  keyboard.release(Key.enter)
  keyboard.press(Key.enter)
  keyboard.release(Key.enter)

print("FINAL RESULTS:")
fail = 0
for key in final_results:
  if (key != -1):
    print(str(key) + " TRIES: " + str(final_results[key]) + " (" + str((100 * final_results[key]) / num_runs) + "%)")
    fail += final_results[key]
  else:
    print("FAILED: " + str(num_runs - fail) + " (" + str((100 * (num_runs - fail)) / num_runs) + "%)")