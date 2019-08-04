# PhoGraphe
> Small picture gallery that highlight rare links between pictures. Each picture is tagged and two pictures are linked if and only if only few pictures contains the same common tags (basically).
> The software uses **Vue** for the frontend with **VisJS-network** to display the network, **Rust WASM** for frontend computations and **Django** for the backend.
***

## Prerequisites
* Static image hosting with SFTP access (see [How to Setup a SFTP user](#setup-sftp-user))
* Python Django for the backend
* Mysql Database or any other database supported by Django
* VueJS for the frontend

## Deployment

### Rust computations

Install **Rust** and **wasm-pack**
```bash
curl https://sh.rustup.rs -sSf | sh
curl https://rustwasm.github.io/wasm-pack/installer/init.sh -sSf | sh
```


### Frontend

1. **Install and build** the application
```bash
npm install
npm build
```

2. Create a **symbolic link** to serve the application
```bash
sudo ln -s  dist /var/www/<your domain>
```

### Backend - basics
1. Clone the **source code**
```bash
git clone https://github.com/Marc-AntoineA/NP.git
```

2. Install `virtual env` and the Python **requirements**
```bash
cd backend
sudo apt-get install python3-venv
python3 -m venv python_env
```

3. **Activate the virtual environment**
```bash
source python_env/bin/activate
deactivate # to deactivate the environent
```

4. **Install the requirements**
```bash
pip install requirements.txt
```

5. Edit the `backend/settings.py`
```python
DATABASES = {
    'default': {
      'ENGINE': 'django.db.backends.mysql',
      'NAME': 'phographebase',
      'USER': 'phographeuser',
      'PASSWORD': '',
      'HOST': 'localhost',
      'PORT': '1433'
    }
}
```

6. **Make migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

7. **Create a superuser**
```bash
python manage.py createsuperuser
```

8. **Start the server** (_testing purpose_)
```bash
python manage.py runserver 0.0.0.0:8000
```
The `0.0.0.0:8000` allows access to the server from outside.


### Backend - `mod_wsgi`

1. Install `mod_wsgi`

2. Install `mod_xsendfile`
```bash
sudo apt-get install libapache2-mod-xsendfile
sudo e2enmod xsendfile
```

### Conf files

### Start

## Helps


### Setup a static apache2 hosting

1. Create the directory into your `/var/www` repository.
```bash
mkdir <url>
```

### Setup a Mysql Database

1. **Install** and login into Mysql
2. **Create the dabase** and **setup the user** with **read and write** and only **local access** (if deployed on the same server than the backend)
```sql
CREATE DATABASE phographebase;
CREATE USER 'phouser'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON prographebase. * TO 'phographeuser'@'localhost';
FLUSH PRIVILEGES;
```
3. Setup the connection with Django

### Setup sftp User

To create the user `<username>` from the group `<user-group>` to have access only to `/var/www/<domain>` with the password you wants.

1. **Setup the user**
```bash
sudo apt-get install openssh-server
sudo groupadd <user-group>
sudo useradd -g <user-group> -d /var/www/<domain>/ -s /sbin/nologin <username>
```

> **Warning** If `-s /sbin/nologin` doesn't exist, use `/usr/sbin/nologin`

2. **Setup your password**
```bash
sudo passwd <username>
```

3. **Test if everything is fine**
```bash
cat /etc/passwd | grep <username>
```
_You should see something like_
```
<username>:x:1002:1002::/var/www/<domain>/:/sbin/nologin
```

4. **uae**

Nope Add permisions chown -R sftpuser:<user-group> /data/dirstatinfo/csvfiles

Configure ssh protocole
$ vim /etc/ssh/sshd_config

Subsystem sftp internal-sftp
Match Group <user-group>
ChrootDirectory /path/to/files
ForceCommand internal-sftp

Enable Chroot
setsebool -P ssh_chroot_rw_homedirs=1

Restart the ssh service
/etc/init.d/sshd restart

Be careful, the Chroot is on the main folder and the chown to the local user in the subfolders
