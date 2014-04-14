

def load(filename):

    f = open(filename,"r")
    data = f.readlines()
    f.close()
    results_3 = {}
    results_4 = {}
    for x in data: 
        
        if "#" in x: 
            if "##" in x: continue 
            size = int(x.split()[0][-1])

        else: 
            if x.split() ==[]: continue
            if size == 3: 
                results_3[float(x.split()[0])] = [float(y) for y in x.split()[1:]]
            if size == 4: 
                results_4[float(x.split()[0])] = [float(y) for y in x.split()[1:]]
    
    return results_3, results_4



