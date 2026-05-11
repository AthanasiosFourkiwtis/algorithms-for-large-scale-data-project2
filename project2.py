#AM: 4940 FOURKIOTIS ATHANASIOS

import random
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


BITS = 100
D = 7
W = 1370
P = 2**127 - 1


class CountMinSketch:
    def __init__(self, d, w):
        self.d = d
        self.w = w

        # Megalos protos arithmos, p > 2^100
        self.p = P

        # Kanonikos pinakas Count-Min
        self.table = [[0 for _ in range(w)] for _ in range(d)]
        self.touched = [set() for _ in range(d)]

        # Gia kathe keli krataw kai 100 athroismata, ena gia kathe bit
        # Ta krataw sparse, gia na min arxikopoiw ola ta adeia kelia se kathe peirama
        self.bit_sums = [{} for _ in range(d)]

        # Vec_p oikogeneia: kathe hash function exei BITS aneksarthtous syntelestes
        # h_i(s) = (a[i][0]*s0 + a[i][1]*s1 + ... + a[i][99]*s99 + b[i]) mod p mod w
        # to string antimetopizetai ws dianysma bits sto Z_p
        self.a = [[random.randint(0, self.p - 1) for _ in range(BITS)] for _ in range(d)]
        self.b = [random.randint(0, self.p - 1) for _ in range(d)]

    def _set_bits(self, x):
        bits = []
        while x:
            low_bit = x & -x
            bits.append(low_bit.bit_length() - 1)
            x -= low_bit
        return bits

    def _hash_from_bits(self, bits, i):
        # Vec_p: esoteriko ginomeno tou dianysmatos bits tou s me ta a[i][.], +b[i], mod p
        val = self.b[i]
        row_a = self.a[i]
        for bit in bits:
            val += row_a[bit]

        # Teliko mod w: pernaei to apotelesma sto eyros [0, w) twn sthlwn tou Count-Min
        return val % self.p % self.w

    def hash(self, x, i):
        return self._hash_from_bits(self._set_bits(x), i)

    def update(self, s, c):
        # To s einai akeraios pou antistoixei sto 100-bit string
        # To c mporei na einai kai arnitiko, giati i domi einai grammiki
        set_bits = self._set_bits(s)

        for i in range(self.d):
            pos = self._hash_from_bits(set_bits, i)
            self.table[i][pos] += c
            self.touched[i].add(pos)

            # Prosthetw to c mono sta bits pou einai 1.
            row_bit_sums = self.bit_sums[i]
            if pos not in row_bit_sums:
                row_bit_sums[pos] = [0 for _ in range(BITS)]

            bucket_bits = row_bit_sums[pos]
            for bit in set_bits:
                bucket_bits[bit] += c

    def find_answer(self):
        # Psaxnw gia keli pou fainetai na exei apomonwmeno to stoixeio me timi 100
        for i in range(self.d):
            for j in self.touched[i]:
                total = self.table[i][j]
                bits = self.bit_sums[i].get(j)

                # Periptwsi opou i apantisi einai to string me ola ta bits 0
                if total == 100 and bits is None:
                    return 0

                # An to bary stoixeio einai mono tou se auto to keli,
                # tote to total einai 100 kai kathe bit-sum einai 0 i 100
                if total == 100 and all(v == 0 or v == 100 for v in bits):
                    answer = 0
                    for bit in range(BITS):
                        if bits[bit] == 100:
                            answer |= 1 << bit
                    return answer

        # Se periptwsi pou den apomonwthike se kamia grammi
        return None


def random_string_100_bits():
    return random.randrange(2**BITS)


def random_strings(n):
    strings = set()
    while len(strings) < n:
        strings.add(random_string_100_bits())
    return list(strings)


def int_to_100bit_string(x):
    # Metatrepei ton akeraio x se string 100 bits
    return format(x, f"0{BITS}b")


