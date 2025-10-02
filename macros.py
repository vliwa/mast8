macro_Names=[]
macro_Expands=[]

#ADD alu:00000001
#mvi 0,0001
#mvi 1,0000
#mv 5,6
macro_Names=macro_Names+["ADD"]
macro_Expands=macro_Expands+[["MVI 0,0b0001", "MVI 1,0b0000", "MV 5,6"]]

#AND alu:00011011
#mvi 0,1011
#mvi 1,0001
#mv 5,6
macro_Names=macro_Names+["AND"]
macro_Expands=macro_Expands+[["MVI 0,0b1011", "MVI 1,0b0001", "MV 5,6"]]
