import numpy as np

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
