import random
import copy

from .strategies import Strategy


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
