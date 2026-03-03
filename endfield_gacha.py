def gacha_rate_at_nth_draw(n):
    # n starting from 1
    if n <= 65:
        return 0.008
    if n <= 79:
        return 0.008 + 0.05 * (n - 65)
    return 1


def _gacha_pdf():
    pfail = 1
    res = []
    for i in range(1, 81):
        res.append(gacha_rate_at_nth_draw(i) * pfail)
        pfail *= 1 - gacha_rate_at_nth_draw(i)
    return res

gacha_pdf = _gacha_pdf()

def _gacha_cdf():
    res = []
    psuccess = 0
    for i in range(1, 81):
        psuccess += gacha_pdf[i - 1]
        res.append(psuccess)
    print(res)

Avg = sum([gacha_pdf[i - 1] * i for i in range(1, 81)])

# ------
import random
import statistics
import copy


class Strategy:
    def __init__(self, target_up_total=1, max_paid_pulls=1000):
        self.target_up_total = target_up_total
        self.max_paid_pulls = max_paid_pulls

    def next_gacha(
        self, banner_id, banner_pulls, pity_count, up_count_total, paid_pulls_total
    ):
        if paid_pulls_total >= self.max_paid_pulls:
            return 0
        if up_count_total >= self.target_up_total:
            return 0
        return 1


class S60(Strategy):
    def __init__(self, target_up_total=1, max_paid_pulls=1000):
        self.target_up_total = target_up_total
        self.max_paid_pulls = max_paid_pulls
        self.bct = 10

    def next_gacha(
        self, banner_id, banner_pulls, pity_count, up_count_total, paid_pulls_total
    ):
        if self.bct <= 0:
            return 0
        if banner_pulls >= 60:
            self.bct -= 1
            return 2
        return 1


