from rest_framework import serializers
from .models import Course
from datetime import date
from dateutil.relativedelta import relativedelta


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'start_date', 'end_date']

    def validate_start_date(self, value):
        if value < date.today():
            raise serializers.ValidationError("Start Date shouldn't be before today!")
        return value

    def create(self, validated_data):
        # If end_date was not provided, set it to 3 months after start_date
        if 'end_date' not in validated_data:
            start_date = validated_data['start_date']
            end_date = start_date + relativedelta(months=3)
            validated_data['end_date'] = end_date

        return super().create(validated_data)

    def update(self, instance, validated_data):
        if validated_data.get('end_date'):
            if instance.start_date >= validated_data['end_date']:
                raise serializers.ValidationError("End Date should be after Start Date!")
        if validated_data.get('start_date'):
            if instance.end_date <= validated_data['start_date']:
                raise serializers.ValidationError("Start Date should be before End Date!")
        if validated_data.get('start_date') and validated_data.get('end_date'):
            if validated_data['start_date'] >= validated_data['end_date']:
                raise serializers.ValidationError("Start Date should be before End Date!")
        if validated_data.get('start_date'):
            instance.start_date = validated_data.get('start_date')
        if validated_data.get('end_date'):
            instance.end_date = validated_data.get('end_date')

        instance.save()
        return instance

    def validate(self, data):
        if data.get('end_date') and data.get('start_date'):
            if data['start_date'] >= data['end_date']:
                raise serializers.ValidationError("End Date should be after Start Date!")
        return data
