import sympy, random

def generate_keypair(bit_length=512):
	p = sympy.nextprime(random.getrandbits(bit_length))
	q = sympy.nextprime(random.getrandbits(bit_length))
	n = p * q
	g = n + 1
	lambda_ = (p - 1) * (q - 1)
	mu = sympy.mod_inverse(lambda_, n)
	return (n, g), (lambda_, mu)

def encrypt(m, public_key):
	n, g = public_key
	r = random.randint(1, n - 1)
	return (pow(g, m, n**2) * pow(r, n, n**2)) % (n**2)

def decrypt(c, private_key, public_key):
	lambda_, mu = private_key
	n, _ = public_key
	l = (pow(c, lambda_, n**2) - 1) // n
	return (l * mu) % n

def homomorphic_sum(a, b, public_key):
	return (a * b) % (public_key[0]**2)


public_key, private_key = generate_keypair(128)

enc1 = encrypt(5, public_key)
print(enc1) # 75042696080311881003721105285833023546234037256871189406054603593273414107194675808782154359890875636008219678257354647151456750847402457204123856890

enc2 = encrypt(3, public_key)
print(enc2) # 269297253929306291153284608946414491483346738328838888044406160105950588673820650688249910373352597049965491330298818622410901670587359945691000319758

enc_sum = homomorphic_sum(enc1, enc2, public_key)
print(enc_sum) # 232817745404365921249916946617154013580946738803385878188677616867767489473531493655408124901849935882016399498283109322848069064027287561237823608127

dec_sum = decrypt(enc_sum, private_key, public_key)
print(dec_sum) # 8