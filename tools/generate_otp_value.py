import argparse

def main():
    args = parse_args()
    word = []
    
    print(f"{args.mode0=}")
    mode0 = add_bits(args.mode0, 4, word)
    print(mode0)        

    print(f"{args.afmux0=}")
    afmux0 = add_bits(args.afmux0, 4, word)
    print(afmux0)        

    print(f"{args.pin0=}")
    pin0 = add_bits(args.pin0, 4, word)
    print(pin0)        

    print(f"{args.port0=}")
    port0 = add_bits(args.port0, 4, word)
    print(port0)        
    
    print(f"{args.mode1=}")
    mode1 = add_bits(args.mode1, 4, word)
    print(mode1)        

    print(f"{args.afmux1=}")
    afmux1 = add_bits(args.afmux1, 4, word)
    print(afmux1)        

    print(f"{args.pin1=}")
    pin1 = add_bits(args.pin1, 4, word)
    print(pin1)        

    print(f"{args.port1=}")
    port1 = add_bits(args.port1, 4, word)
    print(port1)        

    
    word = "".join(word)
    
    print(f"{word} = 0x{int(word, base=2):08x}")

def parse_args():
    parser = argparse.ArgumentParser(
        prog='generate_otp_value.py',
        description='Generate value for otp CFG5.'
    )

    parser.add_argument('--mode0', required=True)
    parser.add_argument('--afmux0', required=True)
    parser.add_argument('--pin0', required=True)
    parser.add_argument('--port0', required=True)

    parser.add_argument('--mode1', required=True)
    parser.add_argument('--afmux1', required=True)
    parser.add_argument('--pin1', required=True)
    parser.add_argument('--port1', required=True)

    return parser.parse_args()

def add_bits(val, bits, list):
    word = gen_bits(val, bits)
    # We use little endian so LSB go first
    list.append(word)
    return word

def gen_bits(val, bits):
    res = int(val, base=10)
    res = f"{res:0{bits}b}"
    return res

if __name__ == "__main__":
    main()

