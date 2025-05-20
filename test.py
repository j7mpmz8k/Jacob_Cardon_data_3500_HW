min_length = 8

character_length = False
has_lowercase = False
has_uppercase = False
has_digit = False
strong_password = False


while strong_password != True:
    password = input("\nEnter a new password: ")
    for i in password:
        if "a" <= i <= "z":
            has_lowercase = True
        if "A" <= i <= "Z":
            has_uppercase = True
        if "0" <= i <= "9":
            has_digit = True
    if len(password) >= min_length:
        character_length = True

    if has_lowercase and has_uppercase and has_digit and character_length:
        print("\nSuccess! Password is strong.\n")
        strong_password = True
    else:
        print("\nPassword is weak. Does not meet following criteria:")
        if not has_lowercase:
            print("\t-Needs lowercase character.")
        if not has_uppercase:
            print("\t-Needs uppercase character.")
        if not has_digit:
            print("\t-Needs at least one number ie. 0-9")
        if not character_length:
            print("\t-Character length must be at least", min_length, "characters.")
        print("Please try again.")