# Database-web-front-project
Columbia University CS 4111 Intro to database project


if you run it on local host:
URL:
http://localhost:8111/

Update at 05/20/2019: you can not run this project now because the PostgreSQL server is out of date. So the Flask will not able to connect to the database for SQL commands.
But you can get a sense of the application by looking at my code.

## The function of this project
*Built searching functions that allows users to view different library information on books, DVDs, and journals. 

*Table Search allows users to view detailed information in table view.
	
*Location Search allows users to look up a book or DVD to see its location.

*Checkedbooks allows users to see what books a particular person has checked out

*University Search allows users to see all books at a particular school

## Some features about the project
* Server is writtend in Flask
* Database is POSTGRESQL
* Webpage are written in HTML format with Bootstrap format
## Screenshot of the webpages

![Image of the Website]
(./screen shot.png)


## The two most interesting operations
First I think the most interesting operation we have on our website is the Login function. 
	
While this search function is very straightforward, we believe it is through this function we learned the most. Our login function can be used by both the students and the librarians.
For students, we essentially run
	
	 
`SELECT * FROM students s where lower(s.name) = lower('{}') and lower(s.sid) = lower('{}')".format(str(username), str(passcode)))`
	
	
and for librarians, we run the database operation 
	
	
`SELECT * FROM librarian l where lower(l.name) = lower('{}') and l.ssn = '{}'".format(str(username), str(passcode)))`
	

 
The second interesting operations would be the Checked Book Search. 
For librarians, this is quite useful to determine the books a particular person has checked out. The SQL query below returns all books a person has checked out. 
	
	
`SELECT R.bookname FROM book R WHERE R.isbn IN(SELECT B.isbn FROM librarian L INNER JOIN checkout_book B ON L.ssn = B.ssn WHERE L.name = '{}')".format(str(name)))`
	
On the other hand, we believe the Checked Book Search is the most frequently used function for our database, helping users to locate their desired books or DVDs. We also managed to allow case insensitive searches for better search results and experience. 

 And we have also added some new features such as login and book search. We do not include insert functionality into our data base since we think the our page is built as primely for searching. 
