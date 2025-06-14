from rest_framework import permissions


class IsOrganizerOrAdmin(permissions.BasePermission):
    """Permesso personalizzato per permettere solo all'organizzatore o all'admin di modificare"""

    def has_object_permission(self, request, view, obj):
        # Permetti solo se l'utente è staff o è l'organizzatore dell'evento
        return request.user.is_staff or obj.organizer == request.user
