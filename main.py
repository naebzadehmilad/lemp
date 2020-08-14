from jinja2 import Template
import configparser
import os
import re
import subprocess
import time
os_type = os.uname().version
conf = configparser.ConfigParser()
pkg = 'apt-get'
pkgmode = 'install'
wget = 'wget'
aptkey = 'apt-key'
addrepo = ' add-apt-repository '
pathnginx = '/etc/apt/sources.list.d/nginxpy.list'


def configuration():
    global nginxstate
    global phpstate
    global phpfpmstate
    global phpfpmstate
    global phpmodulestate
    global dockerizestate
    global reponginx
    global keynginx
    global phprepo
    global phpversion
    global phpfpmv
    global phpm
    global list
    global vhoststate
    global vhostsslstate
    global vhostport
    global vhosthost
    global vhostpath
    global vhostremoteaddr
    global vhostssl
    global vhostsslkey
    global nginxconfstate
    global nginxconfuser
    global nginxconfsectag
    global nginxconfclientbodysize
    global nginxconfgzip
    if os.path.exists('config.cfg'):
            print('##config.cfg is exist##')
    else:
        conf.add_section("nginx")
        conf.set('nginx', 'state-nginx', 'True')
        conf.set('nginx', 'app', 'nginx')
        conf.set('nginx', 'repo',
             'deb  [arch=amd64]  http://nginx.org/packages/mainline/ubuntu/  bionic  nginx , deb-src http://nginx.org/packages/mainline/ubuntu/ bionic nginx')
        conf.set('nginx', 'key', ' http://nginx.org/keys/nginx_signing.key')
        conf.add_section("php")
        conf.set('php', 'state-php', 'True')
        conf.set('php', 'repo-php', ' ppa:ondrej/php')
        conf.set('php', 'app', 'php7.3')
        conf.add_section("php-fpm")
        conf.set('php-fpm', 'state-phpfpm', 'True')
        conf.set('php-fpm', 'app', 'php7.3-fpm')
        conf.add_section("php-modules")
        conf.set('php-modules', 'state-phpmodules', 'True')
        conf.set('php-modules', 'names',
             'php7.3,php7.3-bcmath,php7.3-cli,php7.3-common,php7.3-curl,php7.3-dev,php7.3-fpm,php7.3-gd,php7.3-imap,php7.3-intl,php7.3-json,php7.3-mbstring,php7.3-mysql,php7.3-opcache,php7.3-readline,php7.3-recode,php7.3-soap,php7.3-tidy,php7.3-xml,php7.3-xmlrpc,php7.3-zip')
        conf.add_section("Dockerize")
        conf.set('Dockerize', 'state-Dockerize', 'False')
        conf.add_section('nginx.conf')
        conf.set('nginx.conf', 'state', 'True')
        conf.set('nginx.conf', 'user', 'www-data')
        conf.set('nginx.conf', 'sectag', 'True')
        conf.set('nginx.conf', 'maxclientbodysize', '32M')
        conf.set('nginx.conf', 'gzip', 'True')
        conf.add_section('vhost')
        conf.set('vhost', 'state', 'True')
        conf.set('vhost', 'ssl', 'True')
        conf.set('vhost', 'port', '443')
        conf.set('vhost', 'hostname', 'example')
        conf.set('vhost', 'hostpath', '/var/www/html')
        conf.set('vhost', 'remoteaddr', '192.168.10.0/24')
        conf.set('vhost', 'ssl_certificate', '/etc/ssl/full.crt')
        conf.set('vhost', 'ssl_certificate_key', '/etc/ssl/privkey.key')
        with open('config.cfg', 'w') as configfile:
            conf.write(configfile)
    # read
    conf.read('config.cfg')
    nginxstate = str(conf.get('nginx', 'state-nginx')).split(',')
    nginx = str(conf.get('nginx', 'app')).split(',')
    phpstate = str(conf.get('php', 'state-php')).split(',')
    phpfpmstate = str(conf.get('php-fpm', 'state-phpfpm')).split(',')
    phpmodulestate = str(conf.get('php-modules', 'state-phpmodules')).split(',')
    dockerizestate = str(conf.get('Dockerize', 'state-Dockerize')).split(',')
    reponginx = str(conf.get('nginx', 'repo')).split(',')
    keynginx = str(conf.get('nginx', 'key')).split(',')
    phprepo = str(conf.get('php', 'repo-php')).split(',')
    phpversion = str(conf.get('php', 'app')).split(',')
    phpfpmv = str(conf.get('php-fpm', 'app')).split(',')
    phpm = str(conf.get('php-modules', 'names')).split(',')
    vhoststate = str(conf.get('vhost', 'state')).split(',')
    vhostsslstate = str(conf.get('vhost', 'ssl')).split(',')
    vhostport = str(conf.get('vhost', 'port')).split(',')
    vhosthost = str(conf.get('vhost', 'hostname')).split(',')
    vhostpath = str(conf.get('vhost', 'hostpath')).split(',')
    vhostremoteaddr = str(conf.get('vhost', 'remoteaddr')).split(',')
    vhostssl = str(conf.get('vhost', 'ssl_certificate')).split(',')
    vhostsslkey = str(conf.get('vhost', 'ssl_certificate_key')).split(',')
    nginxconfstate = str(conf.get('nginx.conf', 'state')).split(',')
    nginxconfuser = str(conf.get('nginx.conf', 'user')).split(',')
    nginxconfsectag = str(conf.get('nginx.conf', 'sectag')).split(',')
    nginxconfclientbodysize = str(conf.get('nginx.conf', 'maxclientbodysize')).split(',')
    nginxconfgzip = str(conf.get('nginx.conf', 'gzip')).split(',')

    list = [nginx, nginxstate, phpstate, phpfpmstate, phpmodulestate, dockerizestate, phpm]


