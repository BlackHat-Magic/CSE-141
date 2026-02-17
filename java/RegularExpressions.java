/**
 * This class implements the regular expressions used to parse the input
 */

import java.util.*;

public class RegularExpressions {
	
	
	// Array of reserved words
	private String [] reservedWords = {"int","void","if","while","return","read","write","print","continue","break","binary",
			"decimal"};
	
	// Array of symbols
	private String [] symbols = {"(",")","{","}","[","]",",",";","+","-","*","/","==","!=",">",">=","<","<=",
			"=","&&","||"};
	
	/**
	 * Checks to see if the input matches a space. A space is defined as tab, spacebar, newline
	 * @param str The String to be checked
	 * @return boolean indicating if it is a space
	 */
	public boolean isSpace(String str) {
		char ch;
		for (int i = 0; i < str.length(); i++) {
			ch = str.charAt(i);
			if(ch != ' ' && ch != '\n' && ch != '\r' && ch != '\u001a' && ch != '\t') {
				// this is not space
				return false;
			}
		}
		return true;
	}
	
	/***
	 * Checks to see if a character is a digit
	 * @param c the character to check 
	 * @return boolean indicating if it is a digit
	 */
	private boolean isDigit(char c) {
		return Character.isDigit(c);
	}
	
	/**
	 * Checks to see if the given input matches the pattern for an identifier.
	 * The pattern is: Letter(Letter|digit)*
	 * @param str The input string that is being pasrsed which will be read one charecter at a time
	 * @return boolean indicating if it is an identifier
	 */
	public boolean isIdentifier(String str) {
		if (str.length() < 1) {
			return false;
		}
		if (!Character.isLetter(str.charAt(0)) && str.charAt(0) != '_') {
			return false;
		}
		for (int i = 1; i < str.length(); i++) {
			char c = str.charAt(i);
			if (!Character.isLetterOrDigit(c) && c != '_') {
				return false;
			}
		}
		return true;
	}

	/***
	 * Checks to see if the given input matches the pattern for a number.
	 * The pattern for number is: digit+
	 * @param str The input string that is being parsed which will be read one character at a time
	 * @return boolean indicating if it is a number
	 */
	public boolean isNumber(String str) {
		if (str.length() < 1) {
			return false;
		}
		for (int i = 0; i < str.length(); i++) {
			if (!Character.isDigit(str.charAt(i))) {
				return false;
			}
		}
		return true;
	}
	
	/***
	 * Checks to see if the given input matches the pattern for a reserved word.
	 * reserved words are: int, void, if, while, return, read, write, print, continue, break, binary, decimal
	 * @param str The input string that is being parsed and compaired against the list of reserved words 
	 * @return boolean indicating if it is a reserved word
	 */
	public boolean isReservedWord(String str) {
		if (str.length() < 1) {
			return false;
		}
		// TODO: don't create new list, hashset every time
		List<String> reserved_list = Arrays.asList(
			"int", "void", "if", "while", "return", "read", "write", "print",
			"continue", "break", "binary", "decimal"
		);
		Set<String> reserved_set = new HashSet<>(reserved_list);
		return reserved_set.contains(str);
	}
	
	/***
	 * Checks to see if the given input matches the pattern for a symbol
	 * @param str The input string that is being parsed and compaired against the list of symbols
	 * @return boolean indicating if it is a symbol
	 */
	public boolean isSymbol(String str) {
		// why are bitwise operators not included? (& and |)
		if (str.length() < 1) {
			return false;
		} else if (str.length() > 2) {
			// all symbols are <= two chars
			return false;
		} else if (str.length() == 1) {
			// optimistically assume most performant case
			// handle single-character symbols
			// TODO: don't create 
			char[] symbol_chars = {
				'(', ')', '[', ']', '{', '}', ',', ';', '+', '-', '*', '/', '=', '>',
				'<'
			};
			char target = str.charAt(0);
			for (char c : symbol_chars) {
				if (c == target) {
					return true;
				}
			}
			return false;
		} else {
			// TODO: don't create new list, hashset every time.
			List<String> multichar_symbols_list = Arrays.asList(
				"==", "!=", ">=", "<=", "&&", "||"
			);
			Set<String> multichar_symbols_set = new HashSet<>(multichar_symbols_list);
			return multichar_symbols_set.contains(str);
		}
	}
	
	/**
	 * Checks to see if the given input matches the pattern for a string
	 * The pattern for a string is that it starts and ends with quotations 
	 * @param str The input string that is being parsed
	 * @return boolean indicating if it is a string
	 */
	public boolean isString(String str) {
		if (str.length() < 2) {
			return false;
		}
		if (str.charAt(0) != '"') {
			return false;
		}
		if (str.charAt(str.length() - 1) != '"') {
			return false;
		}
		return true;
	}
	
	/**
	 * Checks to see if the given input matches the pattern for a meta statement
	 * @param str The input string that is being parsed
	 * @return boolean indicating if it is a meta statement
	 */
	public boolean isMetaStatement(String str) {
		if (str.length() < 2) {
			// if of length 1, cannot contain # and newline
			return false;
		}
		// if (str.charAt(str.length() - 1) != '\n') {
		// 	return false;
		// }
		if (str.charAt(0) == '#') {
			return true;
		}
		if (str.charAt(0) == '/' && str.charAt(1) == '/') {
			return true;
		}
		return false;
	}

}
