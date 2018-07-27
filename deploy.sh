# 1. 拉代码到 /var/www/bbs
# 2. 执行 bash deploy.sh

set -ex
deploy_directory=/var/www/web21

# 系统设置
apt-get -y install  zsh curl ufw
# sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
ufw allow 22
ufw allow 80
ufw allow 443
ufw allow 25
ufw default deny incoming
ufw default allow outgoing
ufw status verbose
ufw -f enable

# 装依赖
add-apt-repository -y ppa:deadsnakes/ppa
apt-get update

debconf-set-selections database_secret.conf
debconf-set-selections postfix.conf

apt-get install -y git supervisor nginx python3.6 mysql-server postfix
python3.6 /var/www/web21/get-pip.py
pip3 install jinja2 flask gevent gunicorn pymysql flask_sqlalchemy flask_mail flask_admin

# 删掉 nginx default 设置
rm -f /etc/nginx/sites-enabled/default
rm -f /etc/nginx/sites-available/default

# 建立一个软连接
ln -s -f /var/www/bbs/bbs.conf /etc/supervisor/conf.d/bbs.conf
# 不要再 sites-available 里面放任何东西
ln -s -f /var/www/bbs/bbs.nginx /etc/nginx/sites-enabled/bbs
chmod -R o+rwx /var/www/web21

# 重启服务器
service supervisor restart
service nginx restart

echo 'deploy success'