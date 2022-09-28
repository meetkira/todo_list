from rest_framework import serializers

from core.serializers import ProfileSerializer
from goals.models import GoalCategory, Goal, GoalComment


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
    category = serializers.SlugRelatedField(
        required=False,
        queryset=GoalCategory.objects.all(),
        slug_field='id'
    )

    class Meta:
        model = Goal
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")


# GoalComment -----------------
class GoalCommentCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    goal = serializers.SlugRelatedField(
        required=True,
        queryset=Goal.objects.all(),
        slug_field='id'
    )

    class Meta:
        model = GoalComment
        read_only_fields = ("id", "created", "updated", "user",)
        fields = "__all__"


class GoalCommentSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)
    goal = GoalSerializer(read_only=True)

    class Meta:
        model = GoalComment
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user",)
