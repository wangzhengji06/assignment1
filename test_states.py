"""
test_states.py

Used to implement pytest for states
"""

from app import Action, Status
from app.states import InputAmountState, MenuState, QuitState


class FakeCtx:
    """
    A fake AppView for testing
    """

    def __init__(self, balance=0):
        self._balance = balance

    # AppView surface
    @property
    def balance(self) -> int:
        """
        returns a fake balance
        """
        return self._balance

    def format_amount(self, amount: int) -> str:
        """
        returns a human-readable amount
        """
        return f"{amount}$"

    def deposit(self, amount: int) -> None:
        """
        deposits money into balance
        """
        assert amount >= 0
        self._balance += amount

    def withdraw(self, amount: int):
        """
        withdraws amount from balance
        """
        if amount <= 0:
            return False, "Amount must be positive"
        if amount > self._balance:
            return False, "not enough funds"
        self._balance -= amount
        return True, None


def test_menu_navigation_wraps():
    """
    Assume a balance of 1000
    test whether the menustate is at 0
    test wether Action.UP and Action.DOWN is working
    """
    ctx = FakeCtx(balance=1000)
    s = MenuState()
    s.on_enter()

    assert s.render(ctx).menu.selected_index == 0

    s = s.on_ui(Action.UP, ctx)  # wrap to last
    assert s.render(ctx).menu.selected_index == 4

    s = s.on_ui(Action.DOWN, ctx)
    assert s.render(ctx).menu.selected_index == 0


def test_menu_withdraw_disabled_when_zero_balance():
    """
    Assume a balance of 0
    Test the spec of the menustate for withdraw is disabled
    Move to withdraw and confirm
    Make sure the current Status of menustate is error
    """
    ctx = FakeCtx(balance=0)
    s = MenuState()
    spec = s.render(ctx)
    labels = [it.label for it in spec.menu.items]
    withdraw_idx = labels.index("Withdraw")
    assert spec.menu.items[withdraw_idx].disabled is True

    while s.render(ctx).menu.selected_index != withdraw_idx:
        s = s.on_ui(Action.DOWN, ctx)

    s = s.on_ui(Action.CONFIRM, ctx)
    spec2 = s.render(ctx)
    assert isinstance(s, MenuState)
    assert isinstance(spec2.status, Status.__class__) or spec2.status is not None
    assert spec2.status.kind == "error"


def test_menu_withdraw_disabled_when_zero_balancei_v2():
    """
    Assume a balance of 0
    Test the spec of the menustate for withdraw is disabled
    Move to withdraw and confirm
    Make sure the current Status of menustate is error
    """
    ctx = FakeCtx(balance=0)
    s = MenuState()
    s = s.on_ui(Action.WITHDRAW, ctx)
    spec2 = s.render(ctx)
    assert isinstance(s, MenuState)
    assert isinstance(spec2.status, Status.__class__) or spec2.status is not None
    assert spec2.status.kind == "error"


def test_menu_confirm_show_balance_sets_status_info():
    """
    Assume a balance of 1234
    Select show balance
    The result should be menustate with status info
    """
    ctx = FakeCtx(balance=1234)
    s = MenuState()
    labels = [it.label for it in s.render(ctx).menu.items]
    target = labels.index("Show Balance")
    while s.render(ctx).menu.selected_index != target:
        s = s.on_ui(Action.DOWN, ctx)

    s = s.on_ui(Action.CONFIRM, ctx)
    spec = s.render(ctx)
    assert isinstance(s, MenuState)
    assert spec.status is not None
    assert spec.status.kind == "info"
    assert "1234" in spec.status.text


def test_menu_confirm_show_balance_sets_status_info_v2():
    """
    Assume a balance of 1234
    Select show balance
    The result should be menustate with status info
    """
    ctx = FakeCtx(balance=1234)
    s = MenuState()
    s = s.on_ui(Action.SHOW_BALANCE, ctx)
    spec = s.render(ctx)
    assert isinstance(s, MenuState)
    assert spec.status is not None
    assert spec.status.kind == "info"
    assert "1234" in spec.status.text


