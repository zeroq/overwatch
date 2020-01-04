# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

from django.urls import reverse
from menu import Menu, MenuItem

server_children = (
    MenuItem("Show Server",
            reverse("owservers:index"),
            weight=10),
    MenuItem("Edit Server",
            reverse("owservers:edit_server"),
            weight=80),
)

Menu.add_item("servers", MenuItem(" Server",
    reverse("owservers:index"),
    weight=10,
    children=server_children)
)
