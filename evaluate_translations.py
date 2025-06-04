from metrics import get_bertscore
from metrics import get_metrical_distance
from metrics import get_rhyme_scheme_similarity

# evaluate one or more translation(s) according to the three metrics (Experiment 1 and Experiment 3)

results = open("RESULTS.csv","a") # csv file to write the result to

# file names are stand-in names

# get originals from file (of the format <number>poem<number>poem…<end>)
originals = [x[:x.rfind("<")] for x in open("ORIGINAL_POEMS.txt","r").read().split(">")[1:]]
# get the reference metres from file (of the same format)
metres = [[[float(z.replace("]","").replace("[","")) for z in y.strip().replace(" ","").split(",") if z != ""]
           for y in x[:x.rfind("<")].split("\n") if y != ""]
          for x in open("REFERENCE_METRES.txt","r").read().split(">")[1:]]
# get the reference rhyme schemes from file (where each rhyme scheme is represented as [[line1,line2],…]
rhyme_schemes = [[[int(z.replace("]","").replace("[",""))
                   for z in y.split(",")] for y in x.replace("\n","").replace(" ","").split("],[")] if x != "[]\n"
                 else [] for x in open("REFERENCE_RHYME_SCHEMES.txt","r").readlines()]

candidate_files = [("TRANSLATION.txt", "BACKTRANSLATION.txt", "1"), ("TRANSLATION2.txt", "BACKTRANSLATION2.txt", "2")]

for candidate in candidate_files:
    # get translations and backtranslations (in the same format as for the originals)
    translations = [x[:x.rfind("<")] for x in open(f"./data_final/{candidate[0]}","r").read().split(">")[1:] if len(x) > 3]
    backtranslations = [x[:x.rfind("<")] for x in open(f"./data_final/{candidate[1]}","r").read().split(">")[1:] if len(x) > 3]

    assert len(translations) == len(backtranslations) == len(originals)

    for i in range(len(originals)):
        bs = get_bertscore(candidates=[backtranslations[i]], references=[originals[i]])
        if (bs["precision"][0]+bs["recall"][0]) > 0:
            bert_score = 2*bs["precision"][0]*bs["recall"][0]/(bs["precision"][0]+bs["recall"][0])
        else:
            bert_score = 0
        metrical_distance = get_metrical_distance(translations[i], metres[i], lang="de")
        rhyme_scheme_similarity = get_rhyme_scheme_similarity(translations[i], rhyme_schemes[i], lang="de")[2]

        results.write(",".join([candidate[2], str(i), str(bert_score), str(metrical_distance),
                                str(rhyme_scheme_similarity)]))
results.close()