ziar="""Peste 100 de percheziții în Suceava într-un dosar de corupție.
Procurorii au descins și la spitalul din Rădăuți și IPJ"""

def articol(text):
    jumatate=len(text)//2
    part1=text[:jumatate]
    part2=text[jumatate:]
    # print(text.split(''))
    part1=part1.upper()
    part1=part1.replace(" ","")
    part2=part2[::-1]
    part2=part2.capitalize()
    part2=part2.replace(".","")
    part2 = part2.replace(",", "")
    part2 = part2.replace("!", "")
    part2 = part2.replace("?", "")
    print(part1 + part2)
articol(ziar)