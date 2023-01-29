import numpy as np
import matplotlib.pyplot as plt
import sympy as sp


def Plot(X, Y, uX = [], uY = [], Xlim = [], Ylim = [], Label = 'Messwerte mit Unsicherheit', 
         Xlabel = '', Ylabel = '', size = (12,9)):
    
    plt.rcParams["figure.figsize"] = size    
    if len(uX) == 0:
        uX = np.zeros(X.shape)
    if len(uY) == 0:
        uY = np.zeros(Y.shape)
               
    plt.errorbar(X, Y, xerr=uX , yerr=uY, fmt='.', label = Label, capsize=2, zorder=3)
    
    if not len(Xlim) == 0:
        plt.xlim(Xlim)
    if not len(Ylim) == 0:
        plt.ylim(Ylim)
    
    plt.xlabel(Xlabel, fontsize=16)
    plt.ylabel(Ylabel, fontsize=16)
    plt.grid()
    plt.legend()
    
    
def Fehlerfortpflanzung(Funktion, Variablen, Variablen_Werte, Fehler_Werte, Rückgabe = 'alles'):
    '''Diese Funktion berechnet mittels des Moduls sympy den Wert und den Fehler einer gegebenen Funktion. Dazu nimmt die Funktion vier Arguemente entgegen: die Formel mit der gerechnet werden soll, die Variablen, die Variablenwerte und die Fehler der Variablenwerte. Es werden die Funktion sowie die Formel zur Berechnung des absoluten Fehlers in Latex-Befehlen dargestellt. Außerdem wird der Funktionswert und der Fehler ausgegeben. 
Es gibt ein fünftes optionales Argument Rückgabe: setzt man dieses auf 'werte' gibt die Funktion lediglich eine Liste aus, deren erster Eintrag das berechnete Ergebnis und deren zweiter Eintrag der berechnete Fehler ist.
Der Code könnte beispielsweise wie folgt aussehen:

import sympy as sp

Variablen = L, T = sp.symbols('L T')
Messwerte = [2, 2.84]
Unsicherheiten = [0.01, 0.02]

Erdbeschleunigung = 4 * L * sp.pi**2 / T**2

Fehlerfortpflanzung(Erdbeschleunigung, Variablen, Messwerte, Unsicherheiten, Rückgabe = 'werte')  


Bei der Definition der zu berechnenden Funktion sollte darauf geachtet werden, dass für besondere Zahlen und Funktionen die in Sympy integrierten Zahlen und Funktionen verwendet werden (z.B. sp.exp(...)). Außerdem sollten die Variablen nicht d genannt werden.'''

    fehler = 0
    fehlersymbole=[]
    ableitungen_quadr = []

    for var in Variablen:
        d = sp.symbols('d' + var.name)        
        fehlersymbole.append(d)               
        partial = sp.diff(Funktion, var) * d 
        ableitungen_quadr.append(partial**2)  
        fehler = fehler + partial**2
    
    fehler_abs=sp.simplify(sp.sqrt(fehler))              
    fehler_rel=sp.simplify(sp.sqrt(fehler/Funktion**2))
    
    funktions_wert = float(sp.Subs(Funktion,Variablen,Variablen_Werte).doit())
    err1 = sp.Subs(fehler,Variablen,Variablen_Werte).doit()
    err = float(sp.Subs(err1,fehlersymbole,Fehler_Werte).doit())
    
    if Rückgabe == 'werte':
        result = [funktions_wert, err]
        return result
    
    else:        
        print('Funktion:')
        display(Funktion)
        print('Absoluter Fehler:')
        display(fehler_abs)
        print('Ergebnis:')
        print('f = {0} \pm {1}'.format(funktions_wert, err))
        
        
        
# Tashas Beitrag:
def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])


def properRound(n, decimals=0):
    expoN = n * 10 ** decimals
    if abs(expoN) - abs(np.floor(expoN)) < 0.5:
        return np.floor(expoN) / 10 ** decimals
    return np.ceil(expoN) / 10 ** decimals

def roundingDIN(value, error, printing = False):
    valueFloat = f'{float(value):.20f}' # gives twenty digits after .
    errorFloat = f'{float(error):.20f}'
    
    if error == 0:
        return  [properRound(float(valueFloat)),0.0]
    
    else:
        decimalPointError = str(errorFloat).find(".") # find position of decimal point for value

        error = str(errorFloat).replace(".","") # replace point

        arrayError = [int(x) for x in str(error)] # create array with all digits of the number


        NonZeroError = np.where(np.array(arrayError) != 0)[0][0] # gives index of fist non zero digit
        
        FirstErrorDigit = np.array(arrayError)[NonZeroError] #first non zreo digit of the error 
        SecondErrorDigit = np.array(arrayError)[NonZeroError+1]
        
        if np.array(arrayError)[NonZeroError+2] and np.array(arrayError)[NonZeroError+3] and np.array(arrayError)[NonZeroError+4] == 9:
            SecondErrorDigit +=1
      
        if FirstErrorDigit == 1 or FirstErrorDigit == 2: #if the first error digit is a 1 or 2, the digit next to it will get rounded up
            SecondErrorDigit +=1
            Abort = NonZeroError +1# cancel at this position,  where value needs to round to
        
        else: # for every other digit, the first digit gets rounded up
            FirstErrorDigit +=1
            SecondErrorDigit = 0
            Abort = NonZeroError

        ErrorValue = f'{float(FirstErrorDigit * 10**(-int(NonZeroError))):.20f}' 

        if decimalPointError <= NonZeroError:
            # first non zero digit is behind decimal point
            ErrorValue = f'{float(FirstErrorDigit * 10**(int(-NonZeroError)) + SecondErrorDigit * 10**(int(-NonZeroError-1)))}' 

        elif decimalPointError > NonZeroError:
            # first non zero digit is behind decimal point
            ErrorValue = f'{float(FirstErrorDigit * 10**(int(decimalPointError)-1) + SecondErrorDigit * 10**(int(decimalPointError-2)))}'

        if printing == True:
            print(properRound(float(valueFloat), Abort), "$\pm$", truncate(ErrorValue, Abort))
        return [properRound(float(valueFloat), Abort),float(ErrorValue) ]
