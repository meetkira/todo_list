from django.db import transaction
from rest_framework import serializers

from core.models import User
from core.serializers import ProfileSerializer
from goals.models import GoalCategory, Goal, GoalComment, Board, BoardParticipant


# GoalCategory -----------------
class GoalCategoryCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания категории"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    board = serializers.SlugRelatedField(
        queryset=Board.objects.all(),
        slug_field='id'
    )

    class Meta:
        model = GoalCategory
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"


class GoalCategorySerializer(serializers.ModelSerializer):
    """Сериализатор для получения информации о категории"""
    user = ProfileSerializer(read_only=True)
    board = serializers.SlugRelatedField(
        read_only=True,
        slug_field='id'
    )

    class Meta:
        model = GoalCategory
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user", "board")


# Goal -----------------
class GoalCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания цели"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate_category(self, value):
        if value.is_deleted:
            raise serializers.ValidationError("not allowed in deleted category")

        return value

    class Meta:
        model = Goal
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"


class GoalSerializer(serializers.ModelSerializer):
    """Сериализатор для получения информации о цели"""
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
    """Сериализатор для создания комментария"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    goal = serializers.SlugRelatedField(
        required=True,
        queryset=Goal.objects.all(),
        slug_field='id'
    )

    class Meta:
        model = GoalComment
        read_only_fields = ("id", "created", "updated", "user", "goal")
        fields = "__all__"


class GoalCommentSerializer(serializers.ModelSerializer):
    """Сериализатор для получения информации о комментарии"""
    user = ProfileSerializer(read_only=True)
    goal = GoalSerializer(read_only=True)

    class Meta:
        model = GoalComment
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user",)


# Board -----------------
class BoardCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания доски"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Board
        read_only_fields = ("id", "created", "updated")
        fields = "__all__"

    def create(self, validated_data):
        user = validated_data.pop("user")
        board = Board.objects.create(**validated_data)
        BoardParticipant.objects.create(
            user=user, board=board, role=BoardParticipant.Role.owner
        )
        return board


class BoardParticipantSerializer(serializers.ModelSerializer):
    """Сериализатор для создания участника доски"""
    role = serializers.ChoiceField(
        required=True, choices=BoardParticipant.Role.choices
    )
    user = serializers.SlugRelatedField(
        slug_field="username", queryset=User.objects.all()
    )

    class Meta:
        model = BoardParticipant
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "board")


class BoardListSerializer(serializers.ModelSerializer):
    """Сериализатор для получения списка досок"""

    class Meta:
        model = Board
        fields = "__all__"


class BoardSerializer(serializers.ModelSerializer):
    """Сериализатор для получения информации о доске"""
    participants = BoardParticipantSerializer(many=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Board
        fields = "__all__"
        read_only_fields = ("id", "created", "updated")

    def update(self, instance, validated_data):
        owner = validated_data.pop("user")
        participants = validated_data.pop("participants")
        participants_by_id = {part["user"].id: part for part in participants}

        old_participants = instance.participants.exclude(user=owner)
        with transaction.atomic():
            for old_participant in old_participants:
                if old_participant.user_id not in participants_by_id:
                    old_participant.delete()
                else:
                    if (
                            old_participant.role
                            != participants_by_id[old_participant.user_id]["role"]
                    ):
                        old_participant.role = participants_by_id[old_participant.user_id][
                            "role"
                        ]
                        old_participant.save()
                    participants_by_id.pop(old_participant.user_id)
            for new_participants in participants_by_id.values():
                BoardParticipant.objects.create(
                    board=instance, user=new_participants["user"], role=new_participants["role"]
                )

            instance.title = validated_data["title"]
            instance.save()

        return instance
