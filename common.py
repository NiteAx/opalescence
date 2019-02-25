# Safe config - does not contain credentials / private stuff

admin_roles = ['Cool Squad','Admin','Mods']

def has_any_role(user, role_names=None, role_ids=None):
    for role in user.roles:
        if role_names and role.name in role_names:
            return True
        elif role_ids and role.id in role_ids:
            return True
    return False
