from django.db import models

from events.constants import EVENT_TYPES, CONTRACTS_JSON


class Events(models.Model):
    event_type = models.IntegerField()
    to_wallet = models.CharField(max_length=255)
    from_wallet = models.CharField(max_length=255, blank=True, null=True)
    contract_hash = models.CharField(max_length=255, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    epoch_timestamp = models.IntegerField()
    price_unit_dollar = models.FloatField()
    price_unit_jewel = models.FloatField(blank=True, null=True)
    transaction_hash = models.CharField(max_length=255)
    transaction_gasfee = models.FloatField(blank=True, null=True)
    auction_id = models.IntegerField(blank=True, null=True)
    hero_id = models.IntegerField(blank=True, null=True)
    quest_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'events'

    
    
    def __str__(self):
        return f'{EVENT_TYPES.get(self.event_type)}: {self.quantity} {CONTRACTS_JSON.get(self.contract_hash)} => {self.total_price_event()}'

    def total_price_event(self):
        unit_price = self.price_unit_dollar or 0
        quantity = self.quantity or 1
        return round(unit_price * quantity, 4)

    def get_correct_contract_name(self):
        if self.event_type == 2:
            return f'Hero: {self.hero_id}'
        return CONTRACTS_JSON.get(self.contract_hash.lower())

    def dict_record(self):
        return {
            "price": self.total_price_event(),
            "contract_hash": self.contract_hash,
            "contract_name": self.get_correct_contract_name(),
            "timestamp": self.epoch_timestamp,
            "transaction_gasfee": f'{self.transaction_gasfee} ONE',
            "transaction_hash": self.transaction_hash
        }


class ApiKey(models.Model):
    key = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)

    class Meta:
        db_table = 'apikeys'


# Following models are only used for dev purposes and not relevant for this api

class QuestsTest(models.Model):
    event_type = models.IntegerField()
    to_wallet = models.CharField(max_length=255)
    from_wallet = models.CharField(max_length=255, blank=True, null=True)
    contract_hash = models.CharField(max_length=255, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    epoch_timestamp = models.IntegerField()
    price_unit_dollar = models.FloatField()
    price_unit_jewel = models.FloatField(blank=True, null=True)
    transaction_hash = models.CharField(max_length=255)
    transaction_gasfee = models.FloatField(blank=True, null=True)
    auction_id = models.IntegerField(blank=True, null=True)
    hero_id = models.IntegerField(blank=True, null=True)
    quest_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'quests_test'




class Auctions(models.Model):
    auction_id = models.IntegerField(primary_key=True)
    hero_id = models.IntegerField(blank=True, null=True)
    seller = models.CharField(max_length=255, blank=True, null=True)
    epoch_timestamp = models.IntegerField(blank=True, null=True)
    price_unit_dollar = models.FloatField(blank=True, null=True)
    price_unit_jewel = models.FloatField(blank=True, null=True)
    transaction_hash = models.CharField(max_length=255, blank=True, null=True)
    transaction_gasfee = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auctions'