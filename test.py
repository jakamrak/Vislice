#Program, ki izpiše prvih 200 prastevil


print(2)

for j in range(3, 201):

    je_prastevilo = True

    for mozni_delitelj in range(2, j):
        if j % mozni_delitelj == 0:
            je_prastevilo =  False
            
    if je_prastevilo:
        print(j)


