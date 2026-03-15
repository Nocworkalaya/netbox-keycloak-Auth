REMOTE_AUTH_BACKEND='social_core.backends.keycloak.KeycloakOAuth2'
SOCIAL_AUTH_KEYCLOAK_KEY ='<your-keycloak-client-id>'
SOCIAL_AUTH_KEYCLOAK_SECRET='<your-keycloak-client-secret>'
SOCIAL_AUTH_KEYCLOAK_PUBLIC_KEY="<your-public-key-used-to-create-tokemn>"
SOCIAL_AUTH_KEYCLOAK_AUTHORIZATION_URL='http://<your-keycloak-url>/realms/<your-realm>/protocol/openid-connect/auth'
SOCIAL_AUTH_KEYCLOAK_ACCESS_TOKEN_URL='http://<your-keycloak-url>/realms/<your-realm>/protocol/openid-connect/token'
SOCIAL_AUTH_KEYCLOAK_ID_KEY='preferred_username'
REMOTE_AUTH_GROUP_SYNC_ENABLED=True
REMOTE_AUTH_SUPERUSER_GROUPS=["your-superuser-group"]
REMOTE_AUTH_STAFF_GROUPS=['your-staff-group']
# Header where the username is stored

# Header where groups are passed

# Separator for multiple groups in the header
REMOTE_AUTH_AUTO_CREATE_USER = True
REMOTE_AUTH_AUTO_CREATE_GROUPS=True

SOCIAL_AUTH_PIPELINE = [
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    'users.pipeline.keycloak_group_mapper',  # << custom step
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
]
