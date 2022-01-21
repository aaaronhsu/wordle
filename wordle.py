import random

word_size = 5

f = open("words_long.txt", "r")
with open("wordle.txt", "r+") as f_clear:
  f_clear.truncate(0)

f_out = open("wordle.txt", "w+")

# put all words in a list
potential_words = []
for line in f:
  w = line.strip()

  if len(w) == word_size:
    potential_words.append(w)

correct_letters = []

guess_num = 1



while len(potential_words) > 1:
  # pick a random word from the list

  if guess_num == 1 and len(potential_words[0]) == 5:
    word = "notes"
  elif guess_num == 2 and len(potential_words[0]) == 5:
    word = "acrid"
  else:
    word = potential_words[random.randint(0, len(potential_words) - 1)]

  print(str(len(potential_words)) + " optimal guess: " + word)
  guess = input("word guessed: ")
  while guess == "/NEW" or guess == "/INVALID" or guess == "/ALL" or guess.isdigit():
    if guess == "/INVALID":
      potential_words.remove(word)

    elif guess == "/ALL":
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
      correct_letters.append(guess[i])
      for j in range(len(potential_words) - 1, -1, -1):
        if guess[i] != potential_words[j][i]:
          removed_word = potential_words.pop(j)
          f_out.write("(c " + word + " ) removed word: " + removed_word + " (" + str(guess[i]) + " is not in the " + str(i) + " position of " + removed_word + ")\n")
  
    elif result[i] == 'h':
      for j in range(len(potential_words) - 1, -1, -1):
        if guess[i] not in potential_words[j]:
          removed_word = potential_words.pop(j)
          f_out.write("(h " + word + " ) removed word: " + removed_word + " (" + str(guess[i]) + " is not in " + removed_word + ")\n")

    elif result[i] == 'w':
      for j in range(len(potential_words) - 1, -1, -1):
        if guess[i] in potential_words[j]:

          skip = False
          for k in range(len(guess)):
            if result[k] == 'c' and guess[k] not in correct_letters and guess[k] == guess[i]:
              skip = True
              continue

          if skip or guess[i] in correct_letters:
            continue
          removed_word = potential_words.pop(j)
          f_out.write("(w " + word + " ) removed word: " + removed_word + " (" + str(guess[i]) + " is in " + removed_word + ")\n")

    f_out.write("\n")

  guess_num += 1
