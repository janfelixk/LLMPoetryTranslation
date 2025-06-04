# calculate irregularities (Experiment 2)

# Approach: store the best irregularity value found so far and the corresponding interpretations (i.e., the building
# blocks), sorted by length
# go through the possible lines and the ways metres of this length can be built and add new (better) interpretations

found = dict() # dictionary of dictionaries: {key: length, value: {key: combination, value: elements}
found[1] = {"0.8":[["0.8"]],"1.0":[["1.0"]]} # initialize with the two basic elements

max_length = 13
for l in range(max_length+1):
    if l in [0, 1]: # there are no metres of length 0, and 1 is already given
        continue

    found[l] = dict()

    # for a metre of n syllables, the first of two components can have any length from 1 to l-1, while the second
    # has to "fill up" the full number of n syllables
    for i in range(l-1):
        best_i = found[i+1]
        best_l_minus_i = found[l-i-1]
        for k1 in best_i.keys(): # go through all possible first components
            for k2 in best_l_minus_i.keys(): # go through all possible second components
                for a in best_i[k1]: # go through all possible interpretations of the first component
                    for b in best_l_minus_i[k2]: # go through all possible interpretations of the second component
                        # if the new metre is not represented yet or all prior representations have a higher complexity,
                        # make the new interpretation the only accepted
                        if k1+" "+k2 not in found[l].keys() or len(list(set(a).union(set(b))))+1 < len(found[l][k1+" "+k2][0]):
                            found[l][k1+" "+k2] = [list(set(a).union(set(b)))+[k1+" "+k2]]
                        # if the metre is already represented with the same complexity, add the new interpretation
                        # as an alternative
                        elif len(list(set(a).union(set(b))))+1 == len(found[l][k1+" "+k2][0]):
                            found[l][k1+" "+k2].append(list(set(a).union(set(b)))+[k1+" "+k2])

outfile = open("metrical irregularities.txt","a")
for i in range(max_length-1):
    for metre in found[i+1]:
        for interpretation in found[i+1][metre]:
            components = [c for c in interpretation if c not in ["0.8","1.0"]] # the basic elements are ignored
            outfile.write(metre+"\t"+str(len(interpretation))+"\n") # write to file: metre and complexity (i.e. length of list of necessary "building blocks")
outfile.close()