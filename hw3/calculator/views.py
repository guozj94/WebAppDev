from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home_page(request):
	display_val = 0
	context = {}
	context['prev_val'] = 0
	context['curr_val'] = 0
	context['prev_operator'] = '+'
	context['display_val'] = 0
	context['is_equal'] = False
	context['double_operator'] = False
	return render(request, 'calculator/calculator.html', context)
	
def add_to_context(prev_val, curr_val, prev_operator, is_equal, double_operator, display_val):
	context = {}
	context['prev_val'] = prev_val
	context['curr_val'] = curr_val
	context['prev_operator'] = prev_operator
	context['is_equal'] = is_equal
	context['double_operator'] = double_operator
	context['display_val'] = display_val
	return context


def calculator(request):

	prev_val = request.POST['prev_val']
	curr_val = request.POST['curr_val']
	prev_operator = request.POST['prev_operator']
	is_equal = request.POST['is_equal']
	double_operator = request.POST['double_operator']

	try:		
		if isinstance(int(prev_val), int) and isinstance(int(curr_val), int) and (prev_operator in ['+', '-', '*', '/']) and (is_equal in ['True', 'False']) and (double_operator in ['True', 'False']):
			prev_val = int(prev_val)
			curr_val = int(curr_val)			
	except:
		return render(request, 'calculator/calculator.html', {'display_val': 'ERROR!'})

	print request.POST.get('number', False) in ['0','1','2','3','4','5','6','7','8','9']
	if request.POST.get('number', False) in ['0','1','2','3','4','5','6','7','8','9']:
		is_equal = False
		double_operator = False
		if curr_val == 0:
			curr_val = int(request.POST['number'])
			context = add_to_context(prev_val, curr_val, prev_operator, is_equal, double_operator, curr_val)
			return render(request, 'calculator/calculator.html', context)
		else:
			curr_val = int(curr_val) * 10 + int(request.POST['number'])
			context = add_to_context(prev_val, curr_val, prev_operator, is_equal, double_operator, curr_val)
			return render(request, 'calculator/calculator.html', context)

	if (request.POST.get('sign', False) in ['+', '-', '*', '/']) and (double_operator == 'False'):
		if prev_operator == '+':
			result = prev_val + curr_val
			prev_operator = request.POST['sign']
			prev_val = result
			curr_val = 0
			context = add_to_context(prev_val, curr_val, prev_operator, is_equal, double_operator, result)
			return render(request, 'calculator/calculator.html', context)
		elif prev_operator == '-':
			result = prev_val - curr_val
			prev_operator = request.POST['sign']
			prev_val = result
			curr_val = 0
			context = add_to_context(prev_val, curr_val, prev_operator, is_equal, double_operator, result)
			return render(request, 'calculator/calculator.html', context)
		elif prev_operator == '*':
			result = prev_val * curr_val
			prev_operator = request.POST['sign']
			prev_val = result
			curr_val = 0
			context = add_to_context(prev_val, curr_val, prev_operator, is_equal, double_operator, result)
			return render(request, 'calculator/calculator.html', context)
		elif prev_operator == '/':
			if curr_val == 0:
				context = add_to_context(0, 0, '+', False, False, 'Cannot divide by 0')
				return render(request, 'calculator/calculator.html', context)
			else:
				result = int(prev_val / curr_val)
				prev_operator = request.POST['sign']
				prev_val = result
				curr_val = 0
				context = add_to_context(prev_val, curr_val, prev_operator, is_equal, double_operator, result)
				return render(request, 'calculator/calculator.html', context)

	if request.POST.get('sign', False) == '=':
		if prev_operator == '+':
			result = prev_val + curr_val
			context = add_to_context(0, 0, '+', False, False, result)
			return render(request, 'calculator/calculator.html', context)
		if prev_operator == '-':
			result = prev_val - curr_val
			context = add_to_context(0, 0, '+', False, False, result)
			return render(request, 'calculator/calculator.html', context)
		if prev_operator == '*':
			result = prev_val * curr_val
			context = add_to_context(0, 0, '+', False, False, result)
			return render(request, 'calculator/calculator.html', context)
		if prev_operator == '/':
			if curr_val == 0:
				context = add_to_context(0, 0, '+', False, False, 'Cannot divide by 0')
				return render(request, 'calculator/calculator.html', context)
			else:
				result = int(prev_val / curr_val)
				context = add_to_context(0, 0, '+', False, False, result)
				return render(request, 'calculator/calculator.html', context)


	return render(request, 'calculator/calculator.html', {})

	# if request.POST['number']:
	# 	# print error_info
	# 	print request.POST
	# 	context['display_val'] = request.POST['number']
	# 	return render(request, 'calculator/calculator.html', context)