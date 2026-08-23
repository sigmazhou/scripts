import statistics
from typing import TypedDict

from .gacha_engine import GachaReport


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
