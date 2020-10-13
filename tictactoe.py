import time

X_SIGN = "X"
O_SIGN = "O"
EMPTY_SIGN = "-"
important = [4, 0, 2, 6, 8]


class Game:
    def __init__(self):
        self.m = [EMPTY_SIGN for i in range(9)]  # tic-tac-toe matrix
        self.step = 0
        self.sets = [(X_SIGN, O_SIGN), (O_SIGN, X_SIGN)]  # sign and opponent_sign for each player

    async def move(self, n):
        num = self.step % 2
        sign, opponent_sign = self.sets[num]
        self.m[n] = sign
        self.step += 1
        ans = f'{sign}: {n + 1} \n{self.board(self.m)}'
        if self.step > 3:
            if self.step == 8:
                self.m[self.m.index(EMPTY_SIGN)] = sign
                self.step += 1
            win = self._check_win(sign)
            if win or self.step > 8:
                self.step = 0
                self.m = [EMPTY_SIGN for i in range(9)]
                ans += f'\"{sign}\" won!\n' if win else 'We have a draw!\n'
        return ans

    def check_move_str(self, n):
        if not n or not str(n).isdigit():
            return 'Please, send a number!'
        n = int(n)
        if n < 1 or n > 9:
            return 'Number should be greater than 0 and smaller than 10!'
        if self.m[n-1] != EMPTY_SIGN:
            return 'The cell is not empty!'

    def _check_win(self, s):
        m = self.m
        for i in range(3):
            if m[0+i]+m[3+i]+m[6+i] == s*3 or m[0+i*3]+m[1+i*3]+m[2+i*3] == s*3:
                return True
        if m[4] == s and (m[0] == s and m[8] == s or m[2] == s and m[6] == s):
            return True

    @staticmethod
    def board(m):
        ans = ""
        for i in range(3):
            k = i*3
            ans += f'{m[k]}  {m[k+1]}  {m[k+2]}\n'
        return ans + "\n"

    def smart_move(self, m, sign, opponent_sign):
        win_move = self._smart_move(m, sign)
        if win_move:
            return win_move-1
        block_move = self._smart_move(m, opponent_sign)
        if block_move:
            return block_move-1
        return self._important_places_move(m)

    def _important_places_move(self, m):
        if m[4] == EMPTY_SIGN:
            return 4
        empty = []
        for i in important[1:]:
            if m[i] == EMPTY_SIGN:
                empty.append(i)
        return empty[self.get_num() % len(empty)] if empty else m.index(EMPTY_SIGN)

    @staticmethod
    def _smart_move(m, s):
        if m.count(s) < 2:
            return
        a = m.index(s)
        b = m[a + 1:].index(s) + a + 1
        while True:
            r = b - a
            v = []
            if a == 4 or b == 4 or r == 1 and a % 3 == 0 or r == 3:
                if b > 5:
                    v = [a - r]
                else:
                    v = [b + r]
            elif r == 2 and a % 3 == 0 or r == 6:
                v = [a + int(r / 2)]
            for i in v:
                if -1 < i < 9 and m[i] == EMPTY_SIGN:
                    return i+1  # to avoid return 0 !
            if s not in m[b + 1:]:
                break
            a = b
            b = m[b + 1:].index(s) + b + 1

    @staticmethod
    def get_num():
        return int(time.time()*1000000) % 10  # almost random :)


async def main():
    g = Game()
    while True:
        num = g.step % 2
        if num == 0:
            n = g.smart_move(g.m, *g.sets[num])
        else:
            n = int(input()) - 1
        print(await g.move(n))

# asyncio.get_event_loop().run_until_complete(main())

