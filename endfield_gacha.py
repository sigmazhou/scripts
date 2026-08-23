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
from typing import TypedDict


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
        super().__init__(target_up_total, max_paid_pulls)
        self.bct = 30

    def next_gacha(
        self, banner_id, banner_pulls, pity_count, up_count_total, paid_pulls_total
    ):
        if self.bct <= 0:
            return 0
        if self.bct <= 15:
            self.bct -= 1
            if self.bct <= 0:
                return 0
            return 2
        if banner_pulls >= 60:
            self.bct -= 1
            return 2
        return 1


class S60_30_0(Strategy):
    def __init__(self, target_up_total=1, max_paid_pulls=1000):
        super().__init__(target_up_total, max_paid_pulls)
        self.bct = 30

    def next_gacha(
        self, banner_id, banner_pulls, pity_count, up_count_total, paid_pulls_total
    ):
        if self.bct <= 0:
            return 0
        if self.bct % 3 == 0:
            if banner_pulls >= 60:
                self.bct -= 1
                return 2
            return 1
        if self.bct % 3 == 2:
            if banner_pulls >= 30:
                self.bct -= 1
                return 2
            return 1
        self.bct -= 1
        if self.bct <= 0:
            return 0
        return 2

class S30(Strategy):
    def __init__(self, target_up_total=1, max_paid_pulls=1000):
        super().__init__(target_up_total, max_paid_pulls)
        self.bct = 30

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
        super().__init__(target_up_total, max_paid_pulls)
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


class SUP_SIMPLE(Strategy):
    def __init__(self, target_up_total=1, max_paid_pulls=1000):
        super().__init__(target_up_total, max_paid_pulls)
        self.curr_up_ct = 0

    def next_gacha(
        self, banner_id, banner_pulls, pity_count, up_count_total, paid_pulls_total
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
        super().__init__(target_up_total, max_paid_pulls)
        self.passonect = 60

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
        super().__init__(target_up_total, max_paid_pulls)
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
        super().__init__(target_up_total, max_paid_pulls)
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
        super().__init__(target_up_total, max_paid_pulls)
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


class GachaEngine:
    """Base interface for a gacha simulation model.

    Different models (e.g. EndfieldGacha, SimpleGacha) implement their own pull mechanics
    but share this interface, so GachaAnalyzer/plotting code can compare them interchangeably
    -- both produce GachaReport instances.
    """

    def reset(self) -> None:
        raise NotImplementedError

    def pull(self, source_type="Paid") -> str:
        raise NotImplementedError

    def simulate(self) -> GachaReport:
        raise NotImplementedError

    def generate_report(self) -> GachaReport:
        raise NotImplementedError

    def multiple_sims(self, rounds=1000) -> list[GachaReport]:
        """Run multiple simulations and return list of raw reports."""
        reports = []
        for _ in range(rounds):
            self.reset()
            reports.append(self.simulate())
        return reports

    def set_initial_state(self, **kwargs) -> None:
        """Configure starting state before a sim run. Accepted kwargs are model-specific."""
        raise NotImplementedError


class EndfieldGacha(GachaEngine):
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
        self, pity_count=None, banner_pulls=None, paid_count=None, up_obtained=None, pending_bonus=None, start_new_banner=None
    ):
        self.initial_pity = self.initial_pity if pity_count is None else pity_count
        self.initial_banner_pulls = self.initial_banner_pulls if banner_pulls is None else banner_pulls
        self.initial_up_obtained = self.initial_up_obtained if up_obtained is None else up_obtained
        self.initial_paid_count = self.initial_paid_count if paid_count is None else paid_count
        self.initial_pending_bonus = self.initial_pending_bonus if pending_bonus is None else pending_bonus
        self.start_with_new_banner = self.start_with_new_banner if start_new_banner is None else start_new_banner
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
                        "pity": None,
                        "banner_pulls": self.banner_pulls,
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


