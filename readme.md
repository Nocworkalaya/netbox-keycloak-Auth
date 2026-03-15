


# NetBox Keycloak Group Sync Pipeline

This project adds **automatic group synchronization between Keycloak and NetBox** during OAuth login.

The pipeline extracts roles and groups from the **Keycloak token** and maps them to **NetBox groups**.

It also automatically assigns:

- `is_staff`
- `is_superuser`

based on configured group names.

---

# Architecture

User
↓
Keycloak Login
↓
OIDC Token
↓
NetBox OAuth Pipeline
↓
Extract roles/groups
↓
Create NetBox groups (optional)
↓
Assign groups to user
↓
Apply staff/superuser privileges

---

# Supported Token Claims

The pipeline reads authorization information from three Keycloak token sections.

## 1. Realm Roles

realm_access.roles

Example:

```json
"realm_access": {
  "roles": ["superadmin"]
}


⸻

2. Client Roles

resource_access.<client>.roles

Example:

"resource_access": {
  "netbox": {
    "roles": ["staff"]
  }
}


⸻

3. Groups

groups

Example:

"groups": [
  "noc",
  "network-team"
]


⸻

Example Token

{
 "preferred_username": "rabi",

 "realm_access": {
   "roles": ["superadmin"]
 },

 "resource_access": {
   "netbox": {
     "roles": ["staff"]
   }
 },

 "groups": [
   "noc",
   "network-team"
 ]
}


⸻

Installation

Place the pipeline file in:

netbox/netbox/users/keycloak_pipeline.py


⸻

Enable Pipeline

Edit:

netbox/netbox/configuration.py

Add:

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',

    'users.keycloak_pipeline.keycloak_group_mapper',

    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)


⸻

Configuration Options

Example configuration:

REMOTE_AUTH_AUTO_CREATE_USER = True
REMOTE_AUTH_AUTO_CREATE_GROUPS = True

REMOTE_AUTH_SUPERUSERS_GROUPS = ["superadmin"]
REMOTE_AUTH_STAFF_GROUPS = ["staff"]


⸻

Behavior

Group Sync

When a user logs in:

Keycloak roles/groups
        ↓
Converted to NetBox groups
        ↓
User groups updated


⸻

Staff Mapping

If user belongs to any group listed in:

REMOTE_AUTH_STAFF_GROUPS

Then:

user.is_staff = True


⸻

Superuser Mapping

If user belongs to any group listed in:

REMOTE_AUTH_SUPERUSERS_GROUPS

Then:

user.is_superuser = True


⸻

Keycloak Configuration

You must configure Protocol Mappers so roles/groups appear in the token.

See:

docs/keycloak-group-mapper.md

Typical mappers include:
	•	Realm Role Mapper
	•	Client Role Mapper
	•	Group Membership Mapper

⸻

Verification

After login:
	1.	Capture the access token
	2.	Decode with:

https://jwt.io

Verify claims exist:

realm_access.roles
resource_access.netbox.roles
groups


⸻

Logging

Pipeline logs appear in NetBox logs.

Example:

Detected Keycloak roles/groups: {'noc','staff'}
Created NetBox group: noc
User rabi synced groups: ['noc','staff']


⸻

Troubleshooting

Groups assigned but no admin access

Check:

REMOTE_AUTH_SUPERUSERS_GROUPS
REMOTE_AUTH_STAFF_GROUPS

Group names must match exactly.

⸻

Groups not created

Enable:

REMOTE_AUTH_AUTO_CREATE_GROUPS = True


⸻

Roles not present in token

Check Keycloak Protocol Mappers.

⸻

Recommended Best Practice

Use NetBox-specific roles in Keycloak:

netbox:admin
netbox:staff
netbox:noc

Then map them to NetBox groups.

This prevents unrelated roles from appearing in NetBox.




















