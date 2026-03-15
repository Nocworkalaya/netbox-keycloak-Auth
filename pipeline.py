import logging
from django.conf import settings
from users.models import Group

logger = logging.getLogger("netbox.auth.keycloak")


def keycloak_group_mapper(backend, user, response, *args, **kwargs):
    """
    Sync Keycloak roles/groups with NetBox groups
    and assign staff/superuser privileges.
    """

    roles = set()

    # Realm roles
    realm_roles = response.get("realm_access", {}).get("roles", [])
    roles.update(realm_roles)

    # Client roles
    resource_access = response.get("resource_access", {})
    for client in resource_access.values():
        roles.update(client.get("roles", []))

    # Groups claim
    roles.update(response.get("groups", []))

    logger.debug(f"Detected Keycloak roles/groups: {roles}")

    group_objects = []

    for role in roles:

        try:
            group = Group.objects.get(name=role)

        except Group.DoesNotExist:

            if getattr(settings, "REMOTE_AUTH_AUTO_CREATE_GROUPS", False):
                group = Group.objects.create(name=role)
                logger.info(f"Created NetBox group: {role}")
            else:
                continue

        group_objects.append(group)

    # Assign groups to user
    if group_objects:
        user.groups.set(group_objects)

    # Staff / Superuser logic
    superuser_groups = getattr(settings, "REMOTE_AUTH_SUPERUSER_GROUPS", [])
    staff_groups = getattr(settings, "REMOTE_AUTH_STAFF_GROUPS", [])

    user.is_superuser = any(g.name in superuser_groups for g in group_objects)
    user.is_staff = any(g.name in staff_groups for g in group_objects)

    user.save()

    logger.info(
        f"User {user.username} synced groups: {[g.name for g in group_objects]}"
    )

    return {"user": user}
