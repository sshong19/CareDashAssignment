# CareDash Assignment

## Instrunctions on Running the Program
### Configuring Database
```console

foo@bar:~$ mysql -u root

```

```console

mysql > CREATE USER ‘care’@‘localhost’ IDENTIFIED BY ‘dash’
mysql > CREATE DATABASE caredashdb

```

### Running python script
```console

foo@bar:~$ python3 CareDash_REST_API.py

```

##Explanations on Design
###Data Modeling
I have built a simple GET and POST API that handles data from mysql database. I created a one to many relationship between Doctor model and Review model so that one doctor has relationship with many reviews. I have also set a back reference to doctor so that the doctor name and id can be returned when calling a single review. Apart from creating a unique key of the review, I have also added a review_id column so that the reviews don’t need a unique id along the doctors. For example, “Jane is a nice doctor. Review 1” and “John is a nice doctor. Review 1” can be created without having the duplicate error in the review ids. 

###Scalability
All posts/inserts of doctors and reviews are executed in time complexity of O(1). Query/search of the doctors or reviews are done in O(n). List of all doctors and reviews are done in O(n^2),  and list of all reviews in one doctor is done in O(n). Moreover, search of one review is done in O(n), if query in mysql performs in linear search. Also, scalability of the storage of data would depend on the size of the database. 
