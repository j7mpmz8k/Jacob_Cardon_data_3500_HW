
num = int(input("\nPlease enter a 5 digit number: "))
if num < 10000 or num > 99999:
    print("\nError: That is not a 5 digit number.\n")
else:
    last_num = num % 10
    rev_num = last_num
    excluding_last_num = num
    #print("last_num:", last_num, "\texcluding_last_num:", excluding_last_num)

    for i in range(len(str(num))-1):
        excluding_last_num = excluding_last_num // 10
        last_num = excluding_last_num % 10
        rev_num = rev_num * 10 + last_num
    if num == rev_num:
        print("\nPalindrome!\n")
    else:
        print("\nNot a palindrome.\n")