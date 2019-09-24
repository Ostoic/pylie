import sympy

debug = False

x, y, h = sympy.symbols('x y h', commutative=False)

sl2 = {}
sl2[(x, y)] = h
sl2[(x, h)] = -2 * x
sl2[(y, h)] = 2 * y

sl2[(y, x)] = - sl2[(x, y)]
sl2[(h, x)] = - sl2[(x, h)]
sl2[(h, y)] = - sl2[(y, h)]

class Constant(sympy.NumberSymbol): 
	is_real = True 
	is_irrational = False 
	is_algebraic = True 
	is_NumberSymbol = True
	is_integer = True
	__slots__ = ['name', 'value'] 

	def __new__(cls, name, value): 
		self = super(Constant, cls).__new__(cls) 
		self.name = name 
		self.value = sympy.Float(value) 
		return self 

	def __getnewargs__(self): 
		return (self.name,self.value) 

	def _latex(self, printer): 
		return printer.doprint(sympy.Symbol(self.name)) 

	def _sympystr(self, printer): 
		return printer.doprint(sympy.Symbol(self.name)) 

	def _sympyrepr(self, printer): 
		return printer.doprint(sympy.Symbol(self.name)) 

	def _mathml(self, printer): 
		return printer.doprint(sympy.Symbol(self.name)) 

	def _as_mpf_val(self, prec): 
		return self.value._as_mpf_val(prec)
		
def constants(cs):
	results = ()
	for c in cs.split(', '):
		results += (Constant(c, 1), )
		
	return results

indent = -1
def print_indent(string):
	global indent
	indents = ''
	for i in range(0, indent):
		indents += '  '
		
	print(indents + string)
	
def is_power(a):
	factors = a.factor().args
	return len(factors) > 1 and factors[1].is_constant
	
def has_scalar_multiplier(a):
	factors = a.factor().args
	return (len(factors) > 1 and factors[0].is_constant)

def extract_scalars(factors):
	if factors == ():
		return 1
		
	res = 1
	for c in factors:
		if c.is_constant():
			res *= c
		
	return res
	
def remove_scalars(a, b):
	a_factors = a.factor().args
	b_factors = b.factor().args
	
	a_coeff = extract_scalars(a_factors)
	b_coeff = extract_scalars(b_factors)
	
	if a_coeff != 1:
		a = (a / a_coeff).factor()
	
	if b_coeff:
		b = (b / b_coeff).factor()
		
	if a.is_constant():
		a = 1
		
	if b.is_constant():
		b = 1
		
	return a_coeff * b_coeff, a, b
	
	
def expand_power_factors(factors):
	expanded = ()
	
	if debug:
		print_indent('expand: {}'.format(factors))
		
	if len(factors) == 1 and not factors[0].is_constant():
		factors = factors[0].factor().args
	
	if len(factors) == 2 and factors[1].is_constant():
		base = factors[0]
		power = factors[1]
		
		for i in range(1, power + 1):
			expanded += (base, )
			
		return expanded
			
	return factors

def bracket_impl(a, b):
	if a == b or a == 0 or b == 0:
		return 0
	
	global indent
	indent += 1
	a_terms = sympy.Add.make_args(a)
	b_terms = sympy.Add.make_args(b)
	
	if debug:
		print_indent('(a, b) = ({}, {})'.format(a, b))
		print_indent('a_terms: {}'.format(a_terms))
		print_indent('b_terms: {}'.format(b_terms))
		
	if len(a_terms) > 1:
		res = 0
		for term in a_terms:
			res += bracket_impl(term, b)
		indent -= 1
		return res
		
	if len(b_terms) > 1:
		res = 0
		for term in b_terms:
			res += bracket_impl(a, term)
		indent -= 1
		return res

	if debug:
		print_indent('initial a_factors: {}'.format(a.factor().args))
		print_indent('initial b_factors: {}'.format(b.factor().args))
	
	# Pull out all scalars to the front of the bracket
	coefficient, a, b = remove_scalars(a, b)
	if a == b or a == 0 or b == 0:
		return 0
	
	if debug:
		print_indent('reduced a\'s factors: {}'.format(a.factor().args))
		print_indent('reduced b\'s factors: {}'.format(b.factor().args))
		print_indent('reduced a: {}'.format(a))
		print_indent('reduced b: {}'.format(b))
	
	# Expand powers: e.g. x**2 to have the factor list (x, x) 
	a_factors = expand_power_factors(a.factor().args)
	b_factors = expand_power_factors(b.factor().args)
	
	if debug:
		print_indent('coeff: {}'.format(coefficient))
		
	if debug:
		print_indent('before a: {}, b: {}'.format(a_factors, b_factors))
		
	if b_factors == ():
		if a_factors == ():
			res = coefficient * sl2[(a, b)]
			indent -= 1
			return res
		else:
			res = - coefficient * bracket_impl(b, a)
			indent -= 1
			return res
	else:
		res = - coefficient * (bracket_impl(b_factors[0], a) * b_factors[1] + b_factors[0] * bracket_impl(b_factors[1], a))
		indent -= 1
		return res
		
def bracket(a, b):
	global indent
	try:
		return bracket_impl(a, b)
	except:
		indent = 0
		raise
		
c, c1, c2, c3, d1, d2, d3 = constants('c, c1, c2, c3, d1, d2, d3')