class SUP(Strategy):
    def __init__(self, target_up_total=1, max_paid_pulls=1000):
        self.target_up_total = target_up_total
        self.max_paid_pulls = max_paid_pulls
        self.bct = 20
        self.b1 = 0
        self.bstate = 1

    def next_gacha(
        self, banner_id, banner_pulls, pity_count, up_count_total, paid_pulls_total
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


class S30(Strategy):
    def __init__(self, target_up_total=1, max_paid_pulls=1000):
        self.target_up_total = target_up_total
        self.max_paid_pulls = max_paid_pulls
        self.bct = 20
        self.b1 = 0
        self.bstate = 1
        self.wisdom = 0

    def next_gacha(
        self, banner_id, banner_pulls, pity_count, up_count_total, paid_pulls_total
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
        self.target_up_total = target_up_total
        self.max_paid_pulls = max_paid_pulls
        self.passonect = 10

    def next_gacha(
        self, banner_id, banner_pulls, pity_count, up_count_total, paid_pulls_total
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
        self.target_up_total = target_up_total
        self.max_paid_pulls = max_paid_pulls
        self.passonect = 30

    def next_gacha(
        self, banner_id, banner_pulls, pity_count, up_count_total, paid_pulls_total
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


class EndfieldGacha:
    def __init__(self, strategy: Strategy, free_per_banner=5):
        self.init_strategy = strategy
        self.strategy = copy.deepcopy(self.init_strategy)
        self.free_per_banner = free_per_banner
        # 初始化默认状态
        self.initial_pity = 0
        self.initial_banner_pulls = 0
        self.initial_up_obtained = False
        self.initial_paid_count = 0
        self.reset()

    def set_initial_state(
        self, pity_count=0, banner_pulls=0, paid_count=0, up_obtained=False
    ):
        """
        设置初始状态，支持自定义：
        pity_count: 当前小保底垫了多少抽
        banner_pulls: 当前池子总共垫了多少抽
        up_obtained: 当前池是否已经出过UP(影响120抽大保底判定)
        """
        self.initial_pity = pity_count
        self.initial_banner_pulls = banner_pulls
        self.initial_up_obtained = up_obtained
        self.initial_paid_count = paid_count
        self.reset()

    def reset(self):
        """应用初始化设置重置模拟器"""
        self.strategy = copy.deepcopy(self.init_strategy)
        self.paid_count = self.initial_paid_count
        self.free_count = 0
        self.banner_pulls = self.initial_banner_pulls
        self.pity_count = self.initial_pity
        self.pity_count_5_star = 0
        self.up_obtained_current = self.initial_up_obtained
        self.total_up_count = 0
        self.weapon_token = 0

        self.banner_id = 0
        self.pull_history = []
        self.inventory = {"UP": 0, "6": 0, "5": 0, "4": 0}
        self.welfare_30_used = False
        self.welfare_30_pity_count_5_star = 0
        self.pending_bonus = 0

    def _get_current_prob(self, is_pity_contributing):
        """只有计入保底的抽取才会享受概率递增"""
        base = 0.008
        if not is_pity_contributing:
            return base
        # 65抽后每抽+5%
        return base + max(0, self.pity_count - 65) * 0.05

    def pull(self, source_type="Paid", is_pity_contributing=True):
        """source_type: "Paid", "Free_Banner" (开局5抽), "Free_60Gift" (60送10), "Free_30Gift" (30送10)"""
        if source_type == "Paid":
            self.paid_count += 1
        else:
            self.free_count += 1

        # 判定是否增加保底计数
        if is_pity_contributing:
            self.banner_pulls += 1
            self.pity_count += 1
            self.pity_count_5_star += 1
        else:
            self.welfare_30_pity_count_5_star += 1

        prob = self._get_current_prob(is_pity_contributing)
        rand_val = random.random()

        # 1. 大保底 (仅限计入保底的抽)
        if (
            is_pity_contributing
            and self.banner_pulls == 120
            and not self.up_obtained_current
        ):
            res = "UP"
            self.weapon_token += 2000
        # 2. 小保底
        elif rand_val < prob or (is_pity_contributing and self.pity_count >= 80):
            res = "UP" if random.random() < 0.5 else "6"
            self.weapon_token += 2000
        elif (
            rand_val < prob + 0.08
            or (is_pity_contributing and self.pity_count_5_star >= 10)
            or (not is_pity_contributing and self.welfare_30_pity_count_5_star >= 10)
        ):
            res = "5"
            self.weapon_token += 200
        else:
            res = "4"
            self.weapon_token += 20

        # 记录结果
        self.inventory[res] += 1
        if res == "UP":
            self.total_up_count += 1
            self.up_obtained_current = True

        # 只有在保底序列中抽到6星才重置保底
        if is_pity_contributing:
            if res in {"6", "UP"}:
                self.pity_count = 0
            if res in {"5", "6", "UP"}:
                self.pity_count_5_star = 0
        else:
            if res in {"5", "6", "UP"}:
                self.welfare_30_pity_count_5_star = 0

        self.pull_history.append(
            {
                "banner": self.banner_id,
                "source": source_type,
                "res": res,
                "pity": self.pity_count if is_pity_contributing else None,
                "banner_pulls": self.banner_pulls if is_pity_contributing else None
            }
        )
        return res

    def start_banner(self):
        self.banner_id += 1
        self.banner_pulls = 0
        self.up_obtained_current = False
        self.welfare_30_used = False
        self.welfare_30_pity_count_5_star = 0

        # 每池5抽（计入保底）
        for _ in range(self.free_per_banner):
            self.pull(source_type="Free_Banner", is_pity_contributing=True)
        # 上期60抽赠送的10连（计入保底）
        while self.pending_bonus > 0:
            self.pull(source_type="Free_60Gift", is_pity_contributing=True)
            self.pending_bonus -= 1

    def simulate(self):
        self.start_banner()
        while True:
            action = self.strategy.next_gacha(
                self.banner_id,
                self.banner_pulls,
                self.pity_count,
                self.total_up_count,
                self.paid_count,
            )
            if action == 0:
                break
            if action == 2:
                if self.banner_pulls >= 60:
                    self.pending_bonus += 10
                self.start_banner()
                continue

            # 付费抽（计入保底）
            self.pull(source_type="Paid", is_pity_contributing=True)

            # 30抽送10连（不计入保底）
            if self.banner_pulls >= 30 and not self.welfare_30_used:
                for _ in range(10):
                    self.pull(source_type="Free_30Gift", is_pity_contributing=False)
                self.welfare_30_used = True

            # 240抽额外赠送
            if self.banner_pulls > 0 and self.banner_pulls % 240 == 0:
                self.total_up_count += 1
                self.inventory["UP"] += 1
                self.pull_history.append(
                    {
                        "banner": self.banner_id,
                        "source": "240_Gift",
                        "res": "UP",
                        "pity_at": None,
                    }
                )

        return self.generate_report()

    def generate_report(self):
        total_up = self.inventory["UP"]
        total_6 = self.inventory["UP"] + self.inventory["6"]
        total_all = self.paid_count + self.free_count
        return {
            "paid": self.paid_count,
            "free": self.free_count,
            "total": total_all,
            "weapon_token": self.weapon_token,
            "inv": self.inventory,
            "history": self.pull_history,
            "avg_total_per_6": total_all / total_6 if total_6 > 0 else 0,
            "avg_paid_per_6": self.paid_count / total_6 if total_6 > 0 else 0,
            "avg_total_per_up": total_all / total_up if total_up > 0 else 0,
            "avg_paid_per_up": self.paid_count / total_up if total_up > 0 else 0,
            "weapon_token_per_paid": (
                self.weapon_token / self.paid_count if self.paid_count > 0 else 0
            ),
        }

    def display(self, r):
        print(f"\n{' 终末地抽卡分项统计 ':=^50}")
        print(f"付费抽: {r['paid']:<10} | 免费抽: {r['free']} (含计入保底与不计入部分)")
        print(f"6星总数: {r['inv']['UP'] + r['inv']['6']} (UP: {r['inv']['UP']})")
        print("-" * 50)
        print(f"平均出6星耗时 (总投入/出货): {r['avg_total_per_6']:.2f} 抽")
        print(f"平均出6星成本 (付费/出货): {r['avg_paid_per_6']:.2f} 抽")
        print(f"平均出UP耗时 (总投入/出货): {r['avg_total_per_up']:.2f} 抽")
        print(f"平均出UP成本 (付费/出货): {r['avg_paid_per_up']:.2f} 抽")
        print(f"武库/付费抽: {r['weapon_token_per_paid']:.2f}")
        print("=" * 50)

    def multiple_sims(self, rounds=1000):
        """执行多轮模拟，并统计宏观消耗指标"""
        agg_paid = 0
        agg_free = 0
        agg_up = 0
        agg_6_star = 0
        agg_weapon_token = 0

        for _ in range(rounds):
            self.reset()
            report = self.simulate()

            agg_paid += report["paid"]
            agg_free += report["free"]
            agg_up += report["inv"]["UP"]
            agg_6_star += report["inv"]["UP"] + report["inv"]["6"]
            agg_weapon_token += report["weapon_token"]

        agg_total_pulls = agg_paid + agg_free

        # 计算大样本下的平均指标
        avg_paid_per_6 = agg_paid / agg_6_star if agg_6_star > 0 else 0
        avg_total_per_6 = agg_total_pulls / agg_6_star if agg_6_star > 0 else 0
        avg_paid_per_up = agg_paid / agg_up if agg_up > 0 else 0
        avg_total_per_up = agg_total_pulls / agg_up if agg_up > 0 else 0
        avg_weapon_token_per_paid = agg_weapon_token / agg_paid if agg_paid > 0 else 0

        print(f"\n{' 多轮模拟统计报告 ':=^50}")
        print(f"模拟轮数: {rounds:,} 轮")
        print(
            f"策略目标: 抽满 {self.strategy.target_up_total} 个UP / 预算 {self.strategy.max_paid_pulls} 抽"
        )
        print(
            f"初始垫抽状态: 小保底 {self.initial_pity} 抽 | 大保底 {self.initial_banner_pulls} 抽"
        )
        print("-" * 50)
        print(f"每个 6 星平均消耗 (付费抽): {avg_paid_per_6:>8.2f} 抽")
        print(f"每个 6 星平均消耗 (总抽数): {avg_total_per_6:>8.2f} 抽")
        print("-" * 50)
        print(f"每个 UP 平均消耗 (付费抽): {avg_paid_per_up:>8.2f} 抽")
        print(f"每个 UP 平均消耗 (总抽数): {avg_total_per_up:>8.2f} 抽")
        print("-" * 50)
        print(f"武库/付费抽: {avg_weapon_token_per_paid:>8.2f}")
        print("=" * 50)

        return {
            "avg_paid_per_6": avg_paid_per_6,
            "avg_total_per_6": avg_total_per_6,
            "avg_paid_per_up": avg_paid_per_up,
            "avg_total_per_up": avg_total_per_up,
            "avg_weapon_token_per_paid": avg_weapon_token_per_paid,
        }


if __name__ == "__main__":
    # # --- 测试 1: 看看单次的运气和 display 表现 ---
    print("\n>>> 执行单次模拟测试 <<<")
    strat_multi = MyStrat2(target_up_total=1, max_paid_pulls=10000)
    sim_multi = EndfieldGacha(strat_multi, free_per_banner=5)
    sim_multi.set_initial_state(pity_count=15, banner_pulls=0)
    report_single = sim_multi.simulate()
    sim_multi.display(report_single)
    ct = 0
    for i in report_single['history']:
        print(i)
        ct+=1
        if ct%20 == 0:
            input()

    # --- 测试 2: 看看一万次的多轮数学期望 ---
    # print("\n>>> 执行多轮期望测试1 <<<")
    # strat_multi = S60(target_up_total=1, max_paid_pulls=10000)
    # sim_multi = EndfieldGacha(strat_multi, free_per_banner=0)
    # sim_multi.set_initial_state(pity_count=0, banner_pulls=0)
    # sim_multi.multiple_sims(rounds=10000)

    # print("\n>>> 执行多轮期望测试1v2 <<<")
    # strat_multi = SUP(target_up_total=1, max_paid_pulls=10000)
    # sim_multi = EndfieldGacha(strat_multi, free_per_banner=5)
    # sim_multi.set_initial_state(pity_count=0, banner_pulls=0)
    # sim_multi.multiple_sims(rounds=10000)

    # print("\n>>> 执行多轮期望测试2 <<<")
    # strat_multi = S30(target_up_total=1, max_paid_pulls=10000)
    # sim_multi = EndfieldGacha(strat_multi, free_per_banner=5)
    # sim_multi.set_initial_state(pity_count=0, banner_pulls=0)
    # sim_multi.multiple_sims(rounds=10000)

    # print("\n>>> 执行多轮期望测试1 <<<")
    # strat_multi = MyStrat1(target_up_total=1, max_paid_pulls=10000)
    # sim_multi = EndfieldGacha(strat_multi, free_per_banner=5)
    # sim_multi.set_initial_state(pity_count=15, banner_pulls=0)
    # sim_multi.multiple_sims(rounds=10000)

    # print("\n>>> 执行多轮期望测试2 <<<")
    # strat_multi = MyStrat2(target_up_total=1, max_paid_pulls=10000)
    # sim_multi = EndfieldGacha(strat_multi, free_per_banner=5)
    # sim_multi.set_initial_state(pity_count=15, banner_pulls=0)
    # sim_multi.multiple_sims(rounds=10000)
