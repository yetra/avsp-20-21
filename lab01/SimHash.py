import hashlib


def simhash(text, output_size=128):
    terms = text.strip().split()
    sh = [0] * output_size

    for term in terms:
        digest = hashlib.md5(term.encode()).digest()

        for i in range(output_size):
            byte_i = i // 8
            bit_i = i % 8

            bit = (digest[byte_i] >> bit_i) & 1

            if bit:
                sh[i] += 1
            else:
                sh[i] -= 1

    output = ''.join(map(lambda x: '1' if x >= 0 else '0', sh))

    return hex(int(output, 2))


if __name__ == '__main__':
    print(simhash('fakultet elektrotehnike i racunarstva'))
