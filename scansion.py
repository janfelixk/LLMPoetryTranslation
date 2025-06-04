# predict best metres (Experiment 2)
# corpus used for the testing: see https://github.com/tnhaider/metrical-tagging-in-the-wild/tree/main/data/German/SmallGold/tei_corpus

from metrics import get_stresses
from metrics import edit_distance_alignment

def infer_metre(stresses, candidates, alpha=0.5, beta=0.5):

    # store the best predicted metre and the associated irregularity and cost for each line
    metre = []
    irregularities = []
    value = 0

    for l in stresses:
        min_value = 1000
        min_metre = None
        min_irregularity = None
        # go through all candidate metres to get the best fitting for each line
        for c in candidates:
            # ignore cases where the irregularity alone is already higher
            if alpha*(c[1]) > min_value:
                continue

            cand = c[0]

            # adjust min_value, min_metre, min_irregularity if a better alternative is found
            if edit_distance_alignment(l, cand)[1] + alpha*(c[1]) < min_value:
                min_value = edit_distance_alignment(l, cand)[1] + alpha*(c[1])
                min_metre = c[0]
                min_irregularity = alpha*(c[1])
        metre.append(min_metre)
        irregularities.append(min_irregularity)
        value += min_value

    # try to replace line metres
    def refining(metre, irregularities, value, beta=beta):
        metre = [[metre[i], irregularities[i]] for i in range(len(metre))] # list of candidates for replacement
        lines = [metre[i] for i in range(len(metre)) if metre[i] not in metre[:i]] # list of all unique line metres
        value += len(lines) * beta # add beta * number of unique line metres to the overall cost
        vv = value # the best cost found in this iteration so far
        mm = metre # the best metre (with replaced lines) found in this iteration so far
        while True:
            # go through all pairs of line metres and try to replace one by the other
            for a in lines:
                for b in lines:
                    if a == b:
                        continue
                    ac = a[0]
                    bc = b[0]

                    # adjust the cost by adding the metrical distance associated with the replacement metre, and
                    # subtracting the metrical distance associated with the replaced metre and beta
                    v = value+sum([edit_distance_alignment(stresses[i],bc)[1]+b[1] for i in range(len(metre)) if
                            metre[i]==a])-beta-sum([edit_distance_alignment(stresses[i],ac)[1]+a[1] for i in
                                             range(len(metre)) if metre[i]==a])
                    if v < vv:
                        mm = [b if l==a else l for l in metre]
                        vv = v
            # once all pairs are tested, adjust the overall metre for the best replacement found
            if vv < value:
                metre = mm
                value = vv
                lines = [metre[i] for i in range(len(metre)) if metre[i] not in metre[:i]]
            else:
                break
        return [e[0] for e in metre], value

    return refining(metre, irregularities, value, beta=beta)

if __name__ == "__main__":

    infile_name = "POEMS.txt" # the name of the file with the poems to be analysed
    irregularities_name = "metrical irregularities.txt" # the name of the file where the complexities are stored

    poems = [x[:x.rfind("<")].split("\n") for x in open(infile_name,"r").read().split(">")]
    stresses = [[get_stresses(line, lang="en") for line in poem if line.strip() != ""] for poem in poems]
    candidate_metres = [([float(e) for e in l.split("\t")[0].split(" ")], int(l.strip().split("\t")[1]))
                    for l in open(irregularities_name,"r").readlines()]

    alphas = [0.2, 0.4, 0.6, 0.8, 1.0] # list of alphas to consider
    betas = [0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 5.0, 10.0] # list of betas to consider

    for a in alphas:
        for b in betas:

            outfile_name = f"predicted_metres_{str(a)}_{str(b)}.txt"  # the name of the file where the predicted metres are to be stored
            outfile = open(outfile_name, "a")

            counter = 0
            for poem in poems:
                counter += 1
                outfile.write(f"<{counter}>\n")
                for l in infer_metre(poem, candidate_metres, alpha=a, beta=beta):
                    outfile.write(str(l) + "\n")
            outfile.close()