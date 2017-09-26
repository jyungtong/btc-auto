def calcAvg(arr):
    return reduce(lambda x,y: x+y, arr)/float(len(arr))

def calcMovAvg(arr, ma_size, pointer):
    # first part of price list
    offsetRight = pointer - ma_size + 1
    firstArr = []
    if offsetRight < 0:
        firstArr = arr[:pointer+1]
    else:
        firstArr = arr[offsetRight:pointer+1]

    # second part of price list
    offsetLeft = len(firstArr) - ma_size # check if still have list at behind
    secondArr = []
    if offsetLeft < 0:
        secondArr = arr[offsetLeft:]

    return calcAvg(secondArr + firstArr)
