import jinja2
import time
import configparser
import subprocess
import platform
import os
import re
import subprocess
os_type=os.uname().version
conf = configparser.ConfigParser()
pkg = 'apt-get'
pkgmode='install'
wget='wget'
aptkey='apt-key'
pathnginx='/etc/apt/sources.list.d/nginxpy.list'
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
    conf.add_section("nginx")
    conf.set('nginx', 'state-nginx', 'True')
    conf.set('nginx', 'repo', 'deb  [arch=amd64]  http://nginx.org/packages/mainline/ubuntu/  bionic  nginx , deb-src http://nginx.org/packages/mainline/ubuntu/ bionic nginx')
    conf.set('nginx','key',' http://nginx.org/keys/nginx_signing.key')
    conf.add_section("php")
    conf.set('php', 'state-php', 'True')
    conf.set('php','repo-php','sudo add-apt-repository ppa:ondrej/php')
    conf.set('php', 'version', '7.3')
    conf.add_section("php-fpm")
    conf.set('php-fpm', 'state-phpfpm', 'True')
    conf.set('php-fpm', 'version', '7.3')
    conf.add_section("php-modules")
    conf.set('php-modules', 'state-phpmodules', 'True')
    conf.set('php-modules', 'names', 'php7.3,php7.3-bcmath,php7.3-cli,php7.3-common,php7.3-curl,php7.3-dev,php7.3-fpm,php7.3-gd,php7.3-imap,php7.3-intl,php7.3-json,php7.3-mbstring,php7.3-mysql,php7.3-opcache,php7.3-readline,php7.3-recode,php7.3-soap,php7.3-tidy,php7.3-xml,php7.3-xmlrpc,php7.3-zip')
    conf.add_section("Dockerize")
    conf.set('Dockerize', 'state-Dockerize', 'False')
    with open('config.cfg','w') as configfile:
        conf.write(configfile)
    #read
    nginxstate = str(conf.get('nginx', 'state-nginx')).split(',')
    phpstate=  str(conf.get('php', 'state-php')).split(',')
    phpfpmstate= str(conf.get('php-fpm', 'state-phpfpm')).split(',')
    phpmodulestate=str(conf.get('php-modules', 'state-phpmodules')).split(',')
    dockerizestate= str(conf.get('Dockerize', 'state-Dockerize')).split(',')
    reponginx= str(conf.get('nginx', 'repo')).split(',')
    keynginx=str(conf.get('nginx', 'key')).split(',')
    phprepo=str(conf.get('php', 'repo-php')).split(',')
    phpversion=str(conf.get('php', 'version')).split(',')
    phpfpmv=str(conf.get('php-fpm', 'version')).split(',')
    phpm=str(conf.get('php-modules', 'names')).split(',')
    list=[nginxstate,phpstate,phpfpmstate,phpmodulestate,dockerizestate,phpm]
def checkapp():
    os=re.findall('ubuntu', os_type, re.IGNORECASE) ; os=str(os).replace('[',' ').replace("'",' ').replace(']','').lower()
    if 'ubuntu' not in os:
        print('your os is {user_os} ,this script does work only in ubuntu'.format(user_os=os_type))
        exit()
    #if 'True' in nginxstate or phpstate or phpfpmstate or phpmodulestate or dockerizestate :
    for j in range (len(list)):
            for i in range (len(list[j])):
                if phpstate[0] == 'True' or phpfpmstate[0] =='True' or nginxstate[0] =='True' or phpmodulestate[0]=='True':
                    nginx=subprocess.run(['which', '{app}'.format(app=list[j][i])],stdout=subprocess.DEVNULL)
                    if nginx.returncode != 0 and list[j][i] != 'True' and list[j][i] != 'False':
                         print('not found {app} '.format(app=list[j][i]))
    if nginxstate[0] == 'True':
         subprocess.Popen([wget ,'-P','/tmp', keynginx[0]])
         print('\n\n\n\nDownloading nginx-key...\n')
         time.sleep(10)
         subprocess.Popen(["mv /tmp/ng*.key /tmp/nginx.key"],shell=True)
         subprocess.Popen(["echo {reponginx} > {pathnginx}".format(pathnginx=pathnginx , reponginx=reponginx[0])],shell=True)
         subprocess.Popen(["echo {reponginx} >> {pathnginx}".format(pathnginx=pathnginx , reponginx=reponginx[1])],shell=True)
         subprocess.Popen([pkg, 'update', '-y'])
         subprocess.Popen([pkg, pkgmode, 'nginx', '-y'])
configuration()
checkapp()
