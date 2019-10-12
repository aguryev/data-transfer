

class UserAgentMiddleware:
	#
	# a middleware class to save the User Agent within the system
	#

	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		response = self.get_response(request)

		# update User-Agent
		if request.user.is_authenticated:
			request.user.userinfo.user_agent = request.headers['User-Agent']
			request.user.userinfo.save()

		return response