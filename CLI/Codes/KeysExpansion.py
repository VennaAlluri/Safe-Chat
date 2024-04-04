import numpy as np
import itertools as it
def key_expansion(key):
    k=[hex(ord(i))[2:] for i in key]
    keys=[[0]*16 for _ in range(11)]
    keys[0]=k
    for i in range(1,11):
        ki=np.array(keys[i-1]).reshape(4,4)
        L=rotate_left(ki[3],1)
        S=sub_byte(L)
        Rc=round_constant(S,i-1)
        w1=p_xor(ki[0],Rc)
        w2=p_xor(w1,ki[1])
        w3=p_xor(w2,ki[2])
        w4=p_xor(w3,ki[3])
        keys[i]=list(it.chain(w1,w2,w3,w4))
    for i in range(11):
        for j in range(16):
            keys[i][j] = int(keys[i][j],16)
    return keys


def rotate_left(key,b):
    l=len(key)
    key2 = [0] * l
    st=b%l
    for i in range(l):
        key2[i]=key[(st+i)%l]
    return key2

def round_constant(r,i):
    rc=['01','02','04','08','10','20','40','80','1B','36']
    r[0]=dec_to_hex(int(r[0],16)^int(rc[i],16))
    return r

def sub_byte(sb):
    h = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
    s_box =[['63', '7C', '77', '7B', 'F2', '6B', '6F', 'C5', '30', '01', '67', '2B', 'FE', 'D7', 'AB', '76'],
            ['CA', '82', 'C9', '7D', 'FA', '59', '47', 'F0', 'AD', 'D4', 'A2', 'AF', '9C', 'A4', '72', 'C0'],
            ['B7', 'FD', '93', '26', '36', '3F', 'F7', 'CC', '34', 'A5', 'E5', 'F1', '71', 'D8', '31', '15'],
            ['04', 'C7', '23', 'C3', '18', '96', '05', '9A', '07', '12', '80', 'E2', 'EB', '27', 'B2', '75'],
            ['09', '83', '2C', '1A', '1B', '6E', '5A', 'A0', '52', '3B', 'D6', 'B3', '29', 'E3', '2F', '84'],
            ['53', 'D1', '00', 'ED', '20', 'FC', 'B1', '5B', '6A', 'CB', 'BE', '39', '4A', '4C', '58', 'CF'],
            ['D0', 'EF', 'AA', 'FB', '43', '4D', '33', '85', '45', 'F9', '02', '7F', '50', '3C', '9F', 'A8'],
            ['51', 'A3', '40', '8F', '92', '9D', '38', 'F5', 'BC', 'B6', 'DA', '21', '10', 'FF', 'F3', 'D2'],
            ['CD', '0C', '13', 'EC', '5F', '97', '44', '17', 'C4', 'A7', '7E', '3D', '64', '5D', '19', '73'],
            ['60', '81', '4F', 'DC', '22', '2A', '90', '88', '46', 'EE', 'B8', '14', 'DE', '5E', '0B', 'DB'],
            ['E0', '32', '3A', '0A', '49', '06', '24', '5C', 'C2', 'D3', 'AC', '62', '91', '95', 'E4', '79'],
            ['E7', 'C8', '37', '6D', '8D', 'D5', '4E', 'A9', '6C', '56', 'F4', 'EA', '65', '7A', 'AE', '08'],
            ['BA', '78', '25', '2E', '1C', 'A6', 'B4', 'C6', 'E8', 'DD', '74', '1F', '4B', 'BD', '8B', '8A'],
            ['70', '3E', 'B5', '66', '48', '03', 'F6', '0E', '61', '35', '57', 'B9', '86', 'C1', '1D', '9E'],
            ['E1', 'F8', '98', '11', '69', 'D9', '8E', '94', '9B', '1E', '87', 'E9', 'CE', '55', '28', 'DF'],
            ['8C', 'A1', '89', '0D', 'BF', 'E6', '42', '68', '41', '99', '2D', '0F', 'B0', '54', 'BB', '16'] ]
    for i in range(0,len(sb)):
        m=h.index(sb[i][0].upper())
        n=h.index(sb[i][1].upper())
        sb[i]=s_box[m][n]
    return sb

def p_xor(a,b):
    p=['0']*len(a)
    for i in range(0,len(p)):
        m=int(a[i],16)
        n=int(b[i],16)
        p[i]=dec_to_hex(m^n)
    return p


def dec_to_hex(decimal,n=2):
    conversion_table = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4',5: '5', 6: '6', 7: '7',
                        8: '8', 9: '9', 10: 'A', 11: 'B', 12: 'C',13: 'D', 14: 'E', 15: 'F'}
    hexadecimal = ['0']*n
    i=len(hexadecimal)-1
    while (decimal > 0):
        remainder = decimal % 16
        hexadecimal[i] = conversion_table[remainder]
        decimal = decimal // 16
        i=i-1
    return "".join(hexadecimal)