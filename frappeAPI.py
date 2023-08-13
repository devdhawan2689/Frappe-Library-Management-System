import pandas as pd
import numpy as np
import requests
import datetime
from datetime import date, datetime
from datetime import timedelta
import json

def fetchBooks():
    """
    This Function simply fetches the Books given by the Frappe API and converts it into list containing Column Names as First Index and Values as Second Index
    """
    URL = "https://frappe.io/api/method/frappe-library?page=2&title=and"

    booksList = requests.get(URL)
    
    # Converting Bytes to JSON
    booksData = json.loads(booksList.content)

    columns_names = ['bookID', 'title', 'authors', 'average_rating', 'isbn', 'isbn13', 'language_code', 'num_pages', 'ratings_count', 'text_reviews_count', 'publication_date', 'publisher']
    values = []
    temp_list = []

    # Iterating JSON Data and Storing it in List to Create Data Frame
    for index in range(len(booksData['message'])):
        for key, value in booksData['message'][index].items():
            temp_list.append(value)
        values.append(temp_list)
        temp_list = []
    
    booksDataDF = pd.DataFrame(values, columns = columns_names)
    booksDataList = [columns_names, values]
    return booksDataList

def findBook(name = None, ID = None, authors = None, isbn=None, isbn13=None, language=None):
    """
    This Function searches for Books In The Database based on the paramter passed
    
    (Note - Pass Only One Parameter at a time)
    """

    # Loading Database
    booksAvailable = pd.read_csv('Library_Books_Database.csv')
    
    if name != None:
        if np.where(booksAvailable[booksAvailable['title'].str.contains(name, case=False, na=False)]):
            return booksAvailable[booksAvailable['title'].str.contains(name, case=False, na=False)]
        else:
            return "Book Not Found"
    elif ID != None:
        if np.where(booksAvailable[booksAvailable['bookID'].isin({ID})]):
            return booksAvailable[booksAvailable['bookID'] == ID]
        else:
            return "Book Not Found"
    elif authors != None:
        if np.where(booksAvailable['authors'].str.contains(authors, case=False, na=False)):
            return  booksAvailable[booksAvailable['authors'].str.contains(authors, case=False, na=False)]
        else:
            return "Book Not Found"
    elif isbn != None:
        if np.where(booksAvailable[booksAvailable['isbn'].str.contains(isbn)]):
            return booksAvailable[booksAvailable['isbn'] == isbn]
        else:
            return "Book Not Found"
    elif isbn13 != None:
        if np.where(booksAvailable[booksAvailable['isbn13'].isin({isbn13})]):
            return booksAvailable[booksAvailable['isbn13'] == isbn13]
        else:
            return "Book Not Found"
    elif language != None:
        if np.where(booksAvailable[booksAvailable['language_code'].str.contains(language, case=False, na=False)]):
            return booksAvailable[booksAvailable['language_code'].str.contains(language, case=False, na=False)]
        else:
            return "Book Not Found"

def updateBooksDatabase(addBooksData):
    """
    This Function is used when the Librarian tries to import a new book or a book already present in the database
    
    (Note - Only the Book Quantity is updated for books already existing in the database)
    """
    currentBooksDatabase = pd.read_csv('Library_Books_Database.csv')

    for books in addBooksData:
        del books[-2]

        if np.where(currentBooksDatabase[currentBooksDatabase['bookID'].isin({int(books[0])})]):
            print("Updating Quantity of Book in Database")
            currentBooksDatabase.loc[currentBooksDatabase['bookID'] == int(books[0]), 'quantity'] = int(currentBooksDatabase[currentBooksDatabase['bookID'] == int(books[0])]['quantity']) + int(books[-1])
            currentBooksDatabase.to_csv('Library_Books_Database.csv', index=False)
            return "Successfully Updated The Books Quantity"
        else:
            return "New Book Found, Adding to Database"

def findBooks(name = None, author = None):
    """
    This Function is used to Find Books In The Database
    
    (Note - Only Pass One Parameter for Each Request)
    """
    currentBookDatabase = pd.read_csv('Library_Books_Database.csv')
    
    if name != None:
        if np.where(currentBookDatabase[currentBookDatabase['title'].str.contains(name, case=False, na=False)]):
            return currentBookDatabase[currentBookDatabase['title'].str.contains(name, case=False, na=False)]
        else:
            return "Book Not Found"
    elif author != None:
        if np.where(currentBookDatabase[currentBookDatabase['authors'].str.contains(author, case=False, na=False)]):
            return currentBookDatabase[currentBookDatabase['authors'].str.contains(author, case=False, na=False)]
        else:
            return "Author Not Found"

