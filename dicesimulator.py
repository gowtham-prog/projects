import random
print ("+--------- Dice Simulator -----------+")
print("Enter Y to roll again , N to exit")
opt = "y"
while(opt=="Y"or "y"):
    
    num =random.randint(1,6)

    if num==1:
        print("[_______]")
        print("[___0___]")
        print("[_______]")
    elif num==2:
        print("[_______]")
        print("[_0___0_]")
        print("[_______]")
    elif num==3:
        print("[___0___]")
        print("[___0___]")
        print("[___0___]")

    elif num==4:   
        print("[_0___0_]")
        print("[_______]")
        print("[_0___0_]")

    elif num==5:
        print("[_0___0_]")
        print("[___0___]")
        print("[_0___0_]")
    elif num==6:
        print("[_0___0_]")
        print("[_0___0_]")
        print("[_0___0_]")
    opt= input()