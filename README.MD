$ nano ~/.bashrc

export KHAN_USERNAME=username
export KHAN_PASSWORD=password
export db_host=host
export db_database=database
export db_user=user
export db_password=password
export KHAN_ACCOUNT=account_num

source ~/.bashrc


sudo apt update
sudo apt install postgresql postgresql-contrib
sudo service postgresql start
sudo -u postgres psql
CREATE USER kh_root WITH PASSWORD 'KH!@#123';
CREATE DATABASE khan OWNER myuser;
GRANT ALL PRIVILEGES ON DATABASE khan TO kh_root;
\q

sudo nano /etc/postgresql/14/main/postgresql.conf
listen_addresses = '*'

sudo nano /etc/postgresql/14/main/pg_hba.conf
host    all             all             0.0.0.0/0               md5
sudo service postgresql restart