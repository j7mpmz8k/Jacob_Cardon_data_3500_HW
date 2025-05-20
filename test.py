#additional challenge 1
starting_balance = float(200)
deposit = float(0)
withdraw = float(0)
current_balance = (starting_balance+deposit-withdraw)
atm_status = -1

while atm_status != 4:
    print("Welcome to the python ATM. What would you like to do?")
    print("\t1 check balance")
    print("\t2 deposit money")
    print("\t3 withdraw money")
    print("\t4 quit")
    atm_status = int(input("Enter the number for your selection: "))
    if atm_status != 1 or 2 or 3 or 4:
        print("\nERROR! Please enter 1, 2, 3, or 4\n")
    elif atm_status == 1:
        current_balance = (starting_balance+deposit-withdraw)
        print("\nYour current balance is:", "$"+str(current_balance), "\n")
    elif atm_status == 2:
        deposit += float(input("Please enter how much $$ you want to deposit: "))
        print("\nDeposit success!\n")
    elif atm_status == 3:
        withdraw += float(input("Please enter how much $$ you want to withdraw: "))
        print("\nWithdraw success!\n")
print("\nThank you for using the Python ATM!\n")