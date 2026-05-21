from django.db import models
from model_utils.models import TimeStampedModel

from apps.console.account.models import CoreAccount


class CorePlan(TimeStampedModel):
    name = models.CharField(max_length=128, default="Self-Hosted")
    code = models.CharField(max_length=128, unique=True, default="self_hosted")
    nodes = models.PositiveIntegerField(default=5)

    class Meta:
        db_table = "core_plan"

    def __str__(self):
        return self.name


class CoreBilling(TimeStampedModel):
    class Status(models.IntegerChoices):
        ACTIVE = 1, "Active"
        OVER_USAGE_NODE = 2, "Over Usage Node"
        OVER_USAGE_STORAGE = 3, "Over Usage Storage"
        OVER_USAGE_NODE_AND_STORAGE = 4, "Over Usage Node And Storage"

    account = models.OneToOneField(
        CoreAccount,
        related_name="billing",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    plan = models.ForeignKey(
        CorePlan,
        related_name="billings",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    status = models.IntegerField(choices=Status.choices, default=Status.ACTIVE)
    free_storage = models.BigIntegerField(default=0)
    stripe_customer_id = models.CharField(max_length=255, null=True, blank=True)
    stripe_plan_sub = models.CharField(max_length=255, null=True, blank=True)
    stripe_storage_sub = models.CharField(max_length=255, null=True, blank=True)
    is_legacy_plan = models.BooleanField(default=False)

    class Meta:
        db_table = "core_billing"

    @property
    def good_standing(self):
        return self.status == self.Status.ACTIVE


class CorePayPalCredit(TimeStampedModel):
    txn_id = models.CharField(max_length=255, null=True, blank=True)
    is_applied = models.BooleanField(default=False)

    class Meta:
        db_table = "core_paypal_credit"