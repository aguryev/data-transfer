
def store_file(source, destination_file_name):
	#
	# save source file to destination_file_name location
	#
	with open(destination_file_name, 'wb+') as f:
		for chunk in source.chunks():
			f.write(chunk)