def autocomplete(memberID = None, memberName = None, bookID = None, bookName = None, author = None, ISBN = None, ISBN13 = None, languageCode = None):
    """
    This Function is used to Provide Autocomplete Prompts to the Librarian While Entering Different Details
    
    (Note - Only Pass One Parameter for Each Request)
    """
    memberData = pd.read_csv('Members_Database.csv')
    booksData = pd.read_csv('Library_Books_Database.csv')
    
    if memberID == True:
        memberIDList = list(memberData['Member ID'])
        return memberIDList
    elif memberName == True:
        memberNameList = list(memberData['Member Name'])
        return memberNameList
    elif bookID == True:
        bookIDList = list(booksData['bookID'])
        return bookIDList
    elif bookName == True:
        bookNameList = list(booksData['title'])
        return bookNameList
    elif author == True:
        authorList = list(booksData['authors'])
        return authorList
    elif ISBN == True:
        isbnList = list(booksData['isbn'])
        return isbnList
    elif ISBN13 == True:
        isbn13List = list(booksData['isbn13'])
        return isbn13List
    elif languageCode == True:
        languageCodeList = list(booksData['language_code'])
        return languageCodeList
    else:
        return "Invalid Input Given"

def getMemberInformation(memberID):
    """
    This Function Returns Member Information
    
    (Note - The memberID Data Type Should be int)
    """
    memberData = pd.read_csv('Members_Database.csv')
    
    return memberData[memberData['Member ID'] == memberID]

def getBookInformation(bookName):
    """
    This Function Returns Book Information
    
    (Note - The bookName Data Type Should be str)
    """
    bookData = pd.read_csv('Library_Books_Database.csv')
    
    return bookData[bookData['title'] == bookName]

def issueBookToMember(issueData):
    """
    This Function Issues the Book to Member and Also Calculates and Appends the Due Date
    
    (Note - The Function will Return False, {Reason for False} if the Member has already Issued 2 Books or Has Issued the Same Book Before Else it will Return True, {Reason for True})
    """
    currentIssueData = pd.read_csv('Library_Dues_Database.csv')
    
    currentIssueData = currentIssueData.reset_index(drop=True)
    
    print(len(currentIssueData.index))
    print(issueData)
    print(currentIssueData.info())
    
    if np.where(currentIssueData[currentIssueData['Member ID'].isin({issueData[0]})]):
        memberData = currentIssueData[currentIssueData['Member ID'] == issueData[0]]
        if len(memberData) > 1:
            return False, "Cannot Issue More than Two Books. Return Any One Book First"
        elif len(memberData[memberData['Book ID'] == issueData[2]]) == 1:
            return False, "Cannot Issue Same Book Twice"
            
    print(f"Checking  Quantity for {issueData[2]}")
    quantity_flag = updateBookQuantity(issueData[2])

    if quantity_flag == False:
        print("Cannot Issue Book. Not In Stock")

        return False, "Cannot Issue Book. Not In Stock"

    currentIssueData.loc[len(currentIssueData.index)] = issueData
    
    currentIssueData.to_csv('Library_Dues_Database.csv', index = False)

    return True, "Successfully Issued The Book"

def updateBookQuantity(bookID):
    """
    This Function Updates the Quantity of The Books Added By the Librarian
    
    (Note - The bookID should be int)
    """
    currentBooksDatabase = pd.read_csv('Library_Books_Database.csv')
    
    if np.where(currentBooksDatabase[currentBooksDatabase['bookID'].isin({bookID})]):
            print("Updating Quantity of Book in Database")
            if int(currentBooksDatabase[currentBooksDatabase['bookID'] == bookID]['quantity']) == 0:
                return False
            currentBooksDatabase.loc[currentBooksDatabase['bookID'] == bookID, 'quantity'] = int(currentBooksDatabase[currentBooksDatabase['bookID'] == bookID]['quantity']) - 1
            currentBooksDatabase.to_csv('Library_Books_Database.csv', index = False)
            return True
    else:
        return False

def checkDues():
    """
    This Function Simply Returns the Library Dues Data
    
    (Note - The Function Does not Take any Input)
    """
    duesData = pd.read_csv('Library_Dues_Database.csv')
    
    return duesData

def fetchIssuedBooks(memberID):
    """
    This Function Returns Books Issued By Member
    
    (Note - The memberID Data Type Should be int)
    """
    issuedData = pd.read_csv('Library_Dues_Database.csv')
    
    return issuedData[issuedData['Member ID'] == memberID]