def one_test():
    cms = CountMinSketch(D, W)
    strings = random_strings(1000)

    for s in strings[:999]:
        cms.update(s, 10)

    correct = strings[999]
    cms.update(correct, 100)

    answer = cms.find_answer()
    if answer is None:
        return False

    return answer == correct


def one_verbose_test():
    # Ena paradeigma ektelesis opou typwnw kai tin pragmatiki apantisi
    # kai tin apantisi pou epestrepse o algorithmos.
    cms = CountMinSketch(D, W)
    strings = random_strings(1000)

    for s in strings[:999]:
        cms.update(s, 10)

    correct = strings[999]
    cms.update(correct, 100)
    answer = cms.find_answer()

    print("Correct heavy string:")
    print(int_to_100bit_string(correct))

    print("Answer returned by algorithm:")
    if answer is None:
        print(None)
    else:
        print(int_to_100bit_string(answer))

    print("Correct answer:", answer == correct)


def experiment():
    # I ekfwnisi zita 1000 tyxaies symvoloseires ana peirama.
    trials = 1000
    success = 0

    for _ in range(trials):
        if one_test():
            success += 1

    print("Epityxies:", success)
    print("Synolika peiramata:", trials)
    print("Pososto epityxias:", success / trials * 100, "%")


def success_probability(d, w):
    q = (1 - 1 / w) ** 999
    return 1 - (1 - q) ** d


def find_best_parameters(max_d=100):
    best_d = None
    best_w = None
    best_cells = None

    for d in range(1, max_d + 1):
        w = 1

        while success_probability(d, w) < 0.99:
            w += 1

        cells = d * w

        if best_cells is None or cells < best_cells:
            best_d = d
            best_w = w
            best_cells = cells

    return best_d, best_w, best_cells


def plot_success_probability():
    ds = list(range(1, 13))
    probs = [success_probability(d, W) for d in ds]

    plt.figure(figsize=(8, 5))
    plt.plot(ds, probs, marker="o")
    plt.axhline(y=0.99, linestyle="--", label="99% όριο")
    plt.axvline(x=D, linestyle="--", label=f"επιλογή d = {D}")

    plt.xlabel("Πλήθος γραμμών d")
    plt.ylabel("Πιθανότητα επιτυχίας")
    plt.title(f"Πιθανότητα επιτυχίας για w = {W}")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig("success_probability.png", dpi=200)
    plt.close()


def plot_parameter_search():
    ds = list(range(1, 31))
    ws = []
    cells = []

    for d in ds:
        w = 1
        while success_probability(d, w) < 0.99:
            w += 1
        ws.append(w)
        cells.append(d * w)

    plt.figure(figsize=(8, 5))
    plt.plot(ds, cells, marker="o")
    plt.axvline(x=D, linestyle="--", label=f"επιλογή d = {D}")

    plt.xlabel("Πλήθος γραμμών d")
    plt.ylabel("Βασικά Count-Min κελιά d x w")
    plt.title("Αναζήτηση παραμέτρων για πιθανότητα επιτυχίας >= 99%")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig("parameter_search.png", dpi=200)
    plt.close()

    print()
    print("Pinakas parametrwn apo to grafima:")
    print("d\tw_min\td*w")
    for d, w, cell_count in zip(ds, ws, cells):
        print(f"{d}\t{w}\t{cell_count}")


def main():
    # Den vazw fixed seed: thelw to peirama na vgazei diaforetiko apotelesma kathe fora,
    # gia na fenetai oti to ~99% epityxias den einai stimeno.
    best_d, best_w, best_cells = find_best_parameters()

    print("Best parameters from search for d = 1,...,100:")
    print("d =", best_d)
    print("w =", best_w)
    print("d*w =", best_cells)
    print()

    one_verbose_test()
    print()

    experiment()

    plot_success_probability()
    plot_parameter_search()
    plt.close("all")


if __name__ == "__main__":
    main()