class SimpleGacha(GachaEngine):
    """Simplified gacha model: flat 2% UP / 8% 5* / remaining 4*, soft pity on UP only.

    No banners, free pulls, or non-UP 6* (UP is the only top-rarity outcome). Pity tracks
    pulls since the last UP: flat 2% through pull 50, then +2% per additional pull (capped
    at 100%). Pulling continues/stops per `strategy` (banner_id/banner_pulls are unused --
    pass 0 -- since this model has no banners; use a plain Strategy, not a banner-switching
    one).
    """

    UP_BASE_RATE = 0.02
    UP_SOFT_PITY_START = 50
    UP_SOFT_PITY_STEP = 0.02
    FIVE_STAR_RATE = 0.08

    WEAPON_TOKEN_BY_RES = {"UP": 2000, "5": 200, "4": 20}

    def __init__(self, strategy: Strategy):
        self.init_strategy = strategy
        self.initial_pity = 0
        self.reset()

    def set_initial_state(self, pity_count=None):
        self.initial_pity = self.initial_pity if pity_count is None else pity_count
        self.reset()

    def reset(self):
        self.strategy = copy.deepcopy(self.init_strategy)
        self.paid_count = 0
        self.pity_count = self.initial_pity
        self.up_count_total = 0
        self.weapon_token = 0
        self.pull_history = []
        self.inventory = {"UP": 0, "6": 0, "5": 0, "4": 0}

    def _up_prob(self):
        if self.pity_count <= self.UP_SOFT_PITY_START:
            return self.UP_BASE_RATE
        extra = self.pity_count - self.UP_SOFT_PITY_START
        return min(1.0, self.UP_BASE_RATE + self.UP_SOFT_PITY_STEP * extra)

    def pull(self, source_type="Paid"):
        self.paid_count += 1
        self.pity_count += 1

        prob_up = self._up_prob()
        rand_val = random.random()
        if rand_val < prob_up:
            res = "UP"
        elif rand_val < prob_up + self.FIVE_STAR_RATE:
            res = "5"
        else:
            res = "4"

        self.inventory[res] += 1
        self.weapon_token += self.WEAPON_TOKEN_BY_RES[res]
        if res == "UP":
            self.up_count_total += 1
            self.pity_count = 0

        self.pull_history.append(
            {"source": source_type, "res": res, "pity": self.pity_count}
        )
        return res

    def simulate(self):
        while True:
            action = self.strategy.next_gacha(
                0, 0, self.pity_count, self.up_count_total, self.paid_count
            )
            if action == 0:
                break
            self.pull(source_type="Paid")
        return self.generate_report()

    def generate_report(self):
        return GachaReport(
            paid=self.paid_count,
            free=0,
            weapon_token=self.weapon_token,
            inv=dict(self.inventory),
            history=list(self.pull_history),
            pending_free=0,
        )


class StatSummary(TypedDict):
    avg: float
    p50: float
    p75: float
    p90: float


