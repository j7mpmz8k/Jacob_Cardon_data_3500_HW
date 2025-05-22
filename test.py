'''
3.11
Miles per gallon
relies on updating balance each while loop iteration. Uses a break to end loop when sentinal is typed
'''
#initializing balances
gallons_total = 0
gallons_trip = 0
miles_total = 0

#neutral flag for message loop
log_status = 0

#avg calculations setup
def miles_per_gal():
    return miles_trip/gallons_trip
def total_avg():
    if gallons_total == 0:
        return #prevents division by zero due to gallons_total being zero at first iteraton
    return miles_total/gallons_total

#message loop to update gas/miles trip log
while log_status != -1:#sentinal
    gallons_trip = int(input("Enter the gallons used (-1 to end): "))
    log_status = gallons_trip#checking if gallons entered is sentinal
    if log_status == -1:
        break#backs out of the trip log
    #continues trip log since sentinal was not entered
    else:
        gallons_total += gallons_trip#adding gal used in trip to total
        miles_trip = int(input("Enter the miles driven: "))
        miles_total += miles_trip#adding miles used in trip to tal
        print("\nThe miles/gallon for this tank was", miles_per_gal(), "\n")
print("\nThe overall average miles/gallon was", total_avg(),"\n")#exit message w/total avg