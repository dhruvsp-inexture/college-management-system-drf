from rest_framework import serializers
from .models import Course
from datetime import date
from dateutil.relativedelta import relativedelta


class CourseSerializer(serializers.ModelSerializer):
    start_date = serializers.DateField(default=date.today())
    price = serializers.DecimalField(min_value=0, max_digits=5, decimal_places=2, required=False)

    class Meta:
        model = Course
        fields = '__all__'

    def validate_start_date(self, value):
        if value < date.today():
            raise serializers.ValidationError("Start Date shouldn't be before today!")
        return value

    def create(self, validated_data):
        # If end_date was not provided, set it to 3 months after start_date
        if ('end_date' not in validated_data):
            if 'start_date' not in validated_data:
                start_date = self.fields['start_date'].get_default()
            else:
                start_date = validated_data.get('start_date')
            end_date = start_date + relativedelta(months=3)
            validated_data['end_date'] = end_date

        return super().create(validated_data)

    def update(self, instance, validated_data):
        start_date = validated_data.get('start_date')
        end_date = validated_data.get('end_date')

        if start_date and end_date and (start_date >= end_date):
            raise serializers.ValidationError("Start Date should be before End Date!")

        if start_date and (instance.end_date <= start_date):
            raise serializers.ValidationError("Start Date should be before End Date!")

        if end_date and (instance.start_date >= end_date):
            raise serializers.ValidationError("End Date should be after Start Date!")

        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.start_date = start_date or instance.start_date
        instance.end_date = end_date or instance.end_date
        instance.price = validated_data.get('price', instance.price)
        instance.save()
        return instance

    def validate(self, data):
        if data.get('end_date') and data.get('start_date'):
            if data['start_date'] >= data['end_date']:
                raise serializers.ValidationError("End Date should be after Start Date!")
        return data
