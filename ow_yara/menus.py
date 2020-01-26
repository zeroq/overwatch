# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

from django.urls import reverse
from menu import Menu, MenuItem

client_children = (
    MenuItem("List Rules",
            reverse("owyara:index"),
            weight=10),
    MenuItem("Upload Rules",
            reverse("owyara:upload"),
            weight=80),
)

Menu.add_item("yara", MenuItem(" Yara",
    reverse("owyara:index"),
    weight=10,
    children=client_children)
)