def test_menu_confirm_deposit_transitions_to_input_state():
    """
    Assume a balance of 0
    Select deposit
    The result should be input amount state
    """
    ctx = FakeCtx(balance=0)
    s = MenuState()
    labels = [it.label for it in s.render(ctx).menu.items]
    deposit_idx = labels.index("Deposit")
    while s.render(ctx).menu.selected_index != deposit_idx:
        s = s.on_ui(Action.UP, ctx)

    s2 = s.on_ui(Action.CONFIRM, ctx)
    assert isinstance(s2, InputAmountState)
    assert s2.kind == "deposit"


def test_menu_confirm_deposit_transitions_to_input_state_v2():
    """
    Assume a balance of 0
    Select deposit
    The result should be input amount state
    """
    ctx = FakeCtx(balance=0)
    s = MenuState()
    s2 = s.on_ui(Action.DEPOSIT, ctx)
    assert isinstance(s2, InputAmountState)
    assert s2.kind == "deposit"


def test_input_amount_deposit_success_returns_menu_with_success_banner():
    """
    Assume a balance of 0
    Choose 500 deposit in InputAmountState
    Should return menustate
    Spec should have success status
    500 should be inside status.text
    ctx should have balance of 500
    """
    ctx = FakeCtx(balance=0)
    s = InputAmountState(kind="deposit")
    s.on_enter()

    for ch in "500":
        s = s.on_text(ch, ctx)

    s2 = s.on_ui(Action.CONFIRM, ctx)
    assert isinstance(s2, MenuState)

    spec = s2.render(ctx)
    assert spec.status is not None
    assert spec.status.kind == "success"
    assert "500" in spec.status.text
    assert ctx.balance == 500  # domain actually changed


def test_input_amount_invalid_input_sets_error_and_stays():
    """
    Assume a balance of 0
    Choose x deposit in InputAmountState
    Should return InputAmountState
    Sepc should have error status
    """
    ctx = FakeCtx(balance=0)
    s = InputAmountState(kind="deposit")
    s.on_enter()

    s = s.on_text("x", ctx)  # invalid
    s2 = s.on_ui(Action.CONFIRM, ctx)

    # stays in the same state with an error status/banner (or inline error)
    assert isinstance(s2, InputAmountState)
    spec = s2.render(ctx)
    assert spec.status is not None
    assert spec.status.kind == "error"


def test_input_amount_withdraw_insufficient_funds_returns_error_banner():
    """
    Assume a balance of 100
    Withdraw 500 in InputAmountState
    Should return to MenuState
    Specc should have error status
    """
    ctx = FakeCtx(balance=100)
    s = InputAmountState(kind="withdraw")
    s.on_enter()
    for ch in "500":
        s = s.on_text(ch, ctx)

    s2 = s.on_ui(Action.CONFIRM, ctx)
    assert isinstance(s2, MenuState)

    spec = s2.render(ctx)
    assert spec.status is not None
    assert spec.status.kind == "error"
    assert "not enough" in spec.status.text


def test_input_amount_cancel_returns_to_menu():
    """
    Assume a balance of 100
    Cancel in the deposit state
    Should return to MenuState
    """
    ctx = FakeCtx(balance=100)
    s = InputAmountState(kind="deposit")
    s.on_enter()
    s2 = s.on_ui(Action.CANCEL, ctx)
    assert isinstance(s2, MenuState)


def test_exit_state_sets_should_quit():
    """
    Assume a balance of 100
    Go to Quit state.
    Spec should have should_quit as True
    """
    ctx = FakeCtx(balance=0)
    s = QuitState()
    s.on_enter()
    spec = s.render(ctx)
    assert spec.should_quit is True
