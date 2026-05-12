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
from turtle import pen


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
        self.bct = 20

    def next_gacha(
        self, banner_id, banner_pulls, pity_count, up_count_total, paid_pulls_total
    ):
        if self.bct <= 0:
            return 0
        if self.bct <= 10:
            self.bct -= 1
            if self.bct <= 0:
                return 0
            return 2
        if banner_pulls >= 60:
            self.bct -= 1
            return 2
        return 1

class S30(Strategy):
    def __init__(self, target_up_total=1, max_paid_pulls=1000):
        self.target_up_total = target_up_total
        self.max_paid_pulls = max_paid_pulls
        self.bct = 20

    def next_gacha(
        self, banner_id, banner_pulls, pity_count, up_count_total, paid_pulls_total
    ):
        if self.bct <= 0:
            return 0
        if banner_pulls >= 30:
            self.bct -= 1
            if self.bct <= 0:
                return 0
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


class Swisdom(Strategy):
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



class MyStrat3(Strategy):
    # when already win at 30, should I get to 60
    def __init__(self, target_up_total=1, max_paid_pulls=1000):
        self.target_up_total = target_up_total
        self.max_paid_pulls = max_paid_pulls
        self.passed_one = 0
        self.ucc = 0

    def next_gacha(
        self, banner_id, banner_pulls, pity_count, up_count_total, paid_pulls_total
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
        self.target_up_total = target_up_total
        self.max_paid_pulls = max_paid_pulls
        self.passed_one = 0
        self.ucc = 0

    def next_gacha(
        self, banner_id, banner_pulls, pity_count, up_count_total, paid_pulls_total
    ):
        if not self.passed_one:
            self.passed_one = 1
            self.ucc = up_count_total
            return 2
        if self.ucc == up_count_total:
            return 1
        return 0


class GachaReport:
    """Raw data from a single gacha simulation run."""
    __slots__ = ("paid", "free", "total", "weapon_token", "inv", "history", "pending_free")

    def __init__(self, paid, free, weapon_token, inv, history, pending_free):
        self.paid = paid
        self.free = free
        self.total = paid + free
        self.weapon_token = weapon_token
        self.inv = inv
        self.history = history
        self.pending_free = pending_free

    @property
    def up_count(self):
        return self.inv["UP"]

    @property
    def six_star_count(self):
        return self.inv["UP"] + self.inv["6"]


class EndfieldGacha:
    def __init__(self, strategy: Strategy, free_per_banner=5):
        self.init_strategy = strategy
        self.strategy = copy.deepcopy(self.init_strategy)
        self.free_per_banner = free_per_banner
        self.initial_pity = 0
        self.initial_banner_pulls = 0
        self.initial_up_obtained = False
        self.initial_paid_count = 0
        self.initial_pending_bonus = 0
        self.start_with_new_banner = False
        self.reset()

    def set_initial_state(
        self, pity_count=0, banner_pulls=0, paid_count=0, up_obtained=False, pending_bonus = 0, start_new_banner=False
    ):
        self.initial_pity = pity_count
        self.initial_banner_pulls = banner_pulls
        self.initial_up_obtained = up_obtained
        self.initial_paid_count = paid_count
        self.initial_pending_bonus = pending_bonus
        self.start_with_new_banner = start_new_banner
        self.reset()

    def reset(self):
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
        self.pending_bonus = self.initial_pending_bonus
        if self.start_with_new_banner:
            self.start_banner()

    def _get_current_prob(self, is_pity_contributing):
        base = 0.008
        if not is_pity_contributing:
            return base
        return base + max(0, self.pity_count - 65) * 0.05

    def pull(self, source_type="Paid", is_pity_contributing=True):
        if source_type == "Paid":
            self.paid_count += 1
        else:
            self.free_count += 1

        if is_pity_contributing:
            self.banner_pulls += 1
            self.pity_count += 1
            self.pity_count_5_star += 1
        else:
            self.welfare_30_pity_count_5_star += 1

        prob = self._get_current_prob(is_pity_contributing)
        rand_val = random.random()

        if (
            is_pity_contributing
            and self.banner_pulls == 120
            and not self.up_obtained_current
        ):
            res = "UP"
            self.weapon_token += 2000
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

        self.inventory[res] += 1
        if res == "UP":
            self.total_up_count += 1
            self.up_obtained_current = True

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

        for _ in range(self.free_per_banner):
            self.pull(source_type="Free_Banner", is_pity_contributing=True)
        while self.pending_bonus > 0:
            self.pull(source_type="Free_60Gift", is_pity_contributing=True)
            self.pending_bonus -= 1

    def simulate(self):
        # self.start_banner()
        while True:
            action = self.strategy.next_gacha(
                self.banner_id,
                self.banner_pulls,
                self.pity_count,
                self.total_up_count,
                self.paid_count,
            )
            if self.banner_pulls == 60 and not self.pending_bonus:
                self.pending_bonus += 10
            if action == 0:
                break
            if action == 2:
                self.start_banner()
                continue

            self.pull(source_type="Paid", is_pity_contributing=True)

            if self.banner_pulls == 30 and not self.welfare_30_used:
                for _ in range(10):
                    self.pull(source_type="Free_30Gift", is_pity_contributing=False)
                self.welfare_30_used = True

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
        """Return raw data only - no derived analytics."""
        return GachaReport(
            paid=self.paid_count,
            free=self.free_count,
            weapon_token=self.weapon_token,
            inv=dict(self.inventory),
            history=list(self.pull_history),
            pending_free=self.pending_bonus
        )

    def multiple_sims(self, rounds=1000):
        """Run multiple simulations and return list of raw reports."""
        reports = []
        for _ in range(rounds):
            self.reset()
            reports.append(self.simulate())
        return reports


class GachaAnalyzer:
    """Analyzes gacha simulation reports produced by EndfieldGacha."""
    reports: list[GachaReport]

    def __init__(self, reports):
        """Accept a single GachaReport or a list of GachaReports."""
        if isinstance(reports, GachaReport):
            reports = [reports]
        self.reports = reports
    
    def print_history(self, report_idx=-1):
        for pull in self.reports[report_idx].history:
            print(pull)

    def _aggregate_pull_cost_stats(self):
        """Compute per-sim averages and pooled pull costs across all reports."""
        n = len(self.reports)

        totals = [r.total for r in self.reports]
        paids = [r.paid for r in self.reports]
        up_counts = [r.up_count for r in self.reports]
        six_counts = [r.six_star_count for r in self.reports]
        avg_total_per_up = [r.total / r.up_count for r in self.reports if r.up_count > 0]
        avg_total_per_6 = [r.total / r.six_star_count for r in self.reports if r.six_star_count > 0]

        agg_paid = sum(paids)
        agg_total = sum(totals)
        agg_up = sum(up_counts)
        agg_6 = sum(six_counts)

        return {
            "rounds": n,
            "avg_total_pulls": agg_total / n,
            "avg_paid_pulls": agg_paid / n,
            "avg_up_count": agg_up / n,
            "avg_six_star_count": agg_6 / n,
            "pooled_paid_per_6": agg_paid / agg_6 if agg_6 > 0 else 0,
            "pooled_total_per_6": agg_total / agg_6 if agg_6 > 0 else 0,
            "pooled_paid_per_up": agg_paid / agg_up if agg_up > 0 else 0,
            "pooled_total_per_up": agg_total / agg_up if agg_up > 0 else 0,
            "avg_total_per_up_per_sim": (
                statistics.mean(avg_total_per_up) if avg_total_per_up else 0
            ),
            "avg_total_per_6_per_sim": (
                statistics.mean(avg_total_per_6) if avg_total_per_6 else 0
            ),
            "avg_weapon_token_per_paid": (
                sum(r.weapon_token for r in self.reports) / agg_paid if agg_paid > 0 else 0
            ),
            "avg_pending_free": (sum(r.pending_free for r in self.reports)/n),
            # raw lists for graphing
            "_totals": totals,
            "_paids": paids,
            "_up_counts": up_counts,
            "_six_counts": six_counts,
            "_avg_total_per_up": avg_total_per_up,
            "_avg_total_per_6": avg_total_per_6,
        }

    def print_single_sim_pull_cost(self, index=0):
        """Print pull counts and per-unit costs for one simulation run."""
        r = self.reports[index]
        up = r.up_count
        six = r.six_star_count
        print(f"\n{' 终末地抽卡分项统计 ':=^50}")
        print(f"付费抽: {r.paid:<10} | 免费抽: {r.free}")
        print(f"6星总数: {six} (UP: {up})")
        print("-" * 50)
        print(f"平均出6星耗时 (总投入/出货): {r.total / six:.2f} 抽" if six else "无6星")
        print(f"平均出6星成本 (付费/出货): {r.paid / six:.2f} 抽" if six else "")
        print(f"平均出UP耗时 (总投入/出货): {r.total / up:.2f} 抽" if up else "无UP")
        print(f"平均出UP成本 (付费/出货): {r.paid / up:.2f} 抽" if up else "")
        print(f"武库/付费抽: {r.weapon_token / r.paid:.2f}" if r.paid else "")
        print(f"pending bonus: {r.pending_free} 抽")
        print("=" * 50)

    def print_multi_sim_pull_cost(self):
        """Print aggregated pull cost statistics across all simulation runs."""
        s = self._aggregate_pull_cost_stats()
        print(f"\n{' 多轮模拟统计报告 ':=^50}")
        print(f"模拟轮数: {s['rounds']:,} 轮")
        print("-" * 50)
        print(f"平均总抽数/轮:              {s['avg_total_pulls']:>8.2f} 抽")
        print(f"平均付费抽/轮:              {s['avg_paid_pulls']:>8.2f} 抽")
        print(f"平均UP数/轮:                {s['avg_up_count']:>8.2f}")
        print(f"平均6星数/轮:               {s['avg_six_star_count']:>8.2f}")
        print("-" * 50)
        print(f"每个 6 星平均消耗 (付费抽): {s['pooled_paid_per_6']:>8.2f} 抽")
        print(f"每个 6 星平均消耗 (总抽数): {s['pooled_total_per_6']:>8.2f} 抽")
        print("-" * 50)
        print(f"每个 UP 平均消耗 (付费抽):  {s['pooled_paid_per_up']:>8.2f} 抽")
        print(f"每个 UP 平均消耗 (总抽数):  {s['pooled_total_per_up']:>8.2f} 抽")
        print("-" * 50)
        print(f"每轮平均 总抽/UP:           {s['avg_total_per_up_per_sim']:>8.2f} 抽")
        print(f"每轮平均 总抽/6星:          {s['avg_total_per_6_per_sim']:>8.2f} 抽")
        print("-" * 50)
        print(f"武库/付费抽:                {s['avg_weapon_token_per_paid']:>8.2f}")
        print("-" * 50)
        print(f"pending bonus:             {s['avg_pending_free']:>8.2f} 抽")
        print("=" * 50)

    def plot_pull_and_outcome_distributions(self, save_path=None):
        """Plot histograms of total pulls, paid pulls, UP count, and pulls-per-UP across sims."""
        import matplotlib.pyplot as plt
        import matplotlib

        matplotlib.rcParams["font.sans-serif"] = ["Arial Unicode MS", "SimHei", "DejaVu Sans"]
        matplotlib.rcParams["axes.unicode_minus"] = False

        s = self._aggregate_pull_cost_stats()

        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle(f"抽卡模拟分布 ({s['rounds']} 轮)", fontsize=16)

        # 1. Total pulls distribution
        ax = axes[0, 0]
        ax.hist(s["_totals"], bins=40, edgecolor="black", alpha=0.7, color="steelblue")
        ax.axvline(s["avg_total_pulls"], color="red", linestyle="--", label=f"均值: {s['avg_total_pulls']:.1f}")
        ax.set_title("总抽数分布")
        ax.set_xlabel("总抽数")
        ax.set_ylabel("频次")
        ax.legend()

        # 2. Paid pulls distribution
        ax = axes[0, 1]
        ax.hist(s["_paids"], bins=40, edgecolor="black", alpha=0.7, color="orange")
        ax.axvline(s["avg_paid_pulls"], color="red", linestyle="--", label=f"均值: {s['avg_paid_pulls']:.1f}")
        ax.set_title("付费抽数分布")
        ax.set_xlabel("付费抽数")
        ax.set_ylabel("频次")
        ax.legend()

        # 3. UP count distribution
        ax = axes[1, 0]
        up_counts = s["_up_counts"]
        bins_up = range(min(up_counts), max(up_counts) + 2)
        ax.hist(up_counts, bins=bins_up, edgecolor="black", alpha=0.7, color="mediumpurple", align="left")
        ax.axvline(s["avg_up_count"], color="red", linestyle="--", label=f"均值: {s['avg_up_count']:.2f}")
        ax.set_title("UP获取数分布")
        ax.set_xlabel("UP数量")
        ax.set_ylabel("频次")
        ax.legend()

        # 4. Avg total pulls per UP distribution
        ax = axes[1, 1]
        if s["_avg_total_per_up"]:
            ax.hist(s["_avg_total_per_up"], bins=40, edgecolor="black", alpha=0.7, color="seagreen")
            mean_val = statistics.mean(s["_avg_total_per_up"])
            ax.axvline(mean_val, color="red", linestyle="--", label=f"均值: {mean_val:.1f}")
            ax.set_title("每UP平均总抽数分布")
            ax.set_xlabel("总抽数/UP")
            ax.set_ylabel("频次")
            ax.legend()
        else:
            ax.text(0.5, 0.5, "无UP数据", ha="center", va="center", transform=ax.transAxes)

        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=150)
            print(f"图表已保存至: {save_path}")
        plt.show()


