#!/usr/bin/env python
import web
import logging

import api.views.base
import api.views.notifications


class redirect:
	""" 
		Find and redirect to existed controller with '/' or without it 
	"""
	def GET(self, path):
		web.seeother('/' + path)

urls = (
	"/(.*)/", 'redirect', # Handle urls with slash and without it
	"/query/notification", api.views.notifications.Notification, # API handler for notifications
)
web.config.debug = True
app = web.application(urls, globals(), autoreload=True)

if __name__ == "__main__":
	app.run()
