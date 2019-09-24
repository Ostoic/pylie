import sympy

# A sympy.NumberSymbol that allows us to treat it as a scalar when using the Lie bracket, i.e., [ca, b] = c [a, b]
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