class AggregatedPullCostStats(TypedDict):
    rounds: int
    total_pulls: StatSummary
    paid_pulls: StatSummary
    up_count: StatSummary
    six_star_count: StatSummary
    total_per_up: StatSummary
    total_per_6: StatSummary
    pending_free: StatSummary
    weapon_token: StatSummary
    weapon_token_per_paid__ref: StatSummary
    pooled_paid_per_6: float
    pooled_total_per_6: float
    pooled_paid_per_up: float
    pooled_total_per_up: float
    pooled_weapon_token_per_paid: float
    _totals: list[int]
    _paids: list[int]
    _up_counts: list[int]
    _six_counts: list[int]
    _total_per_up: list[float]
    _total_per_6: list[float]


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

    @staticmethod
    def _stat_summary(data) -> StatSummary:
        if not data:
            return {"avg": 0, "p50": 0, "p75": 0, "p90": 0}
        avg = statistics.mean(data)
        if len(data) == 1:
            v = data[0]
            return {"avg": avg, "p50": v, "p75": v, "p90": v}
        qs = statistics.quantiles(data, n=100, method="inclusive")
        return {"avg": avg, "p50": qs[49], "p75": qs[74], "p90": qs[89]}

    def _aggregate_pull_cost_stats(self) -> AggregatedPullCostStats:
        """Compute per-sim distribution stats and pooled pull costs across all reports."""
        n = len(self.reports)

        totals = [r.total for r in self.reports]
        paids = [r.paid for r in self.reports]
        up_counts = [r.up_count for r in self.reports]
        six_counts = [r.six_star_count for r in self.reports]
        total_per_up = [r.total / r.up_count for r in self.reports if r.up_count > 0]
        total_per_6 = [r.total / r.six_star_count for r in self.reports if r.six_star_count > 0]
        pending_frees = [r.pending_free for r in self.reports]
        weapon_tokens = [r.weapon_token for r in self.reports]

        agg_paid = sum(paids)
        agg_total = sum(totals)
        agg_up = sum(up_counts)
        agg_6 = sum(six_counts)

        return {
            "rounds": n,
            "total_pulls": self._stat_summary(totals),
            "paid_pulls": self._stat_summary(paids),
            "up_count": self._stat_summary(up_counts),
            "six_star_count": self._stat_summary(six_counts),
            "total_per_up": self._stat_summary(total_per_up),
            "total_per_6": self._stat_summary(total_per_6),
            "pending_free": self._stat_summary(pending_frees),
            "weapon_token": self._stat_summary(weapon_tokens),
            "weapon_token_per_paid__ref": (lambda wt, pd: {
                k: wt[k] / pd[k] if pd[k] else 0
                for k in ("avg", "p50", "p75", "p90")
            })(self._stat_summary(weapon_tokens), self._stat_summary(paids)),
            "pooled_paid_per_6": agg_paid / agg_6 if agg_6 > 0 else 0,
            "pooled_total_per_6": agg_total / agg_6 if agg_6 > 0 else 0,
            "pooled_paid_per_up": agg_paid / agg_up if agg_up > 0 else 0,
            "pooled_total_per_up": agg_total / agg_up if agg_up > 0 else 0,
            "pooled_weapon_token_per_paid": (
                sum(r.weapon_token for r in self.reports) / agg_paid if agg_paid > 0 else 0
            ),
            # raw lists for graphing
            "_totals": totals,
            "_paids": paids,
            "_up_counts": up_counts,
            "_six_counts": six_counts,
            "_total_per_up": total_per_up,
            "_total_per_6": total_per_6,
        }

    def print_single_sim_pull_cost(self, index=0):
        """Print pull counts and per-unit costs for one simulation run."""
        r = self.reports[index]
        up = r.up_count
        six = r.six_star_count
        W = 52
        print(f"\n{' 终末地抽卡分项统计 ':=^{W}}")
        print(f"  付费抽: {r.paid:<8}  免费抽: {r.free}")
        print(f"  6星总数: {six}  (UP: {up})")
        print("-" * W)
        if six:
            print(f"  {'总抽/6星':30s} {r.total / six:>8.2f} 抽")
            print(f"  {'付费抽/6星':30s} {r.paid / six:>8.2f} 抽")
        else:
            print("  无6星")
        if up:
            print(f"  {'总抽/UP':30s} {r.total / up:>8.2f} 抽")
            print(f"  {'付费抽/UP':30s} {r.paid / up:>8.2f} 抽")
        else:
            print("  无UP")
        print(f"  {'总武库':30s} {r.weapon_token:>8}")
        if r.paid:
            print(f"  {'武库/付费抽':30s} {r.weapon_token / r.paid:>8.2f}")
        print(f"  {'pending bonus':30s} {r.pending_free:>8} 抽")
        print("=" * W)

    def print_multi_sim_pull_cost(self):
        """Print aggregated pull cost statistics across all simulation runs."""
        s = self._aggregate_pull_cost_stats()
        W = 60

        def row(label, key, unit=""):
            d = s[key]
            u = f" {unit}" if unit else ""
            print(
                f"  {label:<22}"
                f"  {d['avg']:>8.2f}"
                f"  {d['p50']:>8.2f}"
                f"  {d['p75']:>8.2f}"
                f"  {d['p90']:>8.2f}"
                f"{u}"
            )

        print(f"\n{' 多轮模拟统计报告 ':=^{W}}")
        print(f"  模拟轮数: {s['rounds']:,} 轮")
        print("-" * W)
        print(f"  {'每轮分布':<22}  {'avg':>8}  {'p50':>8}  {'p75':>8}  {'p90':>8}")
        print(f"  {'':-<22}  {'---':>8}  {'---':>8}  {'---':>8}  {'---':>8}")
        row("总抽数",            "total_pulls",    "抽")
        row("付费抽",            "paid_pulls",     "抽")
        row("UP 数",             "up_count")
        row("6 星数",            "six_star_count")
        row("总抽/UP  (per sim)", "total_per_up",  "抽")
        row("总抽/6星 (per sim)", "total_per_6",   "抽")
        row("pending bonus",    "pending_free",   "抽")
        row("总武库",            "weapon_token")
        row("总武库/付费抽 *",   "weapon_token_per_paid__ref")
        print("-" * W)
        print("  合并统计 (pooled)")
        print(f"  {'每 6 星消耗 (付费抽)':<26} {s['pooled_paid_per_6']:>8.2f} 抽")
        print(f"  {'每 6 星消耗 (总抽数)':<26} {s['pooled_total_per_6']:>8.2f} 抽")
        print(f"  {'每 UP 消耗 (付费抽)':<26} {s['pooled_paid_per_up']:>8.2f} 抽")
        print(f"  {'每 UP 消耗 (总抽数)':<26} {s['pooled_total_per_up']:>8.2f} 抽")
        print(f"  {'武库/付费抽 (pooled)':<26} {s['pooled_weapon_token_per_paid']:>8.2f}")
        print("=" * W)

    def avg_metrics(self):
        """Return the average per-sim value of the core pull-cost metrics."""
        s = self._aggregate_pull_cost_stats()
        return {
            "paid_pulls": s["paid_pulls"]["avg"],
            "total_pulls": s["total_pulls"]["avg"],
            "six_star_count": s["six_star_count"]["avg"],
            "up_count": s["up_count"]["avg"],
            "weapon_token": s["weapon_token"]["avg"],
            "weapon_token_per_paid": s["weapon_token_per_paid__ref"]["avg"],
        }

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
        ax.axvline(s["total_pulls"]["avg"], color="red", linestyle="--", label=f"均值: {s['total_pulls']['avg']:.1f}")
        ax.set_title("总抽数分布")
        ax.set_xlabel("总抽数")
        ax.set_ylabel("频次")
        ax.legend()

        # 2. Paid pulls distribution
        ax = axes[0, 1]
        ax.hist(s["_paids"], bins=40, edgecolor="black", alpha=0.7, color="orange")
        ax.axvline(s["paid_pulls"]["avg"], color="red", linestyle="--", label=f"均值: {s['paid_pulls']['avg']:.1f}")
        ax.set_title("付费抽数分布")
        ax.set_xlabel("付费抽数")
        ax.set_ylabel("频次")
        ax.legend()

        # 3. UP count distribution
        ax = axes[1, 0]
        up_counts = s["_up_counts"]
        bins_up = range(min(up_counts), max(up_counts) + 2)
        ax.hist(up_counts, bins=bins_up, edgecolor="black", alpha=0.7, color="mediumpurple", align="left")
        ax.axvline(s["up_count"]["avg"], color="red", linestyle="--", label=f"均值: {s['up_count']['avg']:.2f}")
        ax.set_title("UP获取数分布")
        ax.set_xlabel("UP数量")
        ax.set_ylabel("频次")
        ax.legend()

        # 4. Avg total pulls per UP distribution
        ax = axes[1, 1]
        if s["_total_per_up"]:
            ax.hist(s["_total_per_up"], bins=40, edgecolor="black", alpha=0.7, color="seagreen")
            mean_val = statistics.mean(s["_total_per_up"])
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