def checkapp():
    os = re.findall('ubuntu', os_type, re.IGNORECASE);
    os = str(os).replace('[', ' ').replace("'", ' ').replace(']', '').lower()
    if 'ubuntu' not in os:
        print('your os is {user_os} ,this script does work only in ubuntu'.format(user_os=os_type))
        exit()
    # if 'True' in nginxstate or phpstate or phpfpmstate or phpmodulestate or dockerizestate :
    for j in range(len(list)):
        for i in range(len(list[j])):
            if phpstate[0] == 'True' or phpfpmstate[0] == 'True' or nginxstate[0] == 'True' or phpmodulestate[
                0] == 'True':
                check = subprocess.run(['which', '{app}'.format(app=list[j][i])], stdout=subprocess.DEVNULL)
                if check.returncode != 0 and list[j][i] != 'True' and list[j][i] != 'False':
                    print('not found {app} '.format(app=list[j][i]))


def install():
    if nginxstate[0] == 'True':
        subprocess.Popen([wget, '-P', '/tmp', keynginx[0]])
        print('\n\n\n\nDownloading nginx-key...\n')
        time.sleep(10)
        subprocess.Popen(["mv /tmp/ng*.key /tmp/nginx.key"], shell=True)
        subprocess.Popen(["echo {reponginx} > {pathnginx}".format(pathnginx=pathnginx, reponginx=reponginx[0])],
                         shell=True)
        subprocess.Popen(["echo {reponginx} >> {pathnginx}".format(pathnginx=pathnginx, reponginx=reponginx[1])],
                         shell=True)
        subprocess.Popen([pkg, 'update', '-y'])
        subprocess.Popen([pkg, pkgmode, 'nginx', '-y'])
    if phpstate[0] == 'True':
        subprocess.Popen(["{addrepo}   {phprepo} -y".format(addrepo=addrepo, phprepo=phprepo[0])], shell=True)
        for i in range(len(phpm)):
            subprocess.Popen(["{pkg} {pkgmode} -y  {php} ".format(pkg=pkg, pkgmode=pkgmode, php=phpm[i])], shell=True)
    if phpfpmstate[0] == 'True':
        subprocess.Popen(["{pkg} {pkgmode} -y  {phpfpm} ".format(pkg=pkg, pkgmode=pkgmode, phpfpm=phpfpmv[0])],
                         shell=True)


def nginxconf():
    f = open('nginx.conf', "w")
    template = Template("""
user          {{user}} ;
pid                  /run/nginx.pid;
worker_processes     {{workerprocess}};
worker_rlimit_nofile 65535;

events {
    multi_accept       on;
    worker_connections 65535;
    use epoll;
}

http {

    upstream php {
        server unix:/var/run/php/php7.3-fpm.sock;
        server unix:/var/run/php/php7.3-fpm.sock backup;
    }
{% if sectag == 'on' %}
add_header X-XSS-Protection          "1; mode=block" always;
server_tokens off;
location ~ /\.(?!well-known) {
    deny all;
}
{% endif %}

    charset              utf-8;
    sendfile             on;
    tcp_nopush           on;
    tcp_nodelay          on;
    log_not_found        off;
    types_hash_max_size  2048;
    client_max_body_size {{clientbodysize}};

    # MIME
    include              mime.types;
    default_type         application/octet-stream;

    # Logging
    access_log           /var/log/nginx/access.log;
    error_log            /var/log/nginx/error.log warn;

 {%if gzip == 'on' %}
    # Gzip Settings
    gzip on;
    gzip_min_length 10240;
    gzip_comp_level 1;
    gzip_buffers 16 8k;
    gzip_vary on;
    gzip_disable msie6;
    gzip_types
        # text/html is always compressed by HttpGzipModule
        text/css
        text/javascript
        text/xml
        text/plain
        text/x-component
        application/javascript
        application/x-javascript
        application/json
        application/xml
        application/rss+xml
        application/atom+xml
        font/truetype
        font/opentype
        application/vnd.ms-fontobject
        image/svg+xml;
{%endif%}

    # SSL
    ssl_session_timeout  1d;
    ssl_session_cache    shared:SSL:10m;
    ssl_session_tickets  off;

    # Diffie-Hellman parameter for DHE ciphersuites
    ssl_dhparam          /etc/nginx/dhparam.pem;

    # Mozilla Intermediate configuration
    ssl_protocols        TLSv1.2 TLSv1.3;
    ssl_ciphers          ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384;

    # OCSP Stapling
    ssl_stapling         on;
    ssl_stapling_verify  on;
    resolver             1.1.1.1 1.0.0.1 8.8.8.8 8.8.4.4 208.67.222.222 208.67.220.220 valid=60s;
    resolver_timeout     2s;

    # Load configs
    include              /etc/nginx/conf.d/*.conf;
    include              /etc/nginx/sites-enabled/*;
}""")
    f.write(template.render(user=nginxconfuser[0], sectag=nginxconfsectag[0], clientbodysize=nginxconfclientbodysize[0],
                            gzip=nginxconfgzip[0]))
    f.close()


