from django.utils.dateparse import parse_date, parse_datetime
from rest_framework.filters import BaseFilterBackend


class DateRangeFilter(BaseFilterBackend):
    """Apply optional created/modified range filters when query params are present."""

    PARAMS = {
        "created_after": ("created", "gte"),
        "created_before": ("created", "lte"),
        "modified_after": ("modified", "gte"),
        "modified_before": ("modified", "lte"),
    }

    def filter_queryset(self, request, queryset, view):
        model_fields = {field.name for field in queryset.model._meta.get_fields()}

        for param, (field_name, lookup) in self.PARAMS.items():
            raw_value = request.query_params.get(param)
            if not raw_value or field_name not in model_fields:
                continue

            parsed_value = parse_datetime(raw_value) or parse_date(raw_value)
            if parsed_value is None:
                continue

            queryset = queryset.filter(**{f"{field_name}__{lookup}": parsed_value})

        return queryset