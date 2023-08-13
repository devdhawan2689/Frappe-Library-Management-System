# Frappe-Library-Management-System
This Repository Contains Code For the Frappe Flask Test. 

The Flask Website Does the Following Functions -
1. Add Books to The Database
2. Issue Books to Members
3. Return Books
4. Search for Books in the Database
5. Add Members
6. Get All Members Details From The Database
7. Search for Issued Books
8. Check Dues

For Each Request the Flask Server Sends Request to the FrappeAPI.py File. 
This File is responsible for interacting with the Frappe API and the Database for all operations. 
The reason to create seperate file for operatins is to make the code easier to run and understand. 

The CSV Files, 
1. Library_Books_Database.csv
2. Library_Dues_Database.csv
3. Library_Issue_Database.csv
4. Members_Database.csv
Are Used as The Database for the Flask Website.
(The Same can be done on an SQL Server or by using the SQLite3 Module for Python)

Home Page
![image](https://github.com/devdhawan2689/Frappe-Library-Management-System/assets/54425780/7bf963b9-0e69-4455-8e65-c837541de456)
