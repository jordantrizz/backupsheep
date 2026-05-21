from rest_framework import serializers


if not hasattr(serializers, "NullBooleanField"):
	class NullBooleanField(serializers.BooleanField):
		def __init__(self, *args, **kwargs):
			kwargs.setdefault("allow_null", True)
			kwargs.setdefault("required", False)
			super().__init__(*args, **kwargs)


	serializers.NullBooleanField = NullBooleanField
