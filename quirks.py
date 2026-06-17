import time
import re

#region Datatype Validator
def CheckIfNumber(_stringVariable: str) -> bool:
    '''Checks of a string variable is an number'''
    try:
        float(_stringVariable)
        return True
    except ValueError:
        return False

def CheckIfInt(_stringVariable: str) -> bool:
    '''Checks of a string variable is an integer'''
    try:
        int(_stringVariable)
        return True
    except ValueError:
        return False
    
def CheckIfFloat(_stringVariable: str) -> bool:
    '''Allow decimals and fractional numbers'''
    if _stringVariable in ("", ".", "-", "-.", "+", "+."):
        return True
    try:
        float(_stringVariable)
        return True
    except ValueError:
        return False
    
def CheckIfAlpha(_stringVariable: str) -> bool:
    '''Allow letters only.'''
    if _stringVariable == "":
        return True
    return _stringVariable.isalpha()
#endregion

#region Decorators
def RuntimeDecorator(_function: any) -> None:
    def Wrapper(*args, **kwargs):
        '''Call as a decorator to check duration to run code'''
        
        startTime: int  = time.time()
        result = _function(*args, **kwargs) # calls function allowing arguments passed
        duration: int = time.time() - startTime

        print(f"{_function.__name__}() took {duration:.2f} to complete.")
        return result
    return Wrapper
#endregion

#region String functions
def DeleteLastWord(_stringVariable: str) -> str:
    '''Removes the last entered word'''
    pattern = r'(.*)\s+\S+\s*$'
    result = re.sub(pattern, r'\1', _stringVariable)
    return result

def ValidateMaxLength(_string: str, _max: int = 10) -> bool:
    '''If string character count is less than max specified return true'''
    return len(_string) <= _max

def SetMaxLength(_string: str, _max:int = 10) -> str:
    '''Cuts any character after specified length'''
    return _string[:_max]
#endregion

#region misc functions
def financial_format(x: float, *args) -> str:
    if x >= 1_000_000_000:
        return f"${x*1e-9:.1f}B"
    elif x >= 1_000_000:
        return f"${x*1e-6:.1f}M"
    elif x >= 1_000:
        return f"${x*1e-3:.0f}K"
    return f"${x:.0f}"
#endregion