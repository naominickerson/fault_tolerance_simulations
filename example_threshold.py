import st

nTrials=100
prange= [0.06,0.07,0.08,0.09,0.1,0.11,0.12,0.13]
srange = [5,7,9]

results={}
for size in srange:
    if size not in results.keys(): results[size]={}
    
    for p in prange:
        if p not in results[size].keys(): results[size][p]=0
        
        for n in range(nTrials):
            output = st.run2D(size,p)
            if output==[[1,1],[1,1]]:
                results[size][p]+=1


col_width =6

row1 = [""]+[str(p) for p in prange]
print "".join(word.ljust(col_width) for word in row1)

for size in srange:
    
    row = [str(size)]+[str(results[size][p]) for p in prange]
    
    print "".join(word.ljust(col_width) for word in row)
