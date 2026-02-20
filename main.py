import sys
from collections import defaultdict
class SN:
    # Структура данных Союзный Наход для эффективной работы с группами.
    def __init__(self):
        self.parent = {}
        self.rank = {}
    def find(self, x):
        # Найти главного представителя множества.
        if x not in self.parent:
            self.parent[x] = x
            self.rank[x] = 0
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    def union(self, x, y):
        # Объединить два множества.
        px, py = self.find(x), self.find(y)
        if px == py:
            return
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
    def get_groups(self):
        # Получить все группы как словарь {представитель: [элементы]}.
        groups = defaultdict(set)
        for x in self.parent:
            groups[self.find(x)].add(x)
        return groups
def normalize_word(word):
    # Нормализация слова.
    c = []
    for h in word.lower():
        if h.isalpha() or h == "'":
            c.append(h)
    return ''.join(c)
def are_similar(w1, w2):
    # Проверка того, являются ли два слова похожими.
    if len(w1) <= 1 or len(w2) <= 1:
        return False
    len1, len2 = len(w1), len(w2)
    if len1 == len2:
        diff_count = sum(1 for c1, c2 in zip(w1, w2) if c1 != c2)
        return diff_count == 1
    if abs(len1 - len2) == 1:
        if len1 > len2:
            longer, shorter = w1, w2
        else:
            longer, shorter = w2, w1
        if longer[:-1] == shorter and longer[-1] in ('e', 's'):
            return True
        return False
    return False
def build_similarity_graph(words):
    # Построить граф похожести слов и найти компоненты связности. Использует Союзный Наход для эффективного объединения групп.
    uw = set(w for w in words if len(w) > 1)
    wl = list(uw)
    sn = SN()
    for w in wl:
        sn.find(w)
    wbl = defaultdict(list)
    for w in wl:
        wbl[len(w)].append(w)
    for length, group_w in wbl.items():
        n = len(group_w)
        for i in range(n):
            for j in range(i + 1, n):
                if are_similar(group_w[i], group_w[j]):
                    sn.union(group_w[i], group_w[j])
    lens = sorted(wbl.keys())
    for i in range(len(lens) - 1):
        len1, len2 = lens[i], lens[i + 1]
        if len2 - len1 == 1:
            for w1 in wbl[len1]:
                for w2 in wbl[len2]:
                    if are_similar(w1, w2):
                        sn.union(w1, w2)
    return sn
def calculate_context_frequency(words, uf, k):
    # Вычислить контекстную частоту для каждой группы.
    n = len(words)
    groups = uf.get_groups()
    wtg = {}
    for rep, group_words in groups.items():
        for w in group_words:
            wtg[w] = rep
    context_freq = defaultdict(int)
    for i, word in enumerate(words):
        if word not in wtg:
            continue
        group = wtg[word]
        lbound = max(0, i - k)
        rbound = min(n - 1, i + k)
        found_neighbor_in_group = False
        for j in range(lbound, rbound + 1):
            if j == i:
                continue
            neighbor = words[j]
            if neighbor in wtg and wtg[neighbor] == group:
                found_neighbor_in_group = True
                break
        if found_neighbor_in_group:
            context_freq[group] += 1
    return context_freq, groups
def solve():
    # Решаем и тд.
    lines = []
    for line in sys.stdin:
        line = line.rstrip('\n')
        if line == '':
            break
        lines.append(line)
    if not lines:
        return
    k = int(lines[0])
    all_words = []
    for line in lines[1:]:
        raw_words = line.split()
        for raw_word in raw_words:
            normalized = normalize_word(raw_word)
            if normalized:
                all_words.append(normalized)
    if not all_words:
        return
    sn = build_similarity_graph(all_words)
    context_freq, groups = calculate_context_frequency(all_words, sn, k)
    results = []
    for rep, freq in context_freq.items():
        if freq > 0:
            group_words = groups[rep]
            min_word = min(group_words)
            results.append((min_word, freq))
    results.sort(key=lambda x: (-x[1], x[0]))
    for word, freq in results:
        print(f"{word}: {freq}")
if __name__ == "__main__":
    solve()
