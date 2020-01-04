# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

from django.urls import reverse
from menu import Menu, MenuItem

client_children = (
    MenuItem("List Clients",
            reverse("owclients:index"),
            weight=10),
    MenuItem("Add Client",
            reverse("owclients:create_client"),
            weight=80),
)

Menu.add_item("clients", MenuItem(" Clients",
    reverse("owclients:index"),
    weight=10,
    children=client_children)
)
