def neurone(entrees, poids, biais):
    total = 0
    for i in range(len(entrees)):
        total += entrees[i] * poids[i]
    return total + biais
 
print(neurone([1], [14.08], 16.92))
