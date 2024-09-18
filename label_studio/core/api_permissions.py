from rest_framework.permissions import SAFE_METHODS, BasePermission


class HasObjectPermission(BasePermission):
    def has_permission(self, request, view):
        view_permission = True
        if view.permission_required:
            permission_key = view.permission_required if isinstance(view.permission_required, str) else view.permission_required.dict().get(request.method)
            view_permission = request.user.has_perm(permission_key)
        return view_permission

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view) and obj.has_permission(request.user)


class MemberHasOwnerPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method not in SAFE_METHODS and not request.user.own_organization:
            return False

        return obj.has_permission(request.user)
