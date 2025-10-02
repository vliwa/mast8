macro_Names=[]

#ADD alu:01000001
#mv 3,a
#mv 4,b
#mvi 0,0001
#mvi 1,0000
#mv 5,6
macro_Names=macro_Names+["ADD"]
def macro_Add(macro):
    location_Split=macro.split(",")
    mv_A=f"MV 3,{location_Split[0]}"
    mv_B=f"MV 4,{location_Split[1]}"
    return [mv_A]+[mv_B]+["MVI 0,0b0001", "MVI 1,0b0100", "MV 5,6"]

#AND alu:01011011
#mv 3,6
#mv 4,7
#mvi 0,1011
#mvi 1,0001
#mv 5,6
macro_Names=macro_Names+["AND"]
def macro_And(macro):
    location_Split=macro.split(",")
    mv_A=f"MV 3,{location_Split[0]}"
    mv_B=f"MV 4,{location_Split[1]}"
    return [mv_A]+[mv_B]+["MVI 0,0b1011", "MVI 1,0b0101", "MV 5,6"]

def macro_Format(macro):
    opcode_Split=macro.split()
    match opcode_Split[0].upper():
        case "ADD":
            return macro_Add(opcode_Split[1])
        case "AND":
            return macro_And(opcode_Split[1])
