"""
Rolalala - 2016 - Hastad's attack 
"""
import math

"""
http://stackoverflow.com/questions/356090/how-to-compute-the-nth-root-of-a-very-big-integer
"""
def find_invpow(x,n):
	high = 1
	while high ** n < x:
		high *= 2
	low = high/2
	while low < high:
		mid = (low + high) // 2
		if low < mid and mid**n < x:
			low = mid
		elif high > mid and mid**n > x:
			high = mid
		else:
			return mid
	return mid + 1

"""
Get the Flag
"""
def ReverseX(x) :
	m = find_invpow(x, 3)
	size = int(math.log(m, 10) + 1)
	print "Flag : "+"".join([chr((m >> j) & 0xff) for j in reversed(range(0, size << 3, 8))])
	return 1	

def egcd(a, b) :
	if a == 0 :
		return (b, 0, 1)
	else :
		g, x, y = egcd(b % a, a)
		return (g, y - (b // a) * x, x)

"""
Modular inverse
"""
def mulinv(b, n) :
	g, x, _ = egcd(b, n)
	if g == 1:
		return x % n

"""
Step-by-step CRT implementation (cf. demo precedente)
"""
def CrtComputation(C_i, N_i) :
	mu = list()
	nu = list()
	e = list()
	(x_i, N) = (0, 1)
	"""
	Calcul mu_i = PI_(j=1,j!=i)^k(n_j)
	"""
	N = reduce(lambda a, b: a*b, N_i)
	for n_i in N_i :
		mu.append(N/n_i)
	"""
	Calcul nu_i inverse modulo n_i des mu_i
	useful link :
	https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm
	"""
	for mu_i, n_i in zip(mu, N_i) :
		nu.append(mulinv(mu_i, n_i))
	"""
	Calcul e_i = nu_i * mu_i
	"""
	for mu_i, nu_i in zip(mu, nu) :
		e.append(mu_i*nu_i)
	"""
	Calcul et retour de x
	"""	
	for e_i, a_i in zip(e, C_i) :	
		x_i += e_i*a_i
	x = x_i % N
	return x 

def HastadAttack(C_i, N_i, e):
	x = CrtComputation(C_i, N_i)
	return ReverseX(x)

if __name__ == "__main__":
	C_i = [258166178649724503599487742934802526287669691117141193813325965154020153722514921601647187648221919500612597559946901707669147251080002815987547531468665467566717005154808254718275802205355468913739057891997227,82342298625679176036356883676775402119977430710726682485896193234656155980362739001985197966750770180888029807855818454089816725548543443170829318551678199285146042967925331334056196451472012024481821115035402,22930648200320670438709812150490964905599922007583385162042233495430878700029124482085825428033535726942144974904739350649202042807155611342972937745074828452371571955451553963306102347454278380033279926425450]
	N_i = [770208589881542620069464504676753940863383387375206105769618980879024439269509554947844785478530186900134626128158103023729084548188699148790609927825292033592633940440572111772824335381678715673885064259498347,106029085775257663206752546375038215862082305275547745288123714455124823687650121623933685907396184977471397594827179834728616028018749658416501123200018793097004318016219287128691152925005220998650615458757301,982308372262755389818559610780064346354778261071556063666893379698883592369924570665565343844555904810263378627630061263713965527697379617881447335759744375543004650980257156437858044538492769168139674955430611]
	e = 3
	HastadAttack(C_i, N_i, e)		
