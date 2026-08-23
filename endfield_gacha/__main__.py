# python3 -m endfield_gacha

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
from .strategies import (
    Strategy,
    S60,
    S60_30_0,
    S30,
    SUP,
    SUP_SIMPLE,
    Swisdom,
    MyStrat1,
    MyStrat2,
    MyStrat3,
    MyStrat4,
)
from .gacha_engine import GachaReport, GachaEngine, EndfieldGacha, SimpleGacha
from .analysis import (
    GachaAnalyzer,
    WEAPON_TOKEN_PER_PITY_PULL,
    estimate_pity_weapon_token_contribution,
    plot_pity_weapon_token_contribution,
    analyze_pity_carryover_impact,
    plot_pity_carryover_impact,
)


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
