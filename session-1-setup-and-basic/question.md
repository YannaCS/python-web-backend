# Python Interview Questions & Coding Challenges - Session 1

## Concept Questions
* What is Python's main characteristic regarding syntax  compared to other programming languages?  
    Python's syntax is simply and highly readable, it uses indentation (whitespace) to indicate structure.  

* What are the basic data types available in Python?  
    int, float, bool, str, list, tuple, dict, set  

* Why is indentation important in Python?  
    It defines code blocks, which related to the programming logic.  

* What happens when you try to mix incompatible data types in an operation?  
    TypeError raised, e.g. int("5")
* What is Git Flow?  
    A branch system to manage development, a structured workflow containing following branches: 
    - main/master: production ready code
    - develop: integration branch for ongoing development
    - feature: new features
    - release: preparing new release, a stage before real release i.e. main/master
    - hotfix: urgent production fix, between main/master and release

* Explain the difference between `==` and `is` operators
    `==` checks value equality; `is` checks identity, whether they point to the same object in memory.
    e.g.:
    a = 1, b=1
    a == b  # true, same value
    a is b  # false, different memory address
    a == True # false, 1 != True
     

    `True` or `False` are **singleton** objects of type bool, there's only one True object and one False object in memory: 
    id(True) == id(1 == 1)  # same object

* What's the difference between implicit and explicit type conversion?
    implicit conversion (coercion): Python auto converts types when safe: 
    x = 5 + 3.0 # int + float -> float

    explicit conversion (casting): manually convert types by functions like int(), float(), str(): 
    x = int('10') + 3

* What's the difference between `if x:` and `if x == True:`?
    `if x:`: checks the truthiness of x, any nonzero, non-empty, non-None value counts True
    `if x == True`: explicitly checks if x equals the boolean True

---

## Coding Questions

### Coding Problem 1: Palindrome Checker

**Problem:**  
Write a function that checks if a string is a palindrome (reads the same forwards and backwards), ignoring spaces, punctuation, and case.

**Description:**  
A palindrome is a word, phrase, number, or other sequence of characters that reads the same forward and backward. Your function should:
- Ignore spaces
- Ignore punctuation marks
- Be case-insensitive
- Return `True` if the string is a palindrome, `False` otherwise

**Function Signature:**
```python
def is_palindrome(s: str) -> bool:
    """
    Check if a string is a palindrome.
    
    Args:
        s (str): Input string to check
    
    Returns:
        bool: True if palindrome, False otherwise
    
    Example:
        >>> is_palindrome("racecar")
        True
        >>> is_palindrome("A man a plan a canal Panama")
        True
        >>> is_palindrome("hello")
        False
    """
    pass
```
---

### Coding Problem 2: Valid Parentheses

**Problem:**  
Given a string containing just the characters `'(', ')', '{', '}', '[', ']'`, determine if the input string is valid.

**Description:**  
A string is considered valid if:
1. Open brackets must be closed by the same type of brackets
2. Open brackets must be closed in the correct order
3. Every close bracket has a corresponding open bracket of the same type
4. Every open bracket must have a corresponding close bracket

**Function Signature:**
```python
def is_valid_parentheses(s: str) -> bool:
    """
    Check if a string has valid parentheses.
    
    Args:
        s (str): String containing only '(', ')', '{', '}', '[', ']'
    
    Returns:
        bool: True if parentheses are valid, False otherwise
    
    Example:
        >>> is_valid_parentheses("()")
        True
        >>> is_valid_parentheses("()[]{}")
        True
        >>> is_valid_parentheses("(]")
        False
    """
    pass
```