gallons_total = 0
gallons_trip = 0
miles_total = 0
miles_trip = 0
log_status = 0#neutral flag for message loop

def miles_per_gal():
    return miles_trip/gallons_trip

def total_avg():
    return miles_total/gallons_total

while log_status != -1:    
    gallons_trip = int(input("Enter the gallons used (-1 to end): "))
    log_status = gallons_trip
    if log_status == -1:
        break
    else:
        gallons_total += gallons_trip
        miles_trip = int(input("Enter the miles driven: "))
        miles_total += miles_trip
        print("\nThe miles/gallon for this tank was", miles_per_gal(), "\n")
print("\nThe overall average miles/gallon was", total_avg(),"\n")