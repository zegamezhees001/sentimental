# EQUIPMENT

# create env

```
    conda create -n <name env> python=3.7.1 anaconda
    conda activate <name env>
    conda install -c anaconda django=2.2.3
    conda install -c bioconda mysqlclient
    pip install -r requirements.txt
```

# make migration

```
 python manage.py makemigration Team
 python manage.py makemigration Equipment
 python manage.py makemigration Users
 python manage.py makemigration SmsBackEnd
 python manage.py migrate

```

# try to run

```
    python manage.py runserver

```
