# learn_django

### 1.MacOS基础环境
```bash
//brew install
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
brew update

//mysql install
brew install mysql

//redis install
brew install redis

//tree install
brew install tree

//command alias
sed -ie /tree/d ~/.bash_profile
sed -ie /ls/d ~/.bash_profile
echo "alias tree='tree -N'"|tee -a ~/.bash_profile
echo "alias ll='ls -l'"|tee -a ~/.bash_profile

//pip source
mkdir -p ~/.pip
cat > ~/.pip/pip.conf <<EOF
[global]
trusted-host=mirrors.aliyun.com
index-url=http://mirrors.aliyun.com/pypi/simple/
[list]
format=columns
EOF

//git config
git config --global user.name "penn"
git config --global user.email "smallasa@sina.com"
git config --global push.default simple
git config --global core.quotepath false
git config --global credential.helper store --file=.git-credentials
git config --global core.editor vim
git config --global merge.tool vimdiff

//pip3 install Django
pip3 install Django==1.11

//pip3 install mysqlclient
brew uninstall mysql
brew install mysql-connector-c

vim /usr/local/bin/mysql_config
将：
libs="-L$pkglibdir"
libs="$libs -l "
改为：
libs="-L$pkglibdir"
libs="$libs -lmysqlclient -lssl -lcrypto"

vim ~/.bash_profile
export LDFLAGS="-L/usr/local/opt/openssl/lib"
export CPPFLAGS="-I/usr/local/opt/openssl/include"

pip3 install mysqlclient

brew link --overwrite mysql

//mysql start
mysql.server start
mysql -uroot
```

### 2.Django基础环境
```bash
liupengdeMacBook-Pro:~ liupeng$ python3 -V
Python 3.6.6

liupengdeMacBook-Pro:~ liupeng$ pip3 -V
pip 18.0 from /Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/pip (python 3.6)

liupengdeMacBook-Pro:~ liupeng$ pip3 list
Package     Version
----------- -------
Django      1.11
mysqlclient 1.3.13
pip         18.0
pytz        2018.5
setuptools  40.4.3


liupengdeMacBook-Pro:~ liupeng$ mysql -uroot
mysql> select version();
+-----------+
| version() |
+-----------+
| 8.0.12    |
+-----------+
mysql> create database website;
mysql> create user 'website'@'localhost' identified by 'websitepass';
mysql> grant all privileges on website.* to 'website'@'localhost';
mysql> flush privileges;
mysql> show grants for 'website'@'localhost';
+--------------------------------------------------------------+
| Grants for website@localhost                                 |
+--------------------------------------------------------------+
| GRANT USAGE ON *.* TO `website`@`localhost`                  |
| GRANT ALL PRIVILEGES ON `website`.* TO `website`@`localhost` |
+--------------------------------------------------------------+
liupengdeMacBook-Pro:~ liupeng$ mysql -uwebsite -pwebsitepass -hlocalhost -P3306 -e "show databases;"
mysql: [Warning] Using a password on the command line interface can be insecure.
+--------------------+
| Database           |
+--------------------+
| information_schema |
| website            |
+--------------------+
注意：mysql 8.0 使用如下方法授权是错误的
grant all privileges on website.* to 'website'@'localhost' identified by 'websitepass' with grant option;
```