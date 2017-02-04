from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
prev_val = 0
curr_val = 0
prev_operator = '+'
display = 0
is_equal = False
equation = []
double_operator = False

def home_page(request):
	display_val = 0
	return render(request, 'calculator/calculator.html', {'display_val': 0})
	
def calculator(request):
	global curr_val
	global is_equal
	global double_operator
	global prev_operator
	global prev_val
	if 'number' in request.POST: #everytime you refresh create a post!
		print request.POST['number']
		is_equal = False
		double_operator = False
		if curr_val == 0:
			curr_val = int(request.POST['number'])
			print "one number"
			return render(request, 'calculator/calculator.html', {'display_val': curr_val, 'curr_val': curr_val})
		else:
			curr_val = curr_val * 10 + int(request.POST['number'])
			print "two or more number"
			return render(request, 'calculator/calculator.html', {'display_val': curr_val, 'curr_val': curr_val})
	
	if ('sign' in request.POST) and (not double_operator): #if the input is '=', calculate and initialize the calculator
		if prev_operator == '+':
			result = prev_val + curr_val
			prev_operator = request.POST['sign']
			prev_val = result
			curr_val = 0
			return render(request, 'calculator/calculator.html', {'display_val': result, 'curr_val': curr_val, 'prev_val': prev_val, 'prev_operator': prev_operator})
		elif prev_operator == '-':
			result = prev_val - curr_val
			prev_operator = request.POST['sign']
			prev_val = result
			curr_val = 0
			return render(request, 'calculator/calculator.html', {'display_val': result, 'curr_val': curr_val, 'prev_val': prev_val, 'prev_operator': prev_operator})
		elif prev_operator == '*':
			result = prev_val * curr_val
			prev_operator = request.POST['sign']
			prev_val = result
			curr_val = 0
			return render(request, 'calculator/calculator.html', {'display_val': result, 'curr_val': curr_val, 'prev_val': prev_val, 'prev_operator': prev_operator})
		elif prev_operator == '/':
			if curr_val == 0:
				return render(request, 'calculator/calculator.html', {'display_val': 'Can not divide 0!', 'curr_val': 0, 'prev_val': 0, 'prev_operator': '+'})
			else:
				result = int(prev_operator / curr_val)
				prev_operator = request.POST['sign']
				prev_val = result
				curr_val = 0
				return render(request, 'calculator/calculator.html', {'display_val': result, 'curr_val': curr_val, 'prev_val': prev_val, 'prev_operator': prev_operator})

	if request.POST['sign'] == '=':
		if prev_operator == '+':
			result = prev_val + curr_val
			prev_operator = '+'
			prev_val = 0
			curr_val = 0
			return render(request, 'calculator/calculator.html', {'display_val': result, 'curr_val': 0, 'prev_val': 0, 'prev_operator': '+'})
			

	return render(request, 'calculator/calculator.html', {})

	# if request.POST['number']:
	# 	# print error_info
	# 	print request.POST
	# 	context['display_val'] = request.POST['number']
	# 	return render(request, 'calculator/calculator.html', context)