import random
import string

# --- Create variable1 with 100 random letters ---
letters = string.ascii_lowercase  # You can change this to string.ascii_letters for mixed case,
                                 # or string.ascii_uppercase for uppercase only.
variable1_list = [random.choice(letters) for _ in range(10000)]
variable1 = "".join(variable1_list)

# --- Create variable2 by randomizing (shuffling) variable1 ---
# To shuffle, we convert the string to a list of characters, shuffle the list,
# and then join it back into a string.
variable2_list = list(variable1)  # Convert string to list of characters
random.shuffle(variable2_list)    # Shuffle the list in place
variable2 = "".join(variable2_list) # Convert the shuffled list back to a string

# --- Print the variables ---
print(f"Variable 1 (Original Random): {variable1}")
print(f"Variable 2 (Shuffled from V1): {variable2}")

# --- You can also verify they have the same characters, just different order ---
# (This is a bit more advanced, but shows they are anagrams of each other)
from collections import Counter
print(f"\nAre the character counts the same? {Counter(variable1) == Counter(variable2)}")
print(f"Is Variable 1 different from Variable 2? {variable1 != variable2 or len(variable1) == 0}")
# The second check handles the very unlikely case where shuffling results in the same order for short strings,
# or if the string was empty. For 100 characters, it's virtually impossible to shuffle and get the same order.