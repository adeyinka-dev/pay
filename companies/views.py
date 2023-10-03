from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import ClientForm
from .models import Domain


def create_client(request):
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            # Saving the form data to create a new client instance.
            client = form.save()
            # Creating a domain for this company. This allows the company's users to access the app via a unique subdomain.
            domain = Domain()
            # Setting the domain name by combining the client's schema name and your primary domain.
            domain.domain = f"{client.schema_name}.localhost"
            # Associating the domain with the created client.
            domain.tenant = client
            # Indicating that this is the primary domain for the client. There might be secondary ones, but this is the main one.
            domain.is_primary = True
            # Saving
            domain.save()
            return HttpResponse("Successful")
    else:
        form = ClientForm()
    return render(request, "create_client.html", {"form": form})
