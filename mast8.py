import sys
from macros import macro_Names, macro_Format, macro_Pl

def normal_Parse(ins_String):
    match ins_String[0].upper():
        case "MV":
            opcode="00"
        case "MVC":
            opcode="01"
        case "MVZ":
            opcode="10"

    location_Split=ins_String[1].split(",")

    if int(location_Split[0])>7 or int(location_Split[1])>7:
        return "invalid"

    destination=format(int(location_Split[0]), '03b')
    source=format(int(location_Split[1]), '03b')
    locations=destination+source

    instruction_Binary=opcode+locations
    instruction=format(int(instruction_Binary, 2), '02x')
    if verbose: print(instruction)

    return instruction

def imm_Parse(ins_String):
    nibble_Split=ins_String[1].split(",")

    if int(nibble_Split[0])>3:
        return "invalid"

    nibble=format(int(nibble_Split[0]), '02b')

    match nibble_Split[1]:
        case c if c.startswith('0b'):
            data_decimal=int(nibble_Split[1][2:], 2)
            data=format(data_decimal, '04b')
        case c if c.startswith('0x'):
            data_decimal=int(nibble_Split[1][2:], 16)
            data=format(data_decimal, '04b')
        case _:
            data=format(int(nibble_Split[1]), '04b')

    instruction_Binary="11"+nibble+data
    instruction=format(int(instruction_Binary, 2), '02x')
    if verbose: print(instruction)

    return instruction

def label_Parse(label_String):
    return label_String[0]

def strip_Comments(asm):
    mcode_Lines=[]
    i=0
    while i < len(asm):
        if asm[i].startswith('#'):
            if verbose: print("comment")
        else:
            mcode_Lines=mcode_Lines+[asm[i]]
        i+=1

    return mcode_Lines

def ins_Macros_Pl(asm):
    mcode_Lines=asm
    i=0
    while i < len(asm):
        opcode_Split=asm[i].split()
        if opcode_Split[0].upper() in macro_Names:
            macro_Expand=macro_Pl(asm[i])
            if macro_Expand==["invalid"]:
                print("Invalid macro instruction at line "+str((i+1)))
                print("Exiting")
                sys.exit(0)
            mcode_Lines[i:i+1]=macro_Expand
        i+=1
    if verbose: print(mcode_Lines)

    return mcode_Lines

def ins_Macros(asm, labels):
    mcode_Lines=asm
    i=0
    while i < len(asm):
        opcode_Split=asm[i].split()
        if opcode_Split[0].upper() in macro_Names:
            macro_Expand=macro_Format(asm[i], labels)
            mcode_Lines[i:i+1]=macro_Expand
        i+=1
    if verbose: print(mcode_Lines)

    return mcode_Lines

def ins_Sort(asm):
    def sort(ins_List):
        if verbose: print(ins_List)
        opcode_Split=ins_List.split()

        match opcode_Split[0].upper():
            case "MV":
                if verbose: print("mv instruction")
                return ins_List
            case "MVC":
                if verbose: print("mvc instruction")
                return ins_List
            case "MVZ":
                if verbose: print("mvi instruction")
                return ins_List
            case "MVI":
                if verbose: print("mvi instruction")
                return ins_List
            case c if c in macro_Names:
                if verbose: print("macro instruction")
                return ins_List
            case c if c.startswith(':'):
                if verbose: print("label")
                return ins_List
            case _:
                if verbose: print("invalid instruction "+opcode_Split[0])
                return "invalid"

    mcode_Lines=[]
    i=0
    while i < len(asm):
        mcode_Lines=mcode_Lines+[sort(asm[i])]
        i+=1
    if verbose: print(mcode_Lines)

    return mcode_Lines

def ins_Decode(asm):
    def decode(ins_List):
        if verbose: print(ins_List)
        opcode_Split=ins_List.split()

        match opcode_Split[0].upper():
            case "MV":
                if verbose: print("mv instruction")
                return normal_Parse(opcode_Split)
            case "MVC":
                if verbose: print("mvc instruction")
                return normal_Parse(opcode_Split)
            case "MVZ":
                if verbose: print("mvz instruction")
                return normal_Parse(opcode_Split)
            case "MVI":
                if verbose: print("mvi instruction")
                return imm_Parse(opcode_Split)
            case c if c.startswith(':'):
                if verbose: print("label")
                return label_Parse(opcode_Split)
            case _:
                if verbose: print("invalid instruction "+opcode_Split[0])
                return "invalid"

    mcode_Lines=[]
    i=0
    while i < len(asm):
        mcode_Lines=mcode_Lines+[decode(asm[i])]
        i+=1
    if verbose: print(mcode_Lines)

    return mcode_Lines

