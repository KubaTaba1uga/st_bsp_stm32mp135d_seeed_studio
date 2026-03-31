import argparse
import json
import subprocess

def main():
    args = parse_args()
    with open(args.scheme) as fp:
        scheme = json.load(fp)
    rows = []

    for addr_name in scheme:
        addr_obj = scheme[addr_name]
        addr = addr_obj['addr']

        for bits_obj in addr_obj["bits"]:
            off = bits_obj["offset"]
            raddr = int(addr, 16) + int(off, 16)

            value = read_mem(raddr)

            start = bits_obj["start"]
            end = bits_obj["end"]
            width = end - start + 1
            mask = (1 << width) - 1

            value = (value >> start) & mask
            svalue = f"0x{value:x}"

            option = bits_obj.get('options', {}).get(svalue, svalue)

            rows.append([
                addr_name,
                f"0x{raddr:x}",
                bits_obj["name"],
                option
            ])
    headers = ["Block", "Address", "Field", "Value"]

    # compute column widths
    cols = list(zip(*([headers] + rows)))
    widths = [max(len(str(x)) for x in col) for col in cols]

    def fmt(row):
        return " | ".join(str(x).ljust(w) for x, w in zip(row, widths))

    # print
    print(fmt(headers))
    print("-+-".join("-" * w for w in widths))

    for row in rows:
        print(fmt(row))
            
def parse_args():
    parser = argparse.ArgumentParser(
        prog="translate_reg",
        description="Translate register meaning according to the scheme",
    )
    parser.add_argument("scheme")

    args = parser.parse_args()

    return args


def read_mem(addr):
    # print(["devmem","0x{addr:x}", "32"])
    with subprocess.Popen(["devmem",f"0x{addr:x}", "32"], stdout=subprocess.PIPE) as proc:
         proc.wait()

         if proc.returncode != 0:
            raise ValueError("Error in devmem")

         stdout =proc.stdout.read().decode().replace("\n", "")
         # print(f"{stdout=}")
         return int(stdout, base=16)

if __name__ == "__main__":
    main()
