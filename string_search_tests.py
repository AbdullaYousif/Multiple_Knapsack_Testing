def find_character(s, c):
    """
    Find the first occurrence of character c in string s.
    
    Parameters:
    s (str): The string to search in
    c (str): The character to search for (single character)
    
    Returns:
    str: Position message or not found message
    """
    if not isinstance(c, str) or len(c) != 1:
        return "Error: c must be a single character"
    
    position = s.find(c)
    
    if position == -1:
        return f"Character '{c}' not found in string"
    else:
        return f"Character '{c}' found at position {position}"


# Test Cases following Each Choice Criterion
def test_each_choice():
    print("=" * 60)
    print("EACH CHOICE CRITERION - Test Cases")
    print("=" * 60)
    
    tests = [
        # Test Frame: B1 (Empty string)
        ("", "a", "Empty S, c does not matter"),
        
        # Test Frame: B2-B7 (Maximum length, no occurrence)
        ("abcdefghij", "9", "Maxi length, no occurrence"),
        
        # Test Frame: B9-B3-B4 (Several occurrences, nominal length, first at beginning)
        ("abcadaae", "a", "Several occurrences, nominal length, first occurrence at index 0"),
        
        # Test Frame: B3-B4-B8 (Nominal length, first at beginning, one occurrence)
        ("abcbe", "a", "Nominal length, first occurrence at index 0, one occurrence"),
        
        # Test Frame: B3-B5-B8 (Nominal length, first at end, one occurrence)
        ("abcde", "e", "Nominal length, first occurrence at end of string, one occurrence"),
        
        # Test Frame: B3-B7 (Nominal length, no occurrence)
        ("abcde", "f", "Nominal length, no occurrence"),
        
        # Test Frame: B3-B6-B8 (Nominal length, first in middle, one occurrence)
        ("abcde", "c", "Nominal length, first occurrence in middle of string, one occurrence"),
    ]
    
    for s, c, description in tests:
        result = find_character(s, c)
        print(f"\nTest: {description}")
        print(f"  Input: s=\"{s}\", c='{c}'")
        print(f"  Result: {result}")


# Test Cases following Pairwise Criterion
def test_pairwise():
    print("\n" + "=" * 60)
    print("PAIRWISE CRITERION - Test Cases")
    print("=" * 60)
    
    tests = [
        # Test Frame: B2-B4-B8
        ("9abcdefghi", "9", "Maxi length, index 0, 1 occurrence"),
        
        # Test Frame: B2-B5-B8
        ("abcdefghi9", "9", "Maxi length, last index, 1 occurrence"),
        
        # Test Frame: B2-B6-B9
        ("abc9de9fhi", "9", "Maxi length, middle index, several occ."),
        
        # Test Frame: B3-B4-B9
        ("abcadae", "a", "Nominal length, index 0, several occ."),
        
        # Test Frame: B3-B5-B8
        ("abcde", "e", "Nominal length, last index, 1 occ."),
        
        # Test Frame: B3-B6-B8
        ("abcde", "c", "Nominal length, middle index, 1 occ."),
        
        # Test Frame: B2-B7
        ("abcdefghij", "z", "Maxi length, no occurrence"),
        
        # Test Frame: B3-B7
        ("abcde", "f", "Nominal length, no occurrence"),
        
        # Test Frame: B1
        ("", "a", "Empty S, c does not matter"),
    ]
    
    for s, c, description in tests:
        result = find_character(s, c)
        print(f"\nTest: {description}")
        print(f"  Input: s=\"{s}\", c='{c}'")
        print(f"  Result: {result}")


# Test Cases following All Combinations Criterion
def test_all_combinations():
    print("\n" + "=" * 60)
    print("ALL COMBINATIONS CRITERION - Test Cases")
    print("=" * 60)
    
    tests = [
        # Test Frame: B1
        ("", "a", "Empty S, c does not matter"),
        
        # Test Frame: B2-B4-B8
        ("9abcdefghi", "9", "Maxi length, index 0, 1 occurrence"),
        
        # Test Frame: B2-B4-B9
        ("9abc9defg9", "9", "Maxi length, index 0, several occ."),
        
        # Test Frame: B2-B5-B8
        ("abcdefghi9", "9", "Maxi length, last index, 1 occ."),
        
        # Test Frame: B2-B6-B8
        ("abcd9efghi", "9", "Maxi length, middle index, 1 occ."),
        
        # Test Frame: B2-B6-B9
        ("abc9de9fhi", "9", "Maxi length, middle index, several occ."),
        
        # Test Frame: B3-B4-B8
        ("abcde", "a", "Nominal length, index 0, 1 occ."),
        
        # Test Frame: B3-B4-B9
        ("abcadae", "a", "Nominal length, index 0, several occ."),
        
        # Test Frame: B3-B5-B8
        ("abcde", "e", "Nominal length, last index, 1 occ."),
        
        # Test Frame: B3-B6-B8
        ("abcde", "c", "Nominal length, middle index, 1 occ."),
        
        # Test Frame: B3-B6-B9
        ("abcdce", "c", "Nominal length, middle index, several occ."),
        
        # Test Frame: B3-B7
        ("abcde", "f", "Nominal length, no occurrence"),
    ]
    
    for s, c, description in tests:
        result = find_character(s, c)
        print(f"\nTest: {description}")
        print(f"  Input: s=\"{s}\", c='{c}'")
        print(f"  Result: {result}")


# Main execution
if __name__ == "__main__":
    print("STRING SEARCH FUNCTION - INPUT SPACE PARTITIONING TEST CASES")
    print("=" * 60)
    print("\nCharacteristics and Blocks:")
    print("  Length of s:")
    print("    B1: Empty")
    print("    B2: Maximum (10 characters)")
    print("    B3: Nominal (5 characters)")
    print("  Location of (first occurrence of) c in s:")
    print("    B4: Beginning of string")
    print("    B5: End of string")
    print("    B6: Middle of string")
    print("  Number of occurrences:")
    print("    B7: No occurrence")
    print("    B8: One occurrence")
    print("    B9: Several occurrences")
    print()
    
    # Run all test suites
    test_each_choice()
    test_pairwise()
    test_all_combinations()
    
    print("\n" + "=" * 60)
    print("TESTING COMPLETE")
    print("=" * 60)