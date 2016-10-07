"""
Rolalala - 2016 - Wiener's attack 
useful link : http://math.unice.fr/~walter/L1_Arith/cours2.pdf
"""
import math

""" 
Understand the link with the Euclid's algo, and everything will be OK!
"""
def DevContinuedFraction(num, denum) :
	partialQuotients = []
    	divisionRests = []
    	for i in range(int(math.log(denum, 2)/1)) :
		divisionRests = num % denum
		partialQuotients.append(num / denum)
		num = denum
		denum = divisionRests
		if denum == 0 :
	    		break
    	return partialQuotients

""" (cf. useful link p.2) Theorem :
p_-2 = 0 p_-1 = 1   p_n = a_n.p_n-1 + p_n-2
q_-2 = 1 q_-1 = 0   q_n = a_n.q_n-1 + q_n-2 
"""
def DivergentsComputation(partialQuotients) :
	(p1, p2, q1, q2) = (1, 0, 0, 1)
    	convergentsList = []
    	for q in partialQuotients :
		pn = q * p1 + p2
		qn = q * q1 + q2
		convergentsList.append([pn, qn])
		p2 = p1
		q2 = q1
		p1 = pn
		q1 = qn
    	return convergentsList    

"""  
https://dzone.com/articles/cryptographic-functions-python
Be careful to physical attacks see sections below
"""
def SquareAndMultiply(base,exponent,modulus):
    	binaryExponent = []
    	while exponent != 0:
        	binaryExponent.append(exponent%2)
        	exponent = exponent/2
    	result = 1
    	binaryExponent.reverse()
    	for i in binaryExponent:
        	if i == 0:
            		result = (result*result) % modulus
        	else:
            		result = (result*result*base) % modulus
    	return result

def WienerAttack(e, N, C) :
    	testStr = 42 
    	C = SquareAndMultiply(testStr, e, N)
    	for c in DivergentsComputation(DevContinuedFraction(e, N)) :
    		if SquareAndMultiply(C, c[1], N) == testStr :
	    		FullReverse(N, e, c)
	    		return c[1]
    	return -1

"""
Credit for int2Text : 
https://jhafranco.com/2012/01/29/rsa-implementation-in-python/
"""
def GetTheFlag(C, N, d) :
    	p = pow(C, d, N)
    	size = len("{:02x}".format(p)) // 2
    	print "Flag = "+"".join([chr((p >> j) & 0xff) for j in reversed(range(0, size << 3, 8))])

"""
On reprend la demo on cherche (p, q), avec la recherche des racines du P
de scd degre : x^2 - (N - phi(N) + 1)x + N
TODO : regler prblm d'overflow sur le calcul des racines, si quelqu'un a une solution contactez moi :)
"""
def FullReverse(N, e, c) :
    	phi = (e*c[1]-1)/c[0]
    	print "phi = "+str(phi)
    	a = 1
    	b = -(N-phi+1)
    	c = N
    	delta =b*b - 4*a*c
    	if delta > 0 :
		x1 = int((-b + math.sqrt(b*b - 4*a*c)) / (2*a))
		x2 = int((-b - math.sqrt(b*b - 4*a*c)) / (2*a))
		if x1*x2 == N :
	    		print "p = "+str(x1)
	    		print "q = "+str(x2)
		else :
	    		print "** Error **"
    	else :
		print "** ERROR : (p, q)**"

"""
Si N, e, C en hex ::> int("0x0123456789ABCDEF".strip("0x"), 16)
"""
if __name__ == "__main__":
    	C = 00000
    	e = 17993
    	N = 90581

    	print "e : "+str(e)
    	print "N : "+str(N)
    	print "C : "+str(C)
    	d = WienerAttack(e, N, C)
    	if d != -1 :
		print "d = "+str(d)
		GetTheFlag(C, N, d)
    	else :
        	print "** ERROR : Wiener's attack Impossible**"
