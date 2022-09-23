from rest_framework import serializers

from core.serializers import ProfileSerializer
from goals.models import GoalCategory, Goal


# GoalCategory -----------------
class GoalCategoryCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalCategory
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"


class GoalCategorySerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)

    class Meta:
        model = GoalCategory
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")


# Goal -----------------
class GoalCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    category = GoalCategory()
    '''category = serializers.SlugRelatedField(
            required=False,
            queryset=GoalCategory.objects.filter(user=self.request.user, is_deleted=False),
            slug_field='id'
        )'''

    def validate_category(self, value):
        if value.is_deleted:
            raise serializers.ValidationError("not allowed in deleted category")

        if value.user != self.context["request"].user:
            raise serializers.ValidationError("not owner of category")

        return value

    class Meta:
        model = Goal
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"


class GoalSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)
    category = GoalCategorySerializer() # можно редачить
    '''category = serializers.SlugRelatedField(
        required=False,
        queryset=GoalCategory.objects.all(),
        slug_field='id'
    )'''

    class Meta:
        model = Goal
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")


# GoalComment -----------------
class GoalCommentCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    goal = serializers.HiddenField(default=GoalSerializer()) #??

    # goal ??
    class Meta:
        model = GoalCategory
        read_only_fields = ("id", "created", "updated", "user", "goal")
        fields = "__all__"


class GoalCommentSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)
    goal = GoalSerializer(read_only=True)

    class Meta:
        model = GoalCategory
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user", "goal")
