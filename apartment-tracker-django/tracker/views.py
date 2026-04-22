from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg, Count, Q
from .models import Apartment, Roommate, Rating
from .forms import ApartmentForm, RoommateForm, RatingForm


# ── Dashboard ─────────────────────────────────────────────────────────────────
@login_required
def dashboard(request):
    total_apts = Apartment.objects.count()
    total_roommates = Roommate.objects.count()
    total_ratings = Rating.objects.count()

    avg_result = Rating.objects.aggregate(avg=Avg('score'))
    avg_score = round(avg_result['avg'], 1) if avg_result['avg'] else None

    # Filter logic
    rent_max = request.GET.get('rent_max', 5000)
    filter_parking = request.GET.get('parking') == 'on'
    filter_pets = request.GET.get('pets') == 'on'

    apartments = Apartment.objects.annotate(
        avg_score=Avg('ratings__score'),
        num_ratings=Count('ratings')
    ).filter(monthly_rent__lte=rent_max)

    if filter_parking:
        apartments = apartments.filter(has_parking=True)
    if filter_pets:
        apartments = apartments.filter(is_pet_friendly=True)

    context = {
        'total_apts': total_apts,
        'total_roommates': total_roommates,
        'total_ratings': total_ratings,
        'avg_score': avg_score,
        'apartments': apartments,
        'rent_max': rent_max,
        'filter_parking': filter_parking,
        'filter_pets': filter_pets,
    }
    return render(request, 'tracker/dashboard.html', context)


# ── Apartments ────────────────────────────────────────────────────────────────
@login_required
def apartments(request):
    search = request.GET.get('search', '')
    apt_list = Apartment.objects.annotate(
        avg_score=Avg('ratings__score'),
        num_ratings=Count('ratings')
    )
    if search:
        apt_list = apt_list.filter(
            Q(name__icontains=search) | Q(address__icontains=search)
        )

    form = ApartmentForm()
    if request.method == 'POST':
        form = ApartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"'{form.cleaned_data['name']}' added successfully!")
            return redirect('apartments')

    context = {'apartments': apt_list, 'form': form, 'search': search}
    return render(request, 'tracker/apartments.html', context)


@login_required
def apartment_edit(request, pk):
    apt = get_object_or_404(Apartment, pk=pk)
    form = ApartmentForm(instance=apt)
    if request.method == 'POST':
        form = ApartmentForm(request.POST, instance=apt)
        if form.is_valid():
            form.save()
            messages.success(request, f"'{apt.name}' updated successfully!")
            return redirect('apartments')
    return render(request, 'tracker/apartment_edit.html', {'form': form, 'apt': apt})


@login_required
def apartment_delete(request, pk):
    apt = get_object_or_404(Apartment, pk=pk)
    if request.method == 'POST':
        name = apt.name
        apt.delete()
        messages.success(request, f"'{name}' deleted.")
        return redirect('apartments')
    return render(request, 'tracker/apartment_confirm_delete.html', {'apt': apt})


# ── Roommates ─────────────────────────────────────────────────────────────────
@login_required
def roommates(request):
    search = request.GET.get('search', '')
    roommate_list = Roommate.objects.annotate(num_ratings=Count('ratings'))
    if search:
        roommate_list = roommate_list.filter(
            Q(name__icontains=search) | Q(email__icontains=search)
        )

    form = RoommateForm()
    if request.method == 'POST':
        form = RoommateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"'{form.cleaned_data['name']}' added!")
            return redirect('roommates')

    context = {'roommates': roommate_list, 'form': form, 'search': search}
    return render(request, 'tracker/roommates.html', context)


@login_required
def roommate_edit(request, pk):
    roommate = get_object_or_404(Roommate, pk=pk)
    form = RoommateForm(instance=roommate)
    if request.method == 'POST':
        form = RoommateForm(request.POST, instance=roommate)
        if form.is_valid():
            form.save()
            messages.success(request, f"'{roommate.name}' updated!")
            return redirect('roommates')
    return render(request, 'tracker/roommate_edit.html', {'form': form, 'roommate': roommate})


@login_required
def roommate_delete(request, pk):
    roommate = get_object_or_404(Roommate, pk=pk)
    if request.method == 'POST':
        name = roommate.name
        roommate.delete()
        messages.success(request, f"'{name}' deleted.")
        return redirect('roommates')
    return render(request, 'tracker/roommate_confirm_delete.html', {'roommate': roommate})


# ── Rate ──────────────────────────────────────────────────────────────────────
@login_required
def rate(request):
    filter_apt = request.GET.get('filter_apt', '')
    all_ratings = Rating.objects.select_related('apartment', 'roommate').order_by('apartment__name', 'roommate__name')
    if filter_apt:
        all_ratings = all_ratings.filter(apartment_id=filter_apt)

    form = RatingForm()
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            apt = form.cleaned_data['apartment']
            roommate = form.cleaned_data['roommate']
            score = form.cleaned_data['score']
            comment = form.cleaned_data['comment']
            # Upsert — update if exists, create if not
            rating, created = Rating.objects.update_or_create(
                apartment=apt,
                roommate=roommate,
                defaults={'score': score, 'comment': comment}
            )
            if created:
                messages.success(request, f"Rating saved! {roommate.name} gave {apt.name} {score}/5.")
            else:
                messages.success(request, f"Rating updated! {roommate.name} gave {apt.name} {score}/5.")
            return redirect('rate')

    context = {
        'form': form,
        'all_ratings': all_ratings,
        'apartments': Apartment.objects.all(),
        'filter_apt': filter_apt,
    }
    return render(request, 'tracker/rate.html', context)


# ── Compare ───────────────────────────────────────────────────────────────────
@login_required
def compare(request):
    all_apartments = Apartment.objects.all()
    left = None
    right = None
    left_ratings = []
    right_ratings = []
    verdict = None

    left_id = request.GET.get('left')
    right_id = request.GET.get('right')

    if left_id and right_id and left_id != right_id:
        left = get_object_or_404(
            Apartment.objects.annotate(avg_score=Avg('ratings__score'), num_ratings=Count('ratings')),
            pk=left_id
        )
        right = get_object_or_404(
            Apartment.objects.annotate(avg_score=Avg('ratings__score'), num_ratings=Count('ratings')),
            pk=right_id
        )
        left_ratings = Rating.objects.filter(apartment=left).select_related('roommate')
        right_ratings = Rating.objects.filter(apartment=right).select_related('roommate')

        ls = left.avg_score or 0
        rs = right.avg_score or 0
        if ls == rs:
            verdict = ('tie', None)
        elif ls > rs:
            verdict = ('left', left, round(float(ls) - float(rs), 1))
        else:
            verdict = ('right', right, round(float(rs) - float(ls), 1))

    left_right = []
    if left and right:
        left_right = [(left, left_ratings), (right, right_ratings)]

    context = {
        'all_apartments': all_apartments,
        'left': left,
        'right': right,
        'left_right': left_right,
        'left_id': left_id,
        'right_id': right_id,
        'verdict': verdict,
    }
    return render(request, 'tracker/compare.html', context)
