import random

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

word_to_value = dict()

f = open("word_list", "r")
f_common = open("common_words", "r")

common = []
for line in f_common:
  w = line.strip()
  if len(w) == 5:
    common.append(w)


f_out = open("wordle.txt", "w+")

# put all words in a list
potential_words = []
for line in f:
  w = line.strip().lower()


  pts = 0

  if w in common:
    pts += 1000

  dup = dict()
  for letter in range(len(w)):
    
    pts += d[w[letter]]
    if w[letter] in dup:  
      pts -= 10 ** (dup[w[letter]] + 1)
      dup[w[letter]] += 1
    else:
      dup[w[letter]] = 1
  
  word_to_value[w] = pts

  if len(w) == word_size:
    potential_words.append(w)

correct_letters = []

guess_num = 1

hints = dict()
confirmed = []


while len(potential_words) > 1:
  # pick a random word from the list

  if guess_num == 1 and len(potential_words[0]) == 5:
    word = "raise"
  # elif guess_num == 2 and len(potential_words[0]) == 5:
  #   word = "acrid"
  else:
    max_pt = -1
    word = potential_words[0]
    for key in potential_words:
      if word_to_value[key] > max_pt:
        max_pt = word_to_value[key]
        word = key

  print(str(len(potential_words)) + " optimal guess: " + word)
  guess = input("word guessed: ")
  while guess == "/NEW" or guess == "/INVALID" or guess == "/all" or guess.isdigit():
    if guess == "/INVALID":
      potential_words.remove(word)

    elif guess == "/all":
      word_string = ""
      for i in range(len(potential_words)):
        word_string += potential_words[i] + " "
      print(word_string)  

    elif guess.isdigit():
      num_words = int(guess)
      word_string = ""
      for i in range(num_words):
        word_string += potential_words[random.randint(0, len(potential_words) - 1)] + " "
      print(word_string)
    else:
      word = potential_words[random.randint(0, len(potential_words) - 1)]
      print(str(len(potential_words)) + " optimal guess: " + word)
    guess = input("word guessed: ")
  result = input("result: ")

  for i in range(len(result)):
    if result[i] == 'c':
      confirmed.append(i)
      correct_letters.append(guess[i])
      for j in range(len(potential_words) - 1, -1, -1):
        if guess[i] != potential_words[j][i]:
          removed_word = potential_words.pop(j)
          f_out.write("(c " + word + " ) removed word: " + removed_word + " (" + str(guess[i]) + " is not in the " + str(i) + " position of " + removed_word + ")\n")
  
    elif result[i] == 'h':
      if guess[i] not in hints:
        hints[guess[i]] = [i]
      else:
        hints[guess[i]].append(i)

      for j in range(len(potential_words) - 1, -1, -1):
        if guess[i] not in potential_words[j]:
          removed_word = potential_words.pop(j)
          f_out.write("(h " + word + " ) removed word: " + removed_word + " (" + str(guess[i]) + " is not in " + removed_word + ")\n")
        elif guess[i] == potential_words[j][i]:
          removed_word = potential_words.pop(j)
          f_out.write("(h " + word + " ) removed word: " + removed_word + " (" + str(guess[i]) + " is not in " + removed_word + ")\n")


    elif result[i] == 'w':
      for j in range(len(potential_words) - 1, -1, -1):
        if guess[i] in potential_words[j]:

          skip = False
          for k in range(len(guess)):
            if (result[k] == 'c' or guess[k] in correct_letters or result[k] == 'h') and guess[k] == guess[i]:
              skip = True
              continue

          if skip or guess[i] in correct_letters:
            continue
          removed_word = potential_words.pop(j)
          f_out.write("(w " + word + " ) removed word: " + removed_word + " (" + str(guess[i]) + " is in " + removed_word + ")\n")

    f_out.write("\n")

  guess_num += 1

print("it's " + potential_words[0] + "!")