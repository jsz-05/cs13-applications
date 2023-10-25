from fractions import Fraction
from decimal import Decimal, getcontext

#quadratic solver equation from set
def solve(a, b, c):
    getcontext().prec = 1000
    a = Decimal(a)
    b = Decimal(b)
    c = Decimal(c)
    return (int((-b + (b**2 - 4*a*c).sqrt())/(2*a)), int((-b - (b**2 - 4*a*c).sqrt())/(2*a)))

def wiener_attack(e, N):
    #find the coefficients of the continued fraction of e/N
    coefficients = []
    #create fraction object with e and N
    r = Fraction(e, N)
    while r != 0:
        i = r.numerator // r.denominator #use integer division
        coefficients.append(i)
        f = r - i #calculate fractional part of r
        if f == 0: 
            break #if 0 then end the loop since we are done
        else:
            r = 1 / f #invert the fraction r for next iteration

    #find the convergents of the continued fraction of e/N
    #fill rest of list with 0s as placeholders for numerators and denominators that will be computed
    h = [0, 1] + [0]*len(coefficients)
    k = [1, 0] + [0]*len(coefficients)
    #calculate numerator h and denominator k for n convergents
    for n in range(2, len(coefficients)+2):
        #for a continued fraction a0 + 1/(a1 + 1/(a2 + 1/(a3 + ... ))) where a0, a1, a2, a3, ... are coefs
        #convergents are a0, a0 + 1/a1, a0 + 1/(a1 + 1/a2), a0 + 1/(a1 + 1/(a2 + 1/a3)), ...

        #if n=2, h[2] = coefficients[0]*h[1] + h[0] 
        #        k[2] = coefficients[0]*k[1] + k[0]
        
        #equal to second convergent h[2]/k[2] = a0 + 1/a1
        h[n] = coefficients[n-2]*h[n-1] + h[n-2]
        k[n] = coefficients[n-2]*k[n-1] + k[n-2]

    #for each convergent c = a/b
    for n in range(1, len(coefficients)+2):
        a, b = h[n], k[n]
        if a == 0:  #skip if a is zero to avoid division by zero
            continue
        potential_phi = (e*b - 1) // a
        #solve the quadratic
        x1, x2 = solve(1, -(N - potential_phi + 1), N)
        #check if the two factors are correct for N, if not continue
        if x1*x2 == N:
            #if yes return p and q
            return x1, x2


e = 3228301342303266421169117315760265758438425860657333023075829597552395212017796436911884275287966390407617802938724178366942194466205728470372043216608939456839954804786845175572213108129436795860389845100258566530684300969970499328655564039032662829299392356057113051321831341669257402651049244123195487871856258909824305976896584963016002994071619237976649996978528290124785498221252353608474821043968908499822252891280270405656437751865360460356950820053427716165084853009640829990558003626707620986873873743136655180285723789801432322989392606784278059858329547458885482252281296914966739731284337574001556313361
N = 8812043537783992834592375402234870396641825341735701299647176256406599732968051770896882160923003833607299964801885015125425072360113606481397109880575698038805771666789634268060640489589352918776370339512697574115046707945166768935552152018424854018421507242016690189690266914976937170694781207628295144600321937961426645440171812433532486834824184790042133755824432752358221659006307494585013997639562241058478170234884138716515700636502484016416273137975716040363780457577708511916105622536896977870481033894682349535070299894064419115975355100527113719155875811681020802476667931645594671094318025099949648383347

print(wiener_attack(e, N))