# Rough fallback weapon-token-per-pity contribution, used only if
# estimate_pity_weapon_token_contribution() hasn't been run.
WEAPON_TOKEN_PER_PITY_PULL = 26


def estimate_pity_weapon_token_contribution(
    gacha,
    pity_range=range(65),
    rounds=2000,
    plot=False,
    save_path=None,
):
    """Estimate the weapon-token value of carried-over pity via simulation + linear fit.

    gacha: a single GachaEngine instance, pre-configured with everything except pity_count
    (e.g. EndfieldGacha(S30()) with set_initial_state(banner_pulls=0, up_obtained=False,
    start_new_banner=True) already called; SimpleGacha needs no such pre-configuration).
    Each pity_count in pity_range is then applied via gacha.set_initial_state(pity_count=p)
    alone -- set_initial_state only touches the fields it's given, so this leaves the
    pre-configured fields untouched.

    Use a strategy indifferent to UP status (e.g. S30 for EndfieldGacha, or a plain Strategy
    with a very high target_up_total for SimpleGacha) that just grinds a fixed number of
    pulls regardless of outcome. Because the farming schedule is then identical no matter the
    starting pity, any difference in average weapon_token earned is attributable to the
    starting pity shifting the odds of an early hit -- i.e. what that pity would have been
    "worth" had it been farmed under a generic strategy instead of carried over.

    Keep pity_range below the model's soft-pity ramp-up point (e.g. 0-64 for EndfieldGacha,
    whose soft pity starts at n=65 in gacha_rate_at_nth_draw) -- pity counts near hard pity
    ramp up sharply and would skew a linear fit.

    A line is fit through avg weapon_token vs. starting pity_count; its slope is the
    estimated marginal weapon-token contribution per unit of carried-over pity.

    If plot is True, also plots avg weapon_token vs. starting pity_count with the fitted
    line overlaid (see plot_pity_weapon_token_contribution).

    Returns {"slope", "intercept", "avg_tokens"} where avg_tokens maps pity_count -> average
    total weapon_token earned from that starting pity.
    """
    avg_tokens = {}
    for pity in pity_range:
        gacha.set_initial_state(pity_count=pity)
        reports = gacha.multiple_sims(rounds)
        avg_tokens[pity] = statistics.mean(r.weapon_token for r in reports)

    slope, intercept = statistics.linear_regression(
        list(avg_tokens.keys()), list(avg_tokens.values())
    )
    result = {"slope": slope, "intercept": intercept, "avg_tokens": avg_tokens}

    if plot:
        plot_pity_weapon_token_contribution(result, save_path=save_path)

    return result


