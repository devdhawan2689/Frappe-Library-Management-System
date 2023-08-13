# save this as app.py
from flask import Flask, request, render_template
import pandas as pd
import numpy as np
from datetime import date
from datetime import timedelta
import json
import requests
import frappeAPI as frapi

app = Flask(__name__)

@app.route("/")
def homePage():
    checkDues = frapi.alertDuesExceeded()

    if checkDues.empty:
        return render_template('home_page.html', alert=False)
    else:
        memberName = checkDues['Member Name'].values.tolist()
        memberID = checkDues['Member ID'].values.tolist()

        alertData = ""

        for index in range(len(memberName)):
            alertData = "Name - " + str(memberName[index]) + ", ID - " + str(memberID[index]) + ". "

        return render_template('home_page.html', alert=True, alertData=alertData)

@app.route("/login", methods=['GET', 'POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username == 'frappe' and password == 'frappe_login':
        return "Successfully Logged In"
    else:
        return "Invalid Username or Password"

@app.route("/getBooks", methods=['GET', 'POST'])
def getBooks():
    tableData = frapi.fetchBooks()

    columnNames = tableData[0]
    values = tableData[1]

    # print(columnNames)
    # print(values)

    return render_template('add_books.html',  columnNames = columnNames, values = values)

@app.route("/searchpage")
def searchPage():
    bookID = frapi.autocomplete(bookID=True)
    bookName = frapi.autocomplete(bookName=True)
    author = frapi.autocomplete(author=True)
    isbn = frapi.autocomplete(ISBN=True)
    isbn13 = frapi.autocomplete(ISBN13=True)
    languageCode = frapi.autocomplete(languageCode=True)

    autocompleteList = bookID + bookName + author + isbn + isbn13 + languageCode
    
    print(autocompleteList)

    return render_template('search_page.html', autocompleteData = autocompleteList)

@app.route("/searchBook", methods=['GET', 'POST'])
def searchBook():
    parameter = request.form["searchOption"]
    value = request.form["searchTerm"]

    print(parameter)
    print(value)

    if parameter == "Book Name":
        output = frapi.findBook(name=value)
    elif parameter == "ID":
        output = frapi.findBook(ID=int(value))
    elif parameter == "Author":
        output = frapi.findBook(authors=value)
    elif parameter == "ISBN":
        output = frapi.findBook(isbn=value)
    elif parameter == "ISBN13":
        output = frapi.findBook(isbn13=value)
    elif parameter == "Language Code":
        output = frapi.findBook(language=value)
    else:
        return "Invalid Search Parameter Selected"
    
    columnNames = output.columns.tolist()
    values = output.values.tolist()
    
    return render_template('search_books.html',  columnNames = columnNames, values = values)

@app.route("/issueBookPage", methods=['GET', 'POST'])
def issueBookPage():
    memberID = frapi.autocomplete(memberID=True)
    memberName = frapi.autocomplete(memberName=True)
    bookID = frapi.autocomplete(bookID=True)
    bookName = frapi.autocomplete(bookName=True)
    print(f"Book Name - \n{bookName}")

    return render_template('issue_books.html', memberID=memberID, memberName=memberName, bookID=bookID, bookName=bookName)

@app.route("/addBooks", methods=['GET', 'POST'])
def addBooks():
    data = request.get_json() # retrieve the data sent from JavaScript
    # process the data using Python code

    # print(f"Data is \n{data}")

    addBooksData = []
    
    for value in data:
        if value[-1] !='0':
            addBooksData.append(value)
    
    print(f"Books To Add are - {addBooksData}")

    frapi.updateBooksDatabase(addBooksData)
            
    return render_template('successfull.html')

@app.route("/issueBook", methods=['GET', 'POST'])
def issueBook():
    memberID = int(request.form['memberid'])
    memberNameData = frapi.getMemberInformation(memberID)
    print(memberNameData)
    try:
        memberName = memberNameData['Member Name'].values[0]
        bookName = request.form['bookname']
        bookIDData = frapi.getBookInformation(bookName)
        bookID = bookIDData['bookID'].values[0]
    except:
        return render_template('invalid_details.html')
    
    column_names = ['Member ID', 'Member Name',  'Book ID', 'Book Name', 'Issue Date', 'Due Date']

    currentDate = today = date.today()
    dueDate = currentDate + timedelta(days=30)

    LibraryDuesData = [memberID, memberName, bookID, bookName, str(currentDate), str(dueDate)]

    issue_book = frapi.issueBookToMember(LibraryDuesData)

    if issue_book[0] == False:
        return render_template('issue_error.html', error = issue_book[1])
    
    print(LibraryDuesData)

    return render_template('successfull_book_issued.html')

@app.route("/getDues", methods=['GET', 'POST'])
def getDues():
    duesData = frapi.checkDues()

    print(type(duesData))

    return render_template('dues_page.html', tablesData=duesData)

@app.route("/returnBookPage", methods=['GET', 'POST'])
def returnBookPage():
    memberID = frapi.autocomplete(memberID=True)

    return render_template('issue_return_page.html', memberID=memberID)

@app.route("/checkReturn", methods=['GET', 'POST'])
def checkReturn():
    memberID = int(request.form['memberid'])

    duesData = frapi.fetchIssuedBooks(memberID)

    columnNames = list(duesData)
    values = duesData.values.tolist()

    print(columnNames)
    print(values)

    return render_template('select_return_page.html',  columnNames = columnNames, values = values)

@app.route("/returnBook", methods=['GET', 'POST'])
def returnBook():
    data = request.get_json() # retrieve the data sent from JavaScript
    # process the data using Python code

    print(f"Data is \n{data}")

    addBooksData = data[0]

    print(f"Books To Return are - {addBooksData}")

    output = frapi.returnBooks(memberID = int(addBooksData[0]), bookID = int(float(addBooksData[2])))

    fineFlag = output[1]
    fine = output[2]

    return render_template('successfull_return_page.html', fineFlag = fineFlag, fine = fine)

@app.route("/addMemberPage", methods=['GET', 'POST'])
def addMemberPage():
    
    return render_template('add_member.html')

@app.route("/addMember", methods=['GET', 'POST'])
def addMember():
    memberName = request.form['membername']
    memberAge = request.form['memberage']
    memberAddress = request.form['memberaddress']
    memberPhoneNumber = request.form['memberphonenumber']

    frapi.addMember(memberName, memberAge, memberAddress, memberPhoneNumber)
    return render_template('successfull_add_member.html')

@app.route("/getMembers", methods=['GET', 'POST'])
def getMembers():
    output = frapi.getMembers()
    print(type(output))

    columnNames = list(output)
    values = output.values.tolist()

    return render_template('members_database.html', columnNames=columnNames, values=values)

@app.route("/searchIssuedBooksPage", methods=['GET', 'POST'])
def searchIssuedBooksPage():
    bookName = frapi.autocomplete(bookName=True)

    return render_template('search_issued_books.html', bookName=bookName)

@app.route("/searchIssuedBook", methods=['GET', 'POST'])
def searchIssuedBook():
    bookName = request.form['bookname']

    bookDetails = frapi.getBookInformation(bookName)
    bookID = bookDetails['bookID'].values.tolist()

    output = frapi.checkBookIssueDetails(bookID[0])

    columnNames = list(output)
    values = output.values.tolist()

    return render_template('issued_book_details.html', columnNames=columnNames, values=values)

@app.route("/displayDues", methods=['GET', 'POST'])
def displayDues():
    output = frapi.displayDuesExceeded()

    columnNames = list(output)
    values = output.values.tolist()

    return render_template('display_dues.html', columnNames=columnNames, values=values)
    
app.run(host = "localhost", debug = True)

# ['8197', 'Writings to Young Women from Laura Ingalls Wilder: On Wisdom and Virtues (Writings to Young Women on Laura Ingalls Wilder #1)', 'Laura Ingalls Wilder/Stephen W. Hines', '3.99', '1400307848', '9781400307845', 'eng', '113', '108', '11', '5/10/2006', 'Tommy Nelson', '', '10']