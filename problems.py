PROBLEMS = {

    # ── EASY ──────────────────────────────────────────────────────────────────

    1: {
        "title": "Sum of Two Numbers",
        "difficulty": "Easy",
        "desc": (
            "Given two integers A and B on the same line separated by a space, "
            "print their sum."
        ),
        "test_cases": [
            {"input": "2 3",   "output": "5"},
            {"input": "10 20", "output": "30"},
        ]
    },

    2: {
        "title": "Even or Odd",
        "difficulty": "Easy",
        "desc": (
            "Given a single integer N, print 'Even' if it is even, "
            "or 'Odd' if it is odd."
        ),
        "test_cases": [
            {"input": "4",  "output": "Even"},
            {"input": "7",  "output": "Odd"},
        ]
    },

    3: {
        "title": "Reverse a String",
        "difficulty": "Easy",
        "desc": (
            "Given a single string, print it reversed. "
            "The string will not contain spaces."
        ),
        "test_cases": [
            {"input": "hello",  "output": "olleh"},
            {"input": "python", "output": "nohtyp"},
        ]
    },

    4: {
        "title": "Count Vowels",
        "difficulty": "Easy",
        "desc": (
            "Given a lowercase string, print the number of vowels "
            "(a, e, i, o, u) it contains."
        ),
        "test_cases": [
            {"input": "hello",  "output": "2"},
            {"input": "python", "output": "1"},
        ]
    },

    5: {
        "title": "Maximum of Three",
        "difficulty": "Easy",
        "desc": (
            "Given three integers on the same line separated by spaces, "
            "print the largest one."
        ),
        "test_cases": [
            {"input": "3 7 2",    "output": "7"},
            {"input": "-1 -5 -3", "output": "-1"},
        ]
    },

    6: {
        "title": "FizzBuzz",
        "difficulty": "Easy",
        "desc": (
            "Given a single integer N, print 'Fizz' if it is divisible by 3, "
            "'Buzz' if divisible by 5, 'FizzBuzz' if divisible by both, "
            "or the number itself if none of the above."
        ),
        "test_cases": [
            {"input": "15", "output": "FizzBuzz"},
            {"input": "7",  "output": "7"},
        ]
    },

    7: {
        "title": "Sum of List",
        "difficulty": "Easy",
        "desc": (
            "The first line contains an integer N. "
            "The second line contains N space-separated integers. "
            "Print the sum of all the integers."
        ),
        "test_cases": [
            {"input": "5\n1 2 3 4 5",   "output": "15"},
            {"input": "4\n-1 -2 -3 -4", "output": "-10"},
        ]
    },

    # ── MEDIUM ────────────────────────────────────────────────────────────────

    8: {
        "title": "Factorial",
        "difficulty": "Medium",
        "desc": (
            "Given a non-negative integer N, print the factorial of N. "
            "Factorial of 0 is 1."
        ),
        "test_cases": [
            {"input": "0",  "output": "1"},
            {"input": "10", "output": "3628800"},
        ]
    },

    9: {
        "title": "Fibonacci Sequence",
        "difficulty": "Medium",
        "desc": (
            "Given an integer N, print the first N numbers of the Fibonacci "
            "sequence separated by spaces. The sequence starts with 0 and 1."
        ),
        "test_cases": [
            {"input": "5",  "output": "0 1 1 2 3"},
            {"input": "10", "output": "0 1 1 2 3 5 8 13 21 34"},
        ]
    },

    10: {
        "title": "Palindrome Check",
        "difficulty": "Medium",
        "desc": (
            "Given a single lowercase string with no spaces, print 'Yes' if it "
            "is a palindrome (reads the same forwards and backwards), "
            "or 'No' otherwise."
        ),
        "test_cases": [
            {"input": "racecar", "output": "Yes"},
            {"input": "hello",   "output": "No"},
        ]
    },

    11: {
        "title": "Count Character Frequency",
        "difficulty": "Medium",
        "desc": (
            "Given a lowercase string with no spaces, print each unique character "
            "and its count in the order they first appear, one per line in the "
            "format: 'char count'."
        ),
        "test_cases": [
            {"input": "hello",       "output": "h 1\ne 1\nl 2\no 1"},
            {"input": "mississippi", "output": "m 1\ni 4\ns 4\np 2"},
        ]
    },

    12: {
        "title": "Second Largest",
        "difficulty": "Medium",
        "desc": (
            "The first line contains N. The second line contains N "
            "space-separated distinct integers. Print the second largest number."
        ),
        "test_cases": [
            {"input": "3\n10 20 30",     "output": "20"},
            {"input": "5\n1 2 3 4 5",   "output": "4"},
        ]
    },

    13: {
        "title": "Prime Check",
        "difficulty": "Medium",
        "desc": (
            "Given a single integer N (N >= 2), print 'Prime' if it is a prime "
            "number, or 'Not Prime' otherwise."
        ),
        "test_cases": [
            {"input": "17", "output": "Prime"},
            {"input": "25", "output": "Not Prime"},
        ]
    },

    14: {
        "title": "Bubble Sort",
        "difficulty": "Medium",
        "desc": (
            "The first line contains N. The second line contains N "
            "space-separated integers. Print them sorted in ascending order, "
            "separated by spaces."
        ),
        "test_cases": [
            {"input": "5\n5 3 1 4 2", "output": "1 2 3 4 5"},
            {"input": "4\n-1 -3 0 2", "output": "-3 -1 0 2"},
        ]
    },

    15: {
        "title": "Armstrong Number",
        "difficulty": "Medium",
        "desc": (
            "Given a positive integer N, print 'Yes' if it is an Armstrong number, "
            "'No' otherwise. An Armstrong number equals the sum of its digits each "
            "raised to the power of the number of digits. Example: 153 = 1³+5³+3³."
        ),
        "test_cases": [
            {"input": "153", "output": "Yes"},
            {"input": "100", "output": "No"},
        ]
    },

    # ── HARD ──────────────────────────────────────────────────────────────────

    16: {
        "title": "Binary Search",
        "difficulty": "Hard",
        "desc": (
            "The first line contains N (size of sorted array). "
            "The second line contains N space-separated integers in ascending order. "
            "The third line contains the target integer to search for. "
            "Print the index (0-based) if found, or -1 if not found."
        ),
        "test_cases": [
            {"input": "5\n1 3 5 7 9\n5", "output": "2"},
            {"input": "5\n1 3 5 7 9\n6", "output": "-1"},
        ]
    },

    17: {
        "title": "Balanced Parentheses",
        "difficulty": "Hard",
        "desc": (
            "Given a string containing only '(', ')', '{', '}', '[', ']', "
            "print 'Yes' if the brackets are balanced, 'No' otherwise."
        ),
        "test_cases": [
            {"input": "()[]{}", "output": "Yes"},
            {"input": "([)]",   "output": "No"},
        ]
    },

    18: {
        "title": "Two Sum",
        "difficulty": "Hard",
        "desc": (
            "The first line contains N. The second line contains N "
            "space-separated integers. The third line contains target T. "
            "Find two distinct indices i and j such that arr[i] + arr[j] == T. "
            "Print the two indices separated by a space (smaller index first). "
            "There is always exactly one solution."
        ),
        "test_cases": [
            {"input": "4\n2 7 11 15\n9", "output": "0 1"},
            {"input": "3\n-3 4 3\n0",   "output": "0 2"},
        ]
    },

    19: {
        "title": "Longest Common Subsequence",
        "difficulty": "Hard",
        "desc": (
            "Given two strings on separate lines, print the length of their "
            "longest common subsequence (LCS)."
        ),
        "test_cases": [
            {"input": "abcde\nace",  "output": "3"},
            {"input": "abc\ndef",    "output": "0"},
        ]
    },

    20: {
        "title": "Roman to Integer",
        "difficulty": "Hard",
        "desc": (
            "Given a Roman numeral string, convert it to an integer. "
            "Symbols: I=1, V=5, X=10, L=50, C=100, D=500, M=1000. "
            "Subtractive notation applies (e.g. IV=4, IX=9, XL=40, XC=90, CD=400, CM=900)."
        ),
        "test_cases": [
            {"input": "IX",      "output": "9"},
            {"input": "MCMXCIV", "output": "1994"},
        ]
    },

}