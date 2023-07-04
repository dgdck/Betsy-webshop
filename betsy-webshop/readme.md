You need to master the following to complete this assignment:

+ Writing functions and function arguments;
+ SQL joins;
+ Database modelling;

It is time to put all your SQL knowledge to the test. You will design a database for a fictional web marketplace called Betsy. Betsy is a site where people can sell homemade goods. This assignment will test your skills in modelling data as well as using the peewee ORM. The requirements for this assignment can be split into 2 parts: Modelling and Querying.

___
### Modelling

Define your models and initialize the database in models.py

A key part of the Betsy webshop is the database. At its core are the users and the products they offer:


+ A user has a name, address data, and billing information.


+ Each user must be able to own a number of products.


+ The products must have a name, a description, a price per unit, and a quantity describing the amount in stock.


+ The price should be stored in a safe way; rounding errors should be impossible.


+ The tags should not be duplicated.


+ We want to be able to track the purchases made on the marketplace, therefore a transaction model must exist


+ You can assume that only users can purchase goods


+ The transaction model must link a buyer with a purchased product and a quantity of purchased items

As a **bonus** requirement, you must consider the various constraints for all fields and incorporate these constraints in the data model. 

___
### Querying

In order to manage the database, the webshop must have a number of querying utlities. The scaffolding for the utilities can be found in main.py Extend the methods with the relevant functionality.

In this first iteration of the database we want to be able to:


+ Search for products based on a term. Searching for 'sweater' should yield all products that have the word 'sweater' in the name. This search should be case-insensitive


+ View the products of a given user.


+ View all products for a given tag.


+ Add a product to a user.


+ Remove a product from a user.


+ Update the stock quantity of a product.


+ Handle a purchase between a buyer and a seller for a given product

___
### Test data

To test if your database and queries are working we want to be able to populate the database with data quickly. 


+ Add a populate_test_database function that fills the database with example data that works with your queries

___
### Bonus

In the next phase of development, the search functionality of the betsy webshop should be optimized. 


+ The search should target both the name and description fields.


+ Additionally the products should be indexed so that the time spent on querying them is minimized.


+ Finally the search should account for spelling mistakes made by users and return products even if a spelling error is present