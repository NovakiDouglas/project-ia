import json

power_ratings = {
    "3ztrdauvnvxcrcwh": 5,
    "ek5djfjkzph9aqjc": 6,
    "qb4pxg16rxmzk1nx": 5,
    "vcrdajbnz3oinaym": 5,
    "d3anigiooiwqu2fn": 7,
    "vtwijnr25jnbjuce": 9,
    "6b0e90anxpoafzml": 7,
    "7es88vwz091g9twp": 4.5,
    "7jslafyztxaiwclj": 4.5,
    "8qxen4irzg5nkj5r": 9,
    "97jzv6zysedaddxc": 9,
    "egea4igy0fzbvacn": 9,
    "gr0mjaszgtipbrha": 10,
    "hikdqiki4afxjzpx": 9,
    "k3nvx70k6nza9ikn": 9,
    "kbupsncvygymti4s": 18,
    "kmradbddycbq8ssv": 7,
    "nkWJkJFmFPOkwLfn": 9,
    "no6znqdxhjpx0hzm": 18,
    "qwevvqmsemoow5os": 4.5,
    "tmqdgvvefq0vhv84": 5,
    "tsd7kcliyrhr1teq": 4.5,
    "uqq0ojdkbdwa2rnh": 12,
    "v1bsbjn80zmeo1yk": 9,
    "yexfdhauqfpwzd3o": 9,
    "2po4rgebxznqzcgb": 90,
    "8c8hhghcujk1jalb": 14,
    "fcdqykyfrihlpv77": 90,
    "gpkze1ltltqljlku": 14,
    "mp02s19mnrjomgac": 14,
    "q2hurihjsxg5z9je": 14
}

# Gera um mapeamento zero-based das chaves
pid_to_idx = { pid: idx for idx, pid in enumerate(power_ratings.keys()) }

# Salva em prod_idx_map.json
with open("prod_idx_map.json", "w") as f:
    json.dump(pid_to_idx, f, indent=2)

print("prod_idx_map.json gerado com sucesso!")