def strip_Labels(mcode_Lines):
    mcode_Output=[]
    i=0
    while i < len(mcode_Lines):
        match mcode_Lines[i]:
            case c if c.startswith(':'):
                if verbose: print("label removed")
            case _:
                mcode_Output=mcode_Output+[mcode_Lines[i]]
                if verbose: print("instruction '"+mcode_Lines[i]+"'")
        i+=1
    if verbose: print(mcode_Output)

    return mcode_Output

def label_Addressing(mcode_Lines):
    label_Names=[]
    label_Addresses=[]
    i=0
    addr=0
    while i < len(mcode_Lines):
        match mcode_Lines[i]:
            case c if c.startswith(':'):
                label=mcode_Lines[i].strip(':')
                label_Names=label_Names+[label]
                label_Addresses=label_Addresses+[str(addr)]
                if verbose: print("label addressed")
            case _:
                addr+=1
        i+=1

    return label_Names, label_Addresses

def invalid_Check(mcode_Lines):
    i=0
    while i < len(mcode_Lines):
        if mcode_Lines[i]=="invalid":
            print("Invalid instruction at line "+str((i+1)))
            print("Exiting")
            sys.exit(0)
        i+=1
    return

def logisim_Formatting(asm, output_Name):
    logisim=["v3.0 hex words addressed\n"]

    mcodes=asm
    i=len(asm)
    while i<65536:
        mcodes=mcodes+['00']
        if verbose: print(len(mcodes))
        i+=1

    i=0
    while i<65536:
        address=format(i, '04x')

        data_Line=address+":"
        x=i
        while x<i+16:
            data_Line=data_Line+" "+str(mcodes[x])
            x+=1

        logisim=logisim+[data_Line+"\n"]
        i+=16

    output_File=open(output_Name, "w")
    output_File.writelines(logisim)

    print("Output to: "+output_Name)
    return

input_File="input"
output_File="output"
output_Format=""
verbose=False
i=1
while i<len(sys.argv):
    match sys.argv[i]:
        case c if c.startswith('i='):
            input_File=(sys.argv[i].strip('"'))[2:]
        case c if c.startswith('o='):
            output_File=(sys.argv[i].strip('"'))[2:]
        case "-l":
            output_Format="logisim"
        case "-v":
            verbose=True
        case _:
            print("Unknown Input "+sys.argv[i])
    i+=1

asm_File=open(input_File, "r")
asm_Lines=asm_File.readlines()
print("OPENED "+input_File)
print("FILE INPUT")
if verbose: print(asm_Lines)

print("STRIP WHITESPACE")
asm_Lines_Strip=[ins.strip() for ins in asm_Lines]
if verbose: print(asm_Lines_Strip)

print("STRIP COMMENTS")
mcode_Ins=strip_Comments(asm_Lines_Strip)
if verbose: print(mcode_Ins)

print("INSTRUCTION VERIFYING")
mcode_Lines=ins_Sort(mcode_Ins)
mcode_Lines_Pass2=mcode_Lines[:]

print("INVALID INSTRUCTION CHECK")
invalid_Check(mcode_Lines)

print("REPLACE MACROS WITH PLACEHOLDERS")
mcode_Expanded=ins_Macros_Pl(mcode_Lines)

print("LABEL ADDRESSING")
labels=label_Addressing(mcode_Expanded)
if verbose: print(labels)

print("REPLACE MACROS WITH ACTUAL")
mcode_Macros=ins_Macros(mcode_Lines_Pass2, labels)

print("INSTRUCTION DECODING")
mcode_Decoded=ins_Decode(mcode_Macros)

print("STRIP LABELS")
mcode_Output=strip_Labels(mcode_Decoded)

match output_Format:
    case "logisim":
        print("Logisim Output")
        logisim_Formatting(mcode_Output, output_File)
    case "intel":
        print("Intel Output")
    case _:
        print("No Output Format Selected")