def returnBooks(memberID, bookID):
    """
    This Function Issues Book Return and Calculates the Fine Based On the Due Date
    
    (Note - The memberID and bookID should be int)
    """
    duesData = pd.read_csv('Library_Dues_Database.csv')
    bookData = pd.read_csv('Library_Books_Database.csv')
    issueData = pd.read_csv('Library_Issue_Database.csv')
    
    if np.where(bookData[bookData['bookID'].isin({bookID})]):
        print("Issuing Book Return")
        bookData.loc[bookData['bookID'] == bookID, 'quantity'] = int(bookData[bookData['bookID'] == bookID]['quantity']) + 1
        bookData.to_csv('Library_Books_Database.csv', index = False)
    
    if np.where(duesData[duesData['Member ID'].isin({memberID})]):
        print("Updating Book Return Data")
        selectReturn = duesData[ (duesData['Member ID'] == memberID) & (duesData['Book ID'] == bookID) ]
        selectReturnValue = duesData[ (duesData['Member ID'] == memberID) & (duesData['Book ID'] == bookID) ].values.tolist()
        
        dueDate = selectReturn['Due Date'].values[0]
        
        fineFlag = False
        fine = 0
        
        date = datetime.strptime(dueDate, "%Y-%m-%d")
        today = datetime.now()

        if date < today:
            due = (today - date).days
            fineFlag = True
            fine = due * 10
            print(f"Since Returned {due} days after Due, Fine is ₹{fine}")
        else:
            print(False)

        currentDate = today = date.today()
        selectReturnValue[0][-1] = str(currentDate)
        
        duesData.drop(selectReturn.index , inplace=True)
        duesData.to_csv('Library_Dues_Database.csv', index = False)
        
        issueData = issueData.reset_index(drop = True)
        
        issueData.loc[len(issueData)] = selectReturnValue[0]
        
        issueData.to_csv('Library_Issue_Database.csv', index = False)
        
    return "Successfully Updated Books Return Data", fineFlag, fine

def addMember(memberName, memberAge, memberAddress, memberPhoneNumber):
    """
    This Function Allows Librarian to Add New Member
    
    (Note - The Function Should Recieve All Parameters)
    """
    membersData = pd.read_csv('Members_Database.csv')
    
    memberID = len(membersData) + 1
    
    dataToAdd = [int(memberID), memberName, int(memberAge), memberAddress, memberPhoneNumber]
    
    membersData.loc[len(membersData)] = dataToAdd
    
    membersData.to_csv('Members_Database.csv', index=False)

    return membersData

def getMembers():
    """
    This Function Simply Returns All Members
    
    (Note - The Function Does not Take any Input)
    """
    currentMemberData = pd.read_csv('Members_Database.csv')
    
    return currentMemberData

def checkBookIssueDetails(bookID):
    """
    This Function Returns the Details of Members Who have Issued the Book
    
    (Note - The bookID should be int)
    """
    booksIssuedData = pd.read_csv('Library_Dues_Database.csv')
    
    if np.where(booksIssuedData[booksIssuedData['Book ID'].isin({int(bookID)})]):
        return booksIssuedData[booksIssuedData['Book ID'] == int(bookID)]

def alertDuesExceeded():
    """
    This Function Is Executed at the Home Page and Returns Member Details Who Have Exceeded Due Date
    
    (Note - The Function Does not Take any Input)
    """
    duesData = pd.read_csv('Library_Dues_Database.csv')
    alertDF = pd.DataFrame([], columns=['Member ID', 'Member Name', 'Book ID', 'Book Name', 'Issue Date', 'Due Date'])
    
    for i in range(len(duesData)):
        date = datetime.strptime(duesData.loc[i]['Due Date'], "%Y-%m-%d")
        today = datetime.now()

        if date < today:
            due = (today - date).days
            alertDF.loc[len(alertDF)] = duesData.loc[i]
            print(f"Since Returned {due} days after Due, Fine is ₹{due * 10}")
        else:
            print(False)
    
    return alertDF

def displayDuesExceeded():
    """
    This Function Returns Member Details Who Have Exceeded Due Date
    
    (Note - The Function Does not Take any Input)
    """
    duesData = pd.read_csv('Library_Dues_Database.csv')
    duesDF = pd.DataFrame([], columns=['Member ID', 'Member Name', 'Book ID', 'Book Name', 'Issue Date', 'Due Date'])
    
    for i in range(len(duesData)):
        date = datetime.strptime(duesData.loc[i]['Due Date'], "%Y-%m-%d")
        today = datetime.now()

        if date < today:
            due = (today - date).days
            duesDF.loc[len(duesDF)] = duesData.loc[i]
            print(f"Since Returned {due} days after Due, Fine is ₹{due * 10}")
        else:
            print(False)
    
    return duesDF