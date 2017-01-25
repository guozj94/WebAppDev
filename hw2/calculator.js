var num_array = ['0','1','2','3','4','5','6','7','8','9'];

window.onload = function () {
	var prev_val = 0;
	var curr_val = 0;
	var prev_operator = "+";
	var click_element = null;
	var is_equal = false;
	var equation = [];
	var double_operator = false;

	document.addEventListener("click", function(e) {
		e = e || window.event;
		var target = e.target || e.srcElement;
		var value = target.innerText;
		equation.push(value);
		if(equation.length > 1){  //if the inputs are two consecutive operators. if so, hold the calculation.
			if((equation[equation.length - 1] == "+" || 
				equation[equation.length - 1] == "-" || 
				equation[equation.length - 1] == "\xD7" || 
				equation[equation.length - 1] == "\xF7") & 
				(equation[equation.length - 2] == "+" ||
					equation[equation.length - 2] == "-" ||
					equation[equation.length - 2] == "\xD7" ||
					equation[equation.length - 2] == "\xF7")) {
				prev_operator = equation[equation.length - 1];
				double_operator = true;
			}
		}
		if(num_array.indexOf(value) + 1) {  //if input is a number
			if(is_equal) document.getElementById("display").innerHTML = "";
			is_equal = false;
			double_operator = false;
			if(curr_val == 0) {
				curr_val = parseInt(value);
				document.getElementById("display").innerHTML = curr_val;
			}
			else{
				curr_val = curr_val * 10 + parseInt(value);
				document.getElementById("display").innerHTML = curr_val;
			}
		}
		if((value == "+" || value == "-" || value == "\xD7" || value == "\xF7") & !double_operator) {  //in input is an operator
			if(prev_operator == "+") {
				var result = prev_val + curr_val;
				prev_operator = value;
				prev_val = result;
				curr_val = 0;
				document.getElementById("display").innerHTML = result;
			}
			else if(prev_operator == "-") {
				var result = prev_val - curr_val;
				prev_operator = value;
				prev_val = result;
				curr_val = 0;
				document.getElementById("display").innerHTML = result;
			}
			else if(prev_operator == "\xD7") {
				var result = prev_val * curr_val;
				prev_operator = value;
				prev_val = result;
				curr_val = 0;
				document.getElementById("display").innerHTML = result;
			}
			else if(prev_operator == "\xF7") {
				if(curr_val == 0) {
					document.getElementById("display").innerHTML = "0";
					if(!alert("Can't divide 0!")) {
						prev_val = 0;
						curr_val = 0;
						prev_operator = "+";
					}
				}
				else {
					var result = Math.floor(prev_val / curr_val);
					prev_operator = value;
					prev_val = result;
					curr_val = 0;
					document.getElementById("display").innerHTML = result;
				}
			}
		}
		if(value == "=") {  //if the input is '=', calculate and initialize the calculator
			if(prev_operator == "+") {
				var result = prev_val + curr_val;
				prev_operator = "+";
				prev_val = 0;
				curr_val = 0;
				document.getElementById("display").innerHTML = result;
				is_equal = true;
			}
			if(prev_operator == "-") {
				var result = prev_val - curr_val;
				prev_operator = "+";
				prev_val = 0;
				curr_val = 0;
				document.getElementById("display").innerHTML = result;
				is_equal = false;
			}
			if(prev_operator == "\xD7") {
				var result = prev_val * curr_val;
				prev_operator = "+";
				prev_val = 0;
				curr_val = 0;
				document.getElementById("display").innerHTML = result;
			}
			if(prev_operator == "\xF7") {
				if(curr_val == 0) {
					document.getElementById("display").innerHTML = "0";
					if(!alert("Can't divide 0!")) {
						prev_val = 0;
						curr_val = 0;
						prev_operator = "+";
					}
				}
				else {
					var result = Math.floor(prev_val / curr_val);
					prev_operator = "+";
					prev_val = 0;
					curr_val = 0;
					document.getElementById("display").innerHTML = result;
				}
			}
		}
	}, false);
}