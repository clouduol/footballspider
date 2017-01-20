def error():
	try:
		print(10/0)
	except ZeroDivisionError as e:
		print(e)
	print("hello")
error()
