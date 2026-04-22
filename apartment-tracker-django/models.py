from django.db import models


class Apartment(models.Model):
    name = models.CharField(max_length=150)
    listing_url = models.TextField()
    image_url = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    bedrooms = models.IntegerField()
    bathrooms = models.DecimalField(max_digits=3, decimal_places=1)
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2)
    has_parking = models.BooleanField(default=False)
    is_pet_friendly = models.BooleanField(default=False)
    has_in_unit_laundry = models.BooleanField(default=False)
    status = models.CharField(max_length=50, default='active')
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'apartments'
        ordering = ['-date_added']

    def __str__(self):
        return self.name

    def avg_score(self):
        ratings = self.ratings.all()
        if not ratings:
            return None
        return round(sum(r.score for r in ratings) / len(ratings), 1)

    def amenity_list(self):
        amenities = []
        if self.has_parking:
            amenities.append('Parking')
        if self.is_pet_friendly:
            amenities.append('Pet-friendly')
        if self.has_in_unit_laundry:
            amenities.append('In-unit laundry')
        return amenities


class Roommate(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'roommates'
        ordering = ['name']

    def __str__(self):
        return self.name

    def rating_count(self):
        return self.ratings.count()


class Rating(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name='ratings')
    roommate = models.ForeignKey(Roommate, on_delete=models.CASCADE, related_name='ratings')
    score = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    rated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ratings'
        unique_together = [['apartment', 'roommate']]
        ordering = ['apartment__name', 'roommate__name']

    def __str__(self):
        return f"{self.roommate.name} → {self.apartment.name}: {self.score}/5"

    def stars(self):
        return '★' * self.score + '☆' * (5 - self.score)
