import sys
from macros import macro_Names, macro_Expands

def normal_Parse(ins_String):
    match ins_String[0]:
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
    return instruction

def imm_Parse(ins_String):
    nibble_Split=ins_String[1].split(",")

    if int(nibble_Split[0])>3:
        return "invalid"

    nibble=format(int(nibble_Split[0]), '02b')

    match nibble_Split[1]:
        case c if c.startswith('0b'):
            data_decimal=int(nibble_Split[1][2:], 2)
            print(data_decimal)
            data=format(data_decimal, '04b')
        case c if c.startswith('0x'):
            data_decimal=int(nibble_Split[1][2:], 16)
            data=format(data_decimal, '04b')
        case _:
            data=format(int(nibble_Split[1]), '04b')

    instruction_Binary="11"+nibble+data
    instruction=format(int(instruction_Binary, 2), '02x')
    return instruction

def label_Parse(label_String):
    return label_String[0]

def ins_Macros(asm):
    mcode_Lines=asm
    i=0
    while i < len(asm):
        if asm[i] in macro_Names:
            macro_Index=macro_Names.index(asm[i])
            macro_Expand=macro_Expands[macro_Index]
            mcode_Lines[i:i + 1] = macro_Expand
        i+=1
    print(mcode_Lines)

    return mcode_Lines

def ins_Sort(asm):
    print(asm)
    opcode_Split=asm.split()
    print(opcode_Split)

    match opcode_Split[0]:
        case "MV":
            print("normal instruction")
            return asm
        case "MVC":
            print("normal instruction")
            return asm
        case "MVZ":
            print("normal instruction")
            return asm
        case "MVI":
            print("immediate instruction")
            return asm
        case c if c.startswith(':'):
            print("label")
            return asm
        case c if c.startswith('#'):
            print("comment")
            return "comment"
        case _:
            print("invalid instruction "+opcode_Split[0])
            return "invalid"
    return

def ins_Decode(asm):
    print(asm)
    opcode_Split=asm.split()
    print(opcode_Split)

    match opcode_Split[0]:
        case "MV":
            print("normal instruction")
            return normal_Parse(opcode_Split)
        case "MVC":
            print("normal instruction")
            return normal_Parse(opcode_Split)
        case "MVZ":
            print("normal instruction")
            return normal_Parse(opcode_Split)
        case "MVI":
            print("immediate instruction")
            return imm_Parse(opcode_Split)
        case c if c.startswith(':'):
            print("label")
            return label_Parse(opcode_Split)
        case c if c.startswith('#'):
            print("comment")
            return "comment"
        case _:
            print("invalid instruction "+opcode_Split[0])
            return "invalid"
    return

def logisim_Formatting(asm, output_Name):
    logisim=["v3.0 hex words addressed\n"]

    mcodes=asm
    i=len(asm)
    while i<65536:
        mcodes=mcodes+['00']
        print(len(mcodes))
        i+=1

    i=0
    while i<65536:
        address=format(i, '04x')

        data_Line=address+":"
        x=i
        while x<i+16:
            data_Line=data_Line+" "+str(mcodes[x])
            x+=1

        #print(data_Line)
        logisim=logisim+[data_Line+"\n"]
        i+=16

    output_File=open(output_Name, "w")
    output_File.writelines(logisim)

    print("Output to: "+output_Name)
    return

input_File="input"
output_File="output"
output_Format=""
i=1
while i<len(sys.argv):
    match sys.argv[i]:
        case c if c.startswith('i='):
            input_File=sys.argv[i].lstrip('i=')
        case c if c.startswith('o='):
            output_File=sys.argv[i].lstrip('o=')
        case c if c.startswith('-'):
            output_Format=sys.argv[i].lstrip('-')
        case _:
            print("Unknown Input")
    i+=1

asm_File=open(input_File, "r")
asm_Lines=asm_File.readlines()
print("OPENED "+input_File)
print("FILE INPUT")
print(asm_Lines)

asm_Lines_Strip=[ins.strip() for ins in asm_Lines]
print("STRIPPED FILE")
print(asm_Lines_Strip)

print("REPLACE MACROS")
asm_Lines_Strip=ins_Macros(asm_Lines_Strip)

print("INSTRUCTION VERIFYING")
mcode_Lines=[]
i=0
while i < len(asm_Lines_Strip):
    mcode_Lines=mcode_Lines+[ins_Sort(asm_Lines_Strip[i])]
    print(mcode_Lines[i])
    i+=1
print(mcode_Lines)

print("INVALID INSTRUCTION CHECK")
i=0
while i < len(mcode_Lines):
    if mcode_Lines[i]=="invalid":
        print("Invalid instruction at line "+str((i+1)))
        print("Exiting")
        sys.exit(0)
    i+=1

print("LABEL ADDRESSING")
label_Names=[]
label_Addresses=[]
i=0
addr=0
while i < len(mcode_Lines):
    match mcode_Lines[i]:
        case "comment":
            print("comment ignored")
        case c if c.startswith(':'):
            label=mcode_Lines[i].strip(':')
            label_Names=label_Names+[label]
            label_Addresses=label_Addresses+[str(addr)]
            print("label addressed")
        case _:
            addr+=1
    i+=1
print(label_Names)
print(label_Addresses)

print("INSTRUCTION DECODING")
mcode_Lines=[]
i=0
while i < len(asm_Lines_Strip):
    mcode_Lines=mcode_Lines+[ins_Decode(asm_Lines_Strip[i])]
    print(mcode_Lines[i])
    i+=1
print(mcode_Lines)

print("INSTRUCTION ADDRESSING")
ins_Addressed=[]
i=0
while i < len(mcode_Lines):
    match mcode_Lines[i]:
        case "comment":
            print("comment ignored")
        case c if c.startswith(':'):
            print("label ignored")
        case _:
            ins_Addressed=ins_Addressed+[mcode_Lines[i]]
            print("instruction addressed "+mcode_Lines[i])
    i+=1
print(ins_Addressed)

match output_Format:
    case "l":
        print("Logisim Output")
        logisim_Formatting(ins_Addressed, output_File)
    case "i":
        print("Intel Output")
    case _:
        print("No Output Format Selected")
