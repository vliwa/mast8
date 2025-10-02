import sys
macro_Names=[]

#JMP LBL
#mv 3,6
#mv 4,7
#mvi 0,lbln0
#mvi 1,lbln1
#mvi 2,lbln2
#mvi 3,lbln3
#mv 1,6
#mv 6,3
#mv 7,4
#mv 0,1
macro_Names=macro_Names+["JMP"]
def macro_Jmp_Pl(macro):
    length=10
    placeholder_List=[]
    i=1
    while i <= length:
        placeholder=f"MCR;{macro};{i-1}"
        placeholder_List=placeholder_List+[placeholder]
        i+=1

    return placeholder_List

def macro_Jmp(macro, labels):
    label_Names=labels[0]
    label_Addresses=labels[1]

    if macro not in label_Names:
        print("Unknown Label "+macro)
        print("Exiting")
        sys.exit(0)

    address=label_Names.index(macro)
    address_Binary=format(int(label_Addresses[address]), '016b')
    mv_0=f"MVI 0,0b{address_Binary[12:16]}"
    mv_1=f"MVI 1,0b{address_Binary[8:12]}"
    mv_2=f"MVI 2,0b{address_Binary[4:8]}"
    mv_3=f"MVI 3,0b{address_Binary[0:4]}"

    return ["MV 3,6"]+["MV 4,7"]+[mv_0]+[mv_1]+[mv_2]+[mv_3]+["MV 1,6"]+["MV 6,3"]+["MV 7,4"]+["MV 0,1"]

#ADD x,a,b
#alu:01000001
#mv 3,a
#mv 4,b
#mvi 0,0001
#mvi 1,0000
#mv 5,6
#mv a,3
#mv b,4
#mv x,5
macro_Names=macro_Names+["ADD"]
def macro_Add_Pl(macro):
    length=8
    placeholder_List=[]
    i=1
    while i <= length:
        placeholder=f"MCR;{macro};{i-1}"
        placeholder_List=placeholder_List+[placeholder]
        i+=1

    return placeholder_List

def macro_Add(macro):
    location_Split=macro.split(",")

    mv_X=f"MV {location_Split[0]},5"
    mv_A=f"MV 3,{location_Split[1]}"
    mv_B=f"MV 4,{location_Split[2]}"
    restore_A=f"MV {location_Split[1]},3"
    restore_B=f"MV {location_Split[2]},4"

    return [mv_A]+[mv_B]+["MVI 0,0b0001", "MVI 1,0b0100", "MV 5,6"]+[restore_A]+[restore_B]+[mv_X]

#AND x,a,b
#alu:01011011
#mv 3,6
#mv 4,7
#mvi 0,1011
#mvi 1,0001
#mv 5,6
#mv a,3
#mv b,4
#mv x,5
macro_Names=macro_Names+["AND"]
def macro_And_Pl(macro):
    length=8
    placeholder_List=[]
    i=1
    while i <= length:
        placeholder=f"MCR;{macro};{i-1}"
        placeholder_List=placeholder_List+[placeholder]
        i+=1

    return placeholder_List

def macro_And(macro):
    location_Split=macro.split(",")

    mv_X=f"MV {location_Split[0]},5"
    mv_A=f"MV 3,{location_Split[1]}"
    mv_B=f"MV 4,{location_Split[2]}"
    restore_A=f"MV {location_Split[1]},3"
    restore_B=f"MV {location_Split[2]},4"

    return [mv_A]+[mv_B]+["MVI 0,0b1011", "MVI 1,0b0101", "MV 5,6"]+[restore_A]+[restore_B]+[mv_X]

def macro_Pl(macro):
    opcode_Split=macro.split()
    match opcode_Split[0].upper():
        case "JMP":
            return macro_Jmp_Pl(opcode_Split[0])
        case "ADD":
            return macro_Add_Pl(opcode_Split[0])
        case "AND":
            return macro_And_Pl(opcode_Split[0])

def macro_Format(macro, labels):
    opcode_Split=macro.split()
    match opcode_Split[0].upper():
        case "JMP":
            return macro_Jmp(opcode_Split[1], labels)
        case "ADD":
            return macro_Add(opcode_Split[1])
        case "AND":
            return macro_And(opcode_Split[1])
