from rest_framework import serializers
from .models import Produce, FarmerCommunityQuestion, CommunityReply, FarmInputRequest, AdminReplyToRequest




class ProduceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produce
        fields = "__all__"
        read_only_fields = ["farmer", "posted_at", "status"]




class CommunityReplySerializer(serializers.ModelSerializer):
    responder_name = serializers.CharField(source="responder.username", read_only=True)

    class Meta:
        model = CommunityReply
        fields = '__all__'


class FarmerCommunityQuestionSerializer(serializers.ModelSerializer):
    replies = CommunityReplySerializer(many=True, read_only=True)

    class Meta:
        model = FarmerCommunityQuestion
        fields = ['id', 'title', 'description', 'created_at', 'replies']  # exclude farmer here

    def create(self, validated_data):
        user = self.context['request'].user
        # Just to be extra safe, pop farmer if it sneaked in
        validated_data.pop('farmer', None)
        return FarmerCommunityQuestion.objects.create(farmer=user, **validated_data)



class AdminReplyToRequestSerializer(serializers.ModelSerializer):
    admin_name = serializers.CharField(source="admin.username", read_only=True)

    class Meta:
        model = AdminReplyToRequest
        fields = '__all__'


class FarmInputRequestSerializer(serializers.ModelSerializer):
    admin_replies = AdminReplyToRequestSerializer(many=True, read_only=True)

    class Meta:
        model = FarmInputRequest
        fields = '__all__'

