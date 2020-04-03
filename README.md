# Treebay

Treebay is a Django web app for classified plant advertisments.

## Steps for local deployment
1.	Create a folder for the project and make it current working directory
2.	Clone the GitHub repo in it
3.	Create a virtual environment with Python 3.7 and activate it (optional)
4.	Install required packages
```bash
pip install –r requirements.txt
```
5.	Make and run the migrations 
```bash
python manage.py makemigrations
python manage.py migrate
```
6.	Run the population script
```python
population_script.py
```
7.	Run the server 
```bash
python manage.py runserver
```
8.	You’re ready! 

## External Resources

- [jQuery](https://jquery.com/download/) was used extensively in interface implementation
  - [jquery-3.4.1.min.js](https://code.jquery.com/jquery-3.4.1.min.js)
