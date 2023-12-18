# -*- coding: utf-8 -*-
"""
Created on Sat Dec  3 10:15:40 2022

@author: Simone
"""



#ESERCIZIO 1
"""
a) scrivere una funzione esercizio1(L) che presa una lista converta ogni elemento in stringhe e conti
il numero complessivo di carattere usato dalle stringhe risultanti.
"""
def es1(L):
    temp=[]
    for element in L:
        temp.append(str(element))
    accumulatore=0
    for s in temp:
        accumulatore+=len(s)
    return accumulatore

def es1_bis(L):
    accumulatore=0
    for elemento in L:
        accumulatore+=len(str(elemento))
    return accumulatore


#ESERCIZIO 2
"""
b) scrivere una funzione cifra(s,k) che presa una stringa ne restituisca una in cui tutte le lettere sono
“slittate” ciclicamente di k posti nell’alfabeto. Si assuma che s utilizzi solo lelettere minuscole
dell’alfabeto inglese.

"""

def es2(parola,shift):
    alf="abcdefghijklmnopqrstuvwxyz"
    # suggerimento... metodo "find" o "index"?
    nuovaParola=""
    for c in parola:
        # fa qualcosa
        nuovoIndice=(alf.find(c)+shift)%len(alf)
        nuovaParola+=alf[nuovoIndice]
    return nuovaParola

"""
ESERCIZIO 3

c) date due liste di eguale lunghezza, una di stringhe e una di interi scrivere una funzione
esercizio 3(K,V) che restituisce un dizionario che ha per chiavi gli elementi della prima lista e per
valori gli elementi della seconda, se esistono chiavi duplicate la funzione deve dare messaggio di er-
rore e restitusca un dizionario vuoto.


"""

def es3(K,V):
    if len(K)!=len(V):
        print("warning liste diseguali")
        return {}
    else:
        D={}
        index=0
        for chiave in K:
            D[chiave]=V[index]
            index+=1
        if len(D)==len(K):
            return D
        else:
            print("warning chiavi ripetute")
            return {}

"""

d) scrivere una funzione esercizio4(n,m) che crei due set composti da n elementi. Gli elementi sia-
no interi a caso estratti nell’intervallo [1,m]. La funzione restituisca il numero di elementi comuni ai
due insiemi. Eseguire la funzione 1000 volte e stimare il valore medio e la varianza dei risultati ot-
tenuti.

"""
from random import randint

def es4(n,m):
    S1=set({})
    S2=set({})
    for i in range(n):
        S1.add(randint(1,m))
        S2.add(randint(1,m))
    #print("elementi in S1=",len(S1))
    #print("elementi di S2=",len(S2))
    return len(S1.intersection(S2))
    
def es4_bis(n,m):
    L1=[randint(1,m) for i in range(n)]
    L2=[randint(1,m) for i in range(n)]
    return len(set(L1).intersection(set(L2)))

def es4_ter(n,m):
    S1={randint(1,m) for i in range(n)}
    S2={randint(1,m) for i in range(n)}
    return len(S1.intersection(S2))

def simulazione(n,m):
    L=[]
    for i in range(1000):
        L.append(es4(n,m))
    print(L)
    return L, sum(L)/len(L),var(L)

def var(L):
    m=sum(L)/len(L)
    s=0
    for x in L:
        s+=(x-m)**2
    return s/len(L)

"""
Seconda parte
"""
import pandas as pd

"""
CARICARE I DATI IN UN DATAFRAME
"""
DF=pd.read_csv("diabetes.csv")
# nel mio caso il file che sto caricando si trova
# nella directory di lavoro e non serve fornmire il path

"""
prima verifica del DF
"""

DF.info()

"""
istogrammi
"""

DF["Pregnancies"].hist()
# gli altri sono simili

# non richiesto, solo curiosità
pd.crosstab(DF["Pregnancies"],DF["Age"])

"""
Diagramma a torta "pie diagram"
"""
# modo errato
#DF["Age"].plot.pie()

# modo giusto
DF["Outcome"].unique()
positive=sum(DF["Outcome"][DF["Outcome"]==1])
negative=len(DF)-positive
F=pd.DataFrame([negative,positive])
F[0].plot.pie()

"""
box plot
"""
pd.DataFrame(DF["Glucose"]).boxplot()
DF.boxplot("Glucose")

"""
probabilità e  formula di Bayes
"""

# calcolo P(Outcome) per i valori 0 e 1
# uso la funzione groupby e la funzione count
Temp=DF.groupby(["Outcome"]).count().copy()
# Temp è un data frame di 2 righe e  8 colonne
# tutte e 8 le colonne sono eguali
# perchè contengono il conteggio delle occorrenze
# di 0 e 1 nella colonna Outcome
# prendo la prima colonna di Temp, la divido per
# il numeor di elementi in DF ed ottengo una
# Serie con i valori di P(Outcome)
P_OUT=(Temp.iloc[:,0]/len(DF)).copy()

# per calcolare P(Age) posso usare la medesima
# procedura usata per P(Outcome)
Temp=DF.groupby(["Age"]).count().copy()
P_AGE=(Temp.iloc[:,0]/len(DF)).copy()

# calcoliamo P(Outcome,Age), probabilità congiunte
P_OUT_AGE=pd.crosstab(DF["Outcome"],DF["Age"])/len(DF)


