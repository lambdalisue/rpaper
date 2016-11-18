from permission.logics import PermissionLogic
from .middleware import get_record_credential


class ThingPermissionLogic(PermissionLogic):
    def has_perm(self, user_obj, perm, obj=None):
        add_permission = self.get_full_permission_string('add')
        change_permission = self.get_full_permission_string('change')
        delete_permission = self.get_full_permission_string('delete')

        if perm not in (add_permission, change_permission, delete_permission):
            return False
        elif obj is None:
            return user_obj.is_authenticated()
        return obj.owner == user_obj


class RecordPermissionLogic(PermissionLogic):
    def has_perm(self, user_obj, perm, obj=None):
        add_permission = self.get_full_permission_string('add')
        change_permission = self.get_full_permission_string('change')
        delete_permission = self.get_full_permission_string('delete')

        if perm not in (add_permission, change_permission, delete_permission):
            return False
        elif perm == add_permission:
            return True
        elif obj is None:
            return True
        if obj.owner:
            # NOTE:
            # DO NOT FALLBACK TO 'CREDENTIAL' WAY.
            # As I explained below, the 'credential' way has a security risk.
            # So I would like to prepare 'a secure way' for an authenticated
            # user. If a record has made by an authenticated user, the
            # record SHOULD ONLY BE modifiable by that authenticated user.
            # In this case, if the user logged out, even users who share the
            # same web-browser cannot touch the record unless he/she have
            # a way to logged in as that user.
            return obj.owner == user_obj
        # NOTE:
        # The 'credential' way is not secure.
        # While the 'credential' is assumed to saved in a localStorage, users
        # who share same web-browser suffer a security risk. A user can see a
        # 'credential' of other's if he/she have enough skill to dig.
        # However, while the target of this service is a real object in a real
        # world, what he/she can do with a 'credential' is removing/updating
        # the record and the advantage he/she can get is not so valuable.
        # So that I just decided to ignore this security risk for an anonyomous
        # user.
        credential = get_record_credential()
        return credential and str(obj.credential) == credential


PERMISSION_LOGICS = (
    ('reservations.Thing', ThingPermissionLogic()),
    ('reservations.Record', RecordPermissionLogic()),
)
