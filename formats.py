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

def output_Format(mcode, output_Type, verbose):
    output_List=["no output"]
    match output_Type:
        case "logisim":
            print("Logisim Output")
            output_List=logisim_Formatting(mcode, output_Type, verbose)
        case "intel":
            print("Intel Output")
        case _:
            print("No Output Format Selected")

    return output_List
