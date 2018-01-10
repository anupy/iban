## Docker Installation ##

- Docker installation on ubuntu https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-16-04

- Docker installation on mac https://docs.docker.com/docker-for-mac/install/#install-and-run-docker-for-mac

- Docker installation on windows https://docs.docker.com/toolbox/toolbox_install_windows/#step-3-verify-your-installation 

- To donwload Docker image, please use link http://progfeel.co.in/iban/iban.tar

- After installation of docker please ensure docker service is running. Once it is confirmed, import image into it `docker load < iban.tar`

- To list all available images Run command : `docker images`
    - It will list all the available images of the system. Our imported image details are

| REPOSITORY    | TAG           | IMAGE ID     |
| ------------- |:-------------:| -----:       |
| be5a177f67c9  | latest        | 7a1253b9d0fb |

- Now run the docker container and connect ports on which docker services are running with ports of host machine using following command.
- `docker run -i -t -p 8000:8000 -p 8001:8001 -p 8002:8002 -p 8003:8003 -p 8004:8004 be5a177f67c9:latest /bin/bash`

- **be5a177f67c9** is repository name and latest is tag name.

- Docker imported image [id] may be different one. Please find image id of uploaded image from `docker images` command and use in below command

- `docker run -i -t -p 8000:8000 -p 8001:8001 -p 8002:8002 -p 8003:8003 -p 8004:8004 imageID /bin/bash` [For more clarification](http://progfeel.co.in/iban/imageidclarification.png)  

- You will land into the container. Now check postgresql status.  `service postgresql status`

- If it is not running, run it using `service postgresql start`

- If virtual environment **iban** is not active then enable it using following command.

- `workon iban`

- `Run python server`

- `cd /root/iban`

- `python manage.py runserver 0.0.0.0:8000`

- `cd /root/iban2`

- `python manage.py runserver 0.0.0.0:8001`

- `cd /root/iban3`

- `python manage.py runserver 0.0.0.0:8002`

- `cd /root/iban4`
- `python manage.py runserver 0.0.0.0:8003`

- `cd /root/iban5`

- `python manage.py runserver 0.0.0.0:8004`

- Now exit container but make it running. `ctrl p + q` (three keys ctrl p and q)

- Now open browser and run 

http://localhost:8000 (dev1)
superuser credentials are : anupy27 / Splendornet@123

http://localhost:8001 (dev2)
superuser credentials are : anupy27 / Splendornet@123

http://localhost:8002 (dev3)
superuser credentials are : anupy27 / Splendornet@123

http://localhost:8003 (dev4)
superuser credentials are : anupy27 / Splendornet@123

http://localhost:8004 (dev5)
superuser credentials are : anupy27 / Splendornet@123

# iban
## Django application to manage (CRUD) users and their bank account data (IBAN).

### (All below steps are already completed in docker image so no need to follow anything. It is already followed in docker image.) ###
### But to know working environment [Please check this](https://github.com/anup-splendornet/iban/tree/dev1#following-are-the-steps-to-check-working-environment)

- Require Python 3.x 

- git clone from github `git clone https://github.com/anupy/iban.git dev1`

- Setup virtualenvwrapper Ref: [https://virtualenvwrapper.readthedocs.io/en/latest/](https://virtualenvwrapper.readthedocs.io/en/latest/)

- We can alias to Python in my case it is python3 to execute version 3

- `alias python3='/usr/bin/python3'`

- `sudo apt-get -y install python3-pip` One time only

- `pip install virtualenvwrapper` OR `pip3 install virtualenvwrapper` pip3 is soft link / alias.

- `export WORKON_HOME=~/Envs`

- `mkdir -p $WORKON_HOME`

- `source /usr/local/bin/virtualenvwrapper.sh` This can achieved using Ref: [https://stackoverflow.com/questions/21928555/virtualenv-workon-command-not-found](https://stackoverflow.com/questions/21928555/virtualenv-workon-command-not-found)

- `mkvirtualenv iban`

- `pip3 install django==1.11`

- Daily we need only to fire command like `workon iban` to enter specific python version to execute code.

- Ensure Django version by typing `python -m django --version`

- django-admin startproject ibanapp Ref: [https://docs.djangoproject.com/en/1.11/intro/tutorial01/](https://docs.djangoproject.com/en/1.11/intro/tutorial01/)

- Now install postgresql 9.3.x using `apt-get install postgresql` 

- To check installation and version fire command `psql --version`

- Once setup is done, create database in postgres called **iban** 

- Set username and password for database **iban**

- Now run migrate command to set initial database with tables. `python manage.py migrate`

- Now we have added model called IbanDetails and altered email field to unique to add this change into database fire below commands.

- `python manage.py makemigrations`

- `python manage.py makemigrations ibanmanagment` (To ensure, otherwise first command get all the migrations)

- `python manage.py makemigrations oauth` (To ensure, otherwise first command get all the migrations)

- `python manage.py migrate`

- We will create supreadmin through command line.

- Command would be `python manage.py createsuperuser --username=anupy27 --email=anupy27@gmail.com` now you'll will requested to add password of 8 characters.

- Superadmin will have all access, so we will create group called **admin** with permission of **add**, **edit**, **delete** of **iban_details**. (This is important)
-                                                       ##### OR #####
- To autoload permissions and create group through command line instead of creating from superuser, please fire below command.

- `python manage.py loaddata oauth/fixtures/permission_group.json` It will return text as **Installed 4 objects from 1 fixture.**   

## Following are the steps to check working environment. ##

- `python manage.py runserver`
    ##### OR #####
- `python manage.py runserver 0.0.0.0:8000` To run on specific port.
    ##### OR #####
- `python manage.py runserver 0.0.0.0:8000 --settings=iban.settings` to run on specific port and with specific settings.

- Supreadmin call login through [http://127.0.0.1:8000/admin/login/] (http://127.0.0.1:8000/admin/login/) URL.

- Now [http://127.0.0.1:8000/](http://127.0.0.1:8000/) here will ask Administrator to to come and register yourself.

- Administrator will be registered from Gmail but activation would be done from SuperAdmin only. 

- If Administrator is already registered and activated then he will be allowed to login to website else appropriate message will be shown (Activation or Non admin).  

- If Administrator access is already assigned to user through code, then Superadmin won't need to assign admin group / permissions to that user else he need to assign explicitely.

- While Authenticating through Google OAuth if email is exists in database but **admin** access is not then he will not be allowed to enter into website.

- Once everything is fine and Administrator got authenticated he will redirected to Dashboard to manage CRUD of iban_details.

- He can logout through website using logout link, logout through gmail won't affect to our website.

## Unit test cases ##

##### To run all test cases run following command #####
`python manage.py test oauth.tests.OauthTestCase.run_all_test`

##### To run test case where new user / email got registered #####
`./manage.py test oauth.tests.OauthTestCase.check_account_exist_or_create_test_new_user`

##### To run test case where user is active and admin or superadmin OR new creation #####
`./manage.py test oauth.tests.OauthTestCase.check_account_exist_or_create_test`

##### To run test case where user is active #####
`./manage.py test oauth.tests.OauthTestCase.check_account_exist_or_create_test_is_active`

##### To run user is superadmin #####
`./manage.py test oauth.tests.OauthTestCase.check_account_exist_or_create_test_is_superadmin`

##### To run user is admin #####
`./manage.py test oauth.tests.OauthTestCase.check_account_exist_or_create_test_is_admin`

##### To run model of IbanDetails #####
`./manage.py test ibanmanagment.tests.tests_model.IbanModelTestCase.test_iban_details_model`

##### To run model of IbanDetails, should return iban number in string format #####
`./manage.py test ibanmanagment.tests.tests_model.IbanModelTestCase.test_str_is_equal_to_iban_number`

##### To run form working positive test #####
`./manage.py test ibanmanagment.tests.tests_form.IbanFormTestCase.test_form_success`

##### To run form working negative test #####
`./manage.py test ibanmanagment.tests.tests_form.IbanFormTestCase.test_form_error`

##### To run form working negative test #####
`./manage.py test ibanmanagment.tests.tests_form.IbanFormTestCase.test_form_error`

##### To check permission on iban numbers listing #####
`./manage.py test ibanmanagment.tests.tests_list_views.IbanViewTestCase.dashboard_negative_test`

##### To check iban numbers listing count must be 3 #####
`./manage.py test ibanmanagment.tests.tests_list_views.IbanViewTestCase.dashboard_list_test`

##### To check iban numbers listing count must be 0 #####
`./manage.py test ibanmanagment.tests.tests_list_views.IbanViewTestCase.dashboard_no_list_test`

##### To check iban numbers create, update, delete access level permission #####
`./manage.py test ibanmanagment.tests.tests_create_update_delete_views.IbanCreateUpdateDeleteViewTestCase.iban_create_update_delete_test_permission`

##### To check iban numbers create, update, delete access and manupulation level permissions #####
`./manage.py test ibanmanagment.tests.tests_create_update_delete_views.IbanCreateUpdateDeleteViewTestCase.iban_create_update_delete_test_valid`