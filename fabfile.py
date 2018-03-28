#!/usr/bin/env python
# -*- coding: utf-8 -*-

# krylova hugo  standard routines file

# import section
from fabric.api import *

def prepare_deploy():
	print("Clean public folder")
	local("rm -rf ./public/*")
	local("hugo -v -t vogue")

def tar_site():
	with lcd("public"):
		local('tar cjf ../../krylova2.tar.bz2 .')

def send_xserve():
	put("../krylova2.tar.bz2", "~/")
	local("rm -rf ../krylova2.tar.bz2")

def unpak_xserve():
	with cd("/var/www/krylova2/public_html"):
		sudo("rm -rf *")
		sudo("tar xjf ~/krylova2.tar.bz2")
		sudo("chown -R www-data:root *")
		run("rm -rf ~/krylova2.tar.bz2")


# deploy site to test server
def deploy_xserve():
	prepare_deploy()
	tar_site()
	send_xserve()
	unpak_xserve()

# deploy to main server
def deploy_git():
	prepare_deploy()
	with lcd("public"):
		local('git add --all .')
		local('git commit -m "Site update"')
		local('git push')

def deploy():
	env.hosts = ['xserve.kolesnichenko.com']
	prepare_deploy()
	local('rsync -avz -e ssh --progress --delete public/ xserve.kolesnichenko.com:~/krylova.com/')
	sudo('rsync -avz -delete krylova.com/ /var/www/krylova2/public_html/')
	sudo('chown -R www-data:root /var/www/krylova2')
