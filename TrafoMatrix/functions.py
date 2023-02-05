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



def roundingDIN(val, uval, returnAsString = False):
    
    if val <= 0:
        minusNumber = True
    else:
        minusNumber = False
    
    
    
    valS = f'{float(abs(val)):.20f}' # gives twenty digits after .
    uvalS = f'{float(abs(uval)):.20f}'
    
    # takes the uncertainty, puts it into an array
    u_array = np.array(list(str(uvalS)))

    # check if uncertainty is zero. If so, everything will be done here.
    if uval == 0:
        if val == 0:
            uncertainty = 0
            value = 0
            if returnAsString == True:
                return [str("0"), str("0")]
            if returnAsString == False:
                return [0, 0] 

    #-------- remove decimal point --------
    # just for easier calculation. Will remember position of decimal point
    # this will be inserted later on
    # if there is no position of the decimal point, the last entry will be added

    if "." in u_array:
        decimal = True
        decimalPoint = np.where((u_array == "."))[0][0]
        u_array = np.delete(u_array, decimalPoint)
        
    else:
        decimal = False
        decimalPoint = len(u_array)
        

    #-------- uncertainty is not zero --------
    #checks where uncertainty is not zero or decimal point. returns list of indices
    # we only need the first index
    firstIndex = np.where((u_array != "0"))[0][0]


    #-------- inserting new element --------
    # if there is not another element after the first given uncertainty, 
    # this makes sure the program doesn't crash (there must be a smarter way, but idk)
    if firstIndex == len(u_array) - 1:
        secondIndex = 0 
        # just creates a second index = 0
        # append this second index to u_array
        u_array = np.append(u_array, str(secondIndex))


    #-------- rounding uncertainty --------

    # first digit is 1 or 2:
    if u_array[firstIndex] == "1" or u_array[firstIndex] == "2":

        # if second digit is not nine:
        if u_array[firstIndex + 1] != "9":
            # add 1 to the digit to the left
            u_array[firstIndex + 1] = int(u_array[firstIndex + 1]) + 1
            # remove everything after
            u_array = u_array[:(firstIndex + 2)]

        elif u_array[firstIndex + 1] == "9":
            u_array[firstIndex] =  int(u_array[firstIndex]) + 1
            u_array[firstIndex + 1] = 0
            u_array = u_array[:(firstIndex + 2)]
            
        # significant position
        Abort = firstIndex + 1

    elif u_array[firstIndex] == "9":
        u_array[firstIndex] = 0
        
        if firstIndex == 0:
            np.insert(u_array, 0, 1)
            
        else:
            u_array[firstIndex-1] = int(1)
        u_array = u_array[:firstIndex + 1]
        Abort = firstIndex + 1

    # first digit is higher than that
    else:
        # add 1 to this digit
        u_array[firstIndex ] = int(u_array[firstIndex]) + 1
        # remove everything after
        u_array = u_array[:firstIndex + 1]
        Abort = firstIndex

    # if the first non-zero digit is before the decimal point: remember to put 0 in
    if decimalPoint > firstIndex:
        for n in range(decimalPoint-len(u_array)):
            u_array = np.append(u_array, str("0")) 

    #-------- inserting decimal point, joining to str --------
    if decimal == True:
        u_array = np.insert(u_array, decimalPoint, str("."))

    length_uncertainty = len(u_array)
    uncertainty = "".join(u_array)

    DecimalPlaces = len(u_array) - decimalPoint - 1
   
    #-------- value --------
    array =  np.array(list(str(properRound(abs(val), Abort))))

    if "." in array:
        decimalArray = True
        decimalPointArray = np.where((array == "."))[0][0]
        
    else:
        decimalArray = False
        decimalPointArray = len(array)

    DecimalPlacesValue = abs(len(array) - decimalPointArray - 1) 
    # how many DecimalPlaces has value
   
    if DecimalPlaces != -1:
        DecimalPlacesDifference = DecimalPlaces - DecimalPlacesValue  
        if DecimalPlacesDifference == 1:
             for i in range(abs(DecimalPlacesDifference)):
                array = np.append(array, str("0"))
                array = array
                
        else:
            for i in range(abs(DecimalPlacesDifference)):
                array = np.append(array, str("0"))
                array = array[:-(abs(DecimalPlacesDifference)+1)]

    elif DecimalPlaces == -1:
        array = array[:-DecimalPlaces]

    value = "".join(array)
    
    #-------- printing --------

    if minusNumber == True:
       
        if returnAsString == True:
            return ["-" + value, uncertainty]

        else:
            return [-float(value), float(uncertainty)]
        
    if minusNumber == False:
       
        if returnAsString == True:
            return [ value, uncertainty]

        else:
            return [float(value), float(uncertainty)]
    