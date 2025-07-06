from library import Library

def main():
    while(True):
        print("")
        print(f'Welcome to the book {library.name}! Following are the options,')
        choice = '''
        1. Display Books
        2. Display Loans
        3. Display Members
        4. Lend Book
        5. Return Book
        6. Add Book 
        7. Add Member  
        '''
        print(choice)
        
        userInput = input('Press Q to quit or C to continue: ')
        if userInput == 'Q':
            print('Thankyou for coming to the eXchange.')
            break
        elif userInput == 'C':
            userChoice = int(input('Select an option to continue: '))
            if userChoice == 1:
                library.display_books()
            elif userChoice == 2:
                library.display_loans()
            elif userChoice == 3:
                library.display_members() 
            elif userChoice == 4:
                library.lendBook()
            elif userChoice == 5:
                library.returnBook()
            elif userChoice == 6:
                library.addBook()
            elif userChoice == 7:
                library.addMember()
            else:
                print('Choose a valid option: ')
        else:
            print('Please enter a valid option: ')
            
if __name__ == '__main__':
    library = Library() 
    main()