def vhostconf():
    f = open('{hostname}.conf'.format(hostname=vhosthost[0]), "w")
    template = Template("""
    server {
	listen 443  ssl http2; 
         server_name host;
	listen [::]:443 ssl http2 ;
        root path;
set_real_ip_from 192.168.10.0/24; # Ip/network of the reverse proxy (or ip received into REMOTE_ADDR)
real_ip_header X-Forwarded-For;
        ssl_certificate /etc/ssl-new/full.crt;
        ssl_certificate_key /etc/ssl-new/privkey.key;
ssl_stapling on;
ssl_stapling_verify on;
ssl_trusted_certificate /etc/ssl-new/full.crt;
resolver 8.8.8.8 4.2.2.3 valid=200s;
resolver_timeout 40s;
ssl_session_cache shared:SSL:20m;
ssl_session_timeout 1d;
ssl_prefer_server_ciphers on;
ssl_ciphers 'EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH'; 
ssl_session_tickets off;
ssl_protocols TLSv1.2 TLSv1.3;
ssl_buffer_size 64k;
	index index.php index.html index.htm index.nginx-debian.html;

	server_name _;

location /uploads {
           index index.php index.html;

        if (!-e $request_filename)
        {
                rewrite ^/(.+)$ /index.php last;
        }
  try_files $uri $uri/ =404;

    client_max_body_size 1M;
} 



location / {
           index index.php index.html;

        if (!-e $request_filename)
        {
                rewrite ^/(.+)$ /index.php last;
        }
  try_files $uri $uri/ =404;

}

	location ~ \.php$ {
limit_req zone=dos burst=3 nodelay   ; 
 limit_req_status 403;


                           include snippets/fastcgi-php.conf;
                fastcgi_pass  unix:/run/php/php7.3-fpm.sock;

	}

	location ~ /\.ht {
		deny all;
	}

}""")
    f.write(template.render())
    f.close()


# open_file_cache          max=2000 inactive=20s;
# open_file_cache_valid    60s;
# open_file_cache_min_uses 2;
# open_file_cache_errors   off;
def dockerize():
    if dockerizestate[0] == 'True':
        f = open('dockerfile-nginx', "w")
        template = Template("""
        FROM ubuntu
        RUN apt-get update \
        && apt-get install -y software-properties-common \
        && apt-add-repository -y ppa:nginx/stable \
        &&  add-apt-repository  -y ppa:ondrej/php \
        && apt-get update \
        && apt-get install -y nginx php7.3 php7.3-bcmath php7.3-cli php7.3-common php7.3-curl php7.3-dev php7.3-fpm php7.3-gd php7.3-imap php7.3-intl php7.3-json php7.3-mbstring php7.3-mysql php7.3-opcache php7.3-readline php7.3-recode php7.3-soap php7.3-tidy php7.3-xml php7.3-xmlrpc php7.3-zip \
        && rm -rf /var/lib/apt/lists/*
        #ADD nginx/nginx.conf /etc/nginx/nginx.conf
        #ADD nginx/conf.d/default.conf /etc/nginx/conf.d/default.conf

        #ADD data/www /data/www

        RUN rm /etc/nginx/sites-enabled/default

        RUN ln -sf /dev/stdout /var/log/nginx/access.log \
        && ln -sf /dev/stderr /var/log/nginx/error.log

        EXPOSE 80 443

        CMD ["nginx", "-g", "daemon off;"]    
    
""" )
        f.write(template.render())
        f.close()
configuration()
vhostconf()
nginxconf()
dockerize()
# checkapp()
# install()
