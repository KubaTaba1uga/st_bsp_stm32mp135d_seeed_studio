import argparse
import json
import subprocess

def main():
    args = parse_args()
    with open(args.scheme) as fp:
        scheme = json.load(fp)

    for addr_name in scheme:
        addr_obj = scheme[addr_name]
        addr= addr_obj['addr']
        for bits_obj in addr_obj["bits"]:
            off = bits_obj["offset"]            
            raddr = int(addr, base=16) + int(off, base=16)
            # print(f"Processing {addr_name}:{raddr:x}")
            # value = read_mem(raddr)
            value = 0x801
            value = value >> bits_obj["start"]
            svalue = f"{value:b}"
            end = bits_obj["end"] - bits_obj["start"]
            svalue = svalue[::-1]
            svalue = svalue[:end]
            svalue = svalue[::-1]            
            value = int(svalue, base=2)
            svalue = f"0x{value:x}"
            option = bits_obj['options'].get(svalue)
            if not option:
                continue
            print(f"{addr_name}:0x{raddr:x}={option}")            
            


            
    

def parse_args():
    parser = argparse.ArgumentParser(
        prog="translate_reg",
        description="Translate register meaning according to the scheme",
    )
    parser.add_argument("scheme")

    args = parser.parse_args()

    return args


def read_mem(addr):
    with subprocess.Popen(["devmem","{addr:x}", "32"], stdout=subprocess.PIPE) as proc:
        proc.wait()

        if proc.returncode != 0:
            raise ValueError("Error in devmem")
        
        stdout =proc.stdout.read().decode().replace("\n", "")
    print(f"{stdout=}")
    return int(stdout, base=16)

if __name__ == "__main__":
    main()
