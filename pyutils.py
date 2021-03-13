

def hasNumbers(inputString:str) -> bool:
    return any(char.isdigit() for char in inputString)
