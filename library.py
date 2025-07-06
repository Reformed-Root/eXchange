from eXchangeDb import get_connection

conn = get_connection()
cursor = conn.cursor()


class Library:
    def __init__(self):
        self.booksList = []
        self.name = 'The eXchange'
        self.lendDict = {}
        self.conn = get_connection()
        self.cursor = self.conn.cursor()

    def fetch_members(self):
        self.cursor.execute('SELECT * FROM exmembers')
        self.members = self.cursor.fetchall()

    def fetch_books(self):
        self.cursor.execute("SELECT id, title, author, genre FROM exbooks")
        self.booksList = self.cursor.fetchall()  # this will store a list of tuples
        print("✅ Book list fetched from database.")

    def fetch_loans(self):
        self.cursor.execute("""
                            SELECT exloans.id, exmembers.name, exbooks.title, exloans.loan_date
                            FROM exloans
                                     JOIN exbooks ON exloans.book_id = exbooks.id
                                     JOIN exmembers ON exloans.member_id = exmembers.id
                            """)
        rows = self.cursor.fetchall()

        self.loanList = rows  # store raw tuples if you need them elsewhere

        # Convert each row to a dict for easier use
        self.loans = [
            {
                "id": row[0],
                "member_id": row[1],
                "book_id": row[2],
                "loan_date": row[3]
            }
            for row in rows
        ]

        print("📄 Loan records fetched from database.")

    def display_members(self):
        self.fetch_members()
        if not self.members:
            print("No members found.")
        else:
            print(f"\n{len(self.members)} Members Found:")
            print("=" * 100)
            print(f"{'Name':<13} {'Email':<30} {'Phone':<20}")
            print("=" * 100)
            for member in self.members:
                _, name, email, phone = member
                print(f"{name:<13} {email:<30} {phone:<20}")

    def display_books(self):
        self.fetch_books()  # pull fresh data every time you display
        if not self.booksList:
            print("📭 No books in the database.")
            return
        print(f"\n📚 Books in {self.name}:")
        print("-" * 100)
        print(f"{'ID':<3} {'Title':<50} {'Author':<30} {'Genre':<15}")
        print("-" * 100)
        for book in self.booksList:
            book_id, title, author, genre = book
            print(f"{book_id:<3} {title:<50} {author:<30} {genre:<15}")

    def display_loans(self):
        self.fetch_loans()
        if not self.loanList:
            print("No loans to display")
            return
        print(f"\n Current {self.name} Loans:")
        print("_" * 90)
        print(f"{'ID':<3} {'Member Name':<20} {'Book Title':<35} {'Loan Date':<10}")
        print("_" * 90)
        for loan in self.loanList:
            loan_id, member_name, book_title, loan_date = loan
            print(f"{loan_id:<3} {member_name:<20} {book_title:<35}  {loan_date:<10}")

    def lendBook(self):
        book_title = input("Enter the book title: ").strip().lower()
        member_name = input("Enter the member's name: ").strip()

        # Look up book title
        self.cursor.execute("SELECT id FROM exbooks WHERE LOWER(title) LIKE %s", ('%' + book_title + '%',))
        book = self.cursor.fetchone()
        if not book:
            print("❌ Book not found in the catalog.")
            return
        book_id = book[0]

        # Look up member ID
        self.cursor.execute("SELECT id FROM exmembers WHERE name = %s", (member_name,))
        member = self.cursor.fetchone()
        if not member:
            print("❌ Member not found. Please register the member first.")
            return
        member_id = member[0]

        # Check if book is already loaned
        self.cursor.execute("SELECT * FROM exloans WHERE book_id = %s", (book_id,))
        if self.cursor.fetchone():
            print("❌ That book is already loaned out.")
            return

        # Add the loan
        from datetime import datetime
        loan_date = datetime.now().strftime('%Y-%m-%d')

        sql = "INSERT INTO exloans (member_id, book_id, loan_date) VALUES (%s, %s, %s)"
        self.cursor.execute(sql, (member_id, book_id, loan_date))
        self.conn.commit()

        print(f"✅ {book_title} has been loaned to {member_name}.")

    def addBook(self):
        title = input("Enter book title: ")
        author = input("Enter author: ")
        genre = input("Enter genre: ")
        sql = "INSERT INTO exbooks (title, author, genre) VALUES (%s, %s, %s)"
        self.cursor.execute(sql, (title, author, genre))
        self.conn.commit()
        print("✅ Book added to the database.")

    def addMember(self):
        name = input("Enter member's name: ")
        email = input("Enter member's email: ")
        phone = input("Enter member's phone: ")
        sql = "INSERT INTO exmembers (name, email, phone) VALUES (%s, %s, %s)"
        self.cursor.execute(sql, (name, email, phone))
        self.conn.commit()
        print(f"✅ {name} has been added to the database.")

    def returnBook(self):
        book_title = input("Enter the book title: ").strip().lower()
        member_name = input("Enter the member's name: ").strip()

        # Look up book title
        self.cursor.execute("SELECT id FROM exbooks WHERE LOWER(title) LIKE %s", ('%' + book_title + '%',))
        book = self.cursor.fetchone()
        if not book:
            print("❌ Book not found in the catalog.")
            return
        book_id = book[0]

        # Look up member ID
        self.cursor.execute("SELECT id FROM exmembers WHERE name = %s", (member_name,))
        member = self.cursor.fetchone()
        if not member:
            print("❌ Member not found. Please register the member first.")
            return
        member_id = member[0]

        # Check if the loan exists
        self.cursor.execute("SELECT * FROM exloans WHERE book_id = %s AND member_id = %s", (book_id, member_id))
        loan = self.cursor.fetchone()
        if not loan:
            print("❌ This loan does not exist. No record of that book being loaned to this member.")
            return

        # Delete the loan record
        self.cursor.execute("DELETE FROM exloans WHERE book_id = %s AND member_id = %s", (book_id, member_id))
        self.conn.commit()

        print(f"✅ '{book_title}' has been returned by {member_name}.")
