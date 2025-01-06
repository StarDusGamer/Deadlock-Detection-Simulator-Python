import argparse
import math
import copy


#This function is the setup for user input
def parseArguments():
    parser = argparse.ArgumentParser(description="Deadlock Detection Simulator")

    #The input file we are pulling from
    parser.add_argument(
        "input_file",
        help=
            "The input text file contains contents for a Deadlock Detection Simulation")

    args = parser.parse_args()

    return args

def main():
    args = parseArguments()

    #Splitting the data by newlines
    with open(args.input_file, 'r') as file:
        data = file.read().split("\n")

    #If there is spaces in the data, remove them
    data = [s.replace(" ", "") for s in data]

    #Splicing the data into variables
    numProcess = int(data[0])
    numResources = int(data[1])
    avaAllocation = data[2]

    #Data type casting from chracters to integers
    avaAllocation = [int(char) for char in avaAllocation]
    allocation = data[3:numProcess+3]
    allocation = [[int(char) for char in item] for item in allocation]
    request = data[len(allocation)+3:len(data)-1]
    request = [[int(char) for char in item] for item in request]
    print(request)

    deadlockInfo = isDeadlock(allocation,avaAllocation,request)
    if deadlockInfo[0]:
        print(f"Given File contains a deadlock at {deadlockInfo[1]}")
    else:
        print("There is no deadlock in the file, it is in a safe state")

    return 0


def isDeadlock(allocation,available,need):
    complete = False
    deadlock = 0
    previousLen = 0
    sameLen = 0
    check = need[:]

    #Looping to test until all process are complete
    while not complete:

        #Iterate through every process
        for i in range(len(need)):
            if len(check) == 0:
                complete = True
                break

            #If no processes have been completed, count up
            if previousLen == len(check):
                sameLen += 1
            skip = False

            #Skip over complete processes
            if need[i] not in check:
                continue
            print("______Checking_______")
            print(f"Allocation: {allocation[i]} | Need: {need[i]}")
            print(f"Available: {available}")

            #Process cannot be completed right now, come back later
            for j in range(0,len(need[i])):
                if (need[i])[j] > available[j]:
                    skip = True
                    continue
            if skip:
                print("Not Allocated... Continuing next process...")
                previousLen = len(check)
                continue

            #If process successful, add together available and allocation
            available = [a + b for a, b in zip(available, allocation[i])]
            print("Successfully Allocated")

            #Removing successful processes from the duplicate list
            check.remove(need[i])

        # Checks to see if there is a loop
        if sameLen >= len(need) * 2:
            return True,check
        if complete:
            break
    return False,check


main()
