class Strategy:
    def __init__(self, target_up_total=1, max_paid_pulls=1000):
        self.target_up_total = target_up_total
        self.max_paid_pulls = max_paid_pulls
        # plan is a list of string. Every element controls the pull plan for one banner. It can be:
        # 1. a number, means pull to this number of banner pulls
        # 2. UP[optionally a number], means draw this number of UPs from this banner
        self.plan: list[str | int] | None = None
        self.first_banner_id = None

    def _next_gacha_from_plan(self, banner_id, banner_pulls, banner_up_count, pity_count, up_count_total, paid_pulls_total):
        if self.first_banner_id is None:
            self.first_banner_id = banner_id

        plan_index = banner_id - self.first_banner_id
        if plan_index >= len(self.plan):
            return 0

        curr_plan = self.plan[plan_index]

        if isinstance(curr_plan, str) and curr_plan.startswith("UP"):
            target_up = int(curr_plan[2:]) if len(curr_plan) > 2 else 1
            done = banner_up_count >= target_up
        else:
            done = banner_pulls >= int(curr_plan)

        if not done:
            return 1
        return 0 if plan_index == len(self.plan) - 1 else 2

    def next_gacha(
        self, banner_id, banner_pulls, banner_up_count, pity_count, up_count_total, paid_pulls_total
    ):
        if self.plan:
            return self._next_gacha_from_plan(
                banner_id=banner_id,
                banner_pulls=banner_pulls,
                banner_up_count=banner_up_count,
                pity_count=pity_count,
                up_count_total=up_count_total,
                paid_pulls_total=paid_pulls_total,
            )
        if paid_pulls_total >= self.max_paid_pulls:
            return 0
        if up_count_total >= self.target_up_total:
            return 0
        return 1


class S60(Strategy):
    def __init__(self, target_up_total=1, max_paid_pulls=1000):
        super().__init__(target_up_total, max_paid_pulls)
        self.plan = [60]*15+[0]*15


class S60_30_0(Strategy):
    def __init__(self, target_up_total=1, max_paid_pulls=1000):
        super().__init__(target_up_total, max_paid_pulls)
        self.plan = [60, 30, 0] * 10


class S30(Strategy):
    def __init__(self, target_up_total=1, max_paid_pulls=1000):
        super().__init__(target_up_total, max_paid_pulls)
        self.plan = [30]*30


class SUP(Strategy):
    def __init__(self, target_up_total=1, max_paid_pulls=1000):
        super().__init__(target_up_total, max_paid_pulls)
        self.bct = 20
        self.b1 = 0
        self.bstate = 1

    def next_gacha(
        self, banner_id, banner_pulls, banner_up_count, pity_count, up_count_total, paid_pulls_total
    ):
        if self.bct <= 0:
            return 0
        if self.bstate == 1:
            if up_count_total > self.b1:
                if banner_pulls >= 50 and banner_pulls < 60:
                    return 1
                self.b1 = up_count_total
                self.bct -= 1
                self.bstate = 0
                return 2
            else:
                return 1
        else:
            self.b1 = up_count_total
            self.bstate = 1
            self.bct -= 1
            return 2


class SUP_SIMPLE(Strategy):
    def __init__(self, target_up_total=1, max_paid_pulls=1000):
        super().__init__(target_up_total, max_paid_pulls)
        self.curr_up_ct = 0

    def next_gacha(
        self, banner_id, banner_pulls, banner_up_count, pity_count, up_count_total, paid_pulls_total
    ):
        if up_count_total > self.curr_up_ct:
            self.curr_up_ct = up_count_total
            if up_count_total >= self.target_up_total:
                return 0
            return 2
        return 1

class Swisdom(Strategy):
    def __init__(self, target_up_total=1, max_paid_pulls=1000):
        super().__init__(target_up_total, max_paid_pulls)
        self.bct = 20
        self.b1 = 0
        self.bstate = 1
        self.wisdom = 0

    def next_gacha(
        self, banner_id, banner_pulls, banner_up_count, pity_count, up_count_total, paid_pulls_total
    ):
        if self.bct <= 0:
            return 0
        if self.bstate == 1:
            if up_count_total > self.b1:
                if banner_pulls >= 50 and banner_pulls < 60:
                    return 1
                self.b1 = up_count_total
                self.bstate = 0
                self.ct1 = 30
                self.bct -= 1
                if banner_pulls >= 60:
                    self.wisdom = 1
                else:
                    self.wisdom = 0
                return 2
            else:
                return 1
        else:
            if self.wisdom and banner_pulls < 30:
                return 1
            else:
                self.bstate = 1
                self.bct -= 1
                self.b1 = up_count_total
                return 2


class MyStrat1(Strategy):
    def __init__(self, target_up_total=1, max_paid_pulls=1000):
        super().__init__(target_up_total, max_paid_pulls)
        self.passonect = 60

    def next_gacha(
        self, banner_id, banner_pulls, banner_up_count, pity_count, up_count_total, paid_pulls_total
    ):
        if self.passonect > 0:
            if banner_pulls < self.passonect:
                return 1
            else:
                self.passonect = -1
                self.b1 = up_count_total
                return 2
        if paid_pulls_total >= self.max_paid_pulls:
            return 0
        if up_count_total - self.b1 >= self.target_up_total:
            return 0
        return 1


class MyStrat2(Strategy):
    def __init__(self, target_up_total=1, max_paid_pulls=1000):
        super().__init__(target_up_total, max_paid_pulls)
        self.passonect = 30

    def next_gacha(
        self, banner_id, banner_pulls, banner_up_count, pity_count, up_count_total, paid_pulls_total
    ):
        if self.passonect > 0:
            if banner_pulls < self.passonect:
                return 1
            else:
                self.passonect = -1
                self.b1 = up_count_total
                return 2
        if paid_pulls_total >= self.max_paid_pulls:
            return 0
        if up_count_total - self.b1 >= self.target_up_total:
            return 0
        return 1



class MyStrat3(Strategy):
    # when already win at 30, should I get to 60
    def __init__(self, target_up_total=1, max_paid_pulls=1000):
        super().__init__(target_up_total, max_paid_pulls)
        self.passed_one = 0
        self.ucc = 0

    def next_gacha(
        self, banner_id, banner_pulls, banner_up_count, pity_count, up_count_total, paid_pulls_total
    ):
        if not self.passed_one and banner_pulls<60:
            return 1
        if not self.passed_one:
            self.passed_one = 1
            self.ucc = up_count_total
            return 2
        if self.ucc == up_count_total:
            return 1
        return 0


class MyStrat4(Strategy):
    # when already win at 30, should I get to 60
    def __init__(self, target_up_total=1, max_paid_pulls=1000):
        super().__init__(target_up_total, max_paid_pulls)
        self.passed_one = 0
        self.ucc = 0

    def next_gacha(
        self, banner_id, banner_pulls, banner_up_count, pity_count, up_count_total, paid_pulls_total
    ):
        if not self.passed_one:
            self.passed_one = 1
            self.ucc = up_count_total
            return 2
        if self.ucc == up_count_total:
            return 1
        return 0