def plot_pity_weapon_token_contribution(contribution, save_path=None):
    """Plot avg weapon_token vs. starting pity_count, with the fitted contribution line.

    contribution: output of estimate_pity_weapon_token_contribution.
    """
    import matplotlib.pyplot as plt
    import matplotlib

    matplotlib.rcParams["font.sans-serif"] = ["Arial Unicode MS", "SimHei", "DejaVu Sans"]
    matplotlib.rcParams["axes.unicode_minus"] = False

    avg_tokens = contribution["avg_tokens"]
    pity_counts = sorted(avg_tokens.keys())
    ys = [avg_tokens[p] for p in pity_counts]
    fitted = [contribution["intercept"] + contribution["slope"] * p for p in pity_counts]

    _, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(pity_counts, ys, label="模拟均值", color="steelblue")
    ax.plot(
        pity_counts,
        fitted,
        color="red",
        linestyle="--",
        label=f"拟合直线 (斜率={contribution['slope']:.2f})",
    )
    ax.set_title("保底继承数对武库的贡献")
    ax.set_xlabel("继承保底抽数")
    ax.set_ylabel("平均武库")
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150)
        print(f"图表已保存至: {save_path}")
    plt.show()


def analyze_pity_carryover_impact(
    gacha,
    pity_range=range(80),
    rounds=5000,
    weapon_token_per_pity=WEAPON_TOKEN_PER_PITY_PULL,
    save_path=None,
):
    """Simulate carrying each pity count into a new banner and plot the resulting average pull-cost metrics.

    gacha: a single GachaEngine instance, pre-configured with everything except pity_count
    (e.g. EndfieldGacha(SUP_SIMPLE()) with set_initial_state(banner_pulls=0, up_obtained=False,
    start_new_banner=True) already called; SimpleGacha needs no such pre-configuration).
    Each pity_count in pity_range is then applied via gacha.set_initial_state(pity_count=p)
    alone -- set_initial_state only touches the fields it's given, so this leaves the
    pre-configured fields untouched.

    weapon_token_per_pity: marginal weapon-token value of one unit of carried-over pity,
    used to normalize weapon_token (see estimate_pity_weapon_token_contribution).

    Returns the dict mapping carried-over pity_count -> GachaAnalyzer.avg_metrics() output.
    """
    metrics_per_pity = {}
    for pity in pity_range:
        gacha.set_initial_state(pity_count=pity)
        reports = gacha.multiple_sims(rounds)
        metrics_per_pity[pity] = GachaAnalyzer(reports).avg_metrics()

    plot_pity_carryover_impact(
        metrics_per_pity, weapon_token_per_pity=weapon_token_per_pity, save_path=save_path
    )
    return metrics_per_pity


