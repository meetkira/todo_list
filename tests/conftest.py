from pytest_factoryboy import register

from tests.factories import BoardFactory, UserFactory, GoalCategoryFactory, BoardParticipantFactory, GoalFactory, \
    GoalCommentFactory

pytest_plugins = "tests.fixtures"

register(BoardFactory)
register(UserFactory)
register(BoardParticipantFactory)
register(GoalCategoryFactory)
register(GoalFactory)
register(GoalCommentFactory)
