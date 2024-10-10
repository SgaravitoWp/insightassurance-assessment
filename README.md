# Insight Assurance Assessment

In the following directory, you will find the maximum progress on the Insight Assurance technical assessment.

To access the documentation provided by Swagger, please navigate to the **`/documentation`** endpoint.

It is important to note that the technical assessment is not yet complete, and several details related to organization, architecture, and validation are still missing. However, the application meets the minimum requirements specified.

To address the problem presented, a REST API was developed using the Flask framework. Each of its endpoints is designed with intuitive notation that facilitates the understanding of the tasks requested in the technical assessment.

The recommendation not to use GPT was taken into consideration; however, it was employed to generate better documentation. Everything has been thoroughly reviewed.

# Running the Application

To run the application, follow these steps:

## 1. Create and Activate Virtual Environment

Create a virtual environment to isolate the application dependencies. 

```
python -m venv name_of_the_environment
name_of_the_environment\Scripts\activate
```
### 2.  Install Dependencies

Install the required dependencies using the requirements.txt file:
```
pip install -r requirements.txt
```

### 3.  Migrate Database

Subsequently, to initiate and migrate the database 
```
flask db init
flask db migrate
flask db upgrade
```

### 4.  Run the Application

Finally, run the application with the following command:
```
flask run
```


