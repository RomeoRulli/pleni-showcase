"""What the person's own message authorizes, checked in code and not left to the model.

Excerpt from `app/agent/schedule_answers.py`. Comments translated from Portuguese; code unchanged.

The LLM decides which tool to call, but accepting or declining a schedule is a write on someone's
commitment. The write only happens when the current message from the person asks for it, answers "yes"
to a question the bot asked about that schedule, or names the date of one of the schedules the bot
listed. Otherwise the tool shows the schedule and waits for the next message.
"""


@dataclass
class ScheduleAnswers:
    """What the person's current message authorizes; one instance per turn, shared by that turn's tools."""

    message: str
    gate: ConfirmationGate
    writes: int = 0

    def answers_question_about(self, action: Action, schedule_id: str) -> bool:
        """The bot asked about this schedule ("Want to accept the one on 11/29?") and the person said yes."""
        return self.gate.is_approved(_key(action, schedule_id)) and is_yes(self.message)

    def offer_choices(self, action: Action, schedule_ids: list[str]) -> None:
        """The bot will list these schedules and ask which one: the date picked in the next message
        unlocks the write."""
        self.gate.offer(_choice_key(action, sid) for sid in schedule_ids)

    def authorize(self, action: Action, schedule_id: str, plan_dates: str | None = None) -> bool:
        """True: write now (and count it as one of this message's writes). False: the schedule stays
        shown and a "yes" in the next message unlocks it.

        No `await` in here: the turn's tools run in parallel and the count must not interleave.
        """
        key = _key(action, schedule_id)
        allowed = max_answers(self.message)
        under_budget = allowed is None or self.writes < allowed
        picked = (
            self.gate.is_approved(_choice_key(action, schedule_id))
            and cites_date_of(self.message, plan_dates) is True
            and not _QUESTION.search(_plain(self.message))
        )
        if self.answers_question_about(action, schedule_id) or (
            (asks_to(action, self.message) or picked) and under_budget
        ):
            self.writes += 1
            return True
        self.gate.offer([key])
        return False

    def done(self, action: Action, schedule_id: str) -> None:
        """Write done: repeating the same one asks for confirmation again."""
        self.gate.consume([_key(action, schedule_id)])