if __name__ == "__main__":
    # --- 单次模拟测试 ---
    # print("\n>>> 执行单次模拟测试 <<<")
    # strat_multi = MyStrat2(target_up_total=1, max_paid_pulls=10000)
    # sim_multi = EndfieldGacha(strat_multi, free_per_banner=5)
    # sim_multi.set_initial_state(pity_count=15, banner_pulls=0)
    # report_single = sim_multi.simulate()

    # analyzer = GachaAnalyzer(report_single)
    # analyzer.print_single_sim_pull_cost()

    # ct = 0
    # for i in report_single.history:
    #     print(i)
    #     ct+=1
    #     if ct%20 == 0:
    #         input()

    # --- 多轮模拟测试 ---
    # print("\n>>> 执行多轮期望测试 <<<")
    strat_multi = S60(target_up_total=10, max_paid_pulls=10000)
    sim_multi = EndfieldGacha(strat_multi, free_per_banner=10)
    sim_multi.set_initial_state(pity_count=0, banner_pulls=0, start_new_banner=True, pending_bonus=0)
    reports = sim_multi.multiple_sims(rounds=10000)
    analyzer = GachaAnalyzer(reports)
    analyzer.print_multi_sim_pull_cost()
    analyzer.plot_pull_and_outcome_distributions()

    # print("\n>>> 执行单次模拟测试 <<<")
    # strat_multi = MyStrat3(target_up_total=1, max_paid_pulls=10000)
    # sim_multi = EndfieldGacha(strat_multi, free_per_banner=10)
    # sim_multi.set_initial_state(pity_count=0, banner_pulls=32, up_obtained=1)
    # report_single = sim_multi.multiple_sims()

    # analyzer = GachaAnalyzer(report_single)
    # analyzer.print_multi_sim_pull_cost()
    # analyzer.plot_pull_and_outcome_distributions()

    # strat_multi = MyStrat4(target_up_total=1, max_paid_pulls=10000)
    # sim_multi = EndfieldGacha(strat_multi, free_per_banner=10)
    # sim_multi.set_initial_state(pity_count=0, banner_pulls=32, up_obtained=1)
    # report_single = sim_multi.multiple_sims()

    # analyzer = GachaAnalyzer(report_single)
    # analyzer.print_multi_sim_pull_cost()
    # analyzer.plot_pull_and_outcome_distributions()
    