def plot_pity_carryover_impact(
    metrics_per_pity, weapon_token_per_pity=WEAPON_TOKEN_PER_PITY_PULL, save_path=None
):
    """Plot how average pull-cost metrics vary with carried-over pity count.

    metrics_per_pity: dict mapping carried-over pity_count -> GachaAnalyzer.avg_metrics() output.
    weapon_token_per_pity: marginal weapon-token value of one unit of carried-over pity,
    used to normalize weapon_token (see estimate_pity_weapon_token_contribution).
    """
    import matplotlib.pyplot as plt
    import matplotlib

    matplotlib.rcParams["font.sans-serif"] = ["Arial Unicode MS", "SimHei", "DejaVu Sans"]
    matplotlib.rcParams["axes.unicode_minus"] = False

    pity_counts = sorted(metrics_per_pity.keys())
    metric_titles = {
        "paid_pulls": "平均付费抽数",
        "total_pulls": "平均总抽数",
        "six_star_count": "平均6星数",
        "up_count": "平均UP数",
        "weapon_token": "平均武库",
        "weapon_token_per_paid": "平均武库/付费抽",
        # "weapon_token_normalized": f"归一化武库 (+/-保底数*{weapon_token_per_pity:.1f})",
        "weapon_token_per_paid_normalized": "归一化武库/付费抽",
    }

    def metric_values(metric):
        if metric == "weapon_token_normalized":
            # needs recalculation
            return [
                metrics_per_pity[p]["weapon_token"] - p * weapon_token_per_pity - metrics_per_pity[p]["paid_pulls"] * 100
                for p in pity_counts
            ]
        if metric == "weapon_token_per_paid_normalized":
            return [
                (metrics_per_pity[p]["weapon_token"] - p * weapon_token_per_pity)/metrics_per_pity[p]["paid_pulls"]
                for p in pity_counts
            ]
        return [metrics_per_pity[p][metric] for p in pity_counts]

    fig, axes = plt.subplots(2, 4, figsize=(22, 10))
    fig.suptitle("继承保底抽数对下期抽卡的影响", fontsize=16)

    for ax, (metric, title) in zip(axes.flat, metric_titles.items()):
        ax.plot(pity_counts, metric_values(metric), marker="o", markersize=3)
        ax.set_title(title)
        ax.set_xlabel("继承保底抽数")
        ax.set_ylabel(title)
        ax.grid(True, alpha=0.3)

    for ax in axes.flat[len(metric_titles):]:
        ax.axis("off")

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150)
        print(f"图表已保存至: {save_path}")
    plt.show()


if __name__ == "__main__":
    # strat_multi = MyStrat4(target_up_total=1, max_paid_pulls=10000)
    # sim_multi = EndfieldGacha(strat_multi, free_per_banner=10)
    # sim_multi.set_initial_state(pity_count=0, banner_pulls=0, up_obtained=0, start_new_banner=True)
    # # report_single = sim_multi.simulate()
    # report_single = sim_multi.multiple_sims(5000)

    # analyzer = GachaAnalyzer(report_single)
    # # analyzer.print_history()
    # # analyzer.print_single_sim_pull_cost()
    # analyzer.print_multi_sim_pull_cost()
    # # analyzer.plot_pull_and_outcome_distributions()
    
    # strat_multi = MyStrat1(target_up_total=1, max_paid_pulls=10000)
    # sim_multi = EndfieldGacha(strat_multi, free_per_banner=10)
    # sim_multi.set_initial_state(pity_count=0, banner_pulls=0, up_obtained=0, start_new_banner=True)
    # report_single = sim_multi.multiple_sims(5000)

    # analyzer = GachaAnalyzer(report_single)
    # analyzer.print_multi_sim_pull_cost()
    # # analyzer.plot_pull_and_outcome_distributions()

    fpb = 0
    contribution = estimate_pity_weapon_token_contribution(EndfieldGacha(S30(), free_per_banner=fpb))
    print(
        f"weapon token / pity contribution factor: {contribution['slope']:.2f} "
        f"(intercept {contribution['intercept']:.2f})"
    )

    strat = SUP_SIMPLE(target_up_total=1, max_paid_pulls=10000)
    report_per_shuiwei = analyze_pity_carryover_impact(
        EndfieldGacha(strat, free_per_banner=fpb), weapon_token_per_pity=contribution["slope"]
    )

    # simple_strat = Strategy(target_up_total=1, max_paid_pulls=10000)
    # simple_gacha = SimpleGacha(simple_strat)
    # simple_reports = simple_gacha.multiple_sims(5000)
    # GachaAnalyzer(simple_reports).plot_pull_and_outcome_distributions()

    # Compare against the simplified model: new strategy (plain Strategy, no banners) and
    # new engine (SimpleGacha). Its own weapon-token contribution is calibrated separately --
    # SimpleGacha has different rarity odds/payouts than EndfieldGacha, so reusing its slope
    # would be meaningless. Calibration needs a UP-indifferent, fixed-pull-budget grind (like
    # S30 does for EndfieldGacha) -- target_up_total=99999 means it never stops early on UP,
    # so every pity count farms exactly the same 1000 pulls (pity counts stay below
    # SimpleGacha's soft-pity onset at 50).
    # simple_contribution = estimate_pity_weapon_token_contribution(
    #     SimpleGacha(Strategy(target_up_total=99999, max_paid_pulls=1000)),
    #     pity_range=range(50),
    # )

    # report_per_shuiwei_simple = analyze_pity_carryover_impact(
    #     SimpleGacha(Strategy(target_up_total=1, max_paid_pulls=10000)),
    #     weapon_token_per_pity=simple_contribution["slope"],
    # )

