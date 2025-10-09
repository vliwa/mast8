def logisim_Formatting(asm, output_Name, verbose):
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

    return logisim

def intel_Formatting(asm, output_Name, verbose):
    intel=[]

    mcodes=asm
    i=len(asm)
    while i%16!=0:
        mcodes=mcodes+['00']
        i+=1
    if verbose: print(mcodes)
    i=0
    address=0
    while i<len(mcodes):
        data_String=""
        checksum_Sum=0
        x=i
        while x<i+16:
            data_String=data_String+mcodes[x]
            checksum_Sum=checksum_Sum+int(mcodes[x], 16)
            x+=1
        checksum_Sum=checksum_Sum+0x10+address
        checksum_LSB=format(checksum_Sum, '08b')[-8:]
        if verbose: print("checksum "+checksum_LSB)
        flip=checksum_LSB.replace('0', 'o')
        flip=flip.replace('1', '0')
        flip=flip.replace('o', '1')
        if verbose: print("flip "+flip)
        twos_Comp=int(flip, 2)+1
        if verbose: print("twos "+format(twos_Comp, '08b'))
        twos_Comp=format(int(twos_Comp), '02x')
        if verbose: print("twos hex "+twos_Comp)
        data_Line=":10"+f"{format(int(address), '04x')}"+"00"+data_String+twos_Comp
        if verbose: print(data_Line)
        intel=intel+[data_Line+"\n"]
        address=address+16
        i+=16

    intel=intel+[":00000001FF"+"\n"]

    return intel

def output_Format(mcode, output_Type, verbose):
    output_List=["no output"]
    match output_Type:
        case "logisim":
            print("Logisim Output")
            output_List=logisim_Formatting(mcode, output_Type, verbose)
        case "intel":
            print("Intel Output")
            output_List=intel_Formatting(mcode, output_Type, verbose)
        case _:
            print("No Output Format Selected")

    return output_List