# calcoliamo la verisimiglianza o probabilità condizionale
# P(Age| OUTCOME)
# osserviamo che pd.crosstab(DF["Outcome"],DF["Age"])
# ci dà già i conteggi che servono
# in particolare esso fornisce due righe (Outcome=0,1)
# e 52 colonne
# P(Age|Outcome=0) si ottiene dividendo la prima riga
# della crosstab per il numero di record in cui Outcome==0
# P(Age|Outcome=1) si ottiene dividendo la seconda riga
# della crosstab per il numeor di record per cui Outcome=1
P_AGE_given_OUT=pd.crosstab(DF["Outcome"],DF["Age"])

N_Outcome_0=sum(P_AGE_given_OUT.iloc[0,:])
N_Outcome_1=sum(P_AGE_given_OUT.iloc[1,:])

P_AGE_given_OUT.iloc[0,:]=P_AGE_given_OUT.iloc[0,:]/N_Outcome_0
P_AGE_given_OUT.iloc[1,:]=P_AGE_given_OUT.iloc[1,:]/N_Outcome_1



# calcoliamo adesso la probabilità a posteriori
# cioè P(Outcome|Age) usando la formula di Bayes
# P(Outcome| Age)=P(Age|Outcome)P(Outcome)/P(Age)
# traduciamolo negli oggetti che abbiamo già calcolato
# P(Age|Outcome) per noi è P_AGE_given_OUT
# P(Outcome) per noi P_OUT
# P(Age) per noi noi è P_AGE

# procediamo a passetti
# prima ci creaimo un nuovo DF con i dati
# di P_AGE_given_OUT
P_OUT_given_AGE=P_AGE_given_OUT.copy()
# esso è dato da due righe e 52 colonne
# per ottenere la formula di Bayes si deve
# dividere la prima riga per P_OUT[0] e
# la seconda per P_OUT[1]
P_OUT_given_AGE.iloc[0,:]=P_OUT_given_AGE.iloc[0,:]*P_OUT.iloc[0]
P_OUT_given_AGE.iloc[1,:]=P_OUT_given_AGE.iloc[1,:]*P_OUT.iloc[1]
# si deve quindi completare moltiplicando tutte le colonne
# colonna per colonna per i valori in P_AGE
for i in range(len(P_AGE)):
    P_OUT_given_AGE.iloc[0,i]=P_OUT_given_AGE.iloc[0,i]/P_AGE.iloc[i]
    P_OUT_given_AGE.iloc[1,i]=P_OUT_given_AGE.iloc[1,i]/P_AGE.iloc[i]

# visualizzazione
from matplotlib import pyplot as plt

plt.figure("confronto p(A,O) con P(A|O)")
plt.subplot(1,2,1)
plt.title("P(Age|Outcome)")
plt.plot(P_AGE_given_OUT.iloc[0,0:45])
plt.plot(P_AGE_given_OUT.iloc[1,0:45])
plt.ylim([0,1])
plt.subplot(1,2,2)
plt.title("P(Outcome|Age)")
plt.plot(P_OUT_given_AGE.iloc[0,0:45])
plt.plot(P_OUT_given_AGE.iloc[1,0:45])
plt.ylim([0,1]) 
# nota bene, nelle figure si sono riprodotti in grafico
# solo i primi 45 valori
# infatti gli ultimi relativi alle donne
# molto anziane usano pochissimi dati e 
# non sono attendibili
    



# il punto h calcolo di specifici valori 
# P(Outcome! x) per vari valori di x è facilmente ottenuto
# usando il P_OUT_given_AGE
# per esempio guardiamolo per 30,40,50,60
print("P(1|30)=",P_OUT_AGE.iloc[1][30])
print("P(1|40)=",P_OUT_AGE.iloc[1][40])
print("P(1|50)=",P_OUT_AGE.iloc[1][50])
print("P(1|60)=",P_OUT_AGE.iloc[1,][60])


"""
metodo del boosting per stimare
quanto sia significativa la discrepanza
tra la media del gluosio per le donne diabetiche
dalla media del glucosio di tutte le donne
"""
RIPETIZIONI=10000
mediaGlucAll=DF["Glucose"].mean()
mediaGlucDia=DF["Glucose"][DF["Outcome"]==1].mean()

print("La media del glucosio per tutte le donne è \t",mediaGlucAll)
print("La media del glucosio per le diabetiche è\t",mediaGlucDia)
print("quanto è probabile che tale differenza sia dovuta al puro caso?")
print("le donne diabetiche nel dataset sono 268")
print("BOOSTING: sorteggiamo a caso {} volte da tutto il dataframe 268 donne".format(RIPETIZIONI))
print("senza tenere conto se siano diabetiche o meno")
print("e raccogliamo in una lista le medie del glucosio")
print("calcolate per questi {} campioni casuali".format(RIPETIZIONI))
from random import randint
Medie=[]

for i in range(RIPETIZIONI):
    Values=[]
    for k in range(268):
        Values.append(DF["Glucose"][randint(0,len(DF)-1)])
    Medie.append(sum(Values)/len(Values))

DFM=pd.DataFrame(Medie)
print("in {} ripetizioni la media massima osservata è stata {}".format(RIPETIZIONI,max(DFM[0].values)))
DFM.plot.density()
print("osservando il plot si vede che il valore {} media del glucosio per le diabetiche".format(mediaGlucDia))
print("è molto al di là del limite destro del grafico e quindi si presenta con probabilità")
print("pressocchè nulla!")
print("L'osservazione che il glucosio nelle diabetiche è più elevato con altissima probabilità")
print("NON è dovuta al caso ma ad una causa (il diabete!)")
        
   