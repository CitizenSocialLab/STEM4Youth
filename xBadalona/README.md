# README #

## CitizenSocialLab: STEM4Youth xBadalona ##

Experiment designed and implemented to be run in **Badalona** in the framework of the European Project STEM4Youth (nº 710577). This is the result of a co-creation effort among the researchers of OpenSystems (UB) and Dymmons (UOC-IN3), and the students of Enric Borrás school (Badalona).

This participatory experiment consist on a set of dilemmas and behavioural games: **Prisoner's Dilemma, Trust Game and Dictator's Game** designed to shed light on the concerns of students of Enric Borrás school, particularly in gender inequalities and domestic violence. There are one Dictator's Game with Punishment measuring equity and social justice, Trust Game measuring trust and reciprocity and Prisoner's Dilemma measuring cooperation and defection, these games are played in group of 6 individuals.

## Data ##
**Vicens J, Cigarini A, Perelló J. Dataset STEM4Youth: Games xBadalona. 2018. doi:10.5281/zenodo.1308963**  

## Derived Scientific Publications ##
Cite main publication: **Vicens, J., Perelló, J., & Duch, J. (2018). Citizen Social Lab: A digital platform for human behaviour experimentation within a citizen science framework. arXiv preprint arXiv:1807.00037.**

*More publications currently in preparation.*

## Configuration ##
Steps are necessary to get xBadalona install, up and running in local network.

### Creation of the project ###

__Database MySQL__  
Create MySQL database: name\_db  
Create user database: user\_db  
Create password database: pass\_db

Introduce this information about the database in: `/xBadalona/settings.py`

__Environment__   
```mkvirtualenv jocstem ```  

__Requirements__  
```pip install -r requirements.txt```

__MongoDB__  
```mongod --dbpath /.../xBadalona/ddbb```

__Load text__   
File with text and translations:  `/.../xBadalona/game/i18n/translations.xlsx`  
   
```python excel_to_mongodb.py```

__Run Server__  
```python manage.py runserver localhost:port```

__Migrations__  
```python manage.py makemigrations```  
```python manage.py migrate```  

### Run project in Local ###

__Step 1: Run MySQL server__  
Run MySQL: `mysql.server start`

__Step 2: Open terminal tabs and work on the environment__  

in Tab 1: MongoDB  
in Tab 2: MySQL  
in Tab 3: Run Application  

Work on environment (in each terminal tab): `workon jocstem`

__Step 3: Run MongoDB (Tab 1)__  
Run mongodb: `mongod --dbpath /.../xBadalona/ddbb`

__Step 4: MySQL actions (Tab 2)__  
Directory: `cd /.../xBadalona/`   
Database: `mysql -u user_db -p (pass_db)`

Drop database: `drop database xBadalona;`  
Create database: `create database xBadalona;`  
Exit: `exit;`

Modification of fields of database: `python manage.py makemigrations`  
Refresh database:
`python manage.py migrate` 

__Step 5: Load texts (Tab 2)__    
Load translations: `python excel_to_mongodb.py`

__Step 6: Run Server (Tab 3)__  
Directory: `cd /.../xBadalona/ `   
Runserver: `python manage.py runserver localhost:port`


### Access client ###
Client application:  
**http://localhost:port/**  
 
Control and Administration:  
**http://localhost:port/admin**

## Versions ##
Version 1.0

## License ##
CitizenSocialLab | STEM4Youth (c) by Julian Vicens

CitizenSocialLab | STEM4Youth is licensed under a
Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.

You should have received a copy of the license along with this work. If not, see [CC BY-NC-SA license](https://creativecommons.org/licenses/by-nc-sa/4.0/)

## Contributors ##

[Julián Vicens](https://github.com/jvicens)

## Contact ##

Julian Vicens: **julianvicens@gmail.com**
