#!/usr/bin/env python
import web, api
import logging
from api.views import *

class redirect:
	""" 
		Find and redirect to existed controller with '/' or without it 
	"""
	def GET(self, path):
		web.seeother('/' + path)

urls = (
	"/(.*)/", 'redirect', # Handle urls with slash and without it
	"/query/notification", api.views.notifications.Notification, # API handler for notifications
	"/auth", api.views.authentication.Auth, # API to authenticate users
	
	"/query/messages", api.views.messages.Messages,
	"/token/manager", api.views.tokenManager.tokenManager,
	"/image/upload", api.views.images.ImageUpload, # API to upload images
	"/profile/mgl", api.views.profile.ManageGetList, 
)

web.config.debug = False

if __name__ == "__main__":
	app = web.application(urls, globals(), autoreload=True)
	app.run()
