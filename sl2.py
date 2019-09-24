import sympy
import constant

debug = False

x, y, h = sympy.symbols('x y h', commutative=False)

sl2 = {}
sl2[(x, y)] = h
sl2[(x, h)] = -2 * x
sl2[(y, h)] = 2 * y

sl2[(y, x)] = - sl2[(x, y)]
sl2[(h, x)] = - sl2[(x, h)]
sl2[(h, y)] = - sl2[(y, h)]

indent = -1
def print_debug(string):
	if not debug:
		return
		
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
	
	if len(factors) == 2:
		if factors[1].is_constant():
			return 1
		elif factors[0].is_constant():
			return factors[0]
	
	res = 1
	for c in factors:
		if c.is_constant():
			res *= c
		
	return res
	
def remove_scalars(a, b):
	a_coeff = extract_scalars(a.factor().args)
	b_coeff = extract_scalars(b.factor().args)
	
	print_debug('a_coeff: {}'.format(a_coeff))
	print_debug('b_coeff: {}'.format(b_coeff))
	
	if a_coeff != 0:
		a = (a / a_coeff).factor()
	
	if b_coeff != 0:
		b = (b / b_coeff).factor()
		
	if a.is_constant():
		a = 1
		
	if b.is_constant():
		b = 1
		
	return a_coeff * b_coeff, a, b
	
	
def expand_power_factors(factors):
	expanded = ()
	print_debug('expand: {}'.format(factors))
		
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
	
	# Get sum arguments
	a_terms = sympy.Add.make_args(a)
	b_terms = sympy.Add.make_args(b)
	
	print_debug('(a, b) = ({}, {})'.format(a, b))
	print_debug('a_terms: {}'.format(a_terms))
	print_debug('b_terms: {}'.format(b_terms))
		
	# Split up sum into terms and perform addition on each term separately
	if len(a_terms) > 1:
		res = 0
		for term in a_terms:
			res += bracket_impl(term, b)
		indent -= 1
		return res
	
	# Split up sum into terms and perform addition on each term separately
	if len(b_terms) > 1:
		res = 0
		for term in b_terms:
			res += bracket_impl(a, term)
		indent -= 1
		return res

	print_debug('initial a_factors: {}'.format(a.factor().args))
	print_debug('initial b_factors: {}'.format(b.factor().args))
	
	# Pull out all scalars to the front of the bracket
	coefficient, a, b = remove_scalars(a, b)
	
	# Convert any scalar types to sympy scalar types
	a = sympy.sympify(a)
	b = sympy.sympify(b)
	
	if a == b or a == 0 or b == 0:
		return 0
		
	print_debug('reduced a\'s factors: {}'.format(a.factor().args))
	print_debug('reduced b\'s factors: {}'.format(b.factor().args))
	print_debug('reduced a: {}'.format(a))
	print_debug('reduced b: {}'.format(b))
	
	# Expand powers: e.g. x**2 to have the factor list (x, x) 
	a_factors = expand_power_factors(a.factor().args)
	b_factors = expand_power_factors(b.factor().args)
	
	print_debug('coeff: {}'.format(coefficient))
	print_debug('before a: {}, b: {}'.format(a_factors, b_factors))
	
	
	if b_factors == ():
		# This is a single pair (a, b), so attempt to index the structure constants
		if a_factors == ():
			res = coefficient * sl2[(a, b)]
			indent -= 1
			return res
		# If this didn't work, then try the negative of the flipped bracket
		else:
			res = - coefficient * bracket_impl(b, a)
			indent -= 1
			return res
			
	# If b as multiple factors then apply the bracket identity that works with Lie algebras arising from associative algebra muiltiplciation: [a, bc] = [a, b]c + b[a, c]
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
		
c, c1, c2, c3, d1, d2, d3 = constant.constants('c, c1, c2, c3, d1, d2, d